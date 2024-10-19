from datetime import datetime

from flask import request, make_response
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from extensions import bcrypt
from models import Task
from models import db, User


def save_to_db(instance):
    db.session.add(instance)
    db.session.commit()


class HomeAPI(MethodView):
    def get(self):
        return '<h1>Hi, Welcome to Todo!</h1>'

    
class UserRegistration(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not username:
            return make_response({'message':'Username required!'}) , 400
        if not password:
            return make_response({'message':'Password required!'}), 400
        if password != confirm_password:
            return make_response({'message':'Passwords do not match!'}), 400
        if User.query.filter_by(user_name=username).first():
            return make_response({'message':'Username already exists!'}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(user_name=username, password=hashed_password)
        save_to_db(new_user)

        return make_response({'message':'User created sucessfully'}), 200

    
class UserLogin(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')


        user = User.query.filter_by(user_name=username).first()
        if not user:
            return make_response({'message':'Invalid user!'}), 401
        
        hashed_password = user.password
        is_valid = bcrypt.check_password_hash(hashed_password, password)
        if not is_valid:
            return make_response({'message':'Invalid password!'}), 401
        access_token = create_access_token(identity=user.id)
        return make_response({access_token:access_token}), 200


class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        return make_response({'message':'User logged out successfully!'}), 200


class create_task(MethodView):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description')
        try:
            due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d')
        except ValueError as e:
            return make_response({'message':'Invalid date format!'}), 400

        status = data.get('status')

        new_task = Task(user_id=user_id, title=title, description=description, due_date=due_date, status=status)
        save_to_db(new_task)

        update_task = {
            'id': new_task.id, 
            'title': new_task.title, 
            'description' : new_task.description, 
            'due_date':new_task.due_date,
            'status': new_task.status
        }
        details = {'message': 'Task created successfully!', 'task': update_task}

        return make_response(details, 200)

    
class get_tasks(MethodView):
    @jwt_required()
    def get(self, user_id):
        tasks = Task.query.filter_by(user_id=user_id).all()
        task_list = []
        for task in tasks:
            task_list.append({
                'id':task.id,
                'title':task.title,
                'description':task.description,
                'due_date':task.due_date,
                'completed':task.status
                })
        return make_response(task_list)

    
class specific_task(MethodView):
    @jwt_required()
    def get(self, task_id):
        task=Task.query.get(task_id)
        return make_response({
            'id':task_id,
            'title':task.title,
            'description':task.description,
            'due_date':task.due_date,
            'completed':task.status
        })


class update_task(MethodView):
    @jwt_required()
    def put(self, task_id):
        task = Task.query.get(task_id)
        data = request.get_json()
        task.title = data.get('title')
        task.description = data.get('description')
        task.due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d')
        task.status = data.get('status')
        db.session.commit()

        return make_response({'message': 'Task updated successfully!'})


class delete_task(MethodView):
    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()

        return make_response({'message': 'Task deleted successfully!'})


class mark_completed(MethodView):
    @jwt_required()
    def put(self, task_id):
        task = Task.query.get(task_id)
        task.status = True
        db.session.commit()

        return make_response({'message': 'Task completed successfully!'})