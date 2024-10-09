# import libraries
import sqlite3

# creating connection
conn = sqlite3.connect('pos_database.db')
c = conn.cursor()

# creating Tables below

# creating product table
c.execute('''
CREATE TABLE IF NOT EXISTS products(
    barcode TEXT PRIMARY KEY,
    name TEXT, 
    price REAL, 
    stock INTEGER)    
''')

# create Sales Table
c.execute('''
CREATE TABLE IF NOT EXISTS sales(
    sales_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    barcode TEXT,
    quantity INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)    
''')

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, 
    password TEXT, 
    role TEXT)
''')

c.execute('''
CREATE TABLE bill (
    bill_no TEXT PRIMARY KEY,
    date TEXT,
    customer_name TEXT,
    customer_no TEXT,
    bill_details TEXT
)
''')

c.execute('''
CREATE TABLE employee (
    emp_id TEXT PRIMARY KEY,
    name TEXT,
    contact_num TEXT,
    address TEXT,
    aadhar_num TEXT,
    password TEXT,
    designation TEXT
)
''')

c.execute('''
CREATE TABLE inventory (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    product_cat TEXT,
    product_subcat TEXT,
    stock INTEGER,
    cp REAL,
    sp REAL,
    totalcp REAL,
    totalsp REAL,
    assumed_profit INTEGER,
    vendor TEXT,
    vendor_phoneno INTEGER
)
''')

c.execute('''
CREATE TALE IF NOT EXISTS employee WHERE ''')

conn.commit()
conn.close()

print("DataBase and table created Successfully.")