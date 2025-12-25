# 📱 Sosyal Medya Platform API Kurulum Rehberi

Bu rehber, Instagram, Facebook, TikTok ve Spotify API'lerinin kurulumunu ve kullanımını açıklar.

## 📋 İçindekiler

1. [Instagram Graph API](#instagram-graph-api)
2. [Facebook Graph API](#facebook-graph-api)
3. [TikTok Creative API](#tiktok-creative-api)
4. [Spotify for Creators API](#spotify-for-creators-api)
5. [Dosya Türü ve Format Gereksinimleri](#dosya-türü-ve-format-gereksinimleri)

---

## 📸 Instagram Graph API

### Gereksinimler

- Facebook Developer hesabı
- Instagram Business Account
- Facebook Page (Instagram Business Account ile bağlı)

### Kurulum Adımları

1. **Facebook Developer Console'a gidin**
   - https://developers.facebook.com/
   - Giriş yapın veya hesap oluşturun

2. **Yeni Uygulama Oluşturun**
   - "My Apps" → "Create App"
   - App türü: "Business"
   - App adı ve contact email girin

3. **Instagram Basic Display veya Instagram Graph API Ekle**
   - App Dashboard → "Add Product"
   - "Instagram" seçin
   - "Instagram Graph API" seçin

4. **Gerekli İzinleri Ekleyin**
   - App Dashboard → Settings → Basic
   - "Add Platform" → "Website"
   - Site URL ekleyin
   - App Review → Permissions and Features
   - Gerekli izinler:
     - `instagram_basic`
     - `instagram_content_publish`
     - `pages_read_engagement`
     - `pages_show_list`

5. **Access Token Alın**
   - Tools → Graph API Explorer
   - App seçin
   - Permissions ekleyin
   - "Generate Access Token" tıklayın
   - Long-lived token için: Tools → Access Token Tool

6. **Instagram Business Account ID Bulun**
   - Graph API Explorer'da: `GET /me/accounts`
   - Page ID'yi bulun
   - `GET /{page-id}?fields=instagram_business_account`
   - Instagram Business Account ID'yi kaydedin

### Kullanım

```python
from src.platform_uploaders import InstagramUploader

# Access token ve Instagram Account ID
access_token = "YOUR_ACCESS_TOKEN"
instagram_account_id = "YOUR_INSTAGRAM_ACCOUNT_ID"

uploader = InstagramUploader(access_token, instagram_account_id)

# Reels yükle
reel_id = uploader.upload_reel(
    video_file="output/video.mp4",
    caption="🎵 My Song\n\n#AIMusic #NeuralBeatsStudio"
)
```

### Video Gereksinimleri

- **Format**: MP4, MOV
- **Reels**: 1080x1920 (9:16), max 90 saniye
- **Post**: 1080x1080 (1:1), max 60 saniye
- **Max Boyut**: 100 MB

---

## 👥 Facebook Graph API

### Gereksinimler

- Facebook Developer hesabı
- Facebook Page (opsiyonel, kullanıcı hesabı için gerekli değil)

### Kurulum Adımları

1. **Facebook Developer Console'a gidin**
   - https://developers.facebook.com/
   - Giriş yapın

2. **Yeni Uygulama Oluşturun**
   - "My Apps" → "Create App"
   - App türü: "Business"
   - App adı ve contact email girin

3. **Facebook Login Ekle**
   - App Dashboard → "Add Product"
   - "Facebook Login" seçin
   - Settings → Valid OAuth Redirect URIs ekleyin

4. **Gerekli İzinleri Ekleyin**
   - App Review → Permissions and Features
   - Gerekli izinler:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_show_list`
     - `user_videos`

5. **Access Token Alın**
   - Tools → Graph API Explorer
   - App seçin
   - Permissions ekleyin
   - "Generate Access Token" tıklayın

6. **Page ID Bulun (Page için)**
   - Graph API Explorer'da: `GET /me/accounts`
   - Page ID'yi kaydedin

### Kullanım

```python
from src.platform_uploaders import FacebookUploader

# Access token ve Page ID (opsiyonel)
access_token = "YOUR_ACCESS_TOKEN"
page_id = "YOUR_PAGE_ID"  # None for user account

uploader = FacebookUploader(access_token, page_id)

# Video yükle
video_id = uploader.upload_video(
    video_file="output/video.mp4",
    title="My Song",
    description="🎵 Generated music by Neural Beats Studio",
    privacy="PUBLIC"
)
```

### Video Gereksinimleri

- **Format**: MP4, MOV
- **Çözünürlük**: Min 1280x720 (16:9)
- **Max Süre**: 240 saniye (4 dakika)
- **Max Boyut**: 1 GB

---

## 🎵 TikTok Creative API

### Gereksinimler

- TikTok Developer hesabı
- TikTok Business Account
- TikTok App oluşturulmuş olmalı

### Kurulum Adımları

1. **TikTok Developer Portal'a gidin**
   - https://developers.tiktok.com/
   - Giriş yapın veya hesap oluşturun

2. **Yeni Uygulama Oluşturun**
   - "My Apps" → "Create App"
   - App bilgilerini doldurun
   - App türü: "Video Upload"

3. **OAuth 2.0 Ayarları**
   - App Settings → OAuth 2.0
   - Redirect URI ekleyin
   - Scopes seçin:
     - `video.upload`
     - `video.publish`

4. **Access Token Alın**
   - OAuth 2.0 flow ile access token alın
   - Authorization code → Access token

5. **App ID ve App Secret Kaydedin**
   - App Settings → Basic Information
   - App ID ve App Secret'ı kaydedin

### Kullanım

```python
from src.platform_uploaders import TikTokUploader

# Access token, App ID ve App Secret
access_token = "YOUR_ACCESS_TOKEN"
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"

uploader = TikTokUploader(access_token, app_id, app_secret)

# Video yükle
video_id = uploader.upload_video(
    video_file="output/video.mp4",
    title="My Song",
    description="🎵 Generated music by Neural Beats Studio",
    privacy_level="PUBLIC_TO_EVERYONE"
)
```

### Video Gereksinimleri

- **Format**: MP4, MOV
- **Çözünürlük**: 1080x1920 (9:16)
- **Max Süre**: 60 saniye (bazı hesaplar için daha uzun)
- **Max Boyut**: ~287 MB

---

## 🎧 Spotify for Creators API

### Gereksinimler

- Spotify Developer hesabı
- Spotify for Creators hesabı
- Podcast oluşturulmuş olmalı

### Önemli Not

⚠️ **Spotify'a müzik yüklemek için doğrudan API desteği yoktur!**

Müzik yüklemek için bir **müzik distributor** kullanmanız gerekir:
- DistroKid (https://distrokid.com/)
- CD Baby (https://cdbaby.com/)
- TuneCore (https://www.tunecore.com/)
- Ditto Music (https://www.dittomusic.com/)

Bu distributor'lar Spotify, Apple Music, Amazon Music gibi platformlara otomatik olarak müzik dağıtır.

### Podcast Video Yükleme

Spotify API sadece **podcast episode'larına video eklemek** için kullanılabilir.

### Kurulum Adımları

1. **Spotify Developer Portal'a gidin**
   - https://developer.spotify.com/
   - Giriş yapın

2. **Yeni Uygulama Oluşturun**
   - Dashboard → "Create an App"
   - App bilgilerini doldurun
   - Redirect URI ekleyin

3. **OAuth 2.0 Ayarları**
   - App Settings → OAuth 2.0
   - Scopes seçin:
     - `user-read-email`
     - `user-library-read`
     - `user-library-modify`
     - `user-modify-playback-state`

4. **Access Token Alın**
   - OAuth 2.0 flow ile access token alın

### Kullanım (Podcast Video)

```python
from src.platform_uploaders import SpotifyUploader

# Access token
access_token = "YOUR_ACCESS_TOKEN"

uploader = SpotifyUploader(access_token)

# Podcast episode'una video ekle
success = uploader.upload_podcast_video(
    video_file="output/video.mp4",
    episode_id="YOUR_EPISODE_ID",
    title="My Song",
    description="🎵 Generated music by Neural Beats Studio"
)
```

### Video Gereksinimleri (Podcast)

- **Format**: MP4, MOV
- **Çözünürlük**: 1920x1080 (16:9)
- **Max Süre**: 3600 saniye (1 saat)
- **Max Boyut**: 500 MB

---

## 📁 Dosya Türü ve Format Gereksinimleri

### Platform Karşılaştırması

| Platform | Format | Çözünürlük | Max Süre | Max Boyut |
|----------|--------|------------|----------|-----------|
| **Instagram Reels** | MP4, MOV | 1080x1920 (9:16) | 90 saniye | 100 MB |
| **Instagram Post** | MP4, MOV | 1080x1080 (1:1) | 60 saniye | 100 MB |
| **Facebook** | MP4, MOV | Min 1280x720 (16:9) | 240 saniye | 1 GB |
| **TikTok** | MP4, MOV | 1080x1920 (9:16) | 60 saniye | 287 MB |
| **Spotify Podcast** | MP4, MOV | 1920x1080 (16:9) | 3600 saniye | 500 MB |
| **YouTube** | MP4, MOV, AVI | 1920x1080 (16:9) | Sınırsız | 256 GB |

### Otomatik Format Dönüştürme

Sistem, platform gereksinimlerine göre otomatik format dönüştürme yapabilir (FFmpeg gerekli):

```python
# Örnek: Instagram Reels için video dönüştürme
# 1080x1920 (9:16) formatına dönüştür
```

### Dosya Türü Kontrolü

Sistem otomatik olarak:
- Dosya formatını kontrol eder
- Platform gereksinimlerine uygunluğunu kontrol eder
- Uygun değilse uyarı verir

---

## 🔐 Güvenlik Notları

1. **Access Token'ları Güvenli Tutun**
   - Token'ları `.env` dosyasında saklayın
   - Git'e commit etmeyin
   - Düzenli olarak yenileyin

2. **API Limitlerine Dikkat Edin**
   - Her platformun rate limit'i vardır
   - Toplu yükleme yaparken limitlere dikkat edin

3. **İzinleri Minimum Tutun**
   - Sadece gerekli izinleri isteyin
   - Gereksiz izinler güvenlik riski oluşturur

---

## 🆘 Sorun Giderme

### Instagram

- **"Invalid access token"**: Token'ı yenileyin
- **"Missing permissions"**: App Review'dan gerekli izinleri onaylatın
- **"Video format not supported"**: 1080x1920 (9:16) veya 1080x1080 (1:1) kullanın

### Facebook

- **"Invalid OAuth access token"**: Token'ı yenileyin
- **"Insufficient permissions"**: Page için `pages_manage_posts` izni gerekli

### TikTok

- **"Invalid access token"**: OAuth 2.0 flow'u tekrar çalıştırın
- **"Video too large"**: 287 MB'dan küçük dosya kullanın

### Spotify

- **"Episode not found"**: Episode ID'yi kontrol edin
- **"Music upload not supported"**: Müzik için distributor kullanın

---

## 📚 Ek Kaynaklar

- [Instagram Graph API Docs](https://developers.facebook.com/docs/instagram-api)
- [Facebook Graph API Docs](https://developers.facebook.com/docs/graph-api)
- [TikTok Creative API Docs](https://developers.tiktok.com/doc/creative-api-overview)
- [Spotify Web API Docs](https://developer.spotify.com/documentation/web-api)

