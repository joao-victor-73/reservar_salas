from flask import Flask, request
from flask_login import LoginManager
from models import db
from routes import register_routes

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para continuar.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuarios.query.get(int(user_id))


    with app.app_context():
        from models import Usuarios
        from utils.decorators import coordenador_required
        register_routes(app)

    return app


app = create_app() # IMPORTANTE: aqui você cria o app SEM rodar localmente

# Só roda servidor se for no ambiente local (desenvolvimento)
if __name__ == "__main__":
    app.run(debug=True)