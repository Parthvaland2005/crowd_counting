from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Load configuration from environment variables or a .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Register blueprints
from .routes import main as main_blueprint
app.register_blueprint(main_blueprint)

# Import models
from .models import *  # Import all models to ensure they are registered with SQLAlchemy

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()