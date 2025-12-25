# 🚀 YouTube API Kurulum Rehberi - Adım Adım

## 📋 Genel Bakış

Bu rehber, YouTube Data API v3'ü kullanarak videolarınızı otomatik olarak YouTube'a yüklemeniz için gerekli tüm adımları içerir.

**Kanal Bilgileri:**
- **Kanal**: Neural Beats Studio
- **Handle**: @NBS-NeuralBeatsStudio
- **Kanal ID**: UCBBEdistMgv1qONZMsvOa8Q
- **Kanal URL**: https://studio.youtube.com/channel/UCBBEdistMgv1qONZMsvOa8Q

---

## 🔐 Adım 1: Google Cloud Console'da Proje Oluştur

### 1.1. Google Cloud Console'a Git

1. **Tarayıcıda aç**: https://console.cloud.google.com/
2. **Google hesabınızla giriş yapın** (YouTube kanalınızla aynı hesap)

### 1.2. Yeni Proje Oluştur

1. Üst menüden **"Select a project"** dropdown'ına tıklayın
2. **"NEW PROJECT"** butonuna tıklayın
3. **Project name**: `Neural Beats Studio YouTube Uploader` (veya istediğiniz isim)
4. **"CREATE"** butonuna tıklayın
5. Proje oluşturulduktan sonra, dropdown'dan yeni projeyi **seçin**

---

## 📡 Adım 2: YouTube Data API v3'ü Etkinleştir

### 2.1. API Library'ye Git

1. Sol menüden **"APIs & Services"** → **"Library"** seçin
2. Veya direkt link: https://console.cloud.google.com/apis/library

### 2.2. YouTube Data API v3'ü Bul ve Etkinleştir

1. Arama kutusuna **"YouTube Data API v3"** yazın
2. **"YouTube Data API v3"** sonucuna tıklayın
3. **"ENABLE"** butonuna tıklayın
4. API etkinleştirildiğinde **"API enabled"** mesajı görünecek

**Not**: API etkinleştirme birkaç saniye sürebilir.

---

## 🔑 Adım 3: OAuth Consent Screen Ayarla

### 3.1. OAuth Consent Screen Sayfasına Git

1. Sol menüden **"APIs & Services"** → **"OAuth consent screen"** seçin
2. Veya direkt link: https://console.cloud.google.com/apis/credentials/consent

### 3.2. User Type Seç

1. **"External"** seçin (kişisel kullanım için)
2. **"CREATE"** butonuna tıklayın

### 3.3. App Bilgilerini Doldur

**App information:**
- **App name**: `Neural Beats Studio`
- **User support email**: YouTube kanalınızla aynı e-posta
- **App logo**: (Opsiyonel - şimdilik atlayabilirsiniz)
- **App domain**: (Opsiyonel - şimdilik atlayabilirsiniz)
- **Developer contact information**: YouTube kanalınızla aynı e-posta

**"SAVE AND CONTINUE"** butonuna tıklayın

### 3.4. Scopes (İzinler)

1. **"ADD OR REMOVE SCOPES"** butonuna tıklayın
2. **"YouTube Data API v3"** bölümünü genişletin
3. Şu scope'ları seçin:
   - ✅ `https://www.googleapis.com/auth/youtube.upload` (Upload videos)
   - ✅ `https://www.googleapis.com/auth/youtube` (Manage your YouTube account)
4. **"UPDATE"** butonuna tıklayın
5. **"SAVE AND CONTINUE"** butonuna tıklayın

### 3.5. Test Users (Test Kullanıcıları)

**ÖNEMLİ**: İlk kullanımda "Testing" modunda olacaksınız. Bu modda sadece test kullanıcıları video yükleyebilir.

1. **"ADD USERS"** butonuna tıklayın
2. **YouTube kanalınızla aynı Google e-posta adresinizi** ekleyin
3. **"ADD"** butonuna tıklayın
4. **"SAVE AND CONTINUE"** butonuna tıklayın

### 3.6. Summary (Özet)

