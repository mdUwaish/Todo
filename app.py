import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

from extensions import bcrypt
from models import db, User, Task


app = Flask(__name__) #creating an instance of the app

# db connection to postgres
load_dotenv(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['JWT_TOKEN_LOCATION'] = ['headers']

bcrypt.init_app(app) #instance for bcrypt

db.init_app(app) #initializing the app with db

migrate = Migrate(app, db) #instance for migration

jwt = JWTManager(app) #instance for jwt

from api import bp as api_bp #importing the blueprint
app.register_blueprint(api_bp) #registering the blueprint

if __name__ == '__main__':
    app.run(debug=True)
