from models.follow import Follow
from config.database import db
from services.utils_service import UtilsService
from exceptions.exceptions import (
    UserNotFound,
    UnfollowedPerson
)

class FollowService:

    @staticmethod
    def follow_user(follower_id, followed_id):
        followed = UtilsService.get_user_by_id(followed_id)

        if not followed:
            raise UserNotFound("Usuário não existe.")
        if not followed_id:
            raise UserNotFound("Usuário não existe.")
        if not UtilsService.strict_comparison(followed_id, follower_id):
            raise UnfollowedPerson("Você não pode seguir a si mesmo")

        relationship_exists = Follow.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()

        if relationship_exists:
            raise UnfollowedPerson("Você já segue esse usuario.")
        
        new_relationship = Follow(
        follower_id=follower_id,
        followed_id=followed_id
        )
        followed_name = (UtilsService.get_user_by_id(followed_id)).username
        db.save(new_relationship)
        return followed_name

    @staticmethod
    def unfollow_user(follower_id, followed_id):
        followed = UtilsService.get_user_by_id(followed_id)

        if not followed:
            raise UserNotFound("Usuário não existe.")
        if not followed_id:
            raise UserNotFound("Usuário não existe.")
        if not UtilsService.strict_comparison(followed_id, follower_id):
            raise UnfollowedPerson("Você não pode deixar de seguir a si mesmo")

        relationship_exists = Follow.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()

        if not relationship_exists:
            raise UnfollowedPerson("Você não segue esse usuario.")
        
        db.delete(relationship_exists)
        followed_name = (UtilsService.get_user_by_id(followed_id)).username
        return followed_name
    

    @staticmethod
    def get_followers(followed_id):
        followers = Follow.query.filter_by(followed_id=followed_id).all()
        
        for f in followers:
            user = UtilsService.get_user_by_id(f.follower_id)
            f.username = user.username
            f.photo_path = user.photo_path

        return followers

    @staticmethod
    def get_following(follower_id):
        following = Follow.query.filter_by(follower_id=follower_id).all()
        
        for f in following:
            user = UtilsService.get_user_by_id(f.followed_id)
            f.username = user.username
            f.photo_path = user.photo_path
        return following