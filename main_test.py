from database_handler import DatabaseHandler
from navigation_controller import NavigationController
from auth_service import AuthService
from tkinter import Tk


def main():
    root = Tk()
    db_handler = DatabaseHandler('pos_database.db')  # Initialize the DatabaseHandler here
    db_handler.connect()

    auth_service = AuthService(db_handler)  # Pass db_handler to AuthService
    controller = NavigationController(db_handler, auth_service, root)  # Pass db_handler to the controller

    controller.show_login()  # Show the login screen initially

    root.mainloop()

if __name__ == "__main__":
    main()
