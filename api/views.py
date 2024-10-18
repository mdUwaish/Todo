from flask import request, jsonify
from datetime import datetime
from flask.views import MethodView
from models import User, db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from models import Task


class HomeAPI(MethodView):
    def get(self):
        return '<h1>Hi, Welcome to Todo!</h1>'
    
class UserRegistration(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message':'Username and password required!'}) , 400
        if User.query.filter_by(user_name=username).first():
            return jsonify({'message':'Username already exists!'}), 400
        
        new_user = User(user_name=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message':'User created sucessfully'}), 200
    
class UserLogin(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(user_name=username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return jsonify({access_token:access_token}), 200

        return jsonify({'message':'Invalid credentials!'}), 401

class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        return jsonify({'message':'User logged out successfully!'}), 200

class create_task(MethodView):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description')
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d')
        status = data.get('status')

        new_task = Task(user_id=user_id, title=title, description=description, due_date=due_date, status=status)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task created successfully!', 'task':{
                        'id': new_task.id, 'title': new_task.title, 'description' : new_task.description, 'due_date':new_task.due_date,
                        'status': new_task.status}})
    
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
        return jsonify(task_list)
    
class specific_task(MethodView):
    @jwt_required()
    def get(self, task_id):
        task=Task.query.get(task_id)
        return jsonify({
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

        return jsonify({'message': 'Task updated successfully!'})

class delete_task(MethodView):
    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully!'})

class mark_completed(MethodView):
    @jwt_required()
    def put(self, task_id):
        task = Task.query.get(task_id)
        task.status = True
        db.session.commit()

        return jsonify({'message': 'Task completed successfully!'})