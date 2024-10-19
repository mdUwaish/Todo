import secrets
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from extensions import bcrypt
from models import db, User, Task


app = Flask(__name__) #creating an instance of the app

# db connection to postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Uwaish%401@localhost:5432/my_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
app.config['SECRET_KEY'] = '1234'
# app.config['JWT_TOKEN_LOCATION'] = ['headers']

bcrypt.init_app(app) #instance for bcrypt

db.init_app(app) #initializing the app with db

migrate = Migrate(app, db) #instance for migration

jwt = JWTManager(app) #instance for jwt

from api import bp as api_bp #importing the blueprint
app.register_blueprint(api_bp) #registering the blueprint

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True)