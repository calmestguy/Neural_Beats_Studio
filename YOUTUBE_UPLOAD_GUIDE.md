# 🎬 YouTube Otomatik Video Yükleme Rehberi

## 📋 Genel Bakış

Bu sistem, müzik dosyalarınızı ve görsellerinizi otomatik olarak eşleştirip YouTube videoları oluşturur ve YouTube'a yükler.

## 🎯 Özellikler

1. **Otomatik Video Oluşturma**: Müzik + görsel = YouTube video
2. **Toplu İşleme**: Tüm müzikleri tek seferde işle
3. **YouTube API Entegrasyonu**: Otomatik yükleme
4. **Metadata Yönetimi**: Başlık, açıklama, etiketler, kategori
5. **Ülke/Tür Desteği**: Video kategorisi ve metadata ayarları

## 📁 Dosya Yapısı

```
D:\Neutral Beats Studio\
├── Rainy City Blues.mp3          # Müzik dosyası
├── Music Resim\
│   └── Rainy City Blues.jpg      # Eşleşen görsel
└── ...
```

## 🚀 Adım 1: YouTube Videoları Oluştur

### Tek Video Oluştur

```bash
python src/create_youtube_video.py \
  --single "Rainy City Blues.mp3" \
  --music-dir "D:\Neutral Beats Studio" \
  --image-dir "D:\Neutral Beats Studio\Music Resim" \
  --output-dir output/youtube
```

### Tüm Müzikleri İşle

```bash
python src/create_youtube_video.py \
  --music-dir "D:\Neutral Beats Studio" \
  --image-dir "D:\Neutral Beats Studio\Music Resim" \
  --output-dir output/youtube
```

### Çözünürlük Ayarları

```bash
# 1080p (Full HD)
python src/create_youtube_video.py --width 1920 --height 1080

# 1440p (2K)
python src/create_youtube_video.py --width 2560 --height 1440

# 2160p (4K)
python src/create_youtube_video.py --width 3840 --height 2160
```

## 🔐 Adım 2: YouTube API Kurulumu

### 1. Google Cloud Console'da Proje Oluştur

1. **Google Cloud Console'a git**: https://console.cloud.google.com/
2. **Yeni proje oluştur**: "Neural Beats Studio" veya benzeri
3. **Projeyi seç**

### 2. YouTube Data API v3'ü Etkinleştir

1. **API Library'ye git**: https://console.cloud.google.com/apis/library
2. **"YouTube Data API v3"** ara
3. **"Enable"** tıkla

### 3. OAuth 2.0 Credentials Oluştur

1. **Credentials sayfasına git**: https://console.cloud.google.com/apis/credentials
2. **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. **Application type**: **"Desktop app"** seç
4. **Name**: "Neural Beats Studio YouTube Uploader"
5. **"CREATE"** tıkla
6. **JSON dosyasını indir** → `credentials.json` olarak kaydet (proje kök dizinine)

### 4. OAuth Consent Screen Ayarla

1. **OAuth consent screen** sayfasına git
2. **User Type**: "External" seç
3. **App name**: "Neural Beats Studio"
4. **User support email**: E-posta adresiniz
5. **Developer contact**: E-posta adresiniz
6. **"SAVE AND CONTINUE"** tıkla
7. **Scopes**: Varsayılanları kabul et
8. **Test users**: Kendi e-posta adresinizi ekleyin (test modunda)
9. **"SAVE AND CONTINUE"** → **"BACK TO DASHBOARD"**

## 📤 Adım 3: YouTube'a Video Yükle

### İlk Kullanım (Authentication)

İlk çalıştırmada tarayıcı açılacak ve Google hesabınızla giriş yapmanız istenecek:

```bash
python src/youtube_upload.py \
  --video output/youtube/Rainy_City_Blues_youtube.mp4 \
  --title "Rainy City Blues" \
  --privacy private
```

**Not**: İlk kullanımda:
- Tarayıcı açılır
- Google hesabınızla giriş yapın
- İzinleri onaylayın
- `token.json` dosyası otomatik oluşturulur (sonraki kullanımlar için)

### Tek Video Yükle

```bash
python src/youtube_upload.py \
  --video output/youtube/Rainy_City_Blues_youtube.mp4 \
  --title "Rainy City Blues - AI Music" \
  --description "🎵 Rainy City Blues\n\nAI-generated music by Neural Beats Studio\n\n#AIMusic #NeuralBeatsStudio" \
  --tags "AI Music,Neural Beats Studio,Music Production" \
  --privacy private \
  --category 10
```

### Toplu Yükleme

```bash
python src/youtube_upload.py \
  --video-dir output/youtube \
  --music-dir "D:\Neutral Beats Studio" \
  --privacy private \
  --category 10
```

### Gizlilik Durumları

- **`private`**: Sadece siz görebilirsiniz (test için)
- **`unlisted`**: Linki olanlar görebilir
- **`public`**: Herkes görebilir (yayın için)

### Video Kategorileri

- **`10`**: Music (müzik için)
- **`24`**: Entertainment
- **`22`**: People & Blogs
- **`15`**: Pets & Animals
- Diğer kategoriler: https://developers.google.com/youtube/v3/docs/videoCategories/list

## 🎨 Metadata Özelleştirme

### Otomatik Metadata

Script, müzik dosyası adından otomatik olarak:
- **Başlık**: Müzik dosyası adı
- **Açıklama**: Marka bilgileri + hashtag'ler
- **Etiketler**: AI Music, Neural Beats Studio, vb.

### Manuel Metadata

