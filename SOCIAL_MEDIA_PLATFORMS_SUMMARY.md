# 🚀 Sosyal Medya Platform Entegrasyonları - Özet

Bu doküman, tüm sosyal medya platformları için API entegrasyonlarını ve kullanımını özetler.

## ✅ Tamamlanan Özellikler

### 1. Platform Uploader Modülleri
- ✅ `src/platform_uploaders.py` - Tüm platformlar için uploader sınıfları
- ✅ Instagram Graph API entegrasyonu
- ✅ Facebook Graph API entegrasyonu
- ✅ TikTok Creative API entegrasyonu
- ✅ Spotify for Creators API entegrasyonu (podcast video)

### 2. Dosya Türü ve Format Desteği
- ✅ Platform bazlı format kontrolü
- ✅ Otomatik format doğrulama
- ✅ Video gereksinimleri kontrolü (çözünürlük, süre, boyut)
- ✅ Format spesifikasyonları (her platform için)

### 3. Sosyal Medya Uploader Uygulaması
- ✅ Platform API ayarları penceresi
- ✅ Her platform için ayrı credentials yönetimi
- ✅ Platform bazlı video yükleme
- ✅ Otomatik metadata uygulama

## 📱 Desteklenen Platformlar

### YouTube ✅ (Tam Destek)
- **Durum**: Tam çalışıyor
- **API**: YouTube Data API v3
- **Özellikler**:
  - Otomatik video yükleme
  - Duplicate kontrolü
  - Dil tespiti
  - Made for Kids: No ayarı
  - Copyright notice
  - Çok dilli açıklama

### Instagram 🔄 (API Gerekli)
- **Durum**: Kod hazır, API credentials gerekli
- **API**: Instagram Graph API (Facebook üzerinden)
- **Özellikler**:
  - Reels yükleme (1080x1920, 9:16)
  - Post yükleme (1080x1080, 1:1)
  - Otomatik format kontrolü
- **Gereksinimler**:
  - Facebook Developer hesabı
  - Instagram Business Account
  - Facebook Page (Instagram ile bağlı)
  - Access Token ve Instagram Account ID

### Facebook 🔄 (API Gerekli)
- **Durum**: Kod hazır, API credentials gerekli
- **API**: Facebook Graph API
- **Özellikler**:
  - Video yükleme (min 1280x720, 16:9)
  - Page veya kişisel profil desteği
  - Otomatik format kontrolü
- **Gereksinimler**:
  - Facebook Developer hesabı
  - Access Token
  - Page ID (opsiyonel)

### TikTok 🔄 (API Gerekli)
- **Durum**: Kod hazır, API credentials gerekli
- **API**: TikTok Creative API
- **Özellikler**:
  - Video yükleme (1080x1920, 9:16)
  - Otomatik format kontrolü
- **Gereksinimler**:
  - TikTok Developer hesabı
  - TikTok Business Account
  - Access Token, App ID, App Secret

### Spotify ⚠️ (Sınırlı Destek)
- **Durum**: Sadece podcast video için
- **API**: Spotify Web API
- **Özellikler**:
  - Podcast episode'larına video ekleme
  - ⚠️ Müzik yükleme için distributor gerekli (API ile mümkün değil)
- **Gereksinimler**:
  - Spotify Developer hesabı
  - Spotify for Creators hesabı
  - Access Token
  - Episode ID

## 📁 Dosya Türü Desteği

### Video Formatları

| Platform | Format | Çözünürlük | Aspect Ratio | Max Süre | Max Boyut |
|----------|--------|------------|--------------|----------|-----------|
| YouTube | MP4, MOV, AVI | 1920x1080 | 16:9 | Sınırsız | 256 GB |
| Instagram Reels | MP4, MOV | 1080x1920 | 9:16 | 90 saniye | 100 MB |
| Instagram Post | MP4, MOV | 1080x1080 | 1:1 | 60 saniye | 100 MB |
| Facebook | MP4, MOV | Min 1280x720 | 16:9 | 240 saniye | 1 GB |
| TikTok | MP4, MOV | 1080x1920 | 9:16 | 60 saniye | 287 MB |
| Spotify Podcast | MP4, MOV | 1920x1080 | 16:9 | 3600 saniye | 500 MB |

### Otomatik Format Kontrolü

Sistem otomatik olarak:
- ✅ Dosya formatını kontrol eder (MP4, MOV)
- ✅ Çözünürlüğü kontrol eder
- ✅ Süreyi kontrol eder
- ✅ Boyutu kontrol eder
- ⚠️ Uygun değilse uyarı verir

## 🚀 Kullanım

### 1. API Credentials Ayarlama

Her platform için API credentials gerekli:

1. **Platform API Kurulum Rehberi'ni okuyun**: `PLATFORM_API_SETUP.md`
2. **API credentials alın**:
   - Instagram: Facebook Developer Console
   - Facebook: Facebook Developer Console
   - TikTok: TikTok Developer Portal
   - Spotify: Spotify Developer Portal
