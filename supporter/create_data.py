import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import psycopg2 # Add PostgreSQL connection library

fake = Faker()

# Configuration
NUM_CUSTOMERS = 100
NUM_PRODUCTS = 10 
NUM_ORDERS = 100
NUM_INVOICES = 100

# Database Configuration
DB_HOST = "localhost"
DB_NAME = "heineken_sellout_db"
DB_USER = "postgres"
DB_PASS = "123"

def generate_synthetic_data_and_seed():
    timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Generate Customers
    regions = ['North', 'South', 'East', 'West', 'Central']
    channels = ['On-trade (Bar/Restaurant)', 'Off-trade (Supermarket/Retail)']
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            'customer_id': i,
            'customer_name': fake.company().replace("'", "''"),
            'region': random.choice(regions),
            'channel': random.choice(channels),
            'created_at': timestamp_now,
            'updated_at': timestamp_now,
            'is_deleted': False
        })

    # Generate Products (Heineken Portfolio)
    heineken_portfolio = [
        ("Heineken", "Heineken Original 330ml Bottle", 330),
        ("Heineken", "Heineken Silver 330ml Can", 330),
        ("Heineken", "Heineken 0.0 330ml Can", 330),
        ("Tiger", "Tiger Crystal 330ml Bottle", 330),
        ("Tiger", "Tiger Beer 330ml Can", 330),
        ("Amstel", "Amstel Light 330ml Bottle", 330),
        ("Edelweiss", "Edelweiss Wheat Beer 330ml", 330),
        ("Bia Viet", "Bia Viet 355ml Can", 355),
        ("Strongbow", "Strongbow Apple Ciders Gold 330ml", 330),
        ("Larue", "Larue Beer 330ml Can", 330)
    ]
    
    products = []
    for i, (brand, sku, vol) in enumerate(heineken_portfolio, 1):
        products.append({
            'product_id': i,
            'brand': brand,
            'sku_name': sku,
            'volume_ml': vol,
            'created_at': timestamp_now,
            'updated_at': timestamp_now,
            'is_deleted': False
        })

    # Generate Orders
    orders = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(1, NUM_ORDERS + 1):
        order_date = fake.date_between(start_date=start_date, end_date='today')
        quantity = random.randint(10, 500) 
        total_price = quantity * random.uniform(15.0, 30.0) 
        
        orders.append({
            'order_id': i,
            'customer_id': random.randint(1, NUM_CUSTOMERS),
            'product_id': random.randint(1, len(heineken_portfolio)),
            'order_date': order_date.strftime('%Y-%m-%d'),
            'quantity_cases': quantity,
            'total_price': round(total_price, 2),
            'created_at': timestamp_now,
            'updated_at': timestamp_now,
            'is_deleted': False
        })

    # Generate Invoices 
    statuses = ['Paid', 'Paid', 'Paid', 'Pending', 'Overdue'] 
    invoices = []
    for i in range(1, NUM_INVOICES + 1):
        order_date = datetime.strptime(orders[i-1]['order_date'], '%Y-%m-%d')
        invoice_date = order_date + timedelta(days=random.randint(1, 14))
        
        invoices.append({
            'invoice_id': i,
            'order_id': i,
            'invoice_date': invoice_date.strftime('%Y-%m-%d'),
            'status': random.choice(statuses),
            'created_at': timestamp_now,
            'updated_at': timestamp_now,
            'is_deleted': False
        })

    # ==========================================
    # CONNECT TO DATABASE AND INSERT DATA
    # ==========================================
    try:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        
        print("Connected! Inserting data...")
        
        # Set up schema
        cur.execute("SET search_path TO sellout;")
        
        # Insert Customers
        for c in customers:
            query = f"INSERT INTO customers (customer_id, customer_name, region, channel, created_at, updated_at, is_deleted) VALUES ({c['customer_id']}, '{c['customer_name']}', '{c['region']}', '{c['channel']}', '{c['created_at']}', '{c['updated_at']}', {c['is_deleted']});"
            cur.execute(query)
            
        # Insert Products
        for p in products:
            query = f"INSERT INTO products (product_id, brand, sku_name, volume_ml, created_at, updated_at, is_deleted) VALUES ({p['product_id']}, '{p['brand']}', '{p['sku_name']}', {p['volume_ml']}, '{p['created_at']}', '{p['updated_at']}', {p['is_deleted']});"
            cur.execute(query)
            
        # Insert Orders
        for o in orders:
            query = f"INSERT INTO orders (order_id, customer_id, product_id, order_date, quantity_cases, total_price, created_at, updated_at, is_deleted) VALUES ({o['order_id']}, {o['customer_id']}, {o['product_id']}, '{o['order_date']}', {o['quantity_cases']}, {o['total_price']}, '{o['created_at']}', '{o['updated_at']}', {o['is_deleted']});"
            cur.execute(query)
            
        # Insert Invoices
        for inv in invoices:
            query = f"INSERT INTO invoices (invoice_id, order_id, invoice_date, status, created_at, updated_at, is_deleted) VALUES ({inv['invoice_id']}, {inv['order_id']}, '{inv['invoice_date']}', '{inv['status']}', '{inv['created_at']}', '{inv['updated_at']}', {inv['is_deleted']});"
            cur.execute(query)
            
        # Save changes to DB
        conn.commit()
        print("Data successfully inserted into the database!")

    except psycopg2.Error as e:
        print(f"Error interacting with the database: {e}")
        if conn:
            conn.rollback() # Rollback if there is an error
    finally:
        # Close connection
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("Closed database connection.")

    # Still keep writing to file for backup
    with open('seed_heineken_data.sql', 'w', encoding='utf-8') as f:
        f.write("SET search_path TO sellout;\n\n")
        for c in customers:
            f.write(f"INSERT INTO customers (customer_id, customer_name, region, channel, created_at, updated_at, is_deleted) VALUES ({c['customer_id']}, '{c['customer_name']}', '{c['region']}', '{c['channel']}', '{c['created_at']}', '{c['updated_at']}', {c['is_deleted']});\n")
        for p in products:
            f.write(f"INSERT INTO products (product_id, brand, sku_name, volume_ml, created_at, updated_at, is_deleted) VALUES ({p['product_id']}, '{p['brand']}', '{p['sku_name']}', {p['volume_ml']}, '{p['created_at']}', '{p['updated_at']}', {p['is_deleted']});\n")
        for o in orders:
            f.write(f"INSERT INTO orders (order_id, customer_id, product_id, order_date, quantity_cases, total_price, created_at, updated_at, is_deleted) VALUES ({o['order_id']}, {o['customer_id']}, {o['product_id']}, '{o['order_date']}', {o['quantity_cases']}, {o['total_price']}, '{o['created_at']}', '{o['updated_at']}', {o['is_deleted']});\n")
        for inv in invoices:
            f.write(f"INSERT INTO invoices (invoice_id, order_id, invoice_date, status, created_at, updated_at, is_deleted) VALUES ({inv['invoice_id']}, {inv['order_id']}, '{inv['invoice_date']}', '{inv['status']}', '{inv['created_at']}', '{inv['updated_at']}', {inv['is_deleted']});\n")
            
    print("Created backup file 'seed_heineken_data.sql'")

if __name__ == "__main__":
    generate_synthetic_data_and_seed()