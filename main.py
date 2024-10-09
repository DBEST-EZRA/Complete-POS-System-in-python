from tkinter import Tk
from navigation_controller import NavigationController
from auth_service import AuthService  # Assuming you have an AuthService class
from database_handler import DatabaseHandler

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    # calling Database handler to control db object
    db_handler = DatabaseHandler('sqlite.db') #pos_database.db
    db_handler.connect()
    auth_service = AuthService(db_handler)
    navigation_controller = NavigationController(root, auth_service)

    # Start with login window
    navigation_controller.show_login()

    root.mainloop()
