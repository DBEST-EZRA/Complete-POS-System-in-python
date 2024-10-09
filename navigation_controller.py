from tkinter import Toplevel
from login_ui import LoginUI


class NavigationController:

    def __init__(self, root, auth_service):
        self.root = root
        self.auth_service = auth_service
        self.current_window = None
        self.username = None


    def show_login(self):
        if self.current_window:
            self.current_window.withdraw()

        # login_window = Toplevel(self.root)
        LoginUI(self.auth_service, self, self.root)
        # self.current_window = login_window

    def show_billing_window(self):
        if self.current_window:  # Hide the current window if it exists
            self.current_window.withdraw()

        # Importing bill_window at the start of the function instead of globally
        from employee import bill_window

        # Create a new Toplevel window for billing
        self.current_window = Toplevel(self.root)

        # Initialize the bill_window and pass the new window and the controller
        billing_window_instance = bill_window(self.current_window, self)

        # Setup the billing UI
        billing_window_instance.setup_billing_ui()


    def close_current_window(self):
        if self.current_window is not None:
            self.current_window.destroy()
            self.current_window = None

    def exit(self):
        if self.current_window is not None:
            self.current_window.destroy()
        exit()

# Entry point
# if __name__ == "__main__":
#
#     root = Tk()
#
#     controller = NavigationController(root)
#     controller.show_login()
