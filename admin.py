# ==================imports===================
import sqlite3
import re
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
import datetime
from tkinter import scrolledtext as tkst




# ============================================

root = Tk()
root.geometry("1366x768")
root.title("Retail Manager(ADMIN)")

user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()

with sqlite3.connect("store1.db") as db:
    cur = db.cursor()


def random_emp_id(stringLength):
    Digits = string.digits
    strr = ''.join(random.choice(Digits) for i in range(stringLength - 3))
    return ('EMP' + strr)


def valid_phone(phone):
    if re.match(r"^(?:\+92|0)\d{10}$", phone):
        return True
    return False


def valid_aadhar(aad):
    if aad.isdigit() and len(aad) == 12:
        return True
    return False


class login_page:
    def __init__(self, root=None):
        # Set up the window properties
        root.geometry("1366x768")
        root.resizable(0, 0)
        root.title("Retail Manager(ADMIN)")

        # Background Image
        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="Images/employee_login.PNG")
        self.label1.configure(image=self.img)

        # Username Icon
        self.username_icon = PhotoImage(file="./images/user.png")
        self.username_icon_label = Label(root, image=self.username_icon, bg="white")
        self.username_icon_label.place(relx=0.57, rely=0.32)

        # Username Entry
        self.user_entry = Entry(root, font="-family {Poppins} -size 12", relief="flat", fg='gray')
        self.user_entry.place(relx=0.59, rely=0.32, width=302, height=24)
        self.user_entry.insert(0, "username")

        # Placeholder handling for Username
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
        self.password_icon_label = Label(root, image=self.password_icon, bg="white")
        self.password_icon_label.place(relx=0.57, rely=0.41)

        # Password Entry
        self.password_entry = Entry(root, font="-family {Poppins} -size 12", relief="flat", fg='gray', show="")
        self.password_entry.place(relx=0.59, rely=0.41, width=302, height=24)
        self.password_entry.insert(0, "*******")

        # Placeholder handling for Password
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
        self.button1 = Button(root)
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
        self.button1.configure(command=self.login)

        # Bind "Enter" key to trigger login
        root.bind('<Return>', lambda event: self.login())
        self.button1.bind("<Return>", lambda event: self.login())


    def login(self, Event=None):
        username = self.user_entry.get()
        password = self.password_entry.get()

        with sqlite3.connect("store1.db") as db:
            cur = db.cursor()
        find_user = "SELECT * FROM employee WHERE name = ? and password = ?"
        cur.execute(find_user, [username, password])
        results = cur.fetchall()
        if results:
            if results[0][6] == "Admin":
                messagebox.showinfo("Login Page", "The login is successful.")
                page1.user_entry.delete(0, END)
                page1.password_entry.delete(0, END)
                root.withdraw()
                global adm
                global page2
                adm = Toplevel()
                page2 = Admin_Page(adm)
                # page2.time()
                adm.protocol("WM_DELETE_WINDOW", exit)
                adm.mainloop()
            else:
                messagebox.showerror("Oops!!", "You are not an admin.")

        else:
            messagebox.showerror("Error", "Incorrect username or password.")
            page1.password_entry.delete(0, END)



def exit():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=root)
    if sure == True:
        adm.destroy()
        root.destroy()


def inventory():
    adm.withdraw()
    global inv
    global page3
    inv = Toplevel()
    page3 = Inventory(inv)
    page3.time()
    inv.protocol("WM_DELETE_WINDOW", exit)
    inv.mainloop()


def employee():
    adm.withdraw()
    global emp
    global page5
    emp = Toplevel()
    page5 = Employee(emp)
    page5.time()
    emp.protocol("WM_DELETE_WINDOW", exit)
    emp.mainloop()


def invoices():
    adm.withdraw()
    global invoice
    invoice = Toplevel()
    page7 = Invoice(invoice)
    page7.time()
    invoice.protocol("WM_DELETE_WINDOW", exit)
    invoice.mainloop()

def reports():
    adm.withdraw()
    global report
    global page21
    report = Toplevel()
    page21 = Report(report)
    page21.time()
    report.protocol("WM_DELETE_WINDOW", exit)
    report.mainloop()

