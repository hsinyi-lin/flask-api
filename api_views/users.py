from flask import jsonify, Blueprint, request

from api_views.token import token_required
from utils.models import User, db

user_data = Blueprint('user_data', __name__)


@user_data.route('/users')
@token_required
def get_users():
    users = User.query.all()

    return jsonify({
        'success': True,
        'data': [
            {
                'uid': user.uid,
                'name': user.name,
                'admin': user.admin
            }
            for user in users
        ]
    })


@user_data.route('/user/<uid>')
@token_required
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()

    return jsonify({
        'success': True,
        'data': {
            'uid': user.uid,
            'name': user.name,
            'admin': user.admin
        }
    })


@user_data.route('/user/<uid>', methods=['PUT'])
@token_required
def edit_user(current_user, uid):
    if current_user.uid != uid:
        return jsonify({'success': False, 'message': '編輯失敗'}), 401

    data = request.get_json()
    user = User.query.filter_by(uid=uid).first()
    user.name = data['name']
    db.session.commit()
    return jsonify({'success': True, 'message': '編輯成功'})