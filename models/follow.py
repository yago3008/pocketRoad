from datetime import datetime, timezone
from config.database import db
import uuid

class Follow(db.Model):
    __tablename__ = "followers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    follower_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    followed_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint("follower_id", "followed_id"),
    )