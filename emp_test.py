import re
import random
import string
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext as tkst



class Employee:
    def __init__(self, username, password, first_name, last_name):
        # User-related information
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def random_bill_number(stringLength):
        lettersAndDigits = string.ascii_letters.upper() + string.digits
        rand_num = ''.join(random.choice(lettersAndDigits) for i in range(stringLength - 2))
        return 'AT' + rand_num

    @staticmethod
    def valid_phone(phone):
        return bool(re.match(r"^(?:\+92|0)\d{10}$", phone))


class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty


class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        if self.items:
            self.items.pop()

    def clear_items(self):
        self.items.clear()

    def total(self):
        return sum(item.price * item.qty for item in self.items)

    def is_empty(self):
        return len(self.items) == 0

    def all_cart_items(self):
        for item in self.items:
            if item.product_name in self.dictionary:
                self.dictionary[item.product_name] += item.qty
            else:
                self.dictionary[item.product_name] = item.qty


class BillWindow:
    def __init__(self, root, navigation_controller=None):
        # Initialize the root window and optional navigation controller
        self.root = root
        self.navigation_controller = navigation_controller
        self.img = None

        # Class attributes for storing user and billing-related information using StringVar
        self.user = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.customer_name = StringVar()
        self.customer_number = StringVar()
        self.bill_number = StringVar()
        self.bill_date = StringVar()

        # Initialize cart for bill window
        self.cart = Cart()

    def setup_billing_ui(self):
        # Call methods to setup UI components
        self.setup_window()
        self.setup_background_image()
        self.setup_labels()
        self.setup_input_fields()
        self.setup_buttons()
        self.setup_dropdowns()
        self.setup_scrolled_text()

    def setup_window(self):
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.title("Amir Traders Billing System")

    def setup_background_image(self):
        try:
            self.img = PhotoImage(file="Images/bill_window.png")
            label = tk.Label(self.root, image=self.img)
            label.place(relx=0, rely=0, width=1366, height=768)
        except Exception as e:
            print("Failed to load image. Check the path:", e)

    def setup_labels(self):
        # Label setup example
        self.create_label(0.038, 0.055, 136, 30, text=self.username.get(), font="-family {Poppins} -size 10")
        self.create_label(0.9, 0.065, 102, 36, text="clock", font="-family {Poppins Light} -size 12")

    def setup_input_fields(self):
        # Input fields for customer data
        self.create_entry(0.509, 0.23, 240, 24, textvariable=self.customer_name)
        self.create_entry(0.791, 0.23, 240, 24, textvariable=self.customer_number)

    def setup_buttons(self):
        # Button setup example
        buttons = [
            (0.031, 0.104, "Logout", 76, 23, self.logout),
            (0.315, 0.234, "Search", 76, 23, self.search_bill),
            (0.048, 0.885, "Total", 86, 25, self.total_bill),
            (0.141, 0.885, "Generate", 84, 25, self.gen_bill),
            (0.230, 0.885, "Clear", 86, 25, self.clear_bill),
            (0.322, 0.885, "Exit", 86, 25, self.exit_billing),
            (0.098, 0.734, "Add To Cart", 86, 26, self.add_to_cart),
            (0.194, 0.734, "Remove", 68, 26, self.remove_product),
        ]
        for relx, rely, text, width, height, command in buttons:
            self.create_button(relx, rely, width, height, text, command)

    def setup_dropdowns(self):
        # Dropdowns setup
        font = ("Poppins", "8")
        self.combo1 = self.create_combobox(0.035, 0.408, 477, 26, font=font)
        self.combo1.bind("<<ComboboxSelected>>", self.get_category)

    def setup_scrolled_text(self):
        self.scrolled_text = tkst.ScrolledText(self.root)
        self.scrolled_text.place(relx=0.439, rely=0.586, width=695, height=275)
        self.scrolled_text.configure(borderwidth=0, font="-family {Podkova} -size 8", state="disabled")

    def create_label(self, relx, rely, width, height, text, font):
        label = Label(self.root)
        label.place(relx=relx, rely=rely, width=width, height=height)
        label.configure(font=font, text=text, background="#ffffff", anchor="w")
        return label

    def create_entry(self, relx, rely, width, height, textvariable):
        entry = Entry(self.root)
        entry.place(relx=relx, rely=rely, width=width, height=height)
        entry.configure(font="-family {Poppins} -size 12", textvariable=textvariable)
        return entry

    def create_button(self, relx, rely, width, height, text, command):
        button = Button(self.root)
        button.place(relx=relx, rely=rely, width=width, height=height)
        button.configure(relief="flat", activebackground="#CF1E14", cursor="hand2", background="#CF1E14",
                         font="-family {Poppins SemiBold} -size 10", text=text, command=command)
        return button

    def create_combobox(self, relx, rely, width, height, font, state="readonly"):
        combo = ttk.Combobox(self.root)
        combo.place(relx=relx, rely=rely, width=width, height=height)
        combo.configure(font=font, state=state)
        return combo

    def get_category(self, event):
        # Method to handle category selection
        self.combo2.configure(state="readonly")
        self.combo2.set('')

    def add_to_cart(self):
        # Method to add item to the cart
        product_name = self.combo3.get()
        if product_name:
            product_qty = self.entry4.get()
            if product_qty.isdigit():
                item = Item(product_name, mrp, int(product_qty))
                self.cart.add_item(item)
                self.update_cart_display()

    def update_cart_display(self):
        # Method to update the cart display in the scrolled text
        self.scrolled_text.configure(state="normal")
        self.scrolled_text.delete('1.0', END)
        for item in self.cart.items:
            self.scrolled_text.insert(END, f"{item.product_name}\t\t{item.qty}\t\t{item.price * item.qty}\n")
        self.scrolled_text.configure(state="disabled")

    def exit_billing(self):
        # Function to exit billing window
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root)
        if sure:
            self.root.destroy()
