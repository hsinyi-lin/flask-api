import datetime

import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from api_views.token import token_required
from utils.models import User, db

auth = Blueprint('auth', __name__)


@auth.route('/user', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'], method='sha256')
    new_user = User(uid=data['uid'], name=data['name'], password=hashed_pw, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': True, 'message': '註冊成功'})


@auth.route('/user/<uid>/perm', methods=['PUT'])
@token_required
def change_perm(current_user, uid):
    if current_user.admin is False:
        return jsonify({'success': False, 'message': '無權限'}), 403

    user = User.query.filter_by(uid=uid).first()
    user.admin = not user.admin
    db.session.commit()
    return jsonify({'success': True, 'message': '更新成功'})


@auth.route('/login', methods=['POST'])
def login():
    authorization = request.authorization

    if not authorization.username or not authorization.password:
        return jsonify({'success': False, 'message': '請檢查是否有輸入完整'}), 400

    user = User.query.filter_by(uid=authorization.username).first()

    if not user:
        return jsonify({'success': False, 'message': '沒有此帳號'}), 404

    check_pw = check_password_hash(user.password, authorization.password)

    if check_pw:
        token = jwt.encode({'uid': user.uid, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                           'secret_test', algorithm='HS256')
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False, 'message': '密碼錯誤'}), 401



