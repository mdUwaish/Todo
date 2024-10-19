from flask import Blueprint
from flask.views import MethodView

from api.views import create_task, get_tasks, HomeAPI, specific_task, UserRegistration, UserLogin
from api.views import mark_completed, update_task, delete_task, UserLogout

bp = Blueprint(
    'api', __name__, url_prefix='/todo'
)

bp.add_url_rule(
    "/",
    view_func=HomeAPI.as_view('index'),
    methods=["GET"]
)

bp.add_url_rule(
    "/user/register",
    view_func=UserRegistration.as_view('UserRegistration'),
    methods=["POST",]
)

bp.add_url_rule(
    "/user/login",
    view_func=UserLogin.as_view('UserLogin'),
    methods=["POST", ]
)

bp.add_url_rule(
    "/user/logout",
    view_func=UserLogout.as_view('UserLogout'),
    methods=["POST", ]
)

bp.add_url_rule(
    "/api/task",
    view_func=create_task.as_view('create_task'),
    methods=["POST", ] 
)

bp.add_url_rule(
    "/api/tasks/user/<int:user_id>",
    view_func=get_tasks.as_view('get_tasks'),
    methods=["GET", ]
)

bp.add_url_rule(
    "/api/tasks/<int:task_id>",
    view_func=specific_task.as_view('specific_task'),
    methods=["GET", ]
)

bp.add_url_rule(
    "/api/task/update/<int:task_id>",
    view_func=update_task.as_view('update_task'),
    methods=["PUT", ]
)

bp.add_url_rule(
    "/api/task/delete/<int:task_id>",
    view_func=delete_task.as_view('delete_task'),
    methods=["DELETE", ]
)

bp.add_url_rule(
    "/api/task/<int:task_id>/complete",
    view_func=mark_completed.as_view('mark_completed'),
    methods=["PUT", ]
)