from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['DATABASE'] = 'app/file.db'

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
