from models.cardex import Cardex
from models.cars import Car
from config.database import db
from services.utils_service import UtilsService
from services.artificial_intelligence_service import AIService
from services.car_service import CarService
from exceptions.exceptions import (
    ManualValidationIsNecessary,
    InvalidFile
)

class CardexService:
    ## FAZER PARSING DO NOME E ANO, PEGAR SEQUENCIA DE DOS ULTIMOS 4 DIGITOS E VALIDAR SE SAO NUMEROS E MAIORES QUE 1940
    @staticmethod
    def cardex_add(user_id, photos, car_model=None, car_year=None, car_brand=None):
        results = []
        if not photos:
            raise InvalidFile("Você precisa enviar pelo menos 1 imagem.")
        
        cardex = Cardex.query.filter_by(user_id=user_id).first()

        if not cardex:
            cardex = Cardex(user_id=user_id)

        for image in photos:
            results.append(AIService.predict_car(image))

        confidence_avg = UtilsService.get_confidence_avg(results)

        print(results, confidence_avg)

        car = CarService.create_car()
        if confidence_avg < 0.92:
            cardex.approved = False
            
        else:
            model, year = UtilsService.parse_car_name(UtilsService.get_best_prediction(results))
            car.model = model
            car.year = year
            cardex.approved = True
        
        db.flush(car)
        cardex.car = car.id
        db.save(cardex)


        
        
        
