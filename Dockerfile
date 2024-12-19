FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a simple entrypoint script
RUN echo '#!/bin/bash\n\
echo "Waiting for postgres..."\n\
sleep 5\n\
python manage.py migrate\n\
python manage.py runserver 0.0.0.0:8000' > /entrypoint.sh && \
chmod +x /entrypoint.sh

EXPOSE 8000

CMD ["/entrypoint.sh"]