import jwt
from flask import request, jsonify
from functools import wraps

from utils.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token 遺失'}), 401

        try:
            data = jwt.decode(token, 'secret_test', algorithms=['HS256'])
            current_user = User.query.filter_by(uid=data['uid']).first()
        except:
            return jsonify({'message': 'Token 失效'}), 401

        return f(current_user, *args, **kwargs)

    return decorated