3. **Uygulamada API Ayarları'na gidin**:
   - "API Ayarları" butonuna tıklayın
   - Her platform için credentials girin
   - Kaydedin

### 2. Video Yükleme

1. **Masaüstü uygulamasını açın**:
   ```bash
   python src/social_media_uploader.py
   ```

2. **Dosyaları seçin**:
   - Müzik dosyası
   - Görsel dosyası (opsiyonel)
   - Video dosyası (opsiyonel, yoksa otomatik oluşturulur)

3. **Metadata'yı doldurun**:
   - "Metadata'yı Doldur (Müzikten)" butonuna tıklayın
   - Otomatik olarak doldurulur

4. **Platform seçin**:
   - YouTube ✅
   - Instagram 🔄
   - Facebook 🔄
   - TikTok 🔄
   - Spotify ⚠️

5. **API'ye bağlanın** (YouTube için):
   - "Bağlan" butonuna tıklayın
   - Tarayıcıda giriş yapın

6. **Yükle**:
   - "Yükle" butonuna tıklayın
   - Sistem otomatik olarak yükler

## 📚 Dokümantasyon

### Ana Rehberler
- `PLATFORM_API_SETUP.md` - API kurulum rehberi
- `PLATFORM_FILE_FORMATS.md` - Dosya formatları ve gereksinimler
- `SOCIAL_MEDIA_AUTO_UPLOAD_GUIDE.md` - Otomatik yükleme rehberi
- `EXISTING_VIDEOS_UPDATE_GUIDE.md` - Mevcut videoları güncelleme

### Kod Dosyaları
- `src/platform_uploaders.py` - Platform uploader sınıfları
- `src/social_media_uploader.py` - Masaüstü uygulaması
- `src/youtube_upload.py` - YouTube upload modülü

## 🔧 Teknik Detaylar

### Platform Uploader Sınıfları

```python
# Instagram
from src.platform_uploaders import InstagramUploader
uploader = InstagramUploader(access_token, instagram_account_id)
reel_id = uploader.upload_reel(video_file, caption)

# Facebook
from src.platform_uploaders import FacebookUploader
uploader = FacebookUploader(access_token, page_id)
video_id = uploader.upload_video(video_file, title, description)

# TikTok
from src.platform_uploaders import TikTokUploader
uploader = TikTokUploader(access_token, app_id, app_secret)
video_id = uploader.upload_video(video_file, title, description)

# Spotify
from src.platform_uploaders import SpotifyUploader
uploader = SpotifyUploader(access_token)
success = uploader.upload_podcast_video(video_file, episode_id, title, description)
```

### Format Kontrolü

```python
from src.platform_uploaders import get_platform_specs

specs = get_platform_specs('instagram')
# {'reels': {...}, 'post': {...}}
```

## ⚠️ Önemli Notlar

### Spotify Müzik Yükleme

⚠️ **Spotify'a müzik yüklemek için doğrudan API desteği yoktur!**

Müzik yüklemek için bir **müzik distributor** kullanmanız gerekir:
- DistroKid
- CD Baby
- TuneCore
- Ditto Music

Bu distributor'lar Spotify, Apple Music, Amazon Music gibi platformlara otomatik olarak müzik dağıtır.

### API Limitleri

Her platformun rate limit'i vardır:
- **Instagram**: Günlük limit
- **Facebook**: Saatlik limit
- **TikTok**: Günlük limit
- **YouTube**: Günlük limit (10,000 units)

Toplu yükleme yaparken limitlere dikkat edin.

### Güvenlik

- Access token'ları güvenli tutun
- `.env` dosyasında saklayın
- Git'e commit etmeyin
- Düzenli olarak yenileyin

## 🆘 Sorun Giderme

### "API credentials gerekli" Hatası

1. Platform API kurulum rehberini okuyun
2. API credentials alın
3. Uygulamada "API Ayarları"ndan girin

### "Format not supported" Hatası

1. Dosya formatını kontrol edin (MP4 veya MOV olmalı)
2. Platform gereksinimlerine uygun format kullanın
3. Gerekirse FFmpeg ile dönüştürün

### "Video too large" Hatası

1. Dosya boyutunu kontrol edin
2. Platform max boyut limitine uyun
3. Compression kullanın

## 🔮 Gelecek Özellikler

1. **Otomatik Format Dönüştürme**
   - FFmpeg entegrasyonu
   - Platform gereksinimlerine göre otomatik dönüştürme

2. **Toplu Yükleme**
   - Birden fazla platforma aynı anda yükleme
   - Toplu format dönüştürme

3. **Video Optimizasyonu**
   - Platform bazlı otomatik optimizasyon
   - Thumbnail otomatik oluşturma

4. **Scheduling**
   - Zamanlanmış yükleme
   - Toplu yükleme planlama

## 📞 Destek

Sorularınız için:
- Dokümantasyonu kontrol edin
- GitHub Issues açın
- API dokümantasyonlarını okuyun

