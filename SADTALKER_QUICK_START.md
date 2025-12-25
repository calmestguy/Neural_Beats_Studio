# 🚀 SadTalker Hızlı Başlangıç

## ⚠️ Önemli Notlar

1. **Python 3.13 Uyumluluk Sorunları:** SadTalker Python 3.11-3.12 ile daha iyi çalışır
2. **Model İndirme:** Otomatik indirme bazen başarısız olabilir, manuel indirme gerekebilir

## 📥 Model İndirme (Manuel - Önerilen)

### Yöntem 1: Hugging Face'den İndir

1. **Hugging Face sayfasına gidin:**
   https://huggingface.co/vinthony/SadTalker/tree/main/checkpoints

2. **Aşağıdaki dosyaları indirin:**
   - `SadTalker_V0.0.2_256.safetensors` (~400 MB)
   - `SadTalker_V0.0.2_512.safetensors` (~400 MB)
   - `mapping_00109-model.pth.tar` (~200 MB)
   - `mapping_00229-model.pth.tar` (~200 MB)
   - `auido2exp_00300-model.pth` (~100 MB)
   - `auido2pose_00140-model.pth` (~100 MB)

3. **Dosyaları yerleştirin:**
   ```
   SadTalker/
     checkpoints/
       SadTalker_V0.0.2_256.safetensors
       SadTalker_V0.0.2_512.safetensors
       mapping_00109-model.pth.tar
       mapping_00229-model.pth.tar
       auido2exp_00300-model.pth
       auido2pose_00140-model.pth
   ```

### Yöntem 2: Git LFS ile İndir

```bash
cd SadTalker
git lfs install
git lfs pull
```

## 🔧 Kurulum

### 1. Bağımlılıkları Yükle

```bash
cd SadTalker
pip install -r requirements.txt
```

**Not:** Python 3.13'te bazı paketler sorun çıkarabilir. Python 3.12 önerilir.

### 2. Modelleri Kontrol Et

```bash
# Windows PowerShell
if (Test-Path "SadTalker\checkpoints") {
    $files = Get-ChildItem "SadTalker\checkpoints" -File
    $files | ForEach-Object {
        $sizeMB = [math]::Round($_.Length/1MB, 2)
        Write-Host "$($_.Name): $sizeMB MB"
    }
}
```

**Beklenen boyutlar:**
- `.safetensors` dosyaları: ~400 MB
- `.pth.tar` dosyaları: ~200 MB
- `.pth` dosyaları: ~100 MB

Eğer dosyalar 0 MB veya çok küçükse, manuel indirme yapın.

## 🎬 Video Oluşturma

### Basit Kullanım

```bash
python src/sadtalker_integration.py \
  --image assets/female_singer_microphone_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --resolution 512
```

### Tam Özellikli

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

### "Models not found" Hatası

1. Modelleri manuel olarak indirin (yukarıdaki yöntem)
2. `SadTalker/checkpoints/` klasörüne yerleştirin
3. Dosya boyutlarını kontrol edin (0 MB değilse sorun var)

### Python 3.13 Uyumluluk Sorunları

**Çözüm 1: Python 3.12 Kullan**

```bash
# Python 3.12 ile virtual environment
python3.12 -m venv venv_sadtalker
venv_sadtalker\Scripts\activate  # Windows
pip install -r SadTalker/requirements.txt
```

**Çözüm 2: D-ID API Kullan (Alternatif)**

Eğer SadTalker kurulumu zor geliyorsa, D-ID API kullanabilirsiniz:

```bash
python src/did_api_video.py \
  --image assets/female_singer_microphone_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --api-key YOUR_DID_API_KEY
```

### Import Hataları

```bash
# SadTalker dizinine gidin
cd SadTalker

# Bağımlılıkları tekrar yükleyin
pip install -r requirements.txt

# Özel paketler
pip install face-alignment imageio imageio-ffmpeg librosa numba resampy pydub scipy kornia tqdm yacs pyyaml joblib scikit-image
```

## 📊 Performans

- **Çözünürlük 256:** ~1-2 dakika (GPU), ~5-10 dakika (CPU)
- **Çözünürlük 512:** ~3-5 dakika (GPU), ~15-30 dakika (CPU)
- **GPU:** CUDA destekli GPU varsa çok daha hızlı

## ✅ Başarı Kontrolü

Video başarıyla oluşturulduysa:
1. `output/` klasöründe `.mp4` dosyası olmalı
2. Dosya boyutu 0'dan büyük olmalı
3. Video oynatılabilir olmalı

## 🎉 Sonraki Adımlar

Video oluşturulduktan sonra:

```bash
# Müzik ekle
python src/combine_music_with_video.py \
  --video output/singer_video.mp4 \
  --music "output/Rainy City Blues.mp3" \
  --video-volume 0.4 \
  --music-volume 0.6
```

## 💡 İpuçları

1. **İlk test:** Düşük çözünürlük (256) ile başlayın
2. **Kalite:** 512 genelde yeterli
3. **GPU:** Varsa mutlaka kullanın (çok daha hızlı)
4. **Alternatif:** D-ID API daha kolay ama ücretli


