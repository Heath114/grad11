from flask import Blueprint, request, jsonify, session
from database import get_db
from datetime import datetime, timezone

orders_bp = Blueprint('orders', __name__)


def compute_status(created_at_str, order_type, current_status):
    if current_status == 'completed':
        return 'completed'
        
    """
    Derive order status from elapsed time since creation.
    Pickup:  pending(0-5s) → preparing(5-10s) → ready(10s+)
    Delivery: pending(0-5s) → preparing(5-10s) → ready(10-15s) → out_for_delivery(15s+)
    """
    try:
        created_at = datetime.fromisoformat(created_at_str).replace(tzinfo=timezone.utc)
    except Exception:
        return 'pending'

    elapsed = (datetime.now(timezone.utc) - created_at).total_seconds()  # seconds

    if order_type == 'Delivery':
        if elapsed < 5:
            return 'pending'
        elif elapsed < 10:
            return 'preparing'
        elif elapsed < 15:
            return 'ready'
        else:
            return 'out_for_delivery'
    else:
        if elapsed < 5:
            return 'pending'
        elif elapsed < 10:
            return 'preparing'
        else:
            return 'ready'


def format_order(order, db):
    items = db.execute(
        'SELECT * FROM order_items WHERE order_id = ?', (order['id'],)
    ).fetchall()

    items_list = []
    for item in items:
        addons = db.execute(
            'SELECT addon_name, addon_price FROM order_item_addons WHERE order_item_id = ?',
            (item['id'],)
        ).fetchall()
        items_list.append({
            'id':       item['id'],
            'name':     item['name'],
            'price':    item['price'],
            'category': item['category'],
            'addOns':   [{'name': a['addon_name'], 'price': a['addon_price']} for a in addons]
        })

    total = sum(
        i['price'] + sum(a['addon_price'] for a in db.execute(
            'SELECT addon_price FROM order_item_addons WHERE order_item_id = ?', (i['id'],)
        ).fetchall())
        for i in db.execute('SELECT * FROM order_items WHERE order_id = ?', (order['id'],)).fetchall()
    )

    status = compute_status(order['created_at'], order['order_type'], order['status'])

    return {
        'id':               order['id'],
        'cafeteriaId':      order['cafeteria_id'],
        'orderType':        order['order_type'],
        'deliveryLocation': order['delivery_location'],
        'paymentMethod':    order['payment_method'],
        'status':           status,
        'createdAt':        order['created_at'],
        'items':            items_list,
        'total':            round(total, 2)
    }


@orders_bp.route('/', methods=['POST'])
def place_order():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Login required'}), 401

    data              = request.get_json()
    cafeteria_id      = data.get('cafeteriaId')
    order_type        = data.get('orderType', 'Pickup')
    delivery_location = data.get('deliveryLocation')
    payment_method    = data.get('paymentMethod', 'Cash')
    items             = data.get('items', [])

    if not cafeteria_id or not items:
        return jsonify({'success': False, 'message': 'Missing order data'}), 400

    if order_type == 'Delivery' and not delivery_location:
        return jsonify({'success': False, 'message': 'Delivery location required'}), 400

    db = get_db()

    order_id = db.execute('''
        INSERT INTO orders (user_id, cafeteria_id, order_type, delivery_location, payment_method, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    ''', (session['user_id'], cafeteria_id, order_type, delivery_location, payment_method)).lastrowid

    for item in items:
        item_id = db.execute('''
            INSERT INTO order_items (order_id, menu_item_id, name, price, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, item.get('menuItemId'), item['name'],
              float(str(item['price']).replace(' JOD', '').replace('JOD', '')),
              item.get('category', ''))).lastrowid

        for addon in item.get('addOns', []):
            db.execute('''
                INSERT INTO order_item_addons (order_item_id, addon_name, addon_price)
                VALUES (?, ?, ?)
            ''', (item_id, addon['name'],
                  float(str(addon['price']).replace(' JOD', '').replace('JOD', ''))))

    db.commit()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    result = format_order(order, db)
    db.close()

    return jsonify({'success': True, 'order': result}), 201


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    db    = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if not order:
        db.close()
        return jsonify({'error': 'Order not found'}), 404
    result = format_order(order, db)
    db.close()
    return jsonify(result)


@orders_bp.route('/<int:order_id>/status', methods=['GET'])
def get_order_status(order_id):
    db    = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    if not order:
        db.close()
        return jsonify({'error': 'Order not found'}), 404
    status = compute_status(order['created_at'], order['order_type'], order['status'])
    db.close()
    return jsonify({'orderId': order_id, 'status': status})


@orders_bp.route('/user', methods=['GET'])
def get_user_orders():
    if 'user_id' not in session or session.get('user_type') != 'user':
        return jsonify({'error': 'Login required'}), 401

    db     = get_db()
    orders = db.execute(
        'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    result = [format_order(o, db) for o in orders]
    db.close()
    return jsonify(result)


@orders_bp.route('/cafeteria/<cafeteria_id>', methods=['GET'])
def get_cafeteria_orders(cafeteria_id):
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    if session.get('cafeteria_id') != cafeteria_id:
        return jsonify({'error': 'Access denied'}), 403

    db = get_db()

    # Join with users to get name + phone
    orders = db.execute('''
        SELECT o.*, u.name, u.last_name, u.phone
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        WHERE o.cafeteria_id = ?
        ORDER BY o.created_at DESC
    ''', (cafeteria_id,)).fetchall()

    result = []
    for o in orders:
        formatted = format_order(o, db)
        formatted['userName']  = f"{o['name']} {o['last_name']}" if o['name'] else 'Unknown'
        formatted['userPhone'] = o['phone'] or ''
        result.append(formatted)

    db.close()
    return jsonify(result)


@orders_bp.route('/cafeteria/<cafeteria_id>/clear', methods=['DELETE'])
def clear_cafeteria_orders(cafeteria_id):
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    if session.get('cafeteria_id') != cafeteria_id:
        return jsonify({'error': 'Access denied'}), 403

    db = get_db()

    order_ids = [r['id'] for r in db.execute(
        'SELECT id FROM orders WHERE cafeteria_id = ?', (cafeteria_id,)
    ).fetchall()]

    for oid in order_ids:
        item_ids = [r['id'] for r in db.execute(
            'SELECT id FROM order_items WHERE order_id = ?', (oid,)
        ).fetchall()]
        for iid in item_ids:
            db.execute('DELETE FROM order_item_addons WHERE order_item_id = ?', (iid,))
        db.execute('DELETE FROM order_items WHERE order_id = ?', (oid,))
    db.execute('DELETE FROM orders WHERE cafeteria_id = ?', (cafeteria_id,))

    db.commit()
    db.close()
    return jsonify({'success': True})

@orders_bp.route('/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Login required'}), 401
        
    db = get_db()
    order = db.execute('SELECT * FROM orders WHERE id = ? AND user_id = ?', (order_id, session['user_id'])).fetchone()
    if not order:
        db.close()
        return jsonify({'error': 'Order not found'}), 404
        
    db.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Order marked as completed'})
