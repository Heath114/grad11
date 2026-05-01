from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
import re

auth_bp = Blueprint('auth', __name__)


def validate_password(password):
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters"
    if len(password) > 20:
        return False, "Password must not exceed 20 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return False, "Password must contain at least one special character"
    return True, "Valid"


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name         = (data.get('name') or '').strip()
    last_name    = (data.get('lastName') or '').strip()
    phone        = (data.get('phone') or '').strip()
    password     = (data.get('password') or '').strip()

    if not all([name, last_name, phone, password]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    if not re.match(r'^\d{10}$', phone):
        return jsonify({'success': False, 'message': 'Phone number must be exactly 10 digits'}), 400

    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400

    db = get_db()
    existing = db.execute('SELECT id FROM users WHERE phone = ?', (phone,)).fetchone()
    if existing:
        db.close()
        return jsonify({'success': False, 'message': 'Phone number already registered'}), 409

    db.execute(
        'INSERT INTO users (name, last_name, phone, password) VALUES (?, ?, ?, ?)',
        (name, last_name, phone, generate_password_hash(password))
    )
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Registration successful'}), 201


@auth_bp.route('/register-admin', methods=['POST'])
def register_admin():
    data        = request.get_json()
    username    = (data.get('username') or '').strip()
    password    = (data.get('password') or '').strip()
    cafeteria_id = (data.get('cafeteriaId') or '').strip()

    if not all([username, password, cafeteria_id]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'success': False, 'message': msg}), 400

    db = get_db()

    existing = db.execute('SELECT id FROM admins WHERE username = ?', (username,)).fetchone()
    if existing:
        db.close()
        return jsonify({'success': False, 'message': 'Admin username already registered'}), 409

    caf = db.execute('SELECT id FROM cafeterias WHERE id = ?', (cafeteria_id,)).fetchone()
    if not caf:
        db.close()
        return jsonify({'success': False, 'message': 'Cafeteria id not found'}), 404

    db.execute(
        'INSERT INTO admins (username, password, cafeteria_id) VALUES (?, ?, ?)',
        (username, generate_password_hash(password), cafeteria_id)
    )
    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Admin registration successful'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data     = request.get_json()
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    if not username or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    db = get_db()

    # Check admins first
    admin = db.execute(
        'SELECT * FROM admins WHERE username = ?', (username,)
    ).fetchone()

    if admin and check_password_hash(admin['password'], password):
        session['user_id']      = None
        session['admin_id']     = admin['id']
        session['username']     = admin['username']
        session['cafeteria_id'] = admin['cafeteria_id']
        session['user_type']    = 'admin'

        caf = db.execute(
            'SELECT name FROM cafeterias WHERE id = ?', (admin['cafeteria_id'],)
        ).fetchone()
        db.close()

        return jsonify({
            'success':       True,
            'userType':      'admin',
            'cafeteriaId':   admin['cafeteria_id'],
            'cafeteriaName': caf['name'] if caf else '',
            'username':      admin['username']
        })

    # Check regular users
    user = db.execute(
        'SELECT * FROM users WHERE phone = ?', (username,)
    ).fetchone()

    if user and check_password_hash(user['password'], password):
        session['user_id']   = user['id']
        session['admin_id']  = None
        session['username']  = user['phone']
        session['user_type'] = 'user'
        db.close()

        return jsonify({
            'success':  True,
            'userType': 'user',
            'userId':   user['id'],
            'name':     user['name'],
            'lastName': user['last_name'],
            'phone':    user['phone']
        })

    db.close()
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out'})


@auth_bp.route('/me', methods=['GET'])
def me():
    if 'user_type' not in session:
        return jsonify({'authenticated': False}), 401

    return jsonify({
        'authenticated': True,
        'userType':      session.get('user_type'),
        'userId':        session.get('user_id'),
        'username':      session.get('username'),
        'cafeteriaId':   session.get('cafeteria_id')
    })