FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Create static directory first
RUN mkdir -p staticfiles

# Copy the project files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=dreamin.settings

# Collect static files
RUN python manage.py collectstatic --noinput

ENV PORT=8000

RUN python manage.py collectstatic --noinput

CMD gunicorn dreamin.wsgi:application --bind 0.0.0.0:$PORT