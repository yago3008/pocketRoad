from flask import Blueprint, request, jsonify, redirect
import requests
from services.user_service import UserService
from middlewares.middleware import secure, admin
from config.oauth_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from exceptions.exceptions import UserAlreadyExists

user_bp = Blueprint("user", __name__)

# ---------------------------
# REGISTER
# ---------------------------
@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        UserService.register_user(
            data.get("email"),
            data.get("username"),
            data.get("password")
        )

        return jsonify({"success": True, "message": "Usuário registrado com sucesso.", "data": None}), 201

    except UserAlreadyExists as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


# ---------------------------
# LOGIN
# ---------------------------
@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        token = UserService.authenticate(
            data.get("username"),
            data.get("password")
        )

        if not token:
            return jsonify({"success": False, "message": "Credenciais inválidas.", "data": None}), 401

        return jsonify({"success": True, "message": "Login realizado com sucesso.", "data": token})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


# ---------------------------
# LOGIN OAUTH
# ---------------------------
@user_bp.route("/auth/google/login")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?client_id=" + GOOGLE_CLIENT_ID +
        "&redirect_uri=" + GOOGLE_REDIRECT_URI +
        "&response_type=code"
        "&scope=email profile openid"
        "&prompt=select_account"
    )
    return redirect(google_auth_url)


# ---------------------------
# LOGIN OAUTH CALLBACK
# ---------------------------
@user_bp.route("/auth/google/callback", methods=["GET"])
def google_callback():
    code = request.args.get("code")

    if not code:
        return jsonify({"success": False, "message": "Código não recebido"}), 400

    # TROCAR O CODE POR ACCESS TOKEN E ID TOKEN
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI
        }
    )

    token_data = token_res.json()

    if "id_token" not in token_data:
        return jsonify({"success": False, "message": "Falha ao autenticar com Google"}), 400

    id_token_google = token_data["id_token"]

    # validar id_token do Google
    google_user = id_token.verify_oauth2_token(
        id_token_google,
        google_requests.Request(),
        GOOGLE_CLIENT_ID
    )

    google_id = google_user["sub"]
    email = google_user.get("email")
    picture = google_user.get("picture")
    name = google_user.get("name")

    jwt_token = UserService.authenticate_google(
        google_id,
        email=email,
        picture=picture,
        name=name
    )

    return jsonify({
        "success": True,
        "message": "Login OAuth realizado com sucesso.",
        "data": {"token": jwt_token}
    })

# ---------------------------
# ESQUECI A SENHA
# ---------------------------
@user_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    try:
        data = request.get_json()
        UserService.forgot_password(
            email = data.get("email")
        )

        return jsonify({"success": True, "message": "Se este e-mail existir, enviaremos um link de recuperação.", "data": None})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500
    
# ---------------------------
# RESET DA SENHA
# ---------------------------
@user_bp.route("/reset-password", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        UserService.reset_password(
            token=request.args.get("token"),
            new_password = data.get("new_password")
        )

        return jsonify({"success": True, "message": "Reset de senha concluido", "data": None})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500
    
# ---------------------------
# ATUALIZAR
# ---------------------------
@user_bp.route("/users/update", methods=["POST"])
@secure
def update_user():
    try:
        user_id = request.user_id
        
        user = UserService.update_user(
            user_id,
            username = request.form.get("username"),
            current_password = request.form.get("current_password"),
            new_password = request.form.get("new_password"),
            confirm_password = request.form.get("confirm_password"),
            remove_photo = request.form.get("remove_photo"),
            photo = request.files.get("photo")
        )

        if not user:
            return jsonify({"success": False, "message": "Usuário não encontrado.", "data": None}), 404

        return jsonify({"success": True, "message": "Usuario atualizado.", "data": user.to_dict()})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


# ---------------------------
# LISTAR TODOS
# ---------------------------
@user_bp.route("/users", methods=["GET"])
@admin
def list_users():
    try:
        users = UserService.get_all_users()

        return jsonify({
            "status": "success",
            "message": "Lista de usuários obtida com sucesso.",
            "data": [
                {"id": u.id, "username": u.username, "photo_path": u.photo_path} for u in users
            ]
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


# ---------------------------
# OBTER UM USUÁRIO
# ---------------------------
@user_bp.route("/users/<int:user_id>", methods=["GET"])
@admin
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)

        if not user:
            return jsonify({"success": False, "message": "Usuário não encontrado.", "data": None}), 404

        return jsonify({"success": True, "message": "Usuario encontrado.", "data": {"id": user.id, "username": user.username, "photo_path": user.photo_path}})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


# ---------------------------
# DELETAR
# ---------------------------
@user_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@admin
def delete_user(user_id):
    try:
        deleted = UserService.delete_user(user_id)

        if not deleted:
            return jsonify({"success": False, "message": "Usuário não encontrado.", "data": None}), 404
        return jsonify({"success": True, "message": "Usuário deletado.", "data": deleted.to_dict()})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


