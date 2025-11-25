from models.cardex import Cardex
from models.cars import Car
from config.database import db
from services.utils_service import UtilsService
from services.artificial_intelligence_service import AIService
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
        print(photos)
        for image in photos:
            results.append(AIService.predict_car(image))
        print(results)
        confidence_avg = sum(item["confidence"] for item in results) / len(results)
        print(confidence_avg)
        if confidence_avg < 0.92:
            cardex.approved = False
            return False
            ##vai ter que mandar pra analise em /admin/analise
        else:
            cardex.approved = True
            return True
            ## chamar funcao generica pra criar carro

        
        
        
