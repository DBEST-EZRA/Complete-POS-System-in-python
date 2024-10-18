from database_handler import DatabaseHandler

# Authentication Service Class
class AuthService:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def login_user(self, username, password):
        # Query the database to check credentials
        self.db_handler.c.execute("SELECT * FROM employee WHERE name = ? AND password = ?", (username, password))
        user = self.db_handler.c.fetchone()
        if user:
            return {"success": True, "message": f"Welcome, {username}!", "role": user[2]}
        else:
            return {"success": False, "message": "Invalid username or password!"}


