FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media/animations media/sounds media/dialogues

# Collect static files
RUN python manage.py collectstatic --noinput

ENV PORT=8000

RUN python manage.py collectstatic --noinput

CMD gunicorn dreamin.wsgi:application --bind 0.0.0.0:$PORT