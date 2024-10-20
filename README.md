# Flask CSV Processing Backend

## Project Overview
This project is a Flask-based backend application designed to:
- Fetch data from CSV files
- Store the data in a PostgreSQL database
- Implement user authentication using login and signup
- Provide APIs for data manipulation and retrieval

## Table of Contents
- [Project Overview](#project-overview)
- [Setup and Installation](#setup-and-installation)
- [Database Structure](#database-structure)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [PostgreSQL Database Setup](#postgresql-database-setup)
- [Deployment](#deployment)

## Setup and Installation

### Prerequisites
1. **Python 3.8 or higher**
2. **Git** (Optional, for cloning the repo)
3. **Postman** (For API testing)

### Local Installation
### There is no need for clonning because i have a deployed urls, so, you can check them directly on postman
1. **Clone the repository:**
   ```bash
   git clone https://github.com/JahnaviKharva/Flask-CSV-Processing
   cd Flask-CSV-Processing

Set up a virtual environment:
python -m venv venv
venv\Scripts\activate  # For Windows
source venv/bin/activate  # For Mac/Linux

Install the required packages:
pip install -r requirements.txt

Set up the database:

Run the following command to create tables in the database:
python setup_database.py #databse is already setup on the railway postgresql, so no need to run it. this is just for the understanding.

Database Structure
The database consists of two tables:

purchase
id: Unique identifier
bill_date: Date of the purchase
bill_no: Bill number
bill_total: Total amount of the bill


purchase_details
id: Unique identifier
purchase_id: Foreign key referencing the purchase table
medicine_name: Name of the medicine
quantity: Quantity purchased
MRP: Maximum Retail Price
item_total: Total amount for the item
expiry_date: Expiry date of the medicine

API Endpoints
The following endpoints are available for testing on the deployed URL: web-production-5d75.up.railway.app

1. User Authentication
Signup

URL: https://web-production-5d75.up.railway.app/signup
Method: POST
Body:Raw-> JSON
{
  "username": "testuser",
  "password": "testpassword"
}

2. Login

URL: https://web-production-5d75.up.railway.app/login
Method: POST
Body:
{
  "username": "testuser",
  "password": "testpassword"
}

Returns a JWT token.

3. Logout
URL: https://web-production-5d75.up.railway.app/logout
Method: POST
Headers:
Authorization: Bearer <your_jwt_token>
Description: Invalidates the user's JWT token.

4.  Upload CSV
URL: https://web-production-5d75.up.railway.app/upload_csv
Method: POST
Body: form-data
Key: file
Value: [CSV file]
Description: Uploads a CSV file
Uploads a CSV file containing the following fields: bill_date, bill_no, medicine_name, quantity, mrp, expiry_date.
The file must have a .csv extension (comma delimited).
It processes the data and inserts it into the purchase and purchase_details tables.
The item_total and bill_total are automatically calculated based on mrp * quantity and the sum of item_total values, respectively.

Add the Authorization header:
Key: Authorization
Value: Bearer <your_access_token>
Click the Send button to test.

6. Fetch Purchase Data

URL: https://web-production-5d75.up.railway.app/get_purchase_data/<bill_no>
Method: GET


6. Update Purchase Detail

URL: https://web-production-5d75.up.railway.app/update_purchase_detail_data/{id}
Method: PUT
Headers:
Authorization: Bearer <your_jwt_token>
Body:
{
  "mrp": 60
}

7. Delete Purchase Detail
URL: https://web-production-5d75.up.railway.app/delete_purchase_detail_data/<id>
Example: https://web-production-5d75.up.railway.app/delete_purchase_detail_data/1
Method: DELETE
Headers:
Authorization: Bearer <your_jwt_token>
Description: Deletes the record with the specified ID from the purchase_details table.

8. Create Purchase CSV
URL: https://web-production-5d75.up.railway.app/create_purchase_csv
Method: GET
Description: Creates a CSV file from data in the purchase and purchase_details tables and stores it locally on the server.
PostgreSQL Database Setup

9. get_all_data
URL: https://web-production-5d75.up.railway.app/get_all_data
Method: GET
Headers:
Authorization: Bearer <your_jwt_token>

Using setup_database.py
Run the script to automatically create tables:
python setup_database.py

Deployment
The app is deployed on Railway and is accessible at web-production-5d75.up.railway.app. #you need to check the url endpoints on postman
