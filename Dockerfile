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
```

**Penjelasan Dockerfile**:
- `FROM` - Base image yang digunakan
- `WORKDIR` - Set direktori kerja
- `COPY` - Copy file dari host ke container
- `RUN` - Jalankan perintah saat build
- `EXPOSE` - Informasikan port yang digunakan
- `CMD` - Perintah default saat container dijalankan

### Step 8: Buat File Requirements

Buat file `requirements.txt`:
```
Flask==3.0.0