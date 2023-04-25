import jwt
from flask import request, jsonify, current_app


def requires_auth(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization').split()[1]

            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expirado.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido.'}), 401

            if payload['role'] != role:
                return jsonify({'error': 'Acceso denegado.'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
