from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from tasks import scanner_bp
app.register_blueprint(scanner_bp, url_prefix='/scan')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
