# 📁 Platform Dosya Formatları ve Gereksinimleri

Bu rehber, her platform için desteklenen dosya türlerini ve format gereksinimlerini açıklar.

## 📊 Platform Karşılaştırması

| Platform | Format | Çözünürlük | Aspect Ratio | Max Süre | Max Boyut | Notlar |
|----------|--------|------------|--------------|----------|-----------|--------|
| **YouTube** | MP4, MOV, AVI | 1920x1080 | 16:9 | Sınırsız | 256 GB | En esnek platform |
| **Instagram Reels** | MP4, MOV | 1080x1920 | 9:16 | 90 saniye | 100 MB | Dikey video |
| **Instagram Post** | MP4, MOV | 1080x1080 | 1:1 | 60 saniye | 100 MB | Kare format |
| **Facebook** | MP4, MOV | Min 1280x720 | 16:9 | 240 saniye | 1 GB | Yatay video |
| **TikTok** | MP4, MOV | 1080x1920 | 9:16 | 60 saniye | 287 MB | Dikey video |
| **Spotify Podcast** | MP4, MOV | 1920x1080 | 16:9 | 3600 saniye | 500 MB | Podcast video |

## 🎬 Video Format Detayları

### YouTube

**Desteklenen Formatlar:**
- MP4 (H.264 codec, AAC audio)
- MOV (QuickTime)
- AVI
- WebM

**Önerilen Ayarlar:**
- **Codec**: H.264
- **Audio**: AAC, 128 kbps veya daha yüksek
- **Frame Rate**: 24, 25, 30, 48, 50, 60 fps
- **Bitrate**: 8 Mbps (1080p için)

**Çözünürlük Seçenekleri:**
- 2160p (4K): 3840x2160
- 1440p (2K): 2560x1440
- 1080p (Full HD): 1920x1080 ✅ Önerilen
- 720p (HD): 1280x720
- 480p (SD): 854x480
- 360p: 640x360
- 240p: 426x240

### Instagram Reels

**Desteklenen Formatlar:**
- MP4 (H.264 codec)
- MOV

**Gereksinimler:**
- **Çözünürlük**: 1080x1920 piksel (9:16 aspect ratio)
- **Max Süre**: 90 saniye
- **Max Boyut**: 100 MB
- **Frame Rate**: 30 fps önerilir
- **Audio**: AAC, 44.1 kHz

**Notlar:**
- Dikey video formatı (portrait)
- Thumbnail otomatik oluşturulur veya manuel seçilebilir

### Instagram Post

**Desteklenen Formatlar:**
- MP4 (H.264 codec)
- MOV

**Gereksinimler:**
- **Çözünürlük**: 1080x1080 piksel (1:1 aspect ratio)
- **Max Süre**: 60 saniye
- **Max Boyut**: 100 MB
- **Frame Rate**: 30 fps önerilir

**Notlar:**
- Kare format (square)
- Feed'de görüntülenir

### Facebook

**Desteklenen Formatlar:**
- MP4 (H.264 codec)
- MOV

**Gereksinimler:**
- **Min Çözünürlük**: 1280x720 (16:9 aspect ratio)
- **Önerilen**: 1920x1080
- **Max Süre**: 240 saniye (4 dakika)
- **Max Boyut**: 1 GB
- **Frame Rate**: 30 fps önerilir

**Notlar:**
- Yatay video formatı (landscape)
- Page veya kişisel profil için yüklenebilir

### TikTok

**Desteklenen Formatlar:**
- MP4 (H.264 codec)
- MOV

**Gereksinimler:**
- **Çözünürlük**: 1080x1920 piksel (9:16 aspect ratio)
- **Max Süre**: 60 saniye (bazı hesaplar için daha uzun)
- **Max Boyut**: ~287 MB
- **Frame Rate**: 30 fps önerilir
- **Audio**: AAC, 44.1 kHz

**Notlar:**
- Dikey video formatı (portrait)
- Müzik eşleştirme özellikleri mevcut

### Spotify Podcast Video

**Desteklenen Formatlar:**
- MP4 (H.264 codec)
- MOV

**Gereksinimler:**
- **Çözünürlük**: 1920x1080 (16:9 aspect ratio)
- **Max Süre**: 3600 saniye (1 saat)
- **Max Boyut**: 500 MB
- **Frame Rate**: 30 fps önerilir

