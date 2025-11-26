from config.database import db
from datetime import datetime, timezone
import uuid
class Cardex(db.Model):
    __tablename__ = "cardex"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Um usuário tem 1 cardex (uselist=False)
    user = db.relationship("User", backref=db.backref("cardex", uselist=False))


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
        }
