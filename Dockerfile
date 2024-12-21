FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=dreamin.settings
ENV PORT=8000

CMD gunicorn dreamin.wsgi:application --bind 0.0.0.0:$PORT