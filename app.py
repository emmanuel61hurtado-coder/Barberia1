from flask import Flask
from extensions import db, login_manager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from routes.client_routes import client_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        db.create_all()
        from models.admin_model import seed_admin
        from models.barber_model import seed_barbers
        from models.service_model import seed_services
        from models.review_model import seed_reviews
        seed_admin()
        seed_barbers()
        seed_services()
        seed_reviews()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
