# Gunakan image Python 3.9 slim sebagai base image
FROM python:3.9-slim

# Update dan upgrade package
RUN apt-get update && apt-get upgrade -y

# Buat user dan group
RUN groupadd appgroup && useradd -u 10001 -g appgroup appuser

# Set workdir
WORKDIR /app

# Saln file environment
COPY app/requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Ubah kepemilikan file & folder workdir
RUN chown -R appuser:appgroup .

# Jalankan aplikasi sebagai user non-root
USER appuser
CMD gunicorn -b 0.0.0.0:${APP_PORT} app:app
