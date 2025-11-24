from flask import Blueprint, request, jsonify
from services.follow_service import FollowService
from middlewares.middleware import secure, admin

follow_bp = Blueprint("follow", __name__)


# ---------------------------
# FOLLOW UM USER
# ---------------------------
@follow_bp.route("/follow/add", methods=["POST"])
@secure
def follow_user():
    try:
        data = request.get_json()
        follower_id = request.user_id
        followed_user = FollowService.follow_user(follower_id, data.get("followed_id"))

        return jsonify({"success": True, "message": f"{followed_user} seguido com sucesso!", "data": None})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500
    

# ---------------------------
# UNFOLLOW UM USER
# ---------------------------
@follow_bp.route("/follow/delete", methods=["POST"])
@secure
def unfollow_user():
    try:
        data = request.get_json()
        follower_id = request.user_id
        followed_user = FollowService.unfollow_user(follower_id, data.get("followed_id"))

        return jsonify({"success": True, "message": f"{followed_user} excluido com sucesso!", "data": None})

    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500


# ---------------------------
# FOLLOWERS DE UM USER
# ---------------------------
@follow_bp.route("/follow/followers/<int:followed_id>", methods=["GET"])
@secure
def get_followers(followed_id):
    try:
        followers = FollowService.get_followers(followed_id)
        return jsonify({"success": True, "message": f"Followers consultados com sucesso!", "data": [{"id": f.id, "username": f.username, "photo_path": f.photo_path} for f in followers]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500
    
# ---------------------------
# FOLLOWING DE UM USER
# ---------------------------
@follow_bp.route("/follow/following/<int:follower_id>", methods=["GET"])
@secure
def get_following(follower_id):
    try:
        following = FollowService.get_following(follower_id)
        return jsonify({"success": True, "message": f"Following consultados com sucesso!", "data": [{"id": f.id, "username": f.username, "photo_path": f.photo_path} for f in following]})
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500