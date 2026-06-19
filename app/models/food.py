"""app/models/food.py — Food database model | Feature: Food Search Database"""
from app.models.base_model import BaseModel


class FoodModel(BaseModel):
    TABLE = 'foods'

    # ── Built-in static food database (100+ items) ──────────────────────────
    FOOD_DB = [
        # ── Nepali / South Asian foods ────────────────────────────────────
        {"id": 1,  "name": "Dal Bhat (1 plate)",       "category": "Nepali",      "calories": 450, "protein": 18, "carbs": 75, "fat": 8},
        {"id": 2,  "name": "Momo (6 pieces, steamed)", "category": "Nepali",      "calories": 290, "protein": 14, "carbs": 32, "fat": 9},
        {"id": 3,  "name": "Momo (6 pieces, fried)",   "category": "Nepali",      "calories": 390, "protein": 14, "carbs": 35, "fat": 18},
        {"id": 4,  "name": "Sel Roti (1 piece)",        "category": "Nepali",      "calories": 180, "protein": 3,  "carbs": 30, "fat": 6},
        {"id": 5,  "name": "Chowmein (1 plate)",        "category": "Nepali",      "calories": 380, "protein": 12, "carbs": 58, "fat": 10},
        {"id": 6,  "name": "Thukpa (1 bowl)",           "category": "Nepali",      "calories": 320, "protein": 15, "carbs": 45, "fat": 8},
        {"id": 7,  "name": "Dhido (1 plate)",           "category": "Nepali",      "calories": 310, "protein": 8,  "carbs": 65, "fat": 2},
        {"id": 8,  "name": "Gundruk Soup (1 bowl)",     "category": "Nepali",      "calories": 60,  "protein": 4,  "carbs": 8,  "fat": 1},
        {"id": 9,  "name": "Aloo Tama (1 bowl)",        "category": "Nepali",      "calories": 190, "protein": 6,  "carbs": 35, "fat": 4},
        {"id": 10, "name": "Chatamari (1 piece)",       "category": "Nepali",      "calories": 220, "protein": 9,  "carbs": 30, "fat": 7},
        {"id": 11, "name": "Samay Baji (1 set)",        "category": "Nepali",      "calories": 480, "protein": 20, "carbs": 62, "fat": 14},
        {"id": 12, "name": "Yomari (1 piece)",          "category": "Nepali",      "calories": 160, "protein": 4,  "carbs": 28, "fat": 4},
        {"id": 13, "name": "Aloo Ko Achar (100g)",      "category": "Nepali",      "calories": 110, "protein": 2,  "carbs": 18, "fat": 4},
        {"id": 14, "name": "Choila (100g)",             "category": "Nepali",      "calories": 210, "protein": 22, "carbs": 4,  "fat": 12},
        {"id": 15, "name": "Buff Curry (100g)",         "category": "Nepali",      "calories": 175, "protein": 20, "carbs": 5,  "fat": 9},
        {"id": 16, "name": "Roti (1 piece)",            "category": "Nepali",      "calories": 95,  "protein": 3,  "carbs": 18, "fat": 2},
        {"id": 17, "name": "Pulao Rice (1 cup)",        "category": "Nepali",      "calories": 280, "protein": 5,  "carbs": 55, "fat": 5},
        {"id": 18, "name": "Lapsi Candy (5 pieces)",    "category": "Nepali",      "calories": 90,  "protein": 0,  "carbs": 22, "fat": 0},

        # ── Grains & Staples ──────────────────────────────────────────────
        {"id": 19, "name": "White Rice (1 cup cooked)", "category": "Grains",      "calories": 206, "protein": 4,  "carbs": 45, "fat": 0},
        {"id": 20, "name": "Brown Rice (1 cup cooked)", "category": "Grains",      "calories": 216, "protein": 5,  "carbs": 45, "fat": 2},
        {"id": 21, "name": "White Bread (1 slice)",     "category": "Grains",      "calories": 79,  "protein": 3,  "carbs": 15, "fat": 1},
        {"id": 22, "name": "Whole Wheat Bread (1 sl.)", "category": "Grains",      "calories": 81,  "protein": 4,  "carbs": 14, "fat": 1},
        {"id": 23, "name": "Oats (100g dry)",           "category": "Grains",      "calories": 389, "protein": 17, "carbs": 66, "fat": 7},
        {"id": 24, "name": "Chapati (1 piece)",         "category": "Grains",      "calories": 104, "protein": 3,  "carbs": 18, "fat": 3},
        {"id": 25, "name": "Pasta (100g cooked)",       "category": "Grains",      "calories": 158, "protein": 6,  "carbs": 31, "fat": 1},
        {"id": 26, "name": "Noodles (100g cooked)",     "category": "Grains",      "calories": 138, "protein": 5,  "carbs": 25, "fat": 2},
        {"id": 27, "name": "Cornflakes (30g)",          "category": "Grains",      "calories": 114, "protein": 2,  "carbs": 26, "fat": 0},
        {"id": 28, "name": "Quinoa (1 cup cooked)",     "category": "Grains",      "calories": 222, "protein": 8,  "carbs": 39, "fat": 4},

        # ── Proteins / Meat ───────────────────────────────────────────────
        {"id": 29, "name": "Chicken Breast (100g)",     "category": "Protein",     "calories": 165, "protein": 31, "carbs": 0,  "fat": 4},
        {"id": 30, "name": "Chicken Thigh (100g)",      "category": "Protein",     "calories": 209, "protein": 26, "carbs": 0,  "fat": 11},
        {"id": 31, "name": "Egg (1 whole large)",       "category": "Protein",     "calories": 78,  "protein": 6,  "carbs": 1,  "fat": 5},
        {"id": 32, "name": "Egg White (1 large)",       "category": "Protein",     "calories": 17,  "protein": 4,  "carbs": 0,  "fat": 0},
        {"id": 33, "name": "Tuna (100g canned)",        "category": "Protein",     "calories": 116, "protein": 26, "carbs": 0,  "fat": 1},
        {"id": 34, "name": "Salmon (100g)",             "category": "Protein",     "calories": 208, "protein": 20, "carbs": 0,  "fat": 13},
        {"id": 35, "name": "Beef Mince (100g lean)",    "category": "Protein",     "calories": 215, "protein": 26, "carbs": 0,  "fat": 12},
        {"id": 36, "name": "Lamb (100g)",               "category": "Protein",     "calories": 294, "protein": 25, "carbs": 0,  "fat": 21},
        {"id": 37, "name": "Pork Chop (100g)",          "category": "Protein",     "calories": 231, "protein": 25, "carbs": 0,  "fat": 14},
        {"id": 38, "name": "Shrimp (100g)",             "category": "Protein",     "calories": 99,  "protein": 24, "carbs": 0,  "fat": 0},
        {"id": 39, "name": "Tofu Firm (100g)",          "category": "Protein",     "calories": 76,  "protein": 8,  "carbs": 2,  "fat": 5},

        # ── Dairy ─────────────────────────────────────────────────────────
        {"id": 40, "name": "Whole Milk (1 cup)",        "category": "Dairy",       "calories": 149, "protein": 8,  "carbs": 12, "fat": 8},
        {"id": 41, "name": "Skim Milk (1 cup)",         "category": "Dairy",       "calories": 83,  "protein": 8,  "carbs": 12, "fat": 0},
        {"id": 42, "name": "Greek Yogurt (100g plain)", "category": "Dairy",       "calories": 59,  "protein": 10, "carbs": 4,  "fat": 0},
        {"id": 43, "name": "Cheddar Cheese (30g)",      "category": "Dairy",       "calories": 120, "protein": 7,  "carbs": 0,  "fat": 10},
        {"id": 44, "name": "Butter (1 tbsp)",           "category": "Dairy",       "calories": 102, "protein": 0,  "carbs": 0,  "fat": 12},
        {"id": 45, "name": "Paneer (100g)",             "category": "Dairy",       "calories": 265, "protein": 18, "carbs": 3,  "fat": 20},
        {"id": 46, "name": "Curd / Dahi (100g)",        "category": "Dairy",       "calories": 61,  "protein": 3,  "carbs": 5,  "fat": 3},

        # ── Legumes ───────────────────────────────────────────────────────
        {"id": 47, "name": "Lentils Dal (100g cooked)", "category": "Legumes",     "calories": 116, "protein": 9,  "carbs": 20, "fat": 0},
        {"id": 48, "name": "Chickpeas (100g cooked)",   "category": "Legumes",     "calories": 164, "protein": 9,  "carbs": 27, "fat": 3},
        {"id": 49, "name": "Black Beans (100g cooked)", "category": "Legumes",     "calories": 132, "protein": 9,  "carbs": 24, "fat": 1},
        {"id": 50, "name": "Kidney Beans (100g)",       "category": "Legumes",     "calories": 127, "protein": 9,  "carbs": 23, "fat": 1},
        {"id": 51, "name": "Soybeans (100g cooked)",    "category": "Legumes",     "calories": 173, "protein": 17, "carbs": 10, "fat": 9},
        {"id": 52, "name": "Peanuts (30g)",             "category": "Legumes",     "calories": 170, "protein": 7,  "carbs": 5,  "fat": 14},
        {"id": 53, "name": "Rajma Curry (1 bowl)",      "category": "Legumes",     "calories": 210, "protein": 11, "carbs": 30, "fat": 5},

        # ── Vegetables ────────────────────────────────────────────────────
        {"id": 54, "name": "Broccoli (100g)",           "category": "Vegetables",  "calories": 34,  "protein": 3,  "carbs": 7,  "fat": 0},
        {"id": 55, "name": "Spinach (100g raw)",        "category": "Vegetables",  "calories": 23,  "protein": 3,  "carbs": 4,  "fat": 0},
        {"id": 56, "name": "Carrot (1 medium)",         "category": "Vegetables",  "calories": 25,  "protein": 1,  "carbs": 6,  "fat": 0},
        {"id": 57, "name": "Potato (100g boiled)",      "category": "Vegetables",  "calories": 87,  "protein": 2,  "carbs": 20, "fat": 0},
        {"id": 58, "name": "Sweet Potato (100g)",       "category": "Vegetables",  "calories": 86,  "protein": 2,  "carbs": 20, "fat": 0},
        {"id": 59, "name": "Tomato (1 medium)",         "category": "Vegetables",  "calories": 22,  "protein": 1,  "carbs": 5,  "fat": 0},
        {"id": 60, "name": "Cucumber (100g)",           "category": "Vegetables",  "calories": 15,  "protein": 1,  "carbs": 4,  "fat": 0},
        {"id": 61, "name": "Cabbage (100g)",            "category": "Vegetables",  "calories": 25,  "protein": 1,  "carbs": 6,  "fat": 0},
        {"id": 62, "name": "Capsicum (1 medium)",       "category": "Vegetables",  "calories": 31,  "protein": 1,  "carbs": 7,  "fat": 0},
        {"id": 63, "name": "Cauliflower (100g)",        "category": "Vegetables",  "calories": 25,  "protein": 2,  "carbs": 5,  "fat": 0},
        {"id": 64, "name": "Onion (1 medium)",          "category": "Vegetables",  "calories": 44,  "protein": 1,  "carbs": 10, "fat": 0},
        {"id": 65, "name": "Garlic (1 clove)",          "category": "Vegetables",  "calories": 4,   "protein": 0,  "carbs": 1,  "fat": 0},

        # ── Fruits ────────────────────────────────────────────────────────
        {"id": 66, "name": "Banana (1 medium)",         "category": "Fruits",      "calories": 105, "protein": 1,  "carbs": 27, "fat": 0},
        {"id": 67, "name": "Apple (1 medium)",          "category": "Fruits",      "calories": 95,  "protein": 0,  "carbs": 25, "fat": 0},
        {"id": 68, "name": "Mango (100g)",              "category": "Fruits",      "calories": 60,  "protein": 1,  "carbs": 15, "fat": 0},
        {"id": 69, "name": "Orange (1 medium)",         "category": "Fruits",      "calories": 62,  "protein": 1,  "carbs": 15, "fat": 0},
        {"id": 70, "name": "Grapes (100g)",             "category": "Fruits",      "calories": 67,  "protein": 1,  "carbs": 17, "fat": 0},
        {"id": 71, "name": "Watermelon (100g)",         "category": "Fruits",      "calories": 30,  "protein": 1,  "carbs": 8,  "fat": 0},
        {"id": 72, "name": "Strawberry (100g)",         "category": "Fruits",      "calories": 32,  "protein": 1,  "carbs": 8,  "fat": 0},
        {"id": 73, "name": "Papaya (100g)",             "category": "Fruits",      "calories": 43,  "protein": 0,  "carbs": 11, "fat": 0},
        {"id": 74, "name": "Avocado (half)",            "category": "Fruits",      "calories": 160, "protein": 2,  "carbs": 9,  "fat": 15},
        {"id": 75, "name": "Guava (1 medium)",          "category": "Fruits",      "calories": 37,  "protein": 1,  "carbs": 8,  "fat": 1},

        # ── Nuts & Seeds ──────────────────────────────────────────────────
        {"id": 76, "name": "Almonds (30g / ~23 nuts)",  "category": "Nuts",        "calories": 164, "protein": 6,  "carbs": 6,  "fat": 14},
        {"id": 77, "name": "Cashews (30g)",             "category": "Nuts",        "calories": 157, "protein": 5,  "carbs": 9,  "fat": 12},
        {"id": 78, "name": "Walnuts (30g)",             "category": "Nuts",        "calories": 185, "protein": 4,  "carbs": 4,  "fat": 18},
        {"id": 79, "name": "Chia Seeds (1 tbsp)",       "category": "Nuts",        "calories": 58,  "protein": 2,  "carbs": 5,  "fat": 4},
        {"id": 80, "name": "Flax Seeds (1 tbsp)",       "category": "Nuts",        "calories": 55,  "protein": 2,  "carbs": 3,  "fat": 4},
        {"id": 81, "name": "Sunflower Seeds (30g)",     "category": "Nuts",        "calories": 165, "protein": 6,  "carbs": 7,  "fat": 14},

        # ── Oils & Fats ───────────────────────────────────────────────────
        {"id": 82, "name": "Olive Oil (1 tbsp)",        "category": "Fats",        "calories": 119, "protein": 0,  "carbs": 0,  "fat": 14},
        {"id": 83, "name": "Coconut Oil (1 tbsp)",      "category": "Fats",        "calories": 121, "protein": 0,  "carbs": 0,  "fat": 14},
        {"id": 84, "name": "Mustard Oil (1 tbsp)",      "category": "Fats",        "calories": 124, "protein": 0,  "carbs": 0,  "fat": 14},
        {"id": 85, "name": "Ghee (1 tbsp)",             "category": "Fats",        "calories": 112, "protein": 0,  "carbs": 0,  "fat": 13},

        # ── Beverages ─────────────────────────────────────────────────────
        {"id": 86, "name": "Chai Tea (1 cup, milk+sugar)", "category": "Beverages","calories": 80,  "protein": 2,  "carbs": 11, "fat": 3},
        {"id": 87, "name": "Black Coffee (1 cup)",      "category": "Beverages",   "calories": 2,   "protein": 0,  "carbs": 0,  "fat": 0},
        {"id": 88, "name": "Orange Juice (1 cup)",      "category": "Beverages",   "calories": 112, "protein": 2,  "carbs": 26, "fat": 0},
        {"id": 89, "name": "Lassi (1 glass, sweet)",    "category": "Beverages",   "calories": 150, "protein": 5,  "carbs": 22, "fat": 5},
        {"id": 90, "name": "Coke / Pepsi (330ml can)",  "category": "Beverages",   "calories": 139, "protein": 0,  "carbs": 35, "fat": 0},
        {"id": 91, "name": "Protein Shake (1 scoop)",   "category": "Beverages",   "calories": 130, "protein": 25, "carbs": 5,  "fat": 2},

        # ── Snacks & Fast Food ────────────────────────────────────────────
        {"id": 92, "name": "Pani Puri (6 pieces)",      "category": "Snacks",      "calories": 180, "protein": 3,  "carbs": 30, "fat": 6},
        {"id": 93, "name": "Samosa (1 piece)",          "category": "Snacks",      "calories": 262, "protein": 5,  "carbs": 30, "fat": 14},
        {"id": 94, "name": "Potato Chips (30g)",        "category": "Snacks",      "calories": 152, "protein": 2,  "carbs": 15, "fat": 10},
        {"id": 95, "name": "Biscuit/Cookie (2 pieces)", "category": "Snacks",      "calories": 130, "protein": 2,  "carbs": 19, "fat": 6},
        {"id": 96, "name": "Burger (beef, standard)",   "category": "Snacks",      "calories": 490, "protein": 28, "carbs": 40, "fat": 24},
        {"id": 97, "name": "Pizza (1 slice, cheese)",   "category": "Snacks",      "calories": 272, "protein": 12, "carbs": 34, "fat": 10},
        {"id": 98, "name": "French Fries (medium)",     "category": "Snacks",      "calories": 365, "protein": 4,  "carbs": 48, "fat": 17},
        {"id": 99, "name": "Dark Chocolate (30g)",      "category": "Snacks",      "calories": 155, "protein": 2,  "carbs": 17, "fat": 9},
        {"id": 100,"name": "Popcorn (30g air-popped)",  "category": "Snacks",      "calories": 109, "protein": 3,  "carbs": 22, "fat": 1},

        # ── Supplements ───────────────────────────────────────────────────
        {"id": 101,"name": "Whey Protein (1 scoop 30g)","category": "Supplements", "calories": 120, "protein": 24, "carbs": 3,  "fat": 2},
        {"id": 102,"name": "Mass Gainer (100g serving)","category": "Supplements", "calories": 380, "protein": 20, "carbs": 60, "fat": 5},
        {"id": 103,"name": "BCAA (1 serving)",          "category": "Supplements", "calories": 20,  "protein": 5,  "carbs": 0,  "fat": 0},
    ]

    @classmethod
    def search(cls, query: str, limit: int = 20):
        """Search food database by name (case-insensitive)."""
        q = query.lower().strip()
        if not q:
            return cls.FOOD_DB[:limit]
        results = [f for f in cls.FOOD_DB if q in f['name'].lower()]
        return results[:limit]

    CUSTOM_ID_OFFSET = 10000  # custom food IDs are db_id + 10000 in the UI

    @classmethod
    def get_by_id(cls, food_id: int):
        # Custom foods use offset IDs (>= 10000) to avoid clashing with static DB
        if food_id >= cls.CUSTOM_ID_OFFSET:
            real_id = food_id - cls.CUSTOM_ID_OFFSET
            try:
                from app.models.database import get_db
                db = get_db()
                cur = db.cursor()
                cur.execute(
                    "SELECT id, name, calories, protein_g AS protein, carbs_g AS carbs, fat_g AS fat, category FROM custom_foods WHERE id=%s",
                    (real_id,)
                )
                row = cur.fetchone()
                if row:
                    return dict(row)
            except Exception:
                pass
            return None
        # Static food DB
        for f in cls.FOOD_DB:
            if f['id'] == food_id:
                return f
        return None

    @classmethod
    def categories(cls):
        seen = []
        cats = []
        for f in cls.FOOD_DB:
            if f['category'] not in seen:
                seen.append(f['category'])
                cats.append(f['category'])
        return cats

    @classmethod
    def by_category(cls, category: str):
        return [f for f in cls.FOOD_DB if f['category'] == category]

    # ── Custom user foods (stored in DB) ────────────────────────────────
    @classmethod
    def add_custom(cls, uid, name, calories, protein, carbs, fat, category='Custom'):
        return cls.execute(
            'INSERT INTO custom_foods(user_id,name,calories,protein_g,carbs_g,fat_g,category,created_at) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s,NOW())',
            (uid, name, calories, protein, carbs, fat, category)
        )

    @classmethod
    def get_custom_by_user(cls, uid):
        return cls.fetch_all(
            'SELECT * FROM custom_foods WHERE user_id=%s ORDER BY created_at DESC', (uid,)
        )

    @classmethod
    def delete_custom(cls, cid, uid):
        return cls.execute('DELETE FROM custom_foods WHERE id=%s AND user_id=%s', (cid, uid))
