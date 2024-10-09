import sqlite3
import re
import random
import string
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
import login_ui as lg
from database_handler import DatabaseHandler


# db_handler = DatabaseHandler('sqlite.db')
def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    rand_num = ''.join(random.choice(lettersAndDigits) for i in range(stringLength - 2))
    return 'AT' + rand_num


def valid_phone(phone):
    if re.match(r"^(?:\+92|0)\d{10}$", phone):
        return True
    return False


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
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        return len(self.items) == 0

    def allCart(self):
        for i in self.items:
            if i.product_name in self.dictionary:
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary.update({i.product_name: i.qty})


# Function to Exit the Billing Window
def exit_billing(parent):
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=parent)
    if sure:
        parent.destroy()


class bill_window:

    def __init__(self, root, navigation_controller=None):
        # Initialize the root window and optional navigation controller
        self.root = root
        self.navigation_controller = navigation_controller
        self.img = None

        # Class attributes for storing user and billing-related information using StringVar
        self.user = StringVar()
        self.username = StringVar()
        self.passwd = StringVar()
        self.fname = StringVar()
        self.lname = StringVar()
        self.new_user = StringVar()
        self.new_passwd = StringVar()
        self.cust_name = StringVar()
        self.cust_num = StringVar()
        self.cust_new_bill = StringVar()
        self.cust_search_bill = StringVar()
        self.bill_date = StringVar()


    def setup_billing_ui(self): # Setting up UI
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

    def setup_background_image(self):       # Setup the background image for the billing screen
        try:
            self.img = PhotoImage(file="Images/bill_window.png")
            self.label = tk.Label(self.root, image=self.img)
            self.label.place(relx=0, rely=0, width=1366, height=768)
        except Exception as e:
            print("Failed to load image. Check the path:", e)

    def setup_labels(self):
        login_instance = lg.LoginUI(auth_service=None, controller=None, root=None)  # Create an instance of LoginUI
        self.username = login_instance.get_username()
        self.create_label(relx=0.038, rely=0.055, width=136, height=30, text=self.username,
                          font="-family {Poppins} -size 10")
        self.clock = self.create_label(relx=0.9, rely=0.065, width=102, height=36, text="clock",
                                       font="-family {Poppins Light} -size 12")
        self.time() #ADDED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def setup_input_fields(self):
        self.entry1 = self.create_entry(relx=0.509, rely=0.23, width=240, height=24, textvariable=self.cust_name)
        self.entry2 = self.create_entry(relx=0.791, rely=0.23, width=240, height=24, textvariable=self.cust_num)
        self.entry3 = self.create_entry(relx=0.102, rely=0.23, width=240, height=24, textvariable=self.cust_search_bill)

    def setup_buttons(self):
        buttons = [
            (0.031, 0.104, "Logout", 76, 23, self.logout),
            (0.315, 0.234, "Search", 76, 23, self.search_bill),
            (0.048, 0.885, "Total", 86, 25, self.total_bill),
            (0.141, 0.885, "Generate", 84, 25, self.gen_bill),
            (0.230, 0.885, "Clear", 86, 25, self.clear_bill),
            (0.322, 0.885, "Exit", 86, 25, exit),
            (0.098, 0.734, "Add To Cart", 86, 26, self.add_to_cart),
            (0.194, 0.734, "Remove", 68, 26, self.remove_product),
            (0.274, 0.734, "Clear", 84, 26, self.clear_selection)
        ]

        for relx, rely, text, x, y, command in buttons:
            self.create_button(relx, rely, width=x, height=y, text=text, command=command)




    def fetch_data(self, query, params=None):
        # Connect to the SQLite database
        conn = sqlite3.connect('sqlite.db')  # Replace with your .db file
        cursor = conn.cursor()

        # Execute the query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Fetch all results
        data = cursor.fetchall()

        # Close the connection
        conn.close()

        # Extract values from the tuples
        return [row[0] for row in data]

    def update_subcategories(self, event):
        # Get the selected category from combo1
        selected_category = self.combo1.get()

        # Query to find subcategories based on the selected category
        find_subcat = """
            SELECT DISTINCT product_subcat
            FROM raw_inventory
            WHERE product_cat = ?
        """

        # Fetch subcategories
        subcategories = self.fetch_data(find_subcat, (selected_category,))

        # Enable combo2 and update its values
        if subcategories:
            self.combo2['values'] = subcategories
            self.combo2.current(0)  # Set to the first item if available
            self.combo2.configure(state="readonly")  # Enable combo2
        else:
            self.combo2['values'] = []
            self.combo2.configure(state="disabled")





    def setup_dropdowns(self):
        text_font = ("Poppins", "8")
        self.combo1 = self.create_combobox(relx=0.035, rely=0.408, width=477, height=26, font=text_font)
        self.combo1.bind("<<ComboboxSelected>>", self.update_subcategories)

        self.combo2 = self.create_combobox(relx=0.035, rely=0.479, width=477, height=26, font=text_font,
                                           state="disabled")
        self.combo3 = self.create_combobox(relx=0.035, rely=0.551, width=477, height=26, font=text_font,
                                           state="disabled")

        self.entry4 = ttk.Entry(self.root)
        self.entry4.place(relx=0.035, rely=0.629, width=477, height=26)
        self.entry4.configure(font="-family {Poppins} -size 8", foreground="#000000", state="disabled")

    def setup_scrolled_text(self):
        self.Scrolledtext1 = tkst.ScrolledText(self.root)
        self.Scrolledtext1.place(relx=0.439, rely=0.586, width=695, height=275)
        self.Scrolledtext1.configure(borderwidth=0, font="-family {Podkova} -size 8", state="disabled")

    def create_label(self, relx, rely, width, height, text, font):
        label = Label(self.root)
        label.place(relx=relx, rely=rely, width=width, height=height)
        label.configure(font=font, foreground="#000000", background="#ffffff", text=text, anchor="w")
        return label

    def create_entry(self, relx, rely, width, height, textvariable):
        entry = Entry(self.root)
        entry.place(relx=relx, rely=rely, width=width, height=height)
        entry.configure(font="-family {Poppins} -size 12", relief="flat", textvariable=textvariable)
        return entry

    def create_button(self, relx, rely, width, height, text, command):
        button = Button(self.root)
        button.place(relx=relx, rely=rely, width=width, height=height)
        button.configure(relief="flat", overrelief="flat", activebackground="#CF1E14", cursor="hand2",
                         foreground="#ffffff", background="#CF1E14", font="-family {Poppins SemiBold} -size 10",
                         borderwidth="0", text=text, command=command)
        return button


