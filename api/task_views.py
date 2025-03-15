from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, db
from datetime import datetime
from user_views import admin_required, validate_access

task_bp = Blueprint('task_bp', __name__)


@task_bp.errorhandler(403)
def forbidden_error(error):
    response = jsonify(error.description)
    response.status_code = 403
    return response


@task_bp.errorhandler(404)
def not_found_error(error):
    response = jsonify(error.description)
    response.status_code = 404
    return response


def check_if_task_exists(task):
    # Check if task exists or user has permissions to see it
    if task is None:
        abort(404, {'error': 'Task not found.'})
    user_id = task.user_id
    validate_access(user_id)


@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_all_tasks():
    admin_required(get_jwt_identity()) # only admin can get all tasks
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    task = Task.query.get(task_id) # return task or None if task not found
    check_if_task_exists(task)
    return jsonify(task.to_dict())


@task_bp.route('/tasks/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_tasks_by_user(user_id):
    validate_access(user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks = [task.to_dict() for task in tasks]
    return jsonify(tasks)


@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = int(data.get('user_id'))
    validate_access(user_id, 'Provided user_id is not assign to current user')
    
    due_date = datetime.strptime(data['due_date'], '%d-%m-%Y')
    task = Task(title=data['title'], description=data['description'], due_date=due_date,
                done=data['done'], user_id=data['user_id'])

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict())


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get(task_id)
    check_if_task_exists(task)

    request_title = request.json.get('title')
    request_description = request.json.get('description')
    request_due_date = datetime.strptime(request.json.get('due_date'), '%d-%m-%Y')
    request_done = request.json.get('done')

    if all((task.title, task.description, task.due_date)) and task.done is not None:
        task.title = request_title
        task.description = request_description
        task.due_date = request_due_date
        task.done = request_done

        db.session.commit()
        return jsonify(task.to_dict())
    else:
        return abort(400, {'error': 'Incomplete task data.'})


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    check_if_task_exists(task)
    db.session.delete(task)
    db.session.commit()
    return jsonify({})
