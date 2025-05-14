FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask Flask-JWT-Extended Flask-SQLAlchemy Flask-Migrate Werkzeug requests marshmallow flask-cors

EXPOSE 5001

CMD ["python", "app.py"]
