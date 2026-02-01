# Gunakan image Python official
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file aplikasi
COPY app/ ./app/

# Expose port 5000
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app/app.py"]
