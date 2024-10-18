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


purchase_bp = Blueprint('purchase_bp', __name__)

@purchase_bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    csv_data = csv.DictReader(file.read().decode('utf-8-sig').splitlines())

    # Standardize headers
    headers = [header.strip().lstrip('\ufeff') for header in csv_data.fieldnames]
    csv_data.fieldnames = headers

    # Required fields for each row in the CSV
    required_fields = ['bill_date', 'bill_no', 'bill_total', 'medicine_name', 'quantity', 'mrp', 'item_total', 'expiry_date']

    for row in csv_data:
        # Validate required fields only
        is_valid, message = validate_required_fields(row, required_fields)
        if not is_valid:
            return jsonify({"error": message}), 400

    return jsonify({"message": "CSV data is inserted"}), 200

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