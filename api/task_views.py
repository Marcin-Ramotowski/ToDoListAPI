from datetime import datetime
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, db
from user_views import admin_required, validate_access

task_bp = Blueprint('task_bp', __name__)

# ============================================================
# 🚀 1. API ENDPOINTS (ROUTES)
# ============================================================

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
    validate_task_data(data)
    due_date = datetime.strptime(data['due_date'], '%d-%m-%Y %H:%M')
    task = Task(title=data['title'], description=data['description'], due_date=due_date,
                done=data['done'], user_id=get_jwt_identity())

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict())


@task_bp.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get(task_id)
    check_if_task_exists(task)

    request_data = request.get_json()
    validate_task_data(request_data)
    request_fields = set(request_data.keys())
    editable_fields = Task.get_editable_fields()

    # PUT requires all values
    if request.method == 'PUT':
        if request_fields != editable_fields:
            abort(400, "Invalid request data structure.")

    for field_name in editable_fields:
        requested_value = request_data.get(field_name)
        if requested_value is None:
            continue
        new_value = datetime.strptime(requested_value, '%d-%m-%Y %H:%M') \
            if field_name == 'due_date' else requested_value
        setattr(task, field_name, new_value)
    db.session.commit()
    return jsonify(task.to_dict())


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)
    check_if_task_exists(task)
    db.session.delete(task)
    db.session.commit()
    return jsonify({})


# ============================================================
# 🔧 2. UTILITIES
# ============================================================

def check_if_task_exists(task):
    # Check if task exists or user has permissions to see it
    if task is None:
        abort(404, "Task not found.")
    user_id = task.user_id
    validate_access(user_id)


def validate_task_data(task):
    due_date = task.get('due_date')
    if due_date:
        try:
            datetime.strptime(due_date, '%d-%m-%Y %H:%M')
        except ValueError:
            abort(400, "Incorrect datetime format. Expected DD-MM-YYYY HH:MM")
    done = task.get('done')
    if done not in (0, 1):
        abort(400, "Incorrect done field value. Expected 0 or 1")
