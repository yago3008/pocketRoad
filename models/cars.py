from config.database import db
import uuid
class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    brand = db.Column(db.String(255), nullable=False)
    brand_hint = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    model_hint = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    type_hint = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    year_hint = db.Column(db.String(4), nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    approved = db.Column(db.Boolean, default=False, nullable=False)

    # Cada carro pertence a UM cardex
    cardex_id = db.Column(db.Integer, db.ForeignKey("cardex.id"), nullable=False)
    # Cardex.cars → lista de carros
    cardex = db.relationship("Cardex", backref=db.backref("cars", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "brand_hint": self.brand_hint,
            "model": self.model,
            "model_hint": self.model_hint,
            "type": self.type,
            "type_hint": self.type_hint,
            "year": self.year,
            "year_hint": self.year_hint,
            "photo": self.photo,
            "approved": self.approved,
            "cardex_id": self.cardex_id
        }
