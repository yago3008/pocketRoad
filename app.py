from flask import Flask
from controllers.user_controller import user_bp
from controllers.follow_controller import follow_bp
from config.database import db
from models.user import User
from werkzeug.security import generate_password_hash
from flask_talisman import Talisman
from flask_cors import CORS
from config.general_config import APP_PORT
from wafaHell import WafaHell

def create_default_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password=generate_password_hash("admin"),
            email="yagomartins30@gmail.com"
        )
        db.session.add(admin)
        db.session.commit()

def create_routes(app):
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(follow_bp, url_prefix="/api")

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    csp = {
        'default-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'script-src': ["'self'"],
        'img-src': ["'self'", "data:"]
    }

    Talisman(app, content_security_policy=csp)

    with app.app_context():
        db.create_all()
        create_default_admin()

    create_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=APP_PORT, host='0.0.0.0')
