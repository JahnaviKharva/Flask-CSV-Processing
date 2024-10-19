import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from .env
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_NAME = os.getenv('DATABASE_NAME', 'purchase_db')
DB_USER = os.getenv('DATABASE_USER', 'postgres')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'your_password_here')
DB_PORT = os.getenv('DATABASE_PORT', '5432')

# Establish a connection to PostgreSQL
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        print("Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Create the database
def create_database(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_NAME)))
            print(f"Database '{DB_NAME}' created successfully")
    except Exception as e:
        print(f"Database creation failed: {e}")

# Create tables in the database
def create_tables():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        with conn.cursor() as cur:
            # Create 'purchase' table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS purchase (
                    id SERIAL PRIMARY KEY,
                    bill_date DATE,
                    bill_no VARCHAR(100),
                    bill_total NUMERIC
                );
            """)
            print("Table 'purchase' created successfully")

            # Create 'purchase_details' table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS purchase_details (
                    id SERIAL PRIMARY KEY,
                    purchase_id INT REFERENCES purchase(id),
                    medicine_name VARCHAR(255),
                    quantity INT,
                    MRP NUMERIC,
                    item_total NUMERIC,
                    expiry_date DATE
                );
            """)
            print("Table 'purchase_details' created successfully")

            # Create 'users' table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
            """)
            print("Table 'users' created successfully")

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Table creation failed: {e}")

# Main function to execute database setup
def main():
    # Step 1: Create the connection
    conn = create_connection()

    # Step 2: Create the database
    if conn:
        create_database(conn)
        conn.close()

    # Step 3: Create tables in the new database
    create_tables()

if __name__ == "__main__":
    main()
