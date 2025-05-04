from flask import Flask, g
from flask.sessions import SecureCookieSessionInterface
from flask_migrate import Migrate
from flask_login import LoginManager
import models
from routes import user_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vZK7siKrV8BL46KsyAIPoQ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
models.init_app(app)
app.register_blueprint(user_blueprint)
login_manager = LoginManager(app)
migrate = Migrate(app, models.db)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')

    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()

        if user:
            return user
        
    return None

class CustomSessionInterface(SecureCookieSessionInterface):
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
