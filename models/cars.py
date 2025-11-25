from config.database import db

class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    photo = db.Column(db.String(255), nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "type": self.type,
            "year": self.year,
            "photo": self.photo
        }
