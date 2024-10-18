from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy() #instance for sqlAlchemy

class User(db.Model):
    __name__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # repr method represents how one object of this datatable will look like
    def __repr__(self):
        return self.user_name


class  Task(db.Model):
    __name__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable= False)
    description = db.Column(db.Text, nullable= True)
    due_date = db.Column(db.DateTime, nullable= False)
    status = db.Column(db.Boolean, default= False)

    def __repr__(self):
        return self.title