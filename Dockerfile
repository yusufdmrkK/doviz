# Temel Python imajını kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimleri kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uygulamanın dinleyeceği portu belirle
EXPOSE 5000

# Uygulamayı çalıştır
# Flask'ın yerleşik sunucusunu kullanıyoruz
CMD ["python", "app.py"]
