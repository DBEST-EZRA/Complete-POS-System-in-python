from database_handler import DatabaseHandler

# Authentication Service Class
class AuthService:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def signup_user(self, username, password, role):
        if username and password and role:
            if self.db_handler.insert_user(username, password, role):
                return {"success": True, "message": "Account created successfully!"}
            else:
                return {"success": False, "message": "Username already exists!"}
        else:
            return {"success": False, "message": "All fields are required!"}

    def login_user(self, username, password):
        # Query the database to check credentials
        self.db_handler.c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.db_handler.c.fetchone()
        if user:
            return {"success": True, "message": f"Welcome, {username}!", "role": user[2]}
        else:
            return {"success": False, "message": "Invalid username or password!"}


