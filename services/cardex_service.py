from models.cardex import Cardex
from models.cars import Car
from config.database import db
from services.utils_service import UtilsService
from services.artificial_intelligence_service import AIService
from services.car_service import CarService
from services.admin_service import AdminService
from exceptions.exceptions import (
    InvalidFile
)

class CardexService:
    @staticmethod
    def cardex_add(user_id, photos, model_hint=None, year_hint=None, brand_hint=None, type_hint=None):
        results = []
        if not photos:
            raise InvalidFile("Você precisa enviar pelo menos 1 imagem.")
        
        
        cardex = Cardex.query.filter_by(user_id=user_id).first()
        car = CarService.create_car()

        if not cardex:
            cardex = Cardex(user_id=user_id)

        for image in photos:
            if not UtilsService.is_image_ext_valid(image):
                raise InvalidFile("Formato de imagem inválido.")
            
            results.append(AIService.predict_car(image))
            #save image 
            image.save(f'')

        confidence_avg = UtilsService.get_confidence_avg(results)

        print(results, confidence_avg)

        
        if confidence_avg < 0.92:
            car.approved = False
        else:
            model, year = UtilsService.parse_car_name(UtilsService.get_best_prediction(results))
            car.model = model
            car.year = year
            car.approved = True
        
        db.flush(car)
        cardex.car = car.id
        db.save(cardex)


        
        
        