1. Tüm bilgileri kontrol edin
2. **"BACK TO DASHBOARD"** butonuna tıklayın

**Not**: İleride "Publish" yaparak herkese açık hale getirebilirsiniz, ancak şimdilik test modu yeterli.

---

## 🔐 Adım 4: OAuth 2.0 Credentials Oluştur

### 4.1. Credentials Sayfasına Git

1. Sol menüden **"APIs & Services"** → **"Credentials"** seçin
2. Veya direkt link: https://console.cloud.google.com/apis/credentials

### 4.2. OAuth Client ID Oluştur

1. Üstte **"+ CREATE CREDENTIALS"** butonuna tıklayın
2. **"OAuth client ID"** seçin

### 4.3. Application Type Seç

1. **"Application type"**: **"Desktop app"** seçin
2. **"Name"**: `Neural Beats Studio YouTube Uploader` (veya istediğiniz isim)
3. **"CREATE"** butonuna tıklayın

### 4.4. Credentials İndir

1. Bir popup açılacak ve **Client ID** ve **Client secret** gösterilecek
2. **"DOWNLOAD JSON"** butonuna tıklayın
3. İndirilen dosyayı **`credentials.json`** olarak kaydedin
4. Dosyayı **proje kök dizinine** koyun: `C:\Users\Haluk\New_Project\AI_Music\credentials.json`

**ÖNEMLİ**: 
- `credentials.json` dosyasını **asla paylaşmayın** veya GitHub'a yüklemeyin
- Bu dosya sizin YouTube kanalınıza erişim sağlar

### 4.5. Popup'ı Kapat