# ADMINPAGEWASHERE!!!!!!!!!!!!!!!!!!!
class Admin_Page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("ADMIN Mode")

        self.label1 = Label(adm)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/admin.png")
        self.label1.configure(image=self.img)

        self.message = Label(adm)
        self.message.place(relx=0.046, rely=0.056, width=62, height=30)
        self.message.configure(font="-family {Poppins} -size 12")
        self.message.configure(foreground="#ffffff")
        self.message.configure(background="#FE6B61")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.button1 = Button(adm)
        self.button1.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Logout""")
        self.button1.configure(command=self.Logout)

        self.button2 = Button(adm)
        self.button2.place(relx=0.14, rely=0.508, width=146, height=63)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#ffffff")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#333333")
        self.button2.configure(background="#ffffff")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Inventory""")
        self.button2.configure(command=inventory)

        self.button3 = Button(adm)
        self.button3.place(relx=0.338, rely=0.508, width=146, height=63)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#ffffff")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#333333")
        self.button3.configure(background="#ffffff")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""Employees""")
        self.button3.configure(command=employee)

        self.button4 = Button(adm)
        self.button4.place(relx=0.536, rely=0.508, width=146, height=63)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#ffffff")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#333333")
        self.button4.configure(background="#ffffff")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""Invoices""")
        self.button4.configure(command=invoices)

        self.button5 = Button(adm)
        self.button5.place(relx=0.732, rely=0.508, width=146, height=63)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#ffffff")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#333333")
        self.button5.configure(background="#ffffff")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""Reports""")
        self.button5.configure(command=reports)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=adm)
        if sure == True:
            adm.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

# ADMINPAGEWASHERE!!!!!!!!!!!!!!!!!!!!!!!!!!
class Inventory:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Inventory")

        self.label1 = Label(inv)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/inventory.png")
        self.label1.configure(image=self.img)

        self.message = Label(inv)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(inv)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(inv)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        # Assuming you have a Tkinter Entry widget named self.entry1
        self.entry1.bind("<Return>", lambda event: self.search_product())

        self.button1 = Button(inv)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_product)

        self.button2 = Button(inv)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(inv)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD PRODUCT""")
        self.button3.configure(command=self.add_product)

        self.button4 = Button(inv)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""UPDATE PRODUCT""")
        self.button4.configure(command=self.update_product)

        self.button5 = Button(inv)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""DELETE PRODUCT""")
        self.button5.configure(command=self.delete_product)

        self.button6 = Button(inv)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(inv, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(inv, orient=VERTICAL)
        self.tree = ttk.Treeview(inv)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Product ID",
                "Name",
                "Category",
                "Sub-Category",
                "In Stock",
                "MRP",
                "Cost Price",
                "Vendor No.",
                "Barcode",
            )
        )

        self.tree.heading("Product ID", text="Product ID", anchor=W)
        self.tree.heading("Name", text="Name", anchor=W)
        self.tree.heading("Category", text="Category", anchor=W)
        self.tree.heading("Sub-Category", text="Sub-Category", anchor=W)
        self.tree.heading("In Stock", text="In Stock", anchor=W)
        self.tree.heading("MRP", text="MRP", anchor=W)
        self.tree.heading("Cost Price", text="Cost Price", anchor=W)
        self.tree.heading("Vendor No.", text="Vendor No.", anchor=W)
        self.tree.heading("Barcode", text="Barcode", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=120)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        self.tree.column("#7", stretch=NO, minwidth=0, width=80)
        self.tree.column("#8", stretch=NO, minwidth=0, width=100)
        self.tree.column("#9", stretch=NO, minwidth=0, width=100)


        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM inventory")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))

    def search_product(self):
        # Get the input entered by the user
        search_query = self.entry1.get().strip()

        # If the search field is empty, show all items
        if not search_query:
            # Clear the selection and reattach all items
            for item in self.tree.get_children():
                self.tree.reattach(item, '', 'end')  # Reattach all items to the tree
            self.tree.selection_set('')  # Clear selection
            messagebox.showinfo("Info", "Showing all products.", parent=inv)  # Optional info message
            return

        found_items = []  # List to store found items

        # Collecting all product data from the tree
        for item in self.tree.get_children():
            item_values = self.tree.item(item)["values"]  # Get the item values
            # Check if the search_query matches product name, product ID, or barcode
            if (search_query.lower() in str(item_values[1]).lower() or  # Assuming name is at index 1
                    search_query.lower() in str(item_values[2]).lower() or  # Assuming ID is at index 2
                    search_query.lower() in str(item_values[8]).lower()):  # Assuming barcode is at index 8
                found_items.append(item)  # Store the found item's identifier

        # Hide all items if matching items are found
        if found_items:
            # Hide all items
            for item in self.tree.get_children():
                self.tree.detach(item)

            # Show only the found items
            for found_item in found_items:
                self.tree.reattach(found_item, '', 'end')

            # Optionally, select the first found item
            self.tree.selection_set(found_items[0])  # Select the first found row
            self.tree.focus(found_items[0])  # Focus on the first found row

            messagebox.showinfo("Success!!", f"{len(found_items)} item(s) found.", parent=inv)
        else:
            # If no items found, show all items again
            for item in self.tree.get_children():
                self.tree.reattach(item, '', 'end')  # Reattach all items to the tree
            messagebox.showinfo("Info", f"No products found for: {search_query}. Showing all products.", parent=inv)

    # =====================================

    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_product(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected products?", parent=inv)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 8 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM inventory WHERE product_id = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Products deleted from database.", parent=inv)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select a product.", parent=inv)

    def update_product(self):
        if len(self.sel) == 1:
            global p_update
            p_update = Toplevel()
            page9 = Update_Product(p_update)
            page9.time()
            p_update.protocol("WM_DELETE_WINDOW", self.ex2)
            global valll
            valll = []
            for i in self.sel:
                for j in self.tree.item(i)["values"]:
                    valll.append(j)

            page9.entry1.insert(0, valll[1])
            page9.entry2.insert(0, valll[2])
            page9.entry3.insert(0, valll[4])
            page9.entry4.insert(0, valll[5])
            page9.entry6.insert(0, valll[3])
            page9.entry7.insert(0, valll[6])
            page9.entry8.insert(0, valll[7])
            page9.entry9.insert(0, valll[8])


        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please choose a product to update.", parent=inv)
        else:
            messagebox.showerror("Error", "Can only update one product at a time.", parent=inv)

        p_update.mainloop()

    def add_product(self):
        global p_add
        global page4
        p_add = Toplevel()
        page4 = add_product(p_add)
        page4.time()
        p_add.mainloop()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=inv)
        if sure == True:
            inv.destroy()
            adm.deiconify()

    def ex2(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=p_update)
        if sure == True:
            p_update.destroy()
            inv.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Product")

        self.label1 = Label(p_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_product.png")
        self.label1.configure(image=self.img)

        self.clock = Label(p_add)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(p_add)
        self.entry1.place(relx=0.132, rely=0.296, width=940, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(p_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = p_add.register(self.testint)

        self.entry3 = Entry(p_add)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(p_add)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")

        self.entry6 = Entry(p_add)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")

        self.entry7 = Entry(p_add)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")

        self.entry8 = Entry(p_add)
        self.entry8.place(relx=0.527, rely=0.646, width=374, height=30)
        self.entry8.configure(font="-family {Poppins} -size 12")
        self.entry8.configure(relief="flat")
        self.entry8.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry9 = Entry(p_add)
        self.entry9.place(relx=0.527, rely=0.296, width=374, height=30)  # Adjusted for Barcode field
        self.entry9.configure(font="-family {Poppins} -size 12")
        self.entry9.configure(relief="flat")

        self.button1 = Button(p_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(p_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def add(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()
        pmrp = self.entry4.get()
        pname = self.entry1.get()
        psubcat = self.entry6.get()
        pcp = self.entry7.get()
        pvendor = self.entry8.get()
        barcode = self.entry9.get()

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_add)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_add)
                                    else:
                                        if valid_phone(pvendor):
                                            if barcode.strip():  # Only checking if barcode is entered
                                                with sqlite3.connect("store1.db") as db:
                                                    cur = db.cursor()
                                                insert = (
                                                    "INSERT INTO inventory(product_name, product_cat, product_subcat, stock, mrp, cost_price, vendor_phn, barcode) VALUES(?,?,?,?,?,?,?,?)"
                                                )
                                                cur.execute(insert,
                                                            [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp),
                                                             pvendor, barcode])
                                                db.commit()
                                                messagebox.showinfo("Success!!",
                                                                    "Product successfully added in inventory.",
                                                                    parent=p_add)
                                                p_add.destroy()
                                                page3.tree.delete(*page3.tree.get_children())
                                                page3.DisplayData()
                                                p_add.destroy()
                                            else:
                                                messagebox.showerror("Oops!", "Please enter or scan the barcode.",
                                                                     parent=p_add)
                                        else:
                                            messagebox.showerror("Oops!", "Invalid phone number.", parent=p_add)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_add)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_add)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_add)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_add)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Update_Product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Product")

        self.label1 = Label(p_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_product.png")
        self.label1.configure(image=self.img)

        self.clock = Label(p_update)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(p_update)
        self.entry1.place(relx=0.132, rely=0.296, width=980, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(p_update)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = p_update.register(self.testint)

        self.entry3 = Entry(p_update)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(p_update)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")

        self.entry6 = Entry(p_update)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")

        self.entry7 = Entry(p_update)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")

        self.entry8 = Entry(p_update)
        self.entry8.place(relx=0.527, rely=0.646, width=374, height=30)
        self.entry8.configure(font="-family {Poppins} -size 12")
        self.entry8.configure(relief="flat")

        self.entry9 = Entry(p_update)
        self.entry9.place(relx=0.527, rely=0.296, width=374, height=30)  # Adjusted for Barcode field
        self.entry9.configure(font="-family {Poppins} -size 12")
        self.entry9.configure(relief="flat")

        self.button1 = Button(p_update)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""UPDATE""")
        self.button1.configure(command=self.update)

        self.button2 = Button(p_update)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def update(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()
        pmrp = self.entry4.get()
        pname = self.entry1.get()
        psubcat = self.entry6.get()
        pcp = self.entry7.get()
        pvendor = self.entry8.get()
        barcode = self.entry9.get()

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_update)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_update)
                                    else:
                                        if valid_phone(pvendor):
                                            product_id = valll[0]
                                            with sqlite3.connect("store1.db") as db:
                                                cur = db.cursor()
                                            update = (
                                                "UPDATE inventory SET product_name = ?, product_cat = ?, product_subcat = ?, stock = ?, mrp = ?, cost_price = ?, vendor_phn = ?, barcode = ? WHERE product_id = ?"
                                            )
                                            cur.execute(update,
                                                        [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp),
                                                         pvendor, product_id, barcode])
                                            db.commit()
                                            messagebox.showinfo("Success!!",
                                                                "Product successfully updated in inventory.",
                                                                parent=p_update)
                                            valll.clear()
                                            Inventory.sel.clear()
                                            page3.tree.delete(*page3.tree.get_children())
                                            page3.DisplayData()
                                            p_update.destroy()
                                        else:
                                            messagebox.showerror("Oops!", "Invalid phone number.", parent=p_update)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_update)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_update)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_update)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_update)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_update)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_update)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)
        self.entry9.delete(0, END)


    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Employee Management")

        self.label1 = Label(emp)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/employee.png")
        self.label1.configure(image=self.img)

        self.message = Label(emp)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(emp)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(emp)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(emp)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_emp)
        self.entry1.bind("<Return>", lambda event: self.search_emp())

        self.button2 = Button(emp)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(emp)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD EMPLOYEE""")
        self.button3.configure(command=self.add_emp)

        self.button4 = Button(emp)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""UPDATE EMPLOYEE""")
        self.button4.configure(command=self.update_emp)

        self.button5 = Button(emp)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#CF1E14")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="#ffffff")
        self.button5.configure(background="#CF1E14")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""DELETE EMPLOYEE""")
        self.button5.configure(command=self.delete_emp)

        self.button6 = Button(emp)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#CF1E14")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="#ffffff")
        self.button6.configure(background="#CF1E14")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(emp, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(emp, orient=VERTICAL)
        self.tree = ttk.Treeview(emp)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Employee ID",
                "Employee Name",
                "Contact No.",
                "Address",
                "Cnic No.",
                "Password",
                "Designation"
            )
        )

        self.tree.heading("Employee ID", text="Employee ID", anchor=W)
        self.tree.heading("Employee Name", text="Employee Name", anchor=W)
        self.tree.heading("Contact No.", text="Contact No.", anchor=W)
        self.tree.heading("Address", text="Address", anchor=W)
        self.tree.heading("Cnic No.", text="Cnic No.", anchor=W)
        self.tree.heading("Password", text="Password", anchor=W)
        self.tree.heading("Designation", text="Designation", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=198)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        self.tree.column("#7", stretch=NO, minwidth=0, width=80)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM employee")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))

    def search_emp(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        to_search = self.entry1.get()
        for search in val:
            if search == to_search:
                self.tree.selection_set(val[val.index(search) - 1])
                self.tree.focus(val[val.index(search) - 1])
                messagebox.showinfo("Success!!", "Employee ID: {} found.".format(self.entry1.get()), parent=emp)
                break
        else:
            messagebox.showerror("Oops!!", "Employee ID: {} not found.".format(self.entry1.get()), parent=emp)

    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_emp(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected employee(s)?", parent=emp)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 7 == 0:
                        to_delete.append(val[j])

                flag = 1

                for k in to_delete:
                    if k == "EMP0000":
                        flag = 0
                        break
                    else:
                        delete = "DELETE FROM employee WHERE emp_id = ?"
                        cur.execute(delete, [k])
                        db.commit()

                if flag == 1:
                    messagebox.showinfo("Success!!", "Employee(s) deleted from database.", parent=emp)
                    self.sel.clear()
                    self.tree.delete(*self.tree.get_children())
                    self.DisplayData()
                else:
                    messagebox.showerror("Error!!", "Cannot delete master admin.")
        else:
            messagebox.showerror("Error!!", "Please select an employee.", parent=emp)

    def update_emp(self):

        if len(self.sel) == 1:
            global e_update
            e_update = Toplevel()
            page8 = Update_Employee(e_update)
            page8.time()
            e_update.protocol("WM_DELETE_WINDOW", self.ex2)
            global vall
            vall = []
            for i in self.sel:
                for j in self.tree.item(i)["values"]:
                    vall.append(j)

            page8.entry1.insert(0, vall[1])
            page8.entry2.insert(0, vall[2])
            page8.entry3.insert(0, vall[4])
            page8.entry4.insert(0, vall[6])
            page8.entry5.insert(0, vall[3])
            page8.entry6.insert(0, vall[5])
            e_update.mainloop()
        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please select an employee to update.")
        else:
            messagebox.showerror("Error", "Can only update one employee at a time.")

    def add_emp(self):
        global e_add
        e_add = Toplevel()
        page6 = add_employee(e_add)
        page6.time()
        e_add.protocol("WM_DELETE_WINDOW", self.ex)
        e_add.mainloop()

    def ex(self):
        e_add.destroy()
        self.tree.delete(*self.tree.get_children())
        self.DisplayData()

    def ex2(self):
        e_update.destroy()
        self.tree.delete(*self.tree.get_children())
        self.DisplayData()

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=emp)
        if sure == True:
            emp.destroy()
            adm.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            emp.destroy()
            root.deiconify()

            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)


