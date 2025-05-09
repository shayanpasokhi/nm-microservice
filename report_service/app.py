import models
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from api.auth_service_api import AuthServiceApi

migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)

models.init_app(app)
migrate.init_app(app, models.db)

jwt = JWTManager(app)

def is_token_blacklisted(jti):
    _json, _status = AuthServiceApi.is_token_blacklisted({'jti': jti})
    if _status:
        return _json.get('blacklisted', False)
    return False

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return is_token_blacklisted(jti)

from routes import report_bp
app.register_blueprint(report_bp, url_prefix='/report')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
