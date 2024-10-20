from flask import Blueprint, request, jsonify, Response
from services.purchase_service import (
    validate_purchase_data,
    insert_purchase_data,
    update_mrp,
    delete_purchase_detail,
    get_purchase_data_by_bill_no,
    fetch_all_purchase_data
)
import csv
from io import StringIO
from models.database import get_db_connection
from utils.validators import validate_required_fields, validate_date_format, validate_positive_integer, validate_mrp
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.utils import secure_filename
from datetime import datetime



purchase_bp = Blueprint('purchase_bp', __name__)

@purchase_bp.route('/upload_csv', methods=['POST'])
@jwt_required()
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    try:
        filename = secure_filename(file.filename)
        file.save(filename)

        # Process CSV file
        with open(filename, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Validate required columns
            required_columns = {'bill_date', 'bill_no', 'medicine_name', 'quantity', 'mrp', 'expiry_date'}
            csv_columns = set(reader.fieldnames)

            if not required_columns.issubset(csv_columns):
                missing_cols = required_columns - csv_columns
                return jsonify({"error": f"Missing columns: {', '.join(missing_cols)}"}), 400

            conn = get_db_connection()
            cur = conn.cursor()

            bill_total = 0  # Initialize bill total

            for row in reader:
                # Convert bill_date from DD-MM-YYYY to a date object
                bill_date = datetime.strptime(row['bill_date'], "%d-%m-%Y").date()

                # Calculate item_total
                item_total = float(row['mrp']) * int(row['quantity'])
                bill_total += item_total

                # Insert into 'purchase' table
                cur.execute(
                    "INSERT INTO purchase (bill_date, bill_no, bill_total) VALUES (%s, %s, %s) ON CONFLICT (bill_no) DO UPDATE SET bill_total = %s RETURNING id",
                    (bill_date, row['bill_no'], bill_total, bill_total)
                )
                purchase_id = cur.fetchone()[0]

                # Insert into 'purchase_details' table
                cur.execute(
                    "INSERT INTO purchase_details (purchase_id, medicine_name, quantity, MRP, item_total, expiry_date) VALUES (%s, %s, %s, %s, %s, %s)",
                    (purchase_id, row['medicine_name'], row['quantity'], row['mrp'], item_total, row['expiry_date'])
                )

            conn.commit()
            cur.close()
            conn.close()

        os.remove(filename)  # Clean up the uploaded file
        return jsonify({"message": "CSV data uploaded and processed successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update MRP Route
@purchase_bp.route('/update_purchase_detail_data/<int:id>', methods=['PUT'])
def update_purchase_detail_data(id):
    data = request.get_json()
    new_mrp = data.get('mrp')

    if not new_mrp:
        return jsonify({"error": "MRP is required"}), 400

    success, msg = update_mrp(id, new_mrp)
    if not success:
        return jsonify({"error": msg}), 500

    return jsonify({"message": msg}), 200

@purchase_bp.route('/get_purchase_data/<bill_no>', methods=['GET'])
def get_purchase_data(bill_no):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch purchase data by joining tables
        cur.execute("""
            SELECT p.bill_date, p.bill_no, p.bill_total, pd.medicine_name, pd.quantity, pd.mrp, pd.item_total, pd.expiry_date
            FROM purchase p
            JOIN purchase_details pd ON p.id = pd.purchase_id
            WHERE p.bill_no = %s;
        """, (bill_no,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return jsonify({"error": "No purchase found for the given bill number"}), 404

        purchase_data = [
            {
                "bill_date": row[0],
                "bill_no": row[1],
                "bill_total": row[2],
                "medicine_name": row[3],
                "quantity": row[4],
                "mrp": row[5],
                "item_total": row[6],
                "expiry_date": row[7]
            }
            for row in rows
        ]

        return jsonify(purchase_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@purchase_bp.route('/delete_purchase_detail_data/<int:id>', methods=['DELETE'])
def delete_purchase_detail_data(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Delete the record from purchase_details table
        cur.execute('DELETE FROM purchase_details WHERE id = %s', (id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Purchase detail deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@purchase_bp.route('/create_purchase_csv', methods=['GET'])
def create_purchase_csv():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch data for CSV creation
        cur.execute("""
            SELECT p.bill_date, p.bill_no, p.bill_total, pd.medicine_name, pd.quantity, pd.mrp, pd.item_total, pd.expiry_date
            FROM purchase p
            JOIN purchase_details pd ON p.id = pd.purchase_id;
        """)

        rows = cur.fetchall()

        # Create CSV in-memory
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['bill_date', 'bill_no', 'bill_total', 'medicine_name', 'quantity', 'mrp', 'item_total', 'expiry_date'])

        for row in rows:
            writer.writerow(row)

        output.seek(0)
        cur.close()
        conn.close()

        return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=purchase_data.csv"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
