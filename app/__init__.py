from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config


db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    try:
        from app.routes.auth import auth_bp
        from app.routes.tasks import task_bp
        from app.routes.categories import category_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(task_bp, url_prefix='/api/tasks')
        app.register_blueprint(category_bp, url_prefix='/api/categories')
    except Exception as e:
        app.logger.error(f'Error registering blueprints: {str(e)}')
        raise

    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
        except Exception as e:
            app.logger.error(f'Error creating database tables: {str(e)}')
            raise

    return app
