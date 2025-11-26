from flask import Blueprint, request, jsonify
from services.cardex_service import CardexService
from middlewares.middleware import secure, admin
from exceptions.exceptions import ManualValidationIsNecessary
cardex_bp = Blueprint("cardex", __name__)


@cardex_bp.route("/cardex/add", methods=["POST"])
@secure
def cardex_add():
    try:
        user_id = request.user_id
        
        cardex = CardexService.cardex_add(
            user_id,
            photos = request.files.getlist("photo"),
            car_model = request.form.get("car_model"),
            car_year = request.form.get("car_year"),
            car_brand = request.form.get("car_brand")
        )

        return jsonify({"success": True, "message": "Carro adicionado com sucesso.", "data": cardex})
    
    except ManualValidationIsNecessary as e:
        return jsonify({"success": True, "message": str(e), "data": None})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": None}), 500

@cardex_bp.route("/cardex/remove", methods=["POST"])
@secure
def cardex_remove():
    pass

@cardex_bp.route("/cardex/<string:id>", methods=["POST"])
@secure
def cardex_view(id):
    pass