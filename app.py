from flask import Flask
from controllers.purchase_controller import purchase_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from controllers.auth_controller import auth_bp 
from config import DevelopmentConfig
from controllers.error_handler import error_bp

app = Flask(__name__)

# Load development configuration
app.config.from_object(DevelopmentConfig)


app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Register the blueprint
app.register_blueprint(purchase_bp)



jwt = JWTManager(app)



# Register the authentication blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(error_bp)


if __name__ == "__main__":
    app.run(debug=True)