#FROM HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




    def create_combobox(self, relx, rely, width, height, font, state="readonly"):
        data = self.fetch_data("SELECT DISTINCT product_cat FROM raw_inventory")
        combo = ttk.Combobox(self.root, values=data) #!!!!!
        combo.place(relx=relx, rely=rely, width=width, height=height)
        combo.configure(font=font, state=state)
        combo.option_add("*TCombobox*Listbox.font", font)
        combo.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")
        return combo


#TO HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT product_name FROM raw_inventory WHERE product_cat = ? and product_subcat = ?"
        # cur.execute(find_product, [self.combo1.get(), self.combo2.get()])
        # result3 = cur.fetchall()
        # pro = []
        # for k in range(len(result3)):
        #     pro.append(result3[k][0])
        #
        # self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>", self.show_qty)
        self.entry4.configure(state="disabled")

    def show_qty(self, Event):
        self.entry4.configure(state="normal")
        self.qty_label = Label(self.root)
        self.qty_label.place(relx=0.033, rely=0.664, width=82, height=26)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        product_name = self.combo3.get()
        find_qty = "SELECT stock FROM raw_inventory WHERE product_name = ?"
        # cur.execute(find_qty, [product_name])
        # results = cur.fetchone()
        # self.qty_label.configure(text="In Stock: {}".format(results[0]))
        self.qty_label.configure(background="#ffffff")
        self.qty_label.configure(foreground="#333333")

    cart = Cart()

    def add_to_cart(self):
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        if strr.find('Total') == -1:
            product_name = self.combo3.get()
            if (product_name != ""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit() == True:
                    if (stock - int(product_qty)) >= 0:
                        sp = mrp * int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=self.root)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=self.root)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=self.root)
        else:
            self.Scrolledtext1.delete('1.0', END)
            new_li = []
            li = strr.split("\n")
            for i in range(len(li)):
                if len(li[i]) != 0:
                    if li[i].find('Total') == -1:
                        new_li.append(li[i])
                    else:
                        break
            for j in range(len(new_li) - 1):
                self.Scrolledtext1.insert('insert', new_li[j])
                self.Scrolledtext1.insert('insert', '\n')
            product_name = self.combo3.get()
            if (product_name != ""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock, product_id FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit() == True:
                    if (stock - int(product_qty)) >= 0:
                        sp = results[0][0] * int(product_qty)
                        item = Item(product_name, mrp, int(product_qty))
                        self.cart.add_item(item)
                        self.Scrolledtext1.configure(state="normal")
                        bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                        self.Scrolledtext1.insert('insert', bill_text)
                        self.Scrolledtext1.configure(state="disabled")
                    else:
                        messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                    messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
            else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)

    def remove_product(self):
        if (self.cart.isEmpty() != True):
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total') == -1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=self.root)
                else:
                    self.Scrolledtext1.configure(state="normal")
                    get_all_bill = (self.Scrolledtext1.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill) - 3]
                    self.Scrolledtext1.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.Scrolledtext1.insert('insert', new_string[i])
                        self.Scrolledtext1.insert('insert', '\n')

                    self.Scrolledtext1.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=self.root)
                else:
                    self.Scrolledtext1.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i]) != 0:
                            if li[i].find('Total') == -1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li) - 1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert', '\n')
                    self.Scrolledtext1.configure(state="disabled")

        else:
            messagebox.showerror("Oops!", "Add a product.", parent=self.root)

    def wel_bill(self):
        self.name_message = Text(self.root)
        self.name_message.place(relx=0.514, rely=0.452, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(self.root)
        self.num_message.place(relx=0.894, rely=0.452, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(self.root)
        self.bill_message.place(relx=0.499, rely=0.477, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(self.root)
        self.bill_date_message.place(relx=0.852, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")

    def total_bill(self):
        if self.cart.isEmpty():
            messagebox.showerror("Oops!", "Add a product.", parent=self.root)
        else:
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total') == -1:
                self.Scrolledtext1.configure(state="normal")
                divider = "\n\n\n" + ("─" * 61)
                self.Scrolledtext1.insert('insert', divider)
                total = "\nTotal\t\t\t\t\t\t\t\t\t\t\tRs. {}".format(self.cart.total())
                self.Scrolledtext1.insert('insert', total)
                divider2 = "\n" + ("─" * 61)
                self.Scrolledtext1.insert('insert', divider2)
                self.Scrolledtext1.configure(state="disabled")
            else:
                return

    state = 1

    def gen_bill(self):

        if self.state == 1:
            strr = self.Scrolledtext1.get('1.0', END)
            self.wel_bill()
            if (self.cust_name.get() == ""):
                messagebox.showerror("Oops!", "Please enter a name.", parent=self.root)
            elif (self.cust_num.get() == ""):
                messagebox.showerror("Oops!", "Please enter a number.", parent=self.root)
            elif valid_phone(self.cust_num.get()) == False:
                messagebox.showerror("Oops!", "Please enter a valid number.", parent=self.root)
            elif (self.cart.isEmpty()):
                messagebox.showerror("Oops!", "Cart is empty.", parent=self.root)
            else:
                if strr.find('Total') == -1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    self.name_message.insert(END, self.cust_name.get())
                    self.name_message.configure(state="disabled")

                    self.num_message.insert(END, self.cust_num.get())
                    self.num_message.configure(state="disabled")

                    self.cust_new_bill.set(random_bill_number(8))

                    self.bill_message.insert(END, self.cust_new_bill.get())
                    self.bill_message.configure(state="disabled")

                    self.bill_date.set(str(date.today()))

                    self.bill_date_message.insert(END, self.bill_date.get())
                    self.bill_date_message.configure(state="disabled")

                    with sqlite3.connect("./Database/store.db") as db:
                        cur = db.cursor()
                    insert = (
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details) VALUES(?,?,?,?,?)"
                    )
                    cur.execute(insert, [self.cust_new_bill.get(), self.bill_date.get(), self.cust_name.get(), self.cust_num.get(),
                                         self.Scrolledtext1.get('1.0', END)])
                    db.commit()
                    # print(self.cart.items)
                    print(self.cart.allCart())
                    for name, qty in self.cart.dictionary.items():
                        update_qty = "UPDATE raw_inventory SET stock = stock - ? WHERE product_name = ?"
                        cur.execute(update_qty, [qty, name])
                        db.commit()
                    messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
                    self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
        else:
            return

    def clear_bill(self):
        self.wel_bill()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.Scrolledtext1.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.Scrolledtext1.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass

    def search_bill(self):
        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [self.cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            self.clear_bill()
            self.wel_bill()
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")

            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")

            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")

            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.state = 0

        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=self.root)
            self.entry3.delete(0, END)

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)



    def logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=getattr(self, 'parent', None))
        if sure:
            if hasattr(self, 'parent') and self.parent:
                self.parent.destroy()
            self.navigation_controller.show_login()


