import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from the environment variables
DB_HOST = os.getenv('DATABASE_HOST')
DB_PORT = os.getenv('DATABASE_PORT')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
DB_NAME = os.getenv('DATABASE_NAME')

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

    # Create a cursor to execute SQL commands
    cur = conn.cursor()

    # SQL command to create the 'users' table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """

    # SQL commands to create the tables
    create_purchase_table = """
    CREATE TABLE IF NOT EXISTS purchase (
        id SERIAL PRIMARY KEY,
        bill_date DATE,
        bill_no VARCHAR(100),
        bill_total NUMERIC
    );
    """

    create_purchase_details_table = """
    CREATE TABLE IF NOT EXISTS purchase_details (
        id SERIAL PRIMARY KEY,
        purchase_id INT REFERENCES purchase(id),
        medicine_name VARCHAR(255),
        quantity INT,
        MRP NUMERIC,
        item_total NUMERIC,
        expiry_date DATE
    );
    """

    # Execute the SQL commands
    cur.execute(create_users_table)
    cur.execute(create_purchase_table)
    cur.execute(create_purchase_details_table)

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

    print("Tables created successfully.")

except Exception as e:
    print(f"Error: {e}")
