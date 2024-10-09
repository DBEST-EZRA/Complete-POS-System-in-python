import sqlite3

# Database Handler Class
class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.c = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        # Create the users table if it doesn't exist
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT)
        ''')
        self.conn.commit()

    def insert_user(self, username, password, role):
        try:
            self.c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def close(self):
        if self.conn:
            self.conn.close()

    def get_cursor(self):
        return self.conn.cursor()

    def fetch_product_categories(self):
        try:
            cur = self.get_cursor()
            find_category_query = "SELECT DISTINCT product_cat FROM raw_inventory"
            cur.execute(find_category_query)
            result = cur.fetchall()
            return [category[0] for category in result]  # Returns a list of unique categories
        except Exception as e:
            print("Failed to fetch product categories:", e)
            return []