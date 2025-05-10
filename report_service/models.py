from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, nullable=False)
    is_infected = db.Column(db.Boolean, nullable=True)
    scanner = db.Column(db.String(64), nullable=False)
    result = db.Column(db.Text)
    user_id = db.Column(db.Integer, nullable=True)
    scanned_at = db.Column(db.DateTime, nullable=True)
