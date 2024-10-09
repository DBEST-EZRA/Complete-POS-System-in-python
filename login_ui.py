from tkinter import *
import tkinter as tk
from tkinter import messagebox
from auth_service import AuthService
from database_handler import DatabaseHandler


# Login UI Class
class LoginUI:
    def __init__(self, auth_service=None, controller=None, root=None):
        self.controller = controller
        self.auth_service = auth_service
        self.root = Toplevel(root) if root else None
        self._current_username = None

        if self.root:
            self.setup_ui()

    def get_username(self):
        return self._current_username

    def set_username(self, username):
        self._current_username = username  # Update this during loginq
    def setup_ui(self):
        # Use self.root instead of top
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("Amir Traders Login")

        # Background Image
        self.label1 = Label(self.root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="Images/employee_login.PNG")
        self.label1.configure(image=self.img)

        # Username Icon
        self.username_icon = PhotoImage(file="./images/user.png")
        self.username_icon_label = Label(self.root, image=self.username_icon, bg="white")
        self.username_icon_label.place(relx=0.57, rely=0.32)

        # Username Entry
        self.user_entry = Entry(self.root, font="-family {Poppins} -size 12", relief="flat", fg='gray')
        self.user_entry.place(relx=0.59, rely=0.32, width=302, height=24)
        self.user_entry.insert(0, "username")

        def on_user_entry_click(event):
            if self.user_entry.get() == "username":
                self.user_entry.delete(0, "end")
                self.user_entry.configure(fg='black')

        def on_user_focusout(event):
            if self.user_entry.get() == "":
                self.user_entry.insert(0, "username")
                self.user_entry.configure(fg='gray')

        self.user_entry.bind("<FocusIn>", on_user_entry_click)
        self.user_entry.bind("<FocusOut>", on_user_focusout)

        # Password Icon
        self.password_icon = PhotoImage(file="./images/lock.png")
        self.password_icon_label = Label(self.root, image=self.password_icon, bg="white")
        self.password_icon_label.place(relx=0.57, rely=0.41)

        # Password Entry
        self.password_entry = Entry(self.root, font="-family {Poppins} -size 12", relief="flat", fg='gray', show="")
        self.password_entry.place(relx=0.59, rely=0.41, width=302, height=24)
        self.password_entry.insert(0, "*******")

        def on_password_entry_click(event):
            if self.password_entry.get() == "*******":
                self.password_entry.delete(0, "end")
                self.password_entry.configure(fg='black', show="*")

        def on_password_focusout(event):
            if self.password_entry.get() == "":
                self.password_entry.insert(0, "*******")
                self.password_entry.configure(fg='gray', show="")

        self.password_entry.bind("<FocusIn>", on_password_entry_click)
        self.password_entry.bind("<FocusOut>", on_password_focusout)

        # Login Button
        self.button1 = Button(self.root)
        self.button1.place(relx=0.59, rely=0.51, width=300, height=45)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#ff3300")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=self.validate_login)  # Add login command


        # Bind "Enter" key to validate_login
        self.root.bind('<Return>', lambda event: self.validate_login())

        self.root.mainloop()

    def validate_login(self):
        username = self.user_entry.get().lower()
        password = self.password_entry.get()

        self.set_username(username)

        if username == "" or password == "":
            messagebox.showwarning("Input Error", "Please fill in both fields.")
            return

        response = self.auth_service.login_user(username, password)

        if response["success"]:
            messagebox.showinfo("Login Successful", response["message"])
            self.root.withdraw()  # Hide login window
            self.controller.show_billing_window()  # Show the billing window
        else:
            messagebox.showerror("Error", response["message"])
            self.password_entry.delete(0, END)





