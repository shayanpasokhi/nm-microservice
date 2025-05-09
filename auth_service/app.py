import models
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config

migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)

models.init_app(app)
migrate.init_app(app, models.db)

jwt = JWTManager(app)

from models import TokenBlocklist

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return models.db.session.query(TokenBlocklist.id).filter_by(jti=jti).first() is not None

from routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
