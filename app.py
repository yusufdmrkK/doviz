import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

# API ayarları
# ************ DİKKAT ************
# API_KEY yerine aldığınız anahtarı (key) girin.
# Genellikle ücretsiz API'lerde bu key'in kod içinde olması sorun olmaz,
# ancak büyük projelerde bu, ortam değişkenlerinden çekilmelidir (os.environ).
API_KEY = "YOUR_EXCHANGERATE_API_KEY"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

@app.route('/')
def home():
    """Ana sayfa: USD bazlı döviz kurlarını API'den çeker ve gösterir."""
    
    # API'ye istek gönderme
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Hatalı durum kodları için istisna fırlatır
        data = response.json()
        
        # 'conversion_rates' verisini alma
        if data.get('result') == 'success':
            rates = data['conversion_rates']
            # Göstermek için sadece birkaç önemli kuru seçelim
            selected_rates = {
                'EUR': rates.get('EUR', 'N/A'),
                'TRY': rates.get('TRY', 'N/A'),
                'GBP': rates.get('GBP', 'N/A'),
                'JPY': rates.get('JPY', 'N/A')
            }
            # selected_rates verisini HTML şablonuna gönderiyoruz
            return render_template('index.html', rates=selected_rates, base_currency="USD")
        else:
            return render_template('error.html', message="API'dan başarılı yanıt alınamadı."), 500

    except requests.exceptions.RequestException as e:
        # Ağ veya istek hatalarını yakalama
        print(f"Hata oluştu: {e}")
        return render_template('error.html', message=f"API'ye bağlanırken hata oluştu: {e}"), 500
    except Exception as e:
        # Diğer beklenmedik hataları yakalama
        print(f"Beklenmedik bir hata oluştu: {e}")
        return render_template('error.html', message=f"Beklenmedik bir hata oluştu: {e}"), 500

if __name__ == '__main__':
    # Flask uygulamasını çalıştırma (yerel test için)
    # Bulut bilişim ortamlarında Gunicorn gibi sunucular kullanılır,
    # ancak Docker ile çalıştırırken sadece bu yeterli olacaktır.
    app.run(host='0.0.0.0', port=5000)
