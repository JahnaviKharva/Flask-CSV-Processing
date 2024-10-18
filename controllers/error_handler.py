from flask import Blueprint, jsonify

error_bp = Blueprint('error_bp', __name__)

# 404 Not Found Error Handler
@error_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "The requested resource was not found"}), 404

# 400 Bad Request Error Handler
@error_bp.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Bad request. Please check your input data"}), 400

# 401 Unauthorized Error Handler
@error_bp.app_errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized. Please provide valid credentials"}), 401

# 403 Forbidden Error Handler
@error_bp.app_errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "Forbidden. You don't have permission to access this resource"}), 403

# 500 Internal Server Error Handler
@error_bp.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "An internal server error occurred. Please try again later"}), 500

# Custom Exception Handling (Optional)
@error_bp.app_errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500
