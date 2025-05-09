import models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)

models.init_app(app)
migrate.init_app(app, models.db)

from routes import report_bp
app.register_blueprint(report_bp, url_prefix='/report')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