class add_employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Employee")

        self.label1 = Label(e_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_employee.png")
        self.label1.configure(image=self.img)

        self.clock = Label(e_add)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = e_add.register(self.testint)
        self.r2 = e_add.register(self.testchar)

        self.entry1 = Entry(e_add)
        self.entry1.place(relx=0.132, rely=0.296, width=374, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(e_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry3 = Entry(e_add)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry4 = Entry(e_add)
        self.entry4.place(relx=0.527, rely=0.296, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry5 = Entry(e_add)
        self.entry5.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry5.configure(font="-family {Poppins} -size 12")
        self.entry5.configure(relief="flat")

        self.entry6 = Entry(e_add)
        self.entry6.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
        self.entry6.configure(show="*")

        self.button1 = Button(e_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(e_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def testchar(self, val):
        if val.isalpha():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def add(self):
        ename = self.entry1.get()
        econtact = self.entry2.get()
        eaddhar = self.entry3.get()
        edes = self.entry4.get()
        eadd = self.entry5.get()
        epass = self.entry6.get()

        if ename.strip():
            if valid_phone(econtact):
                if valid_aadhar(eaddhar):
                    if edes:
                        if eadd:
                            if epass:
                                emp_id = random_emp_id(7)
                                insert = (
                                    "INSERT INTO employee(emp_id, name, contact_num, address, cnic_num, password, designation) VALUES(?,?,?,?,?,?,?)"
                                )
                                cur.execute(insert, [emp_id, ename, econtact, eadd, eaddhar, epass, edes])
                                db.commit()
                                messagebox.showinfo("Success!!",
                                                    "Employee ID: {} successfully added in database.".format(emp_id),
                                                    parent=e_add)
                                self.clearr()
                            else:
                                messagebox.showerror("Oops!", "Please enter a password.", parent=e_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter address.", parent=e_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter designation.", parent=e_add)
                else:
                    messagebox.showerror("Oops!", "Invalid Cnic number.", parent=e_add)
            else:
                messagebox.showerror("Oops!", "Invalid phone number.", parent=e_add)
        else:
            messagebox.showerror("Oops!", "Please enter employee name.", parent=e_add)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        self.entry6.delete(0, END)


class Update_Employee:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Update Employee")

        self.label1 = Label(e_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_employee.png")
        self.label1.configure(image=self.img)

        self.clock = Label(e_update)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.r1 = e_update.register(self.testint)
        self.r2 = e_update.register(self.testchar)

        self.entry1 = Entry(e_update)
        self.entry1.place(relx=0.132, rely=0.296, width=374, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(e_update)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry3 = Entry(e_update)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r1, "%P"))

        self.entry4 = Entry(e_update)
        self.entry4.place(relx=0.527, rely=0.296, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")
        self.entry4.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry5 = Entry(e_update)
        self.entry5.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry5.configure(font="-family {Poppins} -size 12")
        self.entry5.configure(relief="flat")

        self.entry6 = Entry(e_update)
        self.entry6.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")
        self.entry6.configure(show="*")

        self.button1 = Button(e_update)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""UPDATE""")
        self.button1.configure(command=self.update)

        self.button2 = Button(e_update)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def update(self):
        ename = self.entry1.get()
        econtact = self.entry2.get()
        eaddhar = self.entry3.get()
        edes = self.entry4.get()
        eadd = self.entry5.get()
        epass = self.entry6.get()

        if ename.strip():
            if valid_phone(econtact):
                if valid_aadhar(eaddhar):
                    if edes:
                        if eadd:
                            if epass:
                                emp_id = vall[0]
                                update = (
                                    "UPDATE employee SET name = ?, contact_num = ?, address = ?, cnic_num = ?, password = ?, designation = ? WHERE emp_id = ?"
                                )
                                cur.execute(update, [ename, econtact, eadd, eaddhar, epass, edes, emp_id])
                                db.commit()
                                messagebox.showinfo("Success!!",
                                                    "Employee ID: {} successfully updated in database.".format(emp_id),
                                                    parent=e_update)
                                vall.clear()
                                page5.tree.delete(*page5.tree.get_children())
                                page5.DisplayData()
                                Employee.sel.clear()
                                e_update.destroy()
                            else:
                                messagebox.showerror("Oops!", "Please enter a password.", parent=e_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter address.", parent=e_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter designation.", parent=e_add)
                else:
                    messagebox.showerror("Oops!", "Invalid Cnic number.", parent=e_add)
            else:
                messagebox.showerror("Oops!", "Invalid phone number.", parent=e_add)
        else:
            messagebox.showerror("Oops!", "Please enter employee name.", parent=e_add)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)
        self.entry6.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def testchar(self, val):
        if val.isalpha():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Report:
    def __init__(self, top=None):
        # Window setup
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Monthly Sales Report")

        # Partition the window into left (navigation) and right (report display)
        self.left_frame = Frame(top, width=300, bg="#fe5b60")
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = Frame(top)
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Add Widgets to the Left Frame (Navigation)
        self.message = Label(self.left_frame, text="ADMIN", font=("Poppins", 10), bg="#fe5b60", anchor="w")
        self.message.place(relx=0.05, rely=0.05, width=100, height=30)

        # Month and Year Dropdowns
        self.month_label = Label(self.left_frame, text="Select Month:", bg="#fe5b60", font=("Poppins", 12))
        self.month_label.place(relx=0.05, rely=0.15, width=200, height=30)

        months = [datetime.date(1900, i, 1).strftime('%B') for i in range(1, 13)]
        self.month_combobox = ttk.Combobox(self.left_frame, values=months, state="readonly")
        self.month_combobox.place(relx=0.05, rely=0.20, width=200, height=30)

        self.year_label = Label(self.left_frame, text="Select Year:", bg="#fe5b60", font=("Poppins", 12))
        self.year_label.place(relx=0.05, rely=0.30, width=200, height=30)

        years = [str(year) for year in range(2021, datetime.datetime.now().year + 1)]
        self.year_combobox = ttk.Combobox(self.left_frame, values=years, state="readonly")
        self.year_combobox.place(relx=0.05, rely=0.35, width=200, height=30)

        # Generate Report Button
        self.generate_button = Button(self.left_frame, text="Generate Report", font=("Poppins", 12), bg="#CF1E14", fg="white", command=self.generate_report)
        self.generate_button.place(relx=0.05, rely=0.50, width=200, height=40)

        self.exit_button = Button(self.left_frame, text="Exit", font=("Poppins", 12), bg="#CF1E14", fg="white", command=self.exit)
        self.exit_button.place(relx=0.05, rely=0.65, width=100, height=30)

        # Right Frame: Add Treeview widget for table display
        self.tree_frame = Frame(self.right_frame)
        self.tree_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # Create a Treeview for the table
        self.tree = ttk.Treeview(self.tree_frame, columns=('Bill No', 'Date', 'Customer Name', 'Customer No'), show='headings')

        # Define headings and columns
        self.tree.heading('Bill No', text='Bill No')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Customer Name', text='Customer Name')
        self.tree.heading('Customer No', text='Customer No')

        self.tree.column('Bill No', width=100, anchor=W)
        self.tree.column('Date', width=150, anchor=W)
        self.tree.column('Customer Name', width=200, anchor=W)
        self.tree.column('Customer No', width=150, anchor=W)

        # Create a vertical scrollbar for the Treeview
        self.scrollbar = Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Pack the Treeview
        self.tree.pack(fill=BOTH, expand=True)

    # Function to generate the report
    def generate_report(self):
        selected_month = self.month_combobox.get()
        selected_year = self.year_combobox.get()

        if not selected_month or not selected_year:
            messagebox.showwarning("Input Error", "Please select both month and year.")
            return

        # Convert selected month to number
        month_number = list(datetime.date(1900, i, 1).strftime('%B') for i in range(1, 13)).index(selected_month) + 1

        # Connect to SQLite database
        conn = sqlite3.connect('store1.db')
        cursor = conn.cursor()

        # Query to fetch bills within the selected year and month
        query = '''
        SELECT bill_no, date, customer_name, customer_no
        FROM bill
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        '''
        cursor.execute(query, (selected_year, f"{month_number:02d}"))
        bills = cursor.fetchall()

        conn.close()

        # Clear previous data from the table
        for i in self.tree.get_children():
            self.tree.delete(i)

        if bills:
            # Add data rows
            for index, bill in enumerate(bills):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', values=bill, tags=(tag,))

            # Add striped rows
            self.tree.tag_configure('evenrow', background='#ffc271')
            self.tree.tag_configure('oddrow', background='white')
        else:
            messagebox.showinfo("No Data", "No bills found for the selected month and year.")

    # Placeholder function for exit
    def exit(self):
        root.quit()



class Invoice:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Invoices")

        self.label1 = Label(invoice)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/invoices.png")
        self.label1.configure(image=self.img)

        self.message = Label(invoice)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="#000000")
        self.message.configure(background="#ffffff")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(invoice)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="#000000")
        self.clock.configure(background="#ffffff")

        self.entry1 = Entry(invoice)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(invoice)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#CF1E14")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_inv)

        self.button2 = Button(invoice)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#CF1E14")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#CF1E14")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(invoice)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#CF1E14")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="#ffffff")
        self.button3.configure(background="#CF1E14")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""DELETE INVOICE""")
        self.button3.configure(command=self.delete_invoice)

        self.button4 = Button(invoice)
        self.button4.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#CF1E14")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="#ffffff")
        self.button4.configure(background="#CF1E14")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""EXIT""")
        self.button4.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(invoice, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(invoice, orient=VERTICAL)
        self.tree = ttk.Treeview(invoice)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.double_tap)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Bill Number",
                "Date",
                "Customer Name",
                "Customer Phone No.",
                "Time",
            )
        )

        self.tree.heading("Bill Number", text="Bill Number", anchor=W)
        self.tree.heading("Date", text="Date", anchor=W)
        self.tree.heading("Customer Name", text="Customer Name", anchor=W)
        self.tree.heading("Customer Phone No.", text="Customer Phone No.", anchor=W)
        self.tree.heading("Time", text="Time", anchor=W)


        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=219)
        self.tree.column("#2", stretch=NO, minwidth=0, width=219)
        self.tree.column("#3", stretch=NO, minwidth=0, width=219)
        self.tree.column("#4", stretch=NO, minwidth=0, width=219)
        self.tree.column("#5", stretch=NO, minwidth=0, width=219)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM bill")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))

    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def double_tap(self, Event):
        item = self.tree.identify('item', Event.x, Event.y)
        global bill_num
        bill_num = self.tree.item(item)['values'][0]

        global bill
        bill = Toplevel()
        pg = open_bill(bill)
        # bill.protocol("WM_DELETE_WINDOW", exitt)
        bill.mainloop()

    def delete_invoice(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected invoice(s)?",
                                       parent=invoice)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 5 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM bill WHERE bill_no = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Invoice(s) deleted from database.", parent=invoice)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select an invoice", parent=invoice)

    def search_inv(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        to_search = self.entry1.get()
        for search in val:
            if search == to_search:
                self.tree.selection_set(val[val.index(search) - 1])
                self.tree.focus(val[val.index(search) - 1])
                messagebox.showinfo("Success!!", "Bill Number: {} found.".format(self.entry1.get()), parent=invoice)
                break
        else:
            messagebox.showerror("Oops!!", "Bill NUmber: {} not found.".format(self.entry1.get()), parent=invoice)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            invoice.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=invoice)
        if sure == True:
            invoice.destroy()
            adm.deiconify()


class open_bill:
    def __init__(self, top=None):
        top.geometry("765x488")
        top.resizable(0, 0)
        top.title("Bill")

        self.label1 = Label(bill)
        self.label1.place(relx=0, rely=0, width=765, height=488)
        self.img = PhotoImage(file="./images/bill.png")
        self.label1.configure(image=self.img)

        self.name_message = Text(bill)
        self.name_message.place(relx=0.178, rely=0.205, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(bill)
        self.num_message.place(relx=0.854, rely=0.205, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(bill)
        self.bill_message.place(relx=0.150, rely=0.243, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(bill)
        self.bill_date_message.place(relx=0.780, rely=0.243, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.044, rely=0.41, width=695, height=284)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [bill_num])
        results = cur.fetchall()
        if results:
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


page1 = login_page(root)
root.bind("<Return>", login_page.login)
root.mainloop()
