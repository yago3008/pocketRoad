from models.cars import Car
from exceptions.exceptions import CarNotFound
from config.database import db
class AdminService:
    @staticmethod
    def get_cars_to_aprove():
        return Car.query.filter_by(approved=False).all
    
    @staticmethod
    def aprove_car(car_id, car_brand, car_model, car_type, car_year):
        car = Car.query.get(car_id)
        if not car:
            raise CarNotFound("Carro não encontrado")
        car.approved=True
        car.brand = car_brand
        car.model = car_model
        car.type = car_type
        car.year = car_year
        db.save(car)
        
        