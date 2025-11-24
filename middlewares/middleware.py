
from flask import request, jsonify
from functools import wraps
import jwt
from config.jwt_config import SECRET_KEY


def secure(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"status":"error", "message":"Token não fornecido.", "data": None}), 401
        
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"status":"error", "message":"Header Authorization inválido.", "data": None}), 401
        
        token = parts[1]

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"status":"error", "message":"Token expirado.", "data": None}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status":"error", "message":"Token inválido.", "data": None}), 401

        request.user_id = decoded.get("user_id")

        return f(*args, **kwargs)
    
    return decorator


def admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"status":"error", "message":"Token não fornecido.", "data": None}), 401
        
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"status":"error", "message":"Header Authorization inválido.", "data": None}), 401
        
        token = parts[1]

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"status":"error", "message":"Token expirado.", "data": None}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status":"error", "message":"Token inválido.", "data": None}), 401

        role = decoded.get("role")
        print(role)
        if role != "admin":
            return jsonify({"status":"error", "message":"Acesso restrito.", "data": None}), 403

        request.user_id = decoded.get("user_id")
        request.role = role

        return f(*args, **kwargs)
    
    return decorator