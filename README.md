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
python setup_database.py

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
Body:
{
  "username": "testuser",
  "password": "testpassword"
}

Login

URL: https://web-production-5d75.up.railway.app/login
Method: POST
Body:
{
  "username": "testuser",
  "password": "testpassword"
}

Returns a JWT token.
2. Purchase Data
Upload CSV

URL: /upload_csv
Method: POST
Form-data:
Key: file, Value: [CSV file]
Fetch Purchase Data

URL: /get_purchase_data/{bill_no}
Method: GET
Update Purchase Detail

URL: /update_purchase_detail_data/{id}
Method: PUT
Body:
{
  "mrp": 60
}
PostgreSQL Database Setup

Using setup_database.py
Run the script to automatically create tables:
python setup_database.py

Deployment
The app is deployed on Railway and is accessible at web-production-5d75.up.railway.app. #you need to check the url endpoints on postman
