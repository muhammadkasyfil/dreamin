FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

RUN python manage.py collectstatic --noinput

CMD gunicorn dreamin.wsgi:application --bind 0.0.0.0:$PORT