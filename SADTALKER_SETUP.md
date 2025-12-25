# 🎬 SadTalker Kurulum Rehberi

## ✅ Hızlı Başlangıç

### 1. Bağımlılıkları Yükle

```bash
python src/sadtalker_integration.py --install
```

Bu komut:
- SadTalker bağımlılıklarını yükler
- Gerekli Python paketlerini kurar

### 2. Modelleri İndir

```bash
python src/sadtalker_integration.py --download-models
```

Bu komut:
- SadTalker modellerini Hugging Face'den indirir
- `SadTalker/checkpoints/` klasörüne yerleştirir
- ~2-3 GB boyutunda (indirme süresi: internet hızına bağlı)

**Not:** Eğer otomatik indirme çalışmazsa:
1. https://huggingface.co/vinthony/SadTalker/tree/main/checkpoints adresine gidin
2. Tüm `.safetensors` ve `.pth` dosyalarını indirin
3. `SadTalker/checkpoints/` klasörüne yerleştirin

### 3. Video Oluştur

```bash
python src/sadtalker_integration.py \
  --image assets/female_singer_microphone_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --lyrics rainy_city_blues_lyrics.txt \
  --resolution 512 \
  --enhancer gfpgan \
  --background-enhancer realesrgan
```

## 📋 Parametreler

### Gerekli Parametreler

- `--audio`: Ses dosyası (vokal)
- `--image`: Şarkıcı fotoğrafı

### Opsiyonel Parametreler

- `--lyrics`: Şarkı sözleri dosyası (duygu analizi için)
- `--emotion`: Duygu (`happy`, `sad`, `surprised`, `angry`, `neutral`)
- `--output`: Çıktı video dosyası
- `--resolution`: Çözünürlük (`256`, `512`, `1024`, `4k`)
- `--enhancer`: Yüz iyileştirme (`gfpgan`, `RestoreFormer`, `none`)
- `--background-enhancer`: Arka plan iyileştirme (`realesrgan`, `none`)

## 🎯 Örnek Kullanım

### Basit Kullanım

```bash
python src/sadtalker_integration.py \
  --image assets/female_singer_microphone_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav
```

### Tam Özellikli Kullanım

```bash
python src/sadtalker_integration.py \
  --image assets/female_singer_microphone_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --lyrics rainy_city_blues_lyrics.txt \
  --resolution 512 \
  --enhancer gfpgan \
  --background-enhancer realesrgan \
  --output output/singer_video.mp4
```

## ⚠️ Sorun Giderme

### "SadTalker not installed" Hatası

```bash
# SadTalker klasörünü kontrol et
if (Test-Path "SadTalker") { Write-Host "OK" } else { Write-Host "SadTalker klasörü yok!" }

# Eğer yoksa:
git clone https://github.com/OpenTalker/SadTalker.git
```

### "Models not found" Hatası

```bash
# Modelleri indir
python src/sadtalker_integration.py --download-models
```

### Python 3.13 Uyumluluk Sorunları

SadTalker Python 3.11-3.12 ile daha iyi çalışır. Python 3.13'te bazı paketler sorun çıkarabilir.

**Çözüm:** Python 3.12 kullanın veya virtual environment oluşturun:

```bash
# Python 3.12 ile virtual environment
python3.12 -m venv venv_sadtalker
venv_sadtalker\Scripts\activate  # Windows
pip install -r SadTalker/requirements.txt
```

### GPU Kullanımı

SadTalker otomatik olarak GPU kullanır (varsa). CPU'da da çalışır ama daha yavaş.

GPU kontrolü:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
```

## 🚀 Sonraki Adımlar

Video oluşturulduktan sonra:

1. **Müzik ekle:**
```bash
python src/combine_music_with_video.py \
  --video output/singer_video.mp4 \
  --music "output/Rainy City Blues.mp3"
```

2. **Arka plan ekle:**
   - D-ID API kullanarak arka plan ekleyebilirsiniz
   - Veya video editing yazılımları ile

## 📊 Performans

- **Çözünürlük 256:** ~1-2 dakika (hızlı)
- **Çözünürlük 512:** ~3-5 dakika (önerilen)
- **Çözünürlük 1024:** ~10-15 dakika (yavaş)

GPU varsa daha hızlı çalışır.

## 💡 İpuçları

1. **İlk kullanım:** Düşük çözünürlük (256) ile test edin
2. **Kalite:** 512 çözünürlük genelde yeterli
3. **Enhancer:** `gfpgan` yüz kalitesini artırır
4. **Background:** `realesrgan` arka planı iyileştirir

## 🎉 Başarılı!

Artık D-ID.com'a gerek kalmadan kendi videolarınızı oluşturabilirsiniz!


