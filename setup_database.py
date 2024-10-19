import psycopg2
import os

# Get database connection parameters from environment variables
DB_HOST = os.getenv('DATABASE_HOST')
DB_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
DB_PORT = os.getenv('DATABASE_PORT')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    cur = conn.cursor()

    # Create tables
    cur.execute('''
    CREATE TABLE IF NOT EXISTS purchase (
        id SERIAL PRIMARY KEY,
        bill_date DATE,
        bill_no VARCHAR(100),
        bill_total NUMERIC
    );
    
    CREATE TABLE IF NOT EXISTS purchase_details (
        id SERIAL PRIMARY KEY,
        purchase_id INT REFERENCES purchase(id),
        medicine_name VARCHAR(255),
        quantity INT,
        MRP NUMERIC,
        item_total NUMERIC,
        expiry_date DATE
    );
    ''')

    conn.commit()
    cur.close()
    conn.close()

    print("Tables created successfully!")

except Exception as e:
    print(f"Error: {e}")
