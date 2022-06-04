import datetime
import os

import jwt
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from utils.models import User, db

auth = Blueprint('auth', __name__)


@auth.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'], method='sha256')
    new_user = User(uid=data['uid'], name=data['name'], password=hashed_pw, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'created!'})


@auth.route('/users')
def get_users():
    users = User.query.all()
    data = [
        {
            'uid': user.uid,
            'name': user.name,
            'admin': user.admin
        }
        for user in users
    ]

    return jsonify({'data': data})


@auth.route('/user/<uid>')
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()
    data = {
        'uid': user.uid,
        'name': user.name,
        'admin': user.admin
    }

    return jsonify({'data': data})


@auth.route('/user/<uid>', methods=['PUT'])
def edit_user(uid):
    data = request.get_json()
    user = User.query.filter_by(uid=uid).first()
    user.name = data['name']
    db.session.commit()
    return jsonify({'message': 'success!'})


@auth.route('/user/<uid>/perm', methods=['PUT'])
def change_perm(uid):
    user = User.query.filter_by(uid=uid).first()
    user.admin = not user.admin
    db.session.commit()
    return jsonify({'message': 'success!'})
