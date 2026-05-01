from flask import Blueprint, request, jsonify, session
from database import get_db

ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('/<cafeteria_id>', methods=['GET'])
def get_ratings(cafeteria_id):
    db = get_db()
    rows = db.execute('''
        SELECT r.score, r.comment, r.created_at, u.name, u.last_name
        FROM ratings r
        JOIN users u ON r.user_id = u.id
        WHERE r.cafeteria_id = ?
        ORDER BY r.created_at DESC
        LIMIT 20
    ''', (cafeteria_id,)).fetchall()

    summary = db.execute('''
        SELECT ROUND(AVG(score), 1) as avg, COUNT(*) as total
        FROM ratings WHERE cafeteria_id = ?
    ''', (cafeteria_id,)).fetchone()

    db.close()
    return jsonify({
        'average': summary['avg'] or 0,
        'total':   summary['total'],
        'reviews': [{
            'score':     r['score'],
            'comment':   r['comment'],
            'createdAt': r['created_at'],
            'userName':  f"{r['name']} {r['last_name']}"
        } for r in rows]
    })


@ratings_bp.route('/', methods=['POST'])
def submit_rating():
    if session.get('user_type') != 'user':
        return jsonify({'success': False, 'message': 'Login required'}), 401

    data         = request.get_json()
    cafeteria_id = data.get('cafeteriaId')
    score        = data.get('score')
    comment      = (data.get('comment') or '').strip()

    if not cafeteria_id or score is None:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    if not isinstance(score, int) or score < 1 or score > 5:
        return jsonify({'success': False, 'message': 'Score must be between 1 and 5'}), 400

    db = get_db()

    # Upsert — one rating per user per cafeteria
    existing = db.execute(
        'SELECT id FROM ratings WHERE user_id = ? AND cafeteria_id = ?',
        (session['user_id'], cafeteria_id)
    ).fetchone()

    if existing:
        db.execute(
            'UPDATE ratings SET score = ?, comment = ?, created_at = datetime("now") WHERE id = ?',
            (score, comment, existing['id'])
        )
    else:
        db.execute(
            'INSERT INTO ratings (user_id, cafeteria_id, score, comment) VALUES (?, ?, ?, ?)',
            (session['user_id'], cafeteria_id, score, comment)
        )

    db.commit()
    db.close()
    return jsonify({'success': True, 'message': 'Rating submitted'})