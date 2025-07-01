from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    return app