```bash
python src/youtube_upload.py \
  --video output/youtube/video.mp4 \
  --title "Özel Başlık" \
  --description "Özel açıklama\n\nDetaylar..." \
  --tags "Tag1,Tag2,Tag3" \
  --category 10 \
  --privacy public
```

## 🌍 Ülke ve Tür Ayarları

### YouTube Studio'da Ayarlama

1. **YouTube Studio'ya git**: https://studio.youtube.com/
2. **Settings** → **Channel** → **Basic info**
3. **Country of residence**: Ülkenizi seçin
4. **Keywords**: Anahtar kelimeler ekleyin (virgülle ayrılmış)

### Video Metadata ile Tür Belirleme

Script'te `get_music_metadata()` fonksiyonunu özelleştirerek:
- Müzik türünü otomatik tespit edebilirsiniz
- Tür'e göre etiketler ekleyebilirsiniz
- Açıklamaya tür bilgisi ekleyebilirsiniz

**Örnek özelleştirme** (`src/youtube_upload.py`):

```python
def get_music_metadata(music_file):
    music_name = Path(music_file).stem
    
    # Tür tespiti (dosya adından veya audio analyzer ile)
    genre = detect_genre(music_file)  # Örnek: "Blues", "Pop", "Electronic"
    
    metadata = {
        'title': music_name,
        'description': f"🎵 {music_name}\n\nGenre: {genre}\n\nAI-generated music by Neural Beats Studio",
        'tags': ['AI Music', 'Neural Beats Studio', genre, 'Music Production'],
        'category_id': '10',
        'privacy_status': 'private'
    }
    
    return metadata
```

## 🔄 Tam İş Akışı

### 1. Videoları Oluştur

```bash
python src/create_youtube_video.py \
  --music-dir "D:\Neutral Beats Studio" \
  --image-dir "D:\Neutral Beats Studio\Music Resim" \
  --output-dir output/youtube
```

### 2. YouTube'a Yükle (Private - Test)

```bash
python src/youtube_upload.py \
  --video-dir output/youtube \
  --music-dir "D:\Neutral Beats Studio" \
  --privacy private
```

### 3. YouTube Studio'da Kontrol Et

- Video'ları kontrol edin
- Thumbnail'ları kontrol edin
- Metadata'yı kontrol edin
- Gerekirse düzenleyin

### 4. Public'e Al

YouTube Studio'da:
- Video'yu açın
- **Visibility** → **Public** yapın
- Veya script ile: `--privacy public`

## ⚠️ Önemli Notlar

### 1. API Quota Limitleri

YouTube Data API v3 günlük limitleri:
- **Default**: 10,000 units/day
- **Video upload**: 1,600 units/video
- **Günlük maksimum**: ~6 video/yük

**Çözüm**: Toplu yükleme yaparken aralıklı yükleyin veya quota artırımı isteyin.

### 2. Video Format Gereksinimleri

- **Format**: MP4
- **Codec**: H.264 (video), AAC (audio)
- **Çözünürlük**: Minimum 720p (1280x720)
- **Aspect Ratio**: 16:9 (önerilen)
- **Süre**: Minimum 1 saniye

### 3. Telif Hakları

- AI-generated müziklerin telif durumunu kontrol edin
- YouTube Content ID sistemine kayıt yaptırın (opsiyonel)
- Açıklamada "AI-generated" belirtin

### 4. Test Modu

İlk kullanımda OAuth consent screen **"Testing"** modunda olacak:
- Sadece test kullanıcıları yükleyebilir
- **Publish** yaparak herkese açık hale getirebilirsiniz

## 🐛 Sorun Giderme

### "Credentials file not found"

**Çözüm**: `credentials.json` dosyasını Google Cloud Console'dan indirin ve proje kök dizinine koyun.

### "Invalid credentials"

**Çözüm**: 
1. `token.json` dosyasını silin
2. Script'i tekrar çalıştırın
3. Yeni authentication yapın

### "Quota exceeded"

**Çözüm**: 
- Günlük limit aşıldı
- 24 saat bekleyin veya quota artırımı isteyin

### "Video upload failed"

**Çözüm**:
- Video formatını kontrol edin (MP4, H.264, AAC)
- Video boyutunu kontrol edin (çok büyük olabilir)
- İnternet bağlantınızı kontrol edin

## 📊 Örnek Kullanım Senaryoları

### Senaryo 1: Yeni Müzik Yayınlama

```bash
# 1. Video oluştur
python src/create_youtube_video.py --single "New Song.mp3"

# 2. Private olarak yükle (test)
python src/youtube_upload.py \
  --video output/youtube/New_Song_youtube.mp4 \
  --title "New Song - AI Music" \
  --privacy private

# 3. YouTube Studio'da kontrol et
# 4. Public'e al
```

### Senaryo 2: Toplu Yayınlama

```bash
# 1. Tüm videoları oluştur
python src/create_youtube_video.py \
  --music-dir "D:\Neutral Beats Studio" \
  --image-dir "D:\Neutral Beats Studio\Music Resim"

# 2. Private olarak yükle
python src/youtube_upload.py \
  --video-dir output/youtube \
  --privacy private

# 3. Her birini kontrol et ve public'e al
```

## 🎯 Sonuç

Artık müziklerinizi otomatik olarak YouTube'a yükleyebilirsiniz! 🎉

**Kanal Bilgileri**:
- **Kanal**: Neural Beats Studio
- **Handle**: @NBS-NeuralBeatsStudio
- **Kanal ID**: UCBBEdistMgv1qONZMsvOa8Q

