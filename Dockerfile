FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py migrate
EXPOSE 8000
CMD gunicorn djangoProject2.wsgi --bind 0.0.0.0:$PORT