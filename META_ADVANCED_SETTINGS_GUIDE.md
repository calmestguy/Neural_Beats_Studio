# Meta Developers Advanced Settings Rehberi - Neural Beats Studio

**Last Updated:** December 26, 2024

## 📋 Genel Bakış

Neural Beats Studio **tamamen lokal bir desktop uygulamasıdır**. Tüm veriler kullanıcının cihazında saklanır, sunucuda veri saklanmaz. Bu nedenle, Meta'nın Data Deletion Callback URL gereksinimleri bizim durumumuz için farklıdır.

## 🔍 Advanced Settings'teki Önemli Bölümler

### 1. App Authentication

**"Native or desktop app?" Toggle:**
- ✅ **AÇIK** (ON) - Doğru ayar
- Bu, uygulamanın desktop uygulaması olduğunu belirtir

**"Authorize callback URL":**
- Bu alan **boş bırakılabilir** (lokal desktop uygulaması için)
- Veya OAuth callback için kullanılabilir (şu an gerekli değil)

### 2. Download User Identifiers

**Ne Yapmalı:**

Meta'nın mesajı:
> "To ensure compliance with applicable privacy laws and Section 3(d)(i) of the Platform Terms, please promptly review the list of either app-scoped or instant game IDs and delete all records of them from your database. If you would like to opt out of this requirement in the future, please implement a valid **Data Deletion Callback URL**."

**Bizim Durumumuz:**
- ✅ **Veritabanımız YOK** - Tüm veriler lokal cihazda
- ✅ **Sunucu YOK** - Veri saklamıyoruz
- ✅ **User ID saklamıyoruz** - Sadece OAuth token'lar lokal olarak saklanıyor

**Yapılacaklar:**
1. "Download" butonuna tıklayarak kullanıcı ID'lerini indirin (eğer varsa)
2. Kontrol edin: Eğer hiç kullanıcı ID'si yoksa, zaten uyumlusunuz
3. Eğer ID'ler varsa: Bu ID'ler sadece OAuth token'larda olabilir, lokal cihazda

### 3. Data Deletion Callback URL (Opsiyonel)

**Gerekli mi?**
- ❌ **HAYIR** - Lokal desktop uygulaması için gerekli değil
- ✅ **Alternatif**: Data Deletion Instructions URL yeterli

**Eğer Callback URL Eklemek İsterseniz:**

Meta'nın gereksinimleri:
- HTTPS protokolü kullanmalı
- POST isteği almalı
- Signed request'i parse etmeli
- JSON response döndürmeli: `{ "url": "<status_url>", "confirmation_code": "<code>" }`

**Bizim Durumumuz İçin:**
- Lokal uygulama olduğu için callback URL **gerekli değil**
- Basic Settings'teki "Data deletion instructions URL" yeterli
- Kullanıcılar verilerini lokal olarak silebilir

## ✅ Önerilen Ayarlar

### Advanced Settings'te:

1. **App Authentication:**
   - ✅ "Native or desktop app?" → **ON** (Açık)
   - "Authorize callback URL" → **Boş bırakılabilir**

2. **Download User Identifiers:**
   - "Download" butonuna tıklayın
   - Eğer dosya boşsa veya hiç ID yoksa → ✅ Uyumlusunuz
   - Eğer ID'ler varsa → Bu ID'ler sadece lokal OAuth token'larda

3. **Data Deletion:**
   - Basic Settings'te "Data deletion instructions URL" kullanın:
     ```
     https://raw.githubusercontent.com/calmestguy/Neural_Beats_Studio/master/DATA_DELETION.md
     ```
   - Callback URL **gerekli değil** (lokal uygulama)

## 📝 Önemli Notlar

### Neden Callback URL Gerekli Değil?

1. **Lokal Uygulama:**
   - Tüm veriler kullanıcının cihazında
   - Sunucuda veri saklanmıyor
   - Veritabanı yok

2. **OAuth Token'lar:**
   - Sadece lokal `token.json` dosyasında
   - Kullanıcı dosyayı silebilir
   - Platform ayarlarından erişim iptal edilebilir

3. **User ID'ler:**
   - Meta'dan gelen user ID'ler sadece OAuth token'larda
   - Sunucuda saklanmıyor
   - Kullanıcı token'ı sildiğinde ID de silinir

### Meta'nın Beklentileri

Meta, **sunucuda veri saklayan** uygulamalar için callback URL bekler. Bizim durumumuzda:
- ✅ Veri saklamıyoruz → Callback URL gerekli değil
- ✅ Instructions URL yeterli → DATA_DELETION.md
- ✅ Kullanıcılar lokal olarak verilerini silebilir

## 🔧 Eğer Callback URL Eklemek İsterseniz

**Gereksinimler:**
1. HTTPS web sunucusu
2. POST endpoint
3. Signed request parsing
4. JSON response

**Örnek Endpoint (Python Flask):**
```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import json

app = Flask(__name__)

@app.route('/data-deletion-callback', methods=['POST'])
def data_deletion_callback():
    signed_request = request.form.get('signed_request')
    
    # Parse signed request
    encoded_sig, payload = signed_request.split('.', 1)
    app_secret = "YOUR_APP_SECRET"
    
    # Verify signature
    sig = base64.urlsafe_b64decode(encoded_sig + '==')
    expected_sig = hmac.new(
        app_secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).digest()
    
    if sig != expected_sig:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Parse payload
    data = json.loads(base64.urlsafe_b64decode(payload + '=='))
    user_id = data.get('user_id')
    
    # Delete user data (bizim durumumuzda: lokal, yapılacak bir şey yok)
    # Çünkü veri saklamıyoruz
    
    # Return response
    confirmation_code = f"DEL_{user_id}_{int(time.time())}"
    status_url = "https://github.com/calmestguy/Neural_Beats_Studio/blob/master/DATA_DELETION.md"
    
    return jsonify({
        'url': status_url,
        'confirmation_code': confirmation_code
    })

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # HTTPS için
```

**Ancak:** Lokal uygulama olduğu için bu **gerekli değil**.

## ✅ Sonuç

**Advanced Settings için:**
1. ✅ "Native or desktop app?" → ON
2. ✅ "Download User Identifiers" → İndirin ve kontrol edin (muhtemelen boş)
3. ✅ Basic Settings'te "Data deletion instructions URL" kullanın
4. ❌ Callback URL **gerekli değil** (lokal uygulama)

**Meta'ya Açıklama:**
- Uygulama tamamen lokal
- Veri saklamıyoruz
- Instructions URL yeterli
- Kullanıcılar lokal olarak verilerini silebilir

---

**İletişim:**
- Email: neuralbeats20@gmail.com
- GitHub: https://github.com/calmestguy/Neural_Beats_Studio

