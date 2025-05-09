FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir Flask requests marshmallow

EXPOSE 5005

CMD ["python", "app.py"]
