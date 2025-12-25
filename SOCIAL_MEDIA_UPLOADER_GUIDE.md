# Neural Beats Studio - Social Media Uploader Kullanım Kılavuzu

## Genel Bakış

Bu masa üstü uygulaması, müzik içeriklerinizi otomatik olarak çeşitli sosyal medya platformlarına yüklemenizi sağlar.

## Kurulum

### 1. Gerekli Paketler

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. YouTube API Kurulumu

YouTube için API kurulumu gereklidir:

1. Google Cloud Console'da proje oluşturun
2. YouTube Data API v3'ü etkinleştirin
3. OAuth 2.0 credentials oluşturun
4. `credentials.json` dosyasını indirin ve proje klasörüne koyun

Detaylı kurulum için: `YOUTUBE_API_SETUP.md`

## Kullanım

### Uygulamayı Başlatma

```bash
python run_uploader.py
```

veya

```bash
python src/social_media_uploader.py
```

### Adım Adım Kullanım

1. **Dosya Seçimi**
   - **Müzik Dosyası**: Yüklenecek müzik dosyasını seçin (MP3, WAV, M4A)
   - **Görsel Dosyası**: Video thumbnail veya görsel seçin (JPG, PNG)
   - **Video Dosyası (Opsiyonel)**: Hazır video varsa seçin, yoksa müzik + görsel'den otomatik oluşturulur

2. **Metadata Doldurma**
   - Manuel olarak doldurun VEYA
   - "Metadata'yı Doldur (Müzikten)" butonuna tıklayın (otomatik doldurur)

3. **Platform Seçimi**
   - Yüklemek istediğiniz platformları işaretleyin:
     - ✅ YouTube
     - ✅ Instagram
     - ✅ Facebook
     - ✅ TikTok
     - ✅ Spotify

4. **Ayarlar**
   - **Gizlilik**: private, unlisted, veya public seçin
   - **YouTube API**: "Bağlan" butonuna tıklayarak YouTube API'ye bağlanın

5. **Yükleme**
   - "Yükle" butonuna tıklayın
   - İlerleme log alanında görüntülenecektir

## Özellikler

### ✅ Tamamlanan Özellikler

- **YouTube Upload**
  - ✅ Otomatik video yükleme
  - ✅ Duplicate kontrolü (aynı başlıklı video varsa yüklemez)
  - ✅ Dil tespiti (şarkı adına göre: Türkçe, Rusça, Korece, İngilizce)
  - ✅ "Not made for kids" ayarı
  - ✅ Copyright notice otomatik ekleme
  - ✅ Thumbnail yükleme
  - ✅ Metadata otomatik doldurma

### 🚧 Geliştirme Aşamasında

- **Instagram Upload**: Instagram Graph API entegrasyonu gerekli
- **Facebook Upload**: Facebook Graph API entegrasyonu gerekli
- **TikTok Upload**: TikTok Creative API entegrasyonu gerekli
- **Spotify Upload**: Spotify for Artists API entegrasyonu gerekli

## YouTube Özellikleri Detayı

### Duplicate Kontrolü

Aynı başlıklı bir video zaten kanalınızda varsa, yeni yükleme yapılmaz ve log'da "SKIP" mesajı görünür.

### Dil Tespiti

Şarkı başlığına göre otomatik dil tespiti:
- **Türkçe**: Türkçe karakterler (ç, ğ, ı, ö, ş, ü) varsa
- **Rusça**: Kiril karakterler varsa
- **Korece**: Korece karakterler varsa
- **İngilizce**: Varsayılan (global)

### Metadata

Otomatik olarak eklenen metadata:
- Başlık: Müzik dosyası adı
- Açıklama: "Generated music by Neural Beats Studio" + Copyright notice
- Etiketler: music, generated music, neural beats studio
- Kategori: Music (10)
- Dil: Otomatik tespit edilen dil

## Sorun Giderme

### YouTube API Bağlantı Hatası

1. `credentials.json` dosyasının doğru yerde olduğundan emin olun
2. YouTube Data API v3'ün etkin olduğunu kontrol edin
3. OAuth consent screen'in yapılandırıldığını kontrol edin

### Video Dosyası Bulunamadı

- Video dosyası seçin VEYA
- Müzik + Görsel dosyalarını seçin (otomatik video oluşturulacak)

### Import Hatası

Gerekli paketlerin yüklü olduğundan emin olun:
```bash
pip install -r requirements.txt
```

## Notlar

- YouTube için API kurulumu zorunludur
- Diğer platformlar için API entegrasyonları gelecekte eklenecektir
- Tüm yüklemeler log alanında görüntülenir
- Yükleme işlemleri arka planda çalışır (uygulama donmaz)

## Destek

Sorunlar için:
- Log alanını kontrol edin
- `YOUTUBE_API_SETUP.md` dosyasına bakın
- YouTube API kurulumunu doğrulayın

