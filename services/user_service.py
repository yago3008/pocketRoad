import os
from google.oauth2 import id_token
from google.auth.transport import requests
from models.user import User
from config.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from services.utils_service import UtilsService
from services.email_service import EmailService
from config.general_config import RESET_TOKEN_URL
from exceptions.exceptions import (
    UserAlreadyExists,
    UserNotFound,
    UsernameAlreadyTaken,
    InvalidCredentials,
    PasswordDoesntMatch,
    InvalidPassword,
    InvalidFile
)

class UserService:

    @staticmethod
    def register_user(email, username, password):
        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if username_exists:
            raise UserAlreadyExists("Usuário já existe.")

        if email_exists:
            raise UserAlreadyExists("Email já existe.")
        
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw, email=email)
        db.save(new_user)

        return new_user

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            raise InvalidCredentials("Credenciais inválidas.")

        token = UtilsService.generate_jwt(user.id)
        return token

    @staticmethod
    def authenticate_google(google_id, email, picture=None, name=None):
        # 1. Verificar se o usuário já existe
        user = User.query.filter_by(google_id=google_id).first()

        if not user:
            # 2. Criar usuário automaticamente
            user = User(
                username=name or email.split("@")[0],
                email=email,
                password=generate_password_hash(os.urandom(16).hex()),
                google_id=google_id,
                photo_path=picture or "/static/users/default.png"
            )

            db.session.add(user)
            db.session.commit()

        token = UtilsService.generate_jwt(user.id)

        return token

    @staticmethod
    def forgot_password(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"success": True, "message": "Se este e-mail existir, enviaremos um link de recuperação."}
        
        reset_token = UtilsService.generate_jwt(user.id, minutes=15)
        EmailService.send_email_smtp(to_email=user.email,
                                     subject="Reset de senha",
                                     html_body = f"""
                                                <h1>Recuperação de senha</h1>
                                                <p>Clique no link abaixo para redefinir sua senha:</p>
                                                <a href="{RESET_TOKEN_URL}{reset_token}">
                                                    Redefinir senha
                                                </a>
                                                """
                                     )

    def reset_password(token, new_password):
        decoded_jwt = UtilsService.verify_jwt(token)
        user_id = decoded_jwt["user_id"]
        user = User.query.get(user_id)

        user.password = generate_password_hash(new_password)
        
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)

        if not user:
            raise UserNotFound("Usuário não encontrado.")

        return user

    @staticmethod
    def update_user(user_id, username=None, current_password=None, new_password=None, confirm_password=None, photo=None, remove_photo=None):
        user = User.query.get(user_id)

        if not user:
            raise UserNotFound("Usuário não encontrado.")

        if username:
            already_taken = User.query.filter(
                User.username == username,
                User.id != user_id
            ).first()

            if already_taken:
                raise UsernameAlreadyTaken("Esse username já está em uso.")

            user.username = username

        if current_password:
            if not check_password_hash(user.password, current_password):
                raise InvalidPassword("Senha atual incorreta")
            if new_password != confirm_password:
                raise PasswordDoesntMatch("As senhas fornecidas necessitam ser iguais.")
            if new_password:
                user.password = generate_password_hash(new_password)

        if photo:
            allowed = {"image/jpeg", "image/png", "image/webp"}
            if photo.mimetype not in allowed:
                raise InvalidFile("Formato de imagem inválido.")
            
            if user.photo_path and user.photo_path != "/static/users/default.png":
                old_path = user.photo_path.replace("/static", "uploads")
                if os.path.exists(old_path):
                    os.remove(old_path)

            os.makedirs("uploads/users", exist_ok=True)
            filename = f"user_{user_id}.png"
            
            photo_path = os.path.join("uploads/users", filename)
            photo.save(photo_path)

            user.photo_path = f"/static/users/{filename}"

        if remove_photo:
            if user.photo_path and user.photo_path != "/static/users/default.png":
                old_path = user.photo_path.replace("/static", "uploads")
                if os.path.exists(old_path):
                    os.remove(old_path)
            user.photo_path = f"/static/users/default.png"

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)

        if not user:
            raise UserNotFound("Usuário não encontrado.")

        db.session.delete(user)
        db.session.commit()
        return user
