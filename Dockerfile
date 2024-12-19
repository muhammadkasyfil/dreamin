# Menggunakan Python sebagai base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Salin file requirements.txt dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port untuk server Django
EXPOSE 8000

# Jalankan server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]