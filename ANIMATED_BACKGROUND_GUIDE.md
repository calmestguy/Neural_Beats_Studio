# 🎬 Hareketli Arka Plan Video Rehberi

## ✅ Oluşturulan Script

`src/create_animated_background.py` - Şarkı sözlerine göre otomatik animasyonlu arka plan videoları oluşturur.

## 🎯 Özellikler

### Desteklenen Ortamlar

1. **Yağmurlu Şehir Gecesi** (`rainy_city_night`)
   - Yağmur efekti (particle system)
   - Koyu mavi-gece atmosferi
   - Neon ışıklar

2. **Araba İçi** (`car_interior`)
   - Parallax scrolling (hareket eden manzara)
   - Yol çizgileri animasyonu
   - Sokak lambaları
   - Cam üzerinde yağmur

3. **Pencere + Yağmurlu Gece** (`window_rainy_night`)
   - Pencere çerçevesi
   - Cam üzerinde yağmur damlaları
   - Dışarıdaki gece manzarası
   - Sokak lambaları

4. **Rahat Oda** (`cozy_room_window`)
   - Sıcak, rahat atmosfer
   - Pencere görünümü
   - Yanıp sönen ışık animasyonu

## 🚀 Kullanım

### Temel Kullanım

```bash
python src/create_animated_background.py \
  --lyrics rainy_city_blues_lyrics.txt \
  --audio "output/Rainy City Blues.mp3" \
  --output output/animated_background.mp4
```

### Özelleştirme

```bash
python src/create_animated_background.py \
  --lyrics rainy_city_blues_lyrics.txt \
  --audio "output/Rainy City Blues.mp3" \
  --width 1920 \
  --height 1080 \
  --fps 30 \
  --output output/custom_background.mp4
```

## 📋 Parametreler

- `--lyrics`: Şarkı sözleri dosyası (zorunlu)
- `--audio`: Ses dosyası (zorunlu)
- `--output`: Çıktı video dosyası (opsiyonel)
- `--width`: Video genişliği (default: 1920)
- `--height`: Video yüksekliği (default: 1080)
- `--fps`: Frame rate (default: 30)
- `--duration`: Video süresi saniye (otomatik: ses dosyasından)

## 🎨 Otomatik Ortam Seçimi

Script şarkı sözlerini analiz eder ve otomatik olarak uygun ortamı seçer:

- **"rain", "rainy", "city", "night"** → Yağmurlu şehir gecesi
- **"car", "drive", "driving"** → Araba içi
- **"window", "rain", "night"** → Pencere + yağmurlu gece
- **"room", "cozy", "warm"** → Rahat oda

## 💡 Örnek Senaryolar

### Senaryo 1: Yağmurlu Gece Şarkısı

```bash
python src/create_animated_background.py \
  --lyrics rainy_city_blues_lyrics.txt \
  --audio "output/Rainy City Blues.mp3"
```

**Sonuç**: Pencere görünümü + yağmur efekti + gece atmosferi

### Senaryo 2: Araba İçi Seyahat

Şarkı sözlerinde "car", "drive", "road" kelimeleri varsa:
- Otomatik olarak araba içi efekti seçilir
- Hareket eden manzara
- Yol çizgileri animasyonu

### Senaryo 3: Rahat Oda

Şarkı sözlerinde "room", "cozy", "warm" kelimeleri varsa:
- Sıcak, rahat atmosfer
- Pencere görünümü
- Yanıp sönen ışık

## 🔧 Gereksinimler

### Python Paketleri

```bash
pip install opencv-python numpy pillow librosa
```

### FFmpeg

FFmpeg yüklü olmalı:
- Windows: https://ffmpeg.org/download.html
- veya: `winget install Gyan.FFmpeg`

## 📊 Video Özellikleri

- **Format**: MP4 (H.264)
- **Çözünürlük**: 1920x1080 (varsayılan, özelleştirilebilir)
- **FPS**: 30 (varsayılan)
- **Ses**: Şarkı dosyasından otomatik eklenir
- **Süre**: Ses dosyası süresine göre otomatik

## 🎬 Sonuç

Oluşturulan video:
- ✅ Hareketli arka plan (yağmur, araba, ışık animasyonları)
- ✅ Şarkı sözlerine uygun ortam
- ✅ Şarkı sesi otomatik eklenir
- ✅ Yüksek kalite (1080p veya 4K)

## 💡 İpuçları

1. **Daha uzun video**: `--duration` parametresi ile süre belirleyin
2. **4K kalite**: `--width 3840 --height 2160` kullanın
3. **Daha yavaş animasyon**: FPS'i düşürün (`--fps 24`)
4. **Manuel ortam seçimi**: `analyze_environment.py` dosyasını düzenleyin

## 🔄 Sonraki Adımlar

Video oluşturulduktan sonra:
1. Video'yu kontrol edin
2. İsterseniz ek efektler ekleyin
3. Sosyal medyada paylaşın!

---

## 📝 Notlar

- İlk çalıştırmada frame'ler oluşturulur (biraz zaman alabilir)
- FFmpeg yüklü değilse script hata verecektir
- Büyük çözünürlükler daha fazla bellek kullanır

