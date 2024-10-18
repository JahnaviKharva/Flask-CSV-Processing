import re
from datetime import datetime

def validate_required_fields(data, required_fields):
    """
    Validate that all required fields are present in the data.
    """
    # Clean and standardize the field names in the data
    data = {key.strip(): value for key, value in data.items()}

    # Check for missing or empty fields
    missing_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing_fields:
        return False, f"Missing or empty fields: {', '.join(missing_fields)}"
    
    return True, ""

def validate_email(email):
    """
    Validate the format of an email address.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"
    return True, ""


def validate_date_format(date_str, formats=['%Y-%m-%d', '%d-%m-%Y']):
    """
    Validate that the date string matches one of the given formats.
    """
    for date_format in formats:
        try:
            # Try to parse the date with the current format
            datetime.strptime(date_str.strip(), date_format)
            return True, ""
        except ValueError:
            continue
    
    # Join formats without escaping '%' characters
    return False, f"Invalid date format, expected one of: {' or '.join(formats)}"

def validate_positive_integer(value):
    """
    Validate that the value is a positive integer.
    """
    try:
        value = int(value)
        if value > 0:
            return True, ""
        else:
            return False, "Value must be a positive integer"
    except ValueError:
        return False, "Value must be an integer"

def validate_mrp(value):
    """
    Validate that the MRP (Maximum Retail Price) is a positive float.
    """
    try:
        value = float(value)
        if value >= 0:
            return True, ""
        else:
            return False, "MRP must be a non-negative number"
    except ValueError:
        return False, "MRP must be a valid number"
