import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'cafeteria.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    # ── Users 
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            last_name   TEXT    NOT NULL,
            phone       TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    ''')

    # ── Admins 
    c.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    NOT NULL UNIQUE,
            password      TEXT    NOT NULL,
            cafeteria_id  TEXT    NOT NULL
        )
    ''')

    # ── Cafeterias 
    c.execute('''
        CREATE TABLE IF NOT EXISTS cafeterias (
            id          TEXT    PRIMARY KEY,
            name        TEXT    NOT NULL,
            description TEXT,
            location    TEXT,
            hours       TEXT,
            notice      TEXT,
            image       TEXT
        )
    ''')

    # ── Menu Items 
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            cafeteria_id  TEXT    NOT NULL,
            category      TEXT    NOT NULL,
            name          TEXT    NOT NULL,
            description   TEXT,
            price         REAL    NOT NULL,
            image         TEXT,
            is_takeout    INTEGER DEFAULT 0,
            ready_in      TEXT,
            FOREIGN KEY (cafeteria_id) REFERENCES cafeterias(id)
        )
    ''')

    # ── Menu Item Add-ons 
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu_item_addons (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_item_id  INTEGER NOT NULL,
            name          TEXT    NOT NULL,
            price         REAL    NOT NULL,
            FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
        )
    ''')

    # ── Orders 
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id           INTEGER NOT NULL,
            cafeteria_id      TEXT    NOT NULL,
            order_type        TEXT    NOT NULL DEFAULT 'Pickup',
            delivery_location TEXT,
            payment_method    TEXT    NOT NULL DEFAULT 'Cash',
            status            TEXT    NOT NULL DEFAULT 'pending',
            created_at        TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id)      REFERENCES users(id),
            FOREIGN KEY (cafeteria_id) REFERENCES cafeterias(id)
        )
    ''')

    # ── Order Items 
    c.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id      INTEGER NOT NULL,
            menu_item_id  INTEGER,
            name          TEXT    NOT NULL,
            price         REAL    NOT NULL,
            category      TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')

    # ── Order Item Add-ons 
    c.execute('''
        CREATE TABLE IF NOT EXISTS order_item_addons (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            order_item_id INTEGER NOT NULL,
            addon_name    TEXT    NOT NULL,
            addon_price   REAL    NOT NULL,
            FOREIGN KEY (order_item_id) REFERENCES order_items(id)
        )
    ''')

    # ── Ratings 
    c.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            cafeteria_id  TEXT    NOT NULL,
            score         INTEGER NOT NULL CHECK(score BETWEEN 1 AND 5),
            comment       TEXT,
            created_at    TEXT    DEFAULT (datetime('now')),
            UNIQUE(user_id, cafeteria_id),
            FOREIGN KEY (user_id)      REFERENCES users(id),
            FOREIGN KEY (cafeteria_id) REFERENCES cafeterias(id)
        )
    ''')

    # ── Complaints 
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER,
            cafeteria_id  TEXT,
            subject       TEXT    NOT NULL,
            message       TEXT    NOT NULL,
            email         TEXT    NOT NULL,
            type          TEXT    NOT NULL DEFAULT 'complaint',
            created_at    TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id)      REFERENCES users(id),
            FOREIGN KEY (cafeteria_id) REFERENCES cafeterias(id)
        )
    ''')

    conn.commit()
    _seed_admins(c)
    _seed_demo_user(c)
    _seed_cafeterias(c)
    conn.commit()
    conn.close()
    print("Database initialised.")


def _seed_admins(c):
    admins = [
        ('admin1', 'admin1', '1'),
        ('admin2', 'admin2', '2'),
        ('admin3', 'admin3', '3'),
        ('admin4', 'admin4', '4'),
        ('admin5', 'admin5', '5'),
        ('admin6', 'admin6', '6'),
        ('admin7', 'admin7', '7'),
        ('admin8', 'admin8', '8'),
    ]
    for username, password, cafeteria_id in admins:
        c.execute('SELECT id FROM admins WHERE username = ?', (username,))
        if not c.fetchone():
            c.execute(
                'INSERT INTO admins (username, password, cafeteria_id) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), cafeteria_id)
            )

def _seed_demo_user(c):
    c.execute('SELECT id FROM users WHERE phone = ?', ('user1',))
    if not c.fetchone():
        c.execute(
            'INSERT INTO users (name, last_name, phone, password) VALUES (?, ?, ?, ?)',
            ('Demo', 'User', 'user1', generate_password_hash('user1'))
        )


def _seed_cafeterias(c):
    cafeterias = [
        ('1', 'Engineering Cafeteria 1',
         'Authentic Jordanian meals perfect for long study sessions.',
         'Engineering Building Level 2', '7:30 AM - 5:00 PM',
         'Peak hours 11:30 AM – 1:30 PM • Expect short queues during capstone rush.',
         '/photos/engineering1/cover.jpg'),
        ('2', 'Engineering Cafeteria 2',
         'Fresh mezze and grilled specialties for engineers on the go.',
         'Engineering Annex Ground Floor', '8:00 AM - 7:00 PM',
         'Mobile pickup shelf resets every 20 minutes—collect orders promptly.',
         '/photos/engineering2/cover.jpg'),
        ('3', 'Medicine Cafeteria',
         'Nutritious Jordanian meals planned for medical students.',
         'Medical Sciences Pavilion', '6:30 AM - 4:30 PM',
         'Wellness drinks counter closes at 3:00 PM.',
         '/photos/medicine/cover.jpg'),
        ('4', 'Business Cafeteria',
         'Premium Jordanian cuisine for business students.',
         'Business School Atrium', '8:00 AM - 6:00 PM',
         'Group orders available with 30 minutes notice.',
         '/photos/business/cover.jpg'),
        ('5', 'Science Cafeteria',
         'Traditional flavors to fuel your discoveries.',
         'Science Complex Lower Level', '7:45 AM - 6:15 PM',
         'Daily fresh juice specials - ask at counter.',
         '/photos/science/cover.jpg'),
        ('6', 'Arts Cafeteria',
         'Creative mezze and traditional comfort food.',
         'Fine Arts Center Courtyard', '9:00 AM - 8:00 PM',
         'Daily featured pastry from the student baking collective after 3 PM.',
         '/photos/arts/cover.jpg'),
        ('7', 'Law Cafeteria',
         'Hearty meals for long study sessions.',
         'Law School Commons', '7:30 AM - 9:00 PM',
         'Case study combo upgrades available after 6 PM.',
         '/photos/law/cover.jpg'),
        ('8', 'Central Library Cafe',
         'Quiet-friendly snacks and traditional beverages.',
         'Central Library Ground Floor', '7:00 AM - 11:00 PM',
         'Fresh mint tea available all day.',
         '/photos/library/cover.jpg'),
    ]
    for caf in cafeterias:
        c.execute('SELECT id FROM cafeterias WHERE id = ?', (caf[0],))
        if not c.fetchone():
            c.execute('''
                INSERT INTO cafeterias (id, name, description, location, hours, notice, image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', caf)


if __name__ == '__main__':
    init_db()
    
