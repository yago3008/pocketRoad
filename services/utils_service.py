import jwt
from datetime import datetime, timedelta, timezone
from config.jwt_config import SECRET_KEY
from models.user import User

class UtilsService:

    @staticmethod
    def generate_jwt(user_id, minutes=180):
        now = datetime.now(timezone.utc)   
        role = "admin" if user_id == 1 else 'user'
        payload = {
            "user_id": user_id,
            "role": role, 
            "exp": now + timedelta(minutes=minutes),
            "iat": now
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_jwt(token):
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_user_by_id(id):
        user = User.query.get(id)
        if not user:
            return None
        return user
    
    @staticmethod
    def strict_comparison(a, b):
        typeA = type(a) 
        typeB = type(b)
        isClause = typeA is typeB
        equalsClause = a == b
        result = isClause and not equalsClause

        return result