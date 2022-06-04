from flask import Blueprint, jsonify, request

from utils.token import token_required
from utils.models import Todo, db

to_do = Blueprint('to_do', __name__)


@to_do.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=current_user.uid)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'success': True, 'message': '新增成功'})


@to_do.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.uid).first()
    todo.complete = not todo.complete
    db.session.commit()

    return jsonify({'success': True, 'message': '編輯成功'})


@to_do.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.uid).first()

    if not todo:
        return jsonify({'success': False, 'message': '沒有這個項目'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'success': True, 'message': '刪除成功'})


@to_do.route('/todo', methods=['GET'])
@token_required
def get_todos(current_user):
    todo_list = Todo.query.filter_by(user_id=current_user.uid)

    return jsonify({
        'success': True,
        'data': [
            {
                'id': todo.id,
                'text': todo.text,
                'complete': todo.complete,
            }
            for todo in todo_list
        ]
    })


@to_do.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.uid).first()

    return jsonify({
        'success': True,
        'data': {
            'id': todo.id,
            'text': todo.text,
            'complete': todo.complete,
        }
    })