1. **"OK"** butonuna tıklayın (popup'ı kapatır)

---

## ✅ Adım 5: Kurulumu Test Et

### 5.1. Paketleri Yükle (Eğer yüklü değilse)

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 5.2. İlk Authentication (İlk Kullanım)

```bash
python src/youtube_upload.py --video-dir output/youtube --privacy private
```

**Ne olacak:**
1. Script çalışacak
2. Tarayıcı otomatik açılacak
3. Google hesabınızla giriş yapmanız istenecek
4. İzinleri onaylayın (YouTube kanalınıza erişim)
5. **"token.json"** dosyası otomatik oluşturulacak
6. Artık sonraki kullanımlarda otomatik giriş yapacak

**Not**: İlk kullanımda "This app isn't verified" uyarısı görebilirsiniz. Bu normaldir (test modunda). **"Advanced"** → **"Go to Neural Beats Studio (unsafe)"** tıklayın.

---

## 🎬 Adım 6: Videoları Yükle

### 6.1. Tek Video Yükle (Test)

```bash
python src/youtube_upload.py \
  --video output/youtube/video_adi_youtube.mp4 \
  --title "Video Başlığı" \
  --privacy private
```

### 6.2. Toplu Yükleme (17 Video)

```bash
python src/youtube_upload.py \
  --video-dir output/youtube \
  --music-dir "D:\Neutral Beats Studio" \
  --privacy private \
  --category 10
```

**Ne olacak:**
- Tüm videoları bulur
- Müzik dosyalarından metadata çıkarır (başlık, açıklama, etiketler)
- Her videoyu sırayla YouTube'a yükler
- Yükleme ilerlemesini gösterir
- Video ID'lerini ve URL'lerini gösterir

### 6.3. Gizlilik Durumları

- **`private`**: Sadece siz görebilirsiniz (test için önerilen)
- **`unlisted`**: Linki olanlar görebilir
- **`public`**: Herkes görebilir (yayın için)

---

## 📊 Adım 7: YouTube Studio'da Kontrol Et

### 7.1. YouTube Studio'ya Git

1. **YouTube Studio**: https://studio.youtube.com/
2. Sol menüden **"Content"** seçin
3. Yüklenen videoları göreceksiniz

### 7.2. Video Ayarlarını Düzenle

Her video için:
1. Video'ya tıklayın
2. **"Details"** sekmesinde:
   - Başlık, açıklama, etiketleri kontrol edin
   - Gerekirse düzenleyin
3. **"Visibility"** sekmesinde:
   - **"Private"** → **"Public"** yapabilirsiniz (yayın için)
4. **"SAVE"** butonuna tıklayın

### 7.3. Ülke ve Tür Ayarları

1. **"Settings"** → **"Channel"** → **"Basic info"**
2. **"Country of residence"**: Ülkenizi seçin
3. **"Keywords"**: Anahtar kelimeler ekleyin (virgülle ayrılmış)
   - Örnek: `AI Music, Neural Beats Studio, Music Production, Electronic Music`

---

## ⚠️ Önemli Notlar

### 1. API Quota Limitleri

- **Default quota**: 10,000 units/day
- **Video upload**: 1,600 units/video
- **Günlük maksimum**: ~6 video/yük (default quota ile)

**Çözüm**: 
- Toplu yükleme yaparken aralıklı yükleyin (günde 6 video)
- Veya quota artırımı isteyin: https://support.google.com/youtube/contact/yt_api_form

### 2. Test Modu vs Production

**Test Modu (Şu anki durum):**
- Sadece test kullanıcıları video yükleyebilir
- "This app isn't verified" uyarısı gösterilir
- Yeterli: Kişisel kullanım için

**Production Modu (İleride):**
- OAuth consent screen'i "Publish" yapın
- Google verification sürecinden geçin (karmaşık)
- Gerekli: Çok sayıda kullanıcı için

**Şimdilik test modu yeterli!**

### 3. Güvenlik

- **`credentials.json`**: Asla paylaşmayın, GitHub'a yüklemeyin
- **`token.json`**: Otomatik oluşturulur, güvenli tutun
- **`.gitignore`**: Bu dosyaları ekleyin (eğer Git kullanıyorsanız)

### 4. Video Format Gereksinimleri

- **Format**: MP4
- **Codec**: H.264 (video), AAC (audio)
- **Çözünürlük**: Minimum 720p (1280x720)
- **Aspect Ratio**: 16:9 (önerilen)
- **Süre**: Minimum 1 saniye

---

## 🐛 Sorun Giderme

### "Credentials file not found"

**Çözüm**: 
1. `credentials.json` dosyasını Google Cloud Console'dan indirin
2. Proje kök dizinine koyun: `C:\Users\Haluk\New_Project\AI_Music\credentials.json`

### "Invalid credentials"

**Çözüm**: 
1. `token.json` dosyasını silin
2. Script'i tekrar çalıştırın
3. Yeni authentication yapın

### "Quota exceeded"

**Çözüm**: 
- Günlük limit aşıldı (10,000 units)
- 24 saat bekleyin veya quota artırımı isteyin

### "This app isn't verified"

**Çözüm**: 
- Bu normaldir (test modunda)
- **"Advanced"** → **"Go to Neural Beats Studio (unsafe)"** tıklayın

### "Video upload failed"

**Çözüm**:
- Video formatını kontrol edin (MP4, H.264, AAC)
- Video boyutunu kontrol edin (çok büyük olabilir)
- İnternet bağlantınızı kontrol edin

---

## 🎯 Sonraki Adımlar

1. ✅ Google Cloud Console'da proje oluştur
2. ✅ YouTube Data API v3'ü etkinleştir
3. ✅ OAuth consent screen ayarla
4. ✅ OAuth 2.0 credentials oluştur ve indir
5. ✅ `credentials.json` dosyasını proje kök dizinine koy
6. ✅ İlk authentication yap (script çalıştır)
7. ✅ Videoları yükle
8. ✅ YouTube Studio'da kontrol et ve düzenle

---

## 📞 Yardım

Sorun yaşarsanız:
1. `YOUTUBE_UPLOAD_GUIDE.md` dosyasına bakın
2. Google Cloud Console'da API kullanımını kontrol edin
3. YouTube Studio'da video durumunu kontrol edin

**Başarılar! 🎉**