**Notlar:**
- Podcast episode'larına video eklemek için
- Müzik yüklemek için distributor gerekir (API ile mümkün değil)

## 🎵 Audio Format Detayları

### Müzik Dosyaları (Input)

**Desteklenen Formatlar:**
- MP3 (128 kbps veya daha yüksek)
- WAV (PCM, 44.1 kHz)
- M4A (AAC)
- FLAC (lossless)

**Önerilen:**
- **MP3**: 192-320 kbps
- **WAV**: 44.1 kHz, 16-bit veya 24-bit
- **M4A**: 256 kbps AAC

## 🖼️ Görsel Format Detayları

### Thumbnail/Görsel

**Desteklenen Formatlar:**
- JPEG
- PNG
- WebP

**Gereksinimler:**
- **YouTube Thumbnail**: 1280x720 (16:9), max 2 MB
- **Instagram**: 1080x1080 (1:1) veya 1080x1920 (9:16)
- **Facebook**: 1200x630 (1.91:1)

## 🔄 Otomatik Format Dönüştürme

Sistem, platform gereksinimlerine göre otomatik format dönüştürme yapabilir:

### FFmpeg Kullanımı

```bash
# Instagram Reels için (1080x1920, 9:16)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4

# Instagram Post için (1080x1080, 1:1)
ffmpeg -i input.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4

# TikTok için (1080x1920, 9:16)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k -t 60 output.mp4

# Facebook için (1920x1080, 16:9)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k output.mp4
```

### Python ile Otomatik Dönüştürme

```python
import subprocess
from pathlib import Path

def convert_video_for_platform(input_file, output_file, platform):
    """Platform gereksinimlerine göre video dönüştür"""
    specs = get_platform_specs(platform)
    
    if platform == "instagram":
        # Reels için
        width, height = 1080, 1920
    elif platform == "tiktok":
        width, height = 1080, 1920
    elif platform == "facebook":
        width, height = 1920, 1080
    else:
        return False
    
    cmd = [
        "ffmpeg", "-i", str(input_file),
        "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_file)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Dönüştürme hatası: {e}")
        return False
```

## ✅ Dosya Türü Kontrolü

Sistem otomatik olarak:

1. **Dosya uzantısını kontrol eder**
   - MP4, MOV formatlarını destekler
   - Diğer formatlar için uyarı verir

2. **Platform gereksinimlerini kontrol eder**
   - Çözünürlük kontrolü
   - Süre kontrolü
   - Boyut kontrolü

3. **Uygun değilse uyarı verir**
   - Format dönüştürme önerisi
   - Gerekli ayarları gösterir

## 📝 Öneriler

### Video Oluşturma

1. **Yüksek kaliteli kaynak kullanın**
   - En az 1920x1080 çözünürlük
   - 30 fps frame rate

2. **Platform için optimize edin**
   - Instagram Reels: 1080x1920 (dikey)
   - YouTube: 1920x1080 (yatay)
   - TikTok: 1080x1920 (dikey)

3. **Audio kalitesini koruyun**
   - 128 kbps veya daha yüksek
   - AAC codec kullanın

### Toplu İşlem

Birden fazla platform için video oluştururken:

1. **Master video oluştur**: 1920x1080 (yatay)
2. **Platform versiyonları oluştur**:
   - YouTube: Master (1920x1080)
   - Instagram Reels: 1080x1920 (dönüştür)
   - TikTok: 1080x1920 (dönüştür)
   - Facebook: Master (1920x1080)

## 🆘 Sorun Giderme

### "Format not supported" Hatası

- Dosya formatını kontrol edin (MP4 veya MOV olmalı)
- Codec'i kontrol edin (H.264 video, AAC audio)
- FFmpeg ile dönüştürün

### "Resolution not supported" Hatası

- Çözünürlüğü kontrol edin
- Platform gereksinimlerine uygun çözünürlüğe dönüştürün
- Aspect ratio'yu kontrol edin

### "File too large" Hatası

- Dosya boyutunu kontrol edin
- Bitrate'i düşürün
- Süreyi kısaltın
- Compression kullanın

### "Duration too long" Hatası

- Video süresini kontrol edin
- Platform max süre limitine uyun
- Gerekirse videoyu bölün

