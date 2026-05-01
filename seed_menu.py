"""
Run this once to seed all menu items and add-ons into the database.
Usage: python3 seed_menu.py
"""
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'cafeteria.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

menu_data = {
    "1": {
        "menu": [
            {
                "category": "Breakfast",
                "items": [
                    {
                        "name": "Foul & Hummus Platter",
                        "description": "Warm fava beans and creamy hummus with olive oil, served with fresh pita bread.",
                        "price": 2.5,
                        "image": "photos/engineering1/55d38b8c-7fe9-49a2-8d36-2ac059cdb5e7.avif",
                        "addOns": [
                            {"name": "Extra pita", "price": 0.5},
                            {"name": "Pickles & olives", "price": 0.8}
                        ]
                    },
                    {
                        "name": "Manakish Za'atar",
                        "description": "Freshly baked flatbread topped with za'atar and olive oil.",
                        "price": 1.5,
                        "image": "photos/engineering1/Manakish-Zaatar-1-of-1.jpeg",
                        "addOns": [
                            {"name": "Labneh side", "price": 0.7},
                            {"name": "Cheese topping", "price": 1.0}
                        ]
                    }
                ]
            },
            {
                "category": "Main Meals",
                "items": [
                    {
                        "name": "Maqluba (Upside Down Rice)",
                        "description": "Traditional layered rice with chicken, eggplant, cauliflower and Middle Eastern spices.",
                        "price": 4.5,
                        "image": "photos/engineering1/maqluba-upside-down-chicken-and-rice_11005.jpg",
                        "addOns": [
                            {"name": "Yogurt salad", "price": 0.8},
                            {"name": "Extra meat", "price": 2.0}
                        ]
                    },
                    {
                        "name": "Chicken Shawarma Plate",
                        "description": "Marinated chicken shawarma with rice, salad, and tahini sauce.",
                        "price": 3.5,
                        "image": "photos/engineering1/1667937205404.webp",
                        "addOns": [
                            {"name": "French fries", "price": 1.0},
                            {"name": "Garlic sauce", "price": 0.5}
                        ]
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Falafel Sandwich",
                "description": "Crispy falafel with tahini, vegetables, and pickles in fresh pita.",
                "price": 1.8,
                "image": "photos/engineering1/Falafel-Sandwich-Recipe-SQ.jpg",
                "readyIn": "Ready in 8 minutes",
                "addOns": [
                    {"name": "Extra falafel", "price": 0.5},
                    {"name": "French fries inside", "price": 0.7}
                ]
            },
            {
                "name": "Chicken Shawarma Wrap",
                "description": "Tender chicken shawarma with garlic sauce and pickles in saj bread.",
                "price": 2.5,
                "image": "photos/engineering1/Screenshot-2025-07-28-at-11.webp",
                "readyIn": "Ready in 10 minutes",
                "addOns": [
                    {"name": "Extra garlic sauce", "price": 0.3},
                    {"name": "Cheese", "price": 0.7}
                ]
            }
        ]
    },
    "2": {
        "menu": [
            {
                "category": "Breakfast",
                "items": [
                    {
                        "name": "Labneh Plate",
                        "description": "Creamy labneh drizzled with olive oil, served with cucumbers, tomatoes, and pita.",
                        "price": 2.0,
                        "image": "",
                        "addOns": [
                            {"name": "Mint leaves", "price": 0.3},
                            {"name": "Za'atar mix", "price": 0.5}
                        ]
                    }
                ]
            },
            {
                "category": "Lunch",
                "items": [
                    {
                        "name": "Meat Biryani",
                        "description": "Spiced rice with tender lamb, nuts, and raisins.",
                        "price": 5.0,
                        "image": "",
                        "addOns": [
                            {"name": "Yogurt", "price": 0.8},
                            {"name": "Hot sauce", "price": 0.3}
                        ]
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Beef Shawarma Sandwich",
                "description": "Marinated beef with tahini and pickles.",
                "price": 2.8,
                "image": "",
                "readyIn": "Ready in 10 minutes",
                "addOns": [
                    {"name": "Extra meat", "price": 1.0}
                ]
            }
        ]
    },
    "3": {
        "menu": [
            {
                "category": "Healthy Start",
                "items": [
                    {
                        "name": "Balila (Chickpea Bowl)",
                        "description": "Warm chickpeas with lemon, garlic, and cumin.",
                        "price": 2.0,
                        "image": "photos/Medicine/hummus-balila-11.jpg",
                        "addOns": [
                            {"name": "Pita bread", "price": 0.5}
                        ]
                    }
                ]
            },
            {
                "category": "Main Dishes",
                "items": [
                    {
                        "name": "Grilled Chicken with Rice",
                        "description": "Seasoned grilled chicken breast with saffron rice and salad.",
                        "price": 4.0,
                        "image": "photos/Medicine/images.jpg",
                        "addOns": [
                            {"name": "Garlic dip", "price": 0.5}
                        ]
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Grilled Halloumi Wrap",
                "description": "Grilled halloumi cheese with vegetables in saj bread.",
                "price": 2.5,
                "image": "",
                "readyIn": "Ready in 12 minutes",
                "addOns": []
            }
        ]
    },
    "4": {
        "menu": [
            {
                "category": "Executive Breakfast",
                "items": [
                    {
                        "name": "Shakshuka",
                        "description": "Eggs poached in spiced tomato sauce, served with bread.",
                        "price": 3.0,
                        "image": "photos/Business/Shakshuka-main-1.webp",
                        "addOns": [
                            {"name": "Extra egg", "price": 0.7}
                        ]
                    }
                ]
            },
            {
                "category": "Business Lunch",
                "items": [
                    {
                        "name": "Mansaf",
                        "description": "Jordan's national dish - lamb cooked in jameed sauce over rice.",
                        "price": 6.5,
                        "image": "photos/Business/mansaf-4-1-500x500.jpg",
                        "addOns": [
                            {"name": "Extra jameed sauce", "price": 1.0},
                            {"name": "Roasted nuts", "price": 1.5}
                        ]
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Kafta Sandwich",
                "description": "Spiced ground meat kafta with hummus and pickles.",
                "price": 3.0,
                "image": "photos/Business/ground-beef-pita-sandwich-recipe-4.jpg",
                "readyIn": "Ready in 15 minutes",
                "addOns": []
            }
        ]
    },
    "5": {
        "menu": [
            {
                "category": "Traditional Breakfast",
                "items": [
                    {
                        "name": "Fatteh",
                        "description": "Layers of toasted bread, chickpeas, yogurt, and pine nuts.",
                        "price": 3.5,
                        "image": "",
                        "addOns": []
                    }
                ]
            },
            {
                "category": "Lunch",
                "items": [
                    {
                        "name": "Kousa Mahshi (Stuffed Zucchini)",
                        "description": "Zucchini stuffed with rice and meat in tomato sauce.",
                        "price": 4.5,
                        "image": "",
                        "addOns": [
                            {"name": "Yogurt", "price": 0.8}
                        ]
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Mixed Grill Plate",
                "description": "Kafta, shish tawook, and lamb with rice.",
                "price": 5.5,
                "image": "",
                "readyIn": "Ready in 20 minutes",
                "addOns": []
            }
        ]
    },
    "6": {
        "menu": [
            {
                "category": "Mezze",
                "items": [
                    {
                        "name": "Mezze Platter",
                        "description": "Hummus, baba ghanoush, tabbouleh, and pita.",
                        "price": 4.0,
                        "image": "",
                        "addOns": [
                            {"name": "Extra pita", "price": 0.5}
                        ]
                    }
                ]
            },
            {
                "category": "Main Course",
                "items": [
                    {
                        "name": "Chicken Musakhan",
                        "description": "Roasted chicken with sumac, onions, and taboon bread.",
                        "price": 5.0,
                        "image": "",
                        "addOns": []
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Labneh & Za'atar Wrap",
                "description": "Creamy labneh with za'atar, cucumber, and mint.",
                "price": 2.0,
                "image": "",
                "readyIn": "Ready in 8 minutes",
                "addOns": []
            }
        ]
    },
    "7": {
        "menu": [
            {
                "category": "Energizing Breakfast",
                "items": [
                    {
                        "name": "Ful Medames",
                        "description": "Slow-cooked fava beans with lemon, garlic, and olive oil.",
                        "price": 2.5,
                        "image": "",
                        "addOns": [
                            {"name": "Hard boiled egg", "price": 0.5}
                        ]
                    }
                ]
            },
            {
                "category": "Sustaining Meals",
                "items": [
                    {
                        "name": "Lamb Kabsa",
                        "description": "Fragrant rice with tender lamb and mixed vegetables.",
                        "price": 6.0,
                        "image": "",
                        "addOns": []
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Shish Tawook Sandwich",
                "description": "Marinated grilled chicken with garlic sauce and pickles.",
                "price": 2.8,
                "image": "",
                "readyIn": "Ready in 12 minutes",
                "addOns": []
            }
        ]
    },
    "8": {
        "menu": [
            {
                "category": "Study Snacks",
                "items": [
                    {
                        "name": "Knafeh Slice",
                        "description": "Sweet cheese pastry with sugar syrup and pistachios.",
                        "price": 2.0,
                        "image": "",
                        "addOns": []
                    }
                ]
            },
            {
                "category": "Beverages",
                "items": [
                    {
                        "name": "Fresh Mint Tea",
                        "description": "Traditional Jordanian mint tea, served hot.",
                        "price": 0.8,
                        "image": "",
                        "addOns": []
                    },
                    {
                        "name": "Arabic Coffee",
                        "description": "Cardamom-spiced coffee served in small cups.",
                        "price": 1.0,
                        "image": "",
                        "addOns": []
                    }
                ]
            }
        ],
        "takeout": [
            {
                "name": "Tuna Sandwich",
                "description": "Tuna with vegetables and mayonnaise in fresh bread.",
                "price": 2.2,
                "image": "",
                "readyIn": "Ready in 7 minutes",
                "addOns": []
            }
        ]
    }
}


def seed():
    db = get_db()
    c  = db.cursor()

    # Clear existing menu data to avoid duplicates
    c.execute('DELETE FROM menu_item_addons')
    c.execute('DELETE FROM menu_items')

    total_items = 0

    for cafeteria_id, data in menu_data.items():
        # Regular menu items
        for section in data.get('menu', []):
            category = section['category']
            for item in section['items']:
                item_id = c.execute('''
                    INSERT INTO menu_items
                        (cafeteria_id, category, name, description, price, image, is_takeout)
                    VALUES (?, ?, ?, ?, ?, ?, 0)
                ''', (cafeteria_id, category, item['name'],
                      item['description'], item['price'], item.get('image', ''))).lastrowid

                for addon in item.get('addOns', []):
                    c.execute('''
                        INSERT INTO menu_item_addons (menu_item_id, name, price)
                        VALUES (?, ?, ?)
                    ''', (item_id, addon['name'], addon['price']))

                total_items += 1

        # Takeout items
        for item in data.get('takeout', []):
            item_id = c.execute('''
                INSERT INTO menu_items
                    (cafeteria_id, category, name, description, price, image, is_takeout, ready_in)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            ''', (cafeteria_id, 'Takeout', item['name'], item['description'],
                  item['price'], item.get('image', ''), item.get('readyIn', ''))).lastrowid

            for addon in item.get('addOns', []):
                c.execute('''
                    INSERT INTO menu_item_addons (menu_item_id, name, price)
                    VALUES (?, ?, ?)
                ''', (item_id, addon['name'], addon['price']))

            total_items += 1

    db.commit()
    db.close()
    print(f"Seeded {total_items} menu items across 8 cafeterias.")


if __name__ == '__main__':
    seed()
    