// Jordanian Cafeteria Data - Replace this in cafeteria.html
const cafeteriaData = {
    "1": {
        name: "Engineering Cafeteria 1",
        image: "/photos/engeenering 1/55d38b8c-7fe9-49a2-8d36-2ac059cdb5e7.avif",
        description: "Authentic Jordanian meals perfect for long study sessions.",
        details: [
            "Location: Engineering Building Level 2",
            "Hours: 7:30 AM - 5:00 PM",
            "Daily Specials: 11:30 AM - 2:00 PM"
        ],
        notice: "Peak hours 11:30 AM – 1:30 PM • Expect short queues during capstone rush.",
        menu: [
            {
                category: "Breakfast",
                items: [
                    {
                        name: "Foul & Hummus Platter",
                        description: "Warm fava beans and creamy hummus with olive oil, served with fresh pita bread.",
                        price: "2.5 JOD",
                        image: "/photos/engeenering 1/55d38b8c-7fe9-49a2-8d36-2ac059cdb5e7.avif",
                        addOns: [
                            { name: "Extra pita", price: "0.5 JOD" },
                            { name: "Pickles & olives", price: "0.8 JOD" }
                        ]
                    },
                    {
                        name: "Manakish Za'atar",
                        description: "Freshly baked flatbread topped with za'atar and olive oil.",
                        price: "1.5 JOD",
                        image: "photos/engeenering 1/Manakish-Zaatar-1-of-1.jpeg",
                        addOns: [
                            { name: "Labneh side", price: "0.7 JOD" },
                            { name: "Cheese topping", price: "1 JOD" }
                        ]
                    }
                ]
            },
            {
                category: "Main Meals",
                items: [
                    {
                        name: "Maqluba (Upside Down Rice)",
                        description: "Traditional layered rice with chicken, eggplant, cauliflower and Middle Eastern spices.",
                        price: "4.5 JOD",
                        image: "photos/engeenering 1/maqluba-upside-down-chicken-and-rice_11005.jpg",
                        addOns: [
                            { name: "Yogurt salad", price: "0.8 JOD" },
                            { name: "Extra meat", price: "2 JOD" }
                        ]
                    },
                    {
                        name: "Chicken Shawarma Plate",
                        description: "Marinated chicken shawarma with rice, salad, and tahini sauce.",
                        price: "3.5 JOD",
                        image: "photos/engeenering 1/1667937205404.webp",
                        addOns: [
                            { name: "French fries", price: "1 JOD" },
                            { name: "Garlic sauce", price: "0.5 JOD" }
                        ]
                    }
                ]
            }
        ],
        takeout: {
            title: "Sandwiches & Wraps",
            description: "Quick meals perfect for takeaway.",
            items: [
                {
                    name: "Falafel Sandwich",
                    description: "Crispy falafel with tahini, vegetables, and pickles in fresh pita.",
                    price: "1.8 JOD",
                    image: "photos/engeenering 1/Falafel-Sandwich-Recipe-SQ.jpg",
                    readyIn: "Ready in 8 minutes",
                    addOns: [
                        { name: "Extra falafel", price: "0.5 JOD" },
                        { name: "French fries inside", price: "0.7 JOD" }
                    ]
                },
                {
                    name: "Chicken Shawarma Wrap",
                    description: "Tender chicken shawarma with garlic sauce and pickles in saj bread.",
                    price: "2.5 JOD",
                    image: "photos/engeenering 1/Screenshot-2025-07-28-at-11.webp",
                    readyIn: "Ready in 10 minutes",
                    addOns: [
                        { name: "Extra garlic sauce", price: "0.3 JOD" },
                        { name: "Cheese", price: "0.7 JOD" }
                    ]
                }
            ]
        }
    },
    "2": {
        name: "Engineering Cafeteria 2",
        image: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        description: "Fresh mezze and grilled specialties for engineers on the go.",
        details: [
            "Location: Engineering Annex Ground Floor",
            "Hours: 8:00 AM - 7:00 PM",
            "Grab & Go refills every hour"
        ],
        notice: "Mobile pickup shelf resets every 20 minutes—collect orders promptly.",
        menu: [
            {
                category: "Breakfast",
                items: [
                    {
                        name: "Labneh Plate",
                        description: "Creamy labneh drizzled with olive oil, served with cucumbers, tomatoes, and pita.",
                        price: "2 JOD",
                        image: "/photos/engeenering 1/55d38b8c-7fe9-49a2-8d36-2ac059cdb5e7.avif",
                        addOns: [
                            { name: "Mint leaves", price: "0.3 JOD" },
                            { name: "Za'atar mix", price: "0.5 JOD" }
                        ]
                    }
                ]
            },
            {
                category: "Lunch",
                items: [
                    {
                        name: "Meat Biryani",
                        description: "Spiced rice with tender lamb, nuts, and raisins.",
                        price: "5 JOD",
                        image: "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=200",
                        addOns: [
                            { name: "Yogurt", price: "0.8 JOD" },
                            { name: "Hot sauce", price: "0.3 JOD" }
                        ]
                    }
                ]
            }
        ],
        takeout: {
            title: "Quick Bites",
            description: "Fast and delicious portable meals.",
            items: [
                {
                    name: "Beef Shawarma Sandwich",
                    description: "Marinated beef with tahini and pickles.",
                    price: "2.8 JOD",
                    image: "https://images.unsplash.com/photo-1551782450-17144efb5723?w=200",
                    readyIn: "Ready in 10 minutes",
                    addOns: [
                        { name: "Extra meat", price: "1 JOD" }
                    ]
                }
            ]
        }
    },
    "3": {
        name: "Medicine Cafeteria",
        image: "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=800",
        description: "Nutritious Jordanian meals planned for medical students.",
        details: [
            "Location: Medical Sciences Pavilion",
            "Hours: 6:30 AM - 4:30 PM",
        ],
        notice: "Wellness drinks counter closes at 3:00 PM—plan rotations accordingly.",
        menu: [
            {
                category: "Healthy Start",
                items: [
                    {
                        name: "Balila (Chickpea Bowl)",
                        description: "Warm chickpeas with lemon, garlic, and cumin.",
                        price: "2 JOD",
                        image: "photos/Medicine/hummus-balila-11.jpg",
                        addOns: [
                            { name: "Pita bread", price: "0.5 JOD" }
                        ]
                    }
                ]
            },
            {
                category: "Main Dishes",
                items: [
                    {
                        name: "Grilled Chicken with Rice",
                        description: "Seasoned grilled chicken breast with saffron rice and salad.",
                        price: "4 JOD",
                        image: "photos/Medicine/images.jpg",
                        addOns: [
                            { name: "Garlic dip", price: "0.5 JOD" }
                        ]
                    }
                ]
            }
        ],
        takeout: {
            title: "Healthy Wraps",
            description: "Nutritious options for on-call schedules.",
            items: [
                {
                    name: "Grilled Halloumi Wrap",
                    description: "Grilled halloumi cheese with vegetables in saj bread.",
                    price: "2.5 JOD",
                    image: "https://images.unsplash.com/photo-1540912162-ef3c302c3f8f?w=200",
                    readyIn: "Ready in 12 minutes",
                    addOns: []
                }
            ]
        }
    },
    "4": {
        name: "Business Cafeteria",
        image: "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800",
        description: "Premium Jordanian cuisine for business students.",
        details: [
            "Location: Business School Atrium",
            "Hours: 8:00 AM - 6:00 PM",
            "Lunch service: 11:00 AM - 2:30 PM"
        ],
        notice: "Group orders available with 30 minutes notice.",
        menu: [
            {
                category: "Executive Breakfast",
                items: [
                    {
                        name: "Shakshuka",
                        description: "Eggs poached in spiced tomato sauce, served with bread.",
                        price: "3 JOD",
                        image: "photos/Business/Shakshuka-main-1.webp",
                        addOns: [
                            { name: "Extra egg", price: "0.7 JOD" }
                        ]
                    }
                ]
            },
            {
                category: "Business Lunch",
                items: [
                    {
                        name: "Mansaf",
                        description: "Jordan's national dish - lamb cooked in jameed sauce over rice.",
                        price: "6.5 JOD",
                        image: "photos/Business/mansaf-4-1-500x500.jpg",
                        addOns: [
                            { name: "Extra jameed sauce", price: "1 JOD" },
                            { name: "Roasted nuts", price: "1.5 JOD" }
                        ]
                    }
                ]
            }
        ],
        takeout: {
            title: "Executive Meals",
            description: "Premium sandwiches and plates.",
            items: [
                {
                    name: "Kafta Sandwich",
                    description: "Spiced ground meat kafta with hummus and pickles.",
                    price: "3 JOD",
                    image: "photos/Business/ground-beef-pita-sandwich-recipe-4.jpg",
                    readyIn: "Ready in 15 minutes",
                    addOns: []
                }
            ]
        }
    },
    "5": {
        name: "Science Cafeteria",
        image: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800",
        description: "Traditional flavors to fuel your discoveries.",
        details: [
            "Location: Science Complex Lower Level",
            "Hours: 7:45 AM - 6:15 PM",
            "Fresh juices available all day"
        ],
        notice: "Daily fresh juice specials - ask at counter.",
        menu: [
            {
                category: "Traditional Breakfast",
                items: [
                    {
                        name: "Fatteh",
                        description: "Layers of toasted bread, chickpeas, yogurt, and pine nuts.",
                        price: "3.5 JOD",
                        image: "https://images.unsplash.com/photo-YyZoVGbwkfA?w=200",
                        addOns: []
                    }
                ]
            },
            {
                category: "Lunch",
                items: [
                    {
                        name: "Kousa Mahshi (Stuffed Zucchini)",
                        description: "Zucchini stuffed with rice and meat in tomato sauce.",
                        price: "4.5 JOD",
                        image: "https://images.unsplash.com/photo-DkcuZwa1O50?w=200",
                        addOns: [
                            { name: "Yogurt", price: "0.8 JOD" }
                        ]
                    }
                ]
            }
        ],
        takeout: {
            title: "Quick Meals",
            description: "Lab-friendly portable options.",
            items: [
                {
                    name: "Mixed Grill Plate",
                    description: "Kafta, shish tawook, and lamb with rice.",
                    price: "5.5 JOD",
                    readyIn: "Ready in 20 minutes",
                    addOns: [],
                    image: "https://images.unsplash.com/photo-VG6cI5Y9Ikw?w=200"
                }
            ]
        }
    },
    "6": {
        name: "Arts Cafeteria",
        image: "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800",
        description: "Creative mezze and traditional comfort food.",
        details: [
            "Location: Fine Arts Center Courtyard",
            "Hours: 9:00 AM - 8:00 PM",
            "Studio snacks available all day"
        ],
        notice: "Daily featured pastry from the student baking collective after 3 PM.",
        menu: [
            {
                category: "Mezze",
                items: [
                    {
                        name: "Mezze Platter",
                        description: "Hummus, baba ghanoush, tabbouleh, and pita.",
                        price: "4 JOD",
                        image: "https://images.unsplash.com/photo--ssV85Xgl1U?w=200",
                        addOns: [
                            { name: "Extra pita", price: "0.5 JOD" }
                        ]
                    }
                ]
            },
            {
                category: "Main Course",
                items: [
                    {
                        name: "Chicken Musakhan",
                        description: "Roasted chicken with sumac, onions, and taboon bread.",
                        price: "5 JOD",
                        image: "https://images.unsplash.com/photo-RS0bbzjyTDg?w=200",
                        addOns: []
                    }
                ]
            }
        ],
        takeout: {
            title: "Artisan Wraps",
            description: "Gallery-worthy parcels.",
            items: [
                {
                    name: "Labneh & Za'atar Wrap",
                    description: "Creamy labneh with za'atar, cucumber, and mint.",
                    price: "2 JOD",
                    image: "https://images.unsplash.com/photo-_Ry6i-pU3Fs?w=200",
                    readyIn: "Ready in 8 minutes",
                    addOns: []
                }
            ]
        }
    },
    "7": {
        name: "Law Cafeteria",
        image: "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800",
        description: "Hearty meals for long study sessions.",
        details: [
            "Location: Law School Commons",
            "Hours: 7:30 AM - 9:00 PM",
            "Late-night service until exams end"
        ],
        notice: "Case study combo upgrades available after 6 PM.",
        menu: [
            {
                category: "Energizing Breakfast",
                items: [
                    {
                        name: "Ful Medames",
                        description: "Slow-cooked fava beans with lemon, garlic, and olive oil.",
                        price: "2.5 JOD",
                        addOns: [
                            { name: "Hard boiled egg", price: "0.5 JOD" }
                        ]
                    }
                ]
            },
            {
                category: "Sustaining Meals",
                items: [
                    {
                        name: "Lamb Kabsa",
                        description: "Fragrant rice with tender lamb and mixed vegetables.",
                        price: "6 JOD",
                        addOns: []
                    }
                ]
            }
        ],
        takeout: {
            title: "Study Fuel",
            description: "Case-ready combos with precise packaging.",
            items: [
                {
                    name: "Shish Tawook Sandwich",
                    description: "Marinated grilled chicken with garlic sauce and pickles.",
                    price: "2.8 JOD",
                    image: "https://images.unsplash.com/photo-VG6cI5Y9Ikw?w=200",
                    readyIn: "Ready in 12 minutes",
                    addOns: []
                }
            ]
        }
    },
    "8": {
        name: "Central Library Cafe",
        image: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
        description: "Quiet-friendly snacks and traditional beverages.",
        details: [
            "Location: Central Library Ground Floor",
            "Hours: 7:00 AM - 11:00 PM",
            "Quiet service after 8:00 PM"
        ],
        notice: "Fresh mint tea available all day.",
        menu: [
            {
                category: "Study Snacks",
                items: [
                    {
                        name: "Knafeh Slice",
                        description: "Sweet cheese pastry with sugar syrup and pistachios.",
                        price: "2 JOD",
                        addOns: []
                    }
                ]
            },
            {
                category: "Beverages",
                items: [
                    {
                        name: "Fresh Mint Tea",
                        description: "Traditional Jordanian mint tea, served hot.",
                        price: "0.8 JOD",
                        addOns: []
                    },
                    {
                        name: "Arabic Coffee",
                        description: "Cardamom-spiced coffee served in small cups.",
                        price: "1 JOD",
                        addOns: []
                    }
                ]
            }
        ],
        takeout: {
            title: "Library Wraps",
            description: "Silent-study friendly options.",
            items: [
                {
                    name: "Tuna Sandwich",
                    description: "Tuna with vegetables and mayonnaise in fresh bread.",
                    price: "2.2 JOD",
                    image: "https://images.unsplash.com/photo-c1cOeJbj1aY?w=200",
                    readyIn: "Ready in 7 minutes",
                    addOns: []
                }
            ]
        }
    }
};
