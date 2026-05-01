from flask import Blueprint, request, jsonify, session
from database import get_db

complaints_bp = Blueprint('complaints', __name__)

@complaints_bp.route('/', methods=['POST'])
def submit_complaint():
    data         = request.get_json()
    cafeteria_id = data.get('cafeteriaId')
    subject      = (data.get('subject') or '').strip()
    message      = (data.get('message') or '').strip()
    email        = (data.get('email') or '').strip()
    type_        = data.get('type', 'complaint')  # complaint | recommendation

    if not all([subject, message, email]):
        return jsonify({'success': False, 'message': 'Subject, message and email are required'}), 400

    if type_ not in ('complaint', 'recommendation'):
        type_ = 'complaint'

    user_id = session.get('user_id')

    db = get_db()

    db.execute('''
        INSERT INTO complaints (user_id, cafeteria_id, subject, message, email, type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, cafeteria_id, subject, message, email, type_))
    db.commit()
    db.close()

    return jsonify({'success': True, 'message': f'Your {type_} has been submitted successfully'})


@complaints_bp.route('/dev', methods=['GET'])
def list_all_complaints_for_dev():
    """Developer-only: list all complaints as a mock email inbox."""
    db   = get_db()
    rows = db.execute('''
        SELECT c.*, u.name, u.last_name, u.phone, 
               caf.name as cafeteria_name
        FROM complaints c
        LEFT JOIN users u ON c.user_id = u.id
        LEFT JOIN cafeterias caf ON c.cafeteria_id = caf.id
        ORDER BY c.created_at DESC
    ''').fetchall()
    db.close()

    return jsonify([{
        'id':            r['id'],
        'subject':       r['subject'],
        'message':       r['message'],
        'email':         r['email'],
        'type':          r['type'],
        'createdAt':     r['created_at'],
        'cafeteriaName': r['cafeteria_name'] or 'General Support',
        'userName':      f"{r['name']} {r['last_name']}" if r['name'] else 'Anonymous'
    } for r in rows])