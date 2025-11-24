from config.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    photo_path = db.Column(db.String(255), nullable=True, default="/static/users/default.jpg")
    google_id = db.Column(db.String(200), unique=True, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "photo_path": self.photo_path,
            "email": self.email
        }