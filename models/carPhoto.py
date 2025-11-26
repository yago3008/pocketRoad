from config.database import db
from datetime import datetime, timezone
import uuid
class CarPhoto(db.Model):
    __tablename__ = "car_photos"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))

    # relação com Car
    car = db.relationship("Car", backref=db.backref("photos", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "car_id": self.car_id,
            "filename": self.filename,
            "created_at": self.created_at.isoformat(),
        }
