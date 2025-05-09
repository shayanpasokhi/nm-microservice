FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask Flask-JWT-Extended Flask-SQLAlchemy Flask-Migrate Werkzeug requests marshmallow

EXPOSE 5004

CMD ["python", "app.py"]
