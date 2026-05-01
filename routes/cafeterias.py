from flask import Blueprint, jsonify
from database import get_db

cafeterias_bp = Blueprint('cafeterias', __name__)


def build_cafeteria(row, db, include_menu=False):
    caf = {
        'id':          row['id'],
        'name':        row['name'],
        'description': row['description'],
        'location':    row['location'],
        'hours':       row['hours'],
        'notice':      row['notice'],
        'image':       row['image'],
    }

    # Average rating
    rating_row = db.execute('''
        SELECT ROUND(AVG(score), 1) as avg, COUNT(*) as total
        FROM ratings WHERE cafeteria_id = ?
    ''', (row['id'],)).fetchone()
    caf['rating']       = rating_row['avg'] or 0
    caf['rating_count'] = rating_row['total']

    if not include_menu:
        return caf

    # Build menu
    items = db.execute('''
        SELECT * FROM menu_items WHERE cafeteria_id = ? ORDER BY is_takeout, category, id
    ''', (row['id'],)).fetchall()

    menu_dict    = {}
    takeout_list = []

    for item in items:
        addons = db.execute(
            'SELECT name, price FROM menu_item_addons WHERE menu_item_id = ?',
            (item['id'],)
        ).fetchall()

        item_obj = {
            'id':          item['id'],
            'name':        item['name'],
            'description': item['description'],
            'price':       item['price'],
            'image':       item['image'],
            'addOns':      [{'name': a['name'], 'price': a['price']} for a in addons],
        }

        if item['is_takeout']:
            item_obj['readyIn'] = item['ready_in']
            takeout_list.append(item_obj)
        else:
            cat = item['category']
            if cat not in menu_dict:
                menu_dict[cat] = []
            menu_dict[cat].append(item_obj)

    caf['menu']    = [{'category': k, 'items': v} for k, v in menu_dict.items()]
    caf['takeout'] = takeout_list
    return caf


@cafeterias_bp.route('/', methods=['GET'])
def list_cafeterias():
    db   = get_db()
    rows = db.execute('SELECT * FROM cafeterias ORDER BY id').fetchall()
    result = [build_cafeteria(r, db) for r in rows]
    db.close()
    return jsonify(result)


@cafeterias_bp.route('/<cafeteria_id>', methods=['GET'])
def get_cafeteria(cafeteria_id):
    db  = get_db()
    row = db.execute('SELECT * FROM cafeterias WHERE id = ?', (cafeteria_id,)).fetchone()
    if not row:
        db.close()
        return jsonify({'error': 'Cafeteria not found'}), 404
    result = build_cafeteria(row, db, include_menu=True)
    db.close()
    return jsonify(result)