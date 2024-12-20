FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

# Create necessary directories
RUN mkdir -p staticfiles/admin

# Copy the project files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=dreamin.settings

# Collect static files with --clear to ensure clean collection
RUN python manage.py collectstatic --noinput --clear

ENV PORT=8000

RUN python manage.py collectstatic --noinput

CMD gunicorn dreamin.wsgi:application --bind 0.0.0.0:$PORT