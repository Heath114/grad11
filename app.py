from flask import Flask, send_from_directory
from flask_cors import CORS
from database import init_db
from routes.auth import auth_bp
from routes.cafeterias import cafeterias_bp
from routes.orders import orders_bp
from routes.ratings import ratings_bp
from routes.complaints import complaints_bp
import os
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Allow frontend origin
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": [
                'http://localhost:5500',
                'http://127.0.0.1:5500',
                'https://localhost:3000',
                os.environ.get('FRONTEND_URL', 'https://graduationproject2.netlify.app')
            ],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "max_age": 3600
        }
    }
)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cafeterias_bp, url_prefix='/cafeterias')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(ratings_bp, url_prefix='/ratings')
app.register_blueprint(complaints_bp, url_prefix='/complaints')

# Ensure DB exists when running under gunicorn (not just python app.py)
init_db()

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/health')
def health():
    return {'status': 'healthy'}

@app.route('/photos/<path:filename>')
def serve_photos(filename):
    return send_from_directory('photos', filename)

@app.route('/<path:filename>')
def serve_frontend_files(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
