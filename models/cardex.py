from config.database import db
from datetime import datetime, timezone

class Cardex(db.Model):
    __tablename__ = "cardex"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", backref=db.backref("cardex_entries", lazy=True))
    car = db.relationship("Car", backref=db.backref("cardex_entries", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "car_id": self.car_id,
            "approved": self.approved,
            "created_at": self.created_at.isoformat(),
        }
