from models.database import get_db_connection

# Function to validate purchase data from CSV
def validate_purchase_data(row):
    required_columns = ['bill_date', 'bill_no', 'bill_total', 'medicine_name', 'quantity', 'mrp', 'item_total', 'expiry_date']
    for col in required_columns:
        if col not in row or not row[col].strip():
            return False, f"Missing or empty field: {col}"
    return True, ""

# Function to insert purchase data into the database
def insert_purchase_data(row):
    try:
        # Get database connection
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert into purchase table
        cur.execute(
            'INSERT INTO purchase (bill_date, bill_no, bill_total) VALUES (%s, %s, %s) RETURNING id',
            (row['bill_date'].strip(), row['bill_no'].strip(), row['bill_total'].strip())
        )
        purchase_id = cur.fetchone()[0]

        # Insert into purchase_details table
        cur.execute(
            'INSERT INTO purchase_details (purchase_id, medicine_name, quantity, mrp, item_total, expiry_date) VALUES (%s, %s, %s, %s, %s, %s)',
            (purchase_id, row['medicine_name'].strip(), row['quantity'].strip(), row['mrp'].strip(), row['item_total'].strip(), row['expiry_date'].strip())
        )

        # Commit the transaction
        conn.commit()
        cur.close()
        conn.close()

        return True, "Purchase data inserted successfully"

    except Exception as e:
        return False, str(e)

# Function to update MRP in the purchase_details table
def update_mrp(id, new_mrp):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Update the MRP
        cur.execute('UPDATE purchase_details SET mrp = %s WHERE id = %s', (new_mrp, id))
        conn.commit()

        cur.close()
        conn.close()

        return True, "MRP updated successfully"

    except Exception as e:
        return False, str(e)

# Function to delete purchase detail by ID
def delete_purchase_detail(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Delete from purchase_details
        cur.execute('DELETE FROM purchase_details WHERE id = %s', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return True, "Purchase detail deleted successfully"

    except Exception as e:
        return False, str(e)

# Function to fetch purchase data by bill_no
def get_purchase_data_by_bill_no(bill_no):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch data using a JOIN
        cur.execute("""
            SELECT p.bill_date, p.bill_no, p.bill_total, pd.medicine_name, pd.quantity, pd.mrp, pd.item_total, pd.expiry_date
            FROM purchase p
            JOIN purchase_details pd ON p.id = pd.purchase_id
            WHERE p.bill_no = %s;
        """, (bill_no,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows

    except Exception as e:
        return None, str(e)

# Function to fetch data for CSV export
def fetch_all_purchase_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch data from both tables
        cur.execute("""
            SELECT p.bill_date, p.bill_no, p.bill_total, pd.medicine_name, pd.quantity, pd.mrp, pd.item_total, pd.expiry_date
            FROM purchase p
            JOIN purchase_details pd ON p.id = pd.purchase_id;
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows

    except Exception as e:
        return None, str(e)
