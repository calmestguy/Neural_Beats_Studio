# 🎨 AI ile Kadın Şarkıcı Fotoğrafı Oluşturma Rehberi

## 🎯 Özellikler

- **Ana Karakter**: Sarışın, mavi gözlü kadın şarkıcı
- **Varyasyonlar**: Farklı saç renkleri, stilleri
- **Duygusal İfadeler**: Neşeli, üzgün, nötr
- **Yüksek Kalite**: 4K çözünürlük, profesyonel fotoğraf kalitesi

---

## 🚀 Hızlı Başlangıç

### Yöntem 1: Stable Diffusion (Yerel - Önerilen)

**Avantajlar:**
- Ücretsiz
- Offline çalışır
- Sınırsız kullanım
- GPU hızlandırması

**Kurulum:**
```bash
pip install diffusers torch torchvision transformers accelerate
```

**Kullanım:**
```bash
# Sadece ana karakter (sarışın, mavi gözlü)
python src/generate_singer_image.py --method stable_diffusion --single

# Tüm varyasyonlar
python src/generate_singer_image.py --method stable_diffusion
```

### Yöntem 2: Hugging Face API (Online - Kolay)

**Avantajlar:**
- Kurulum yok
- Hızlı
- Ücretsiz tier var

**Dezavantajlar:**
- API key gerektirir
- İnternet gerekli
- Rate limit var

**Kurulum:**
1. https://huggingface.co/settings/tokens → API key al
2. Environment variable olarak ayarla:
   ```bash
   set HUGGINGFACE_API_KEY=your_key_here  # Windows
   export HUGGINGFACE_API_KEY=your_key_here  # Linux/Mac
   ```

**Kullanım:**
```bash
python src/generate_singer_image.py --method huggingface_api --single
```

---

## 📋 Komut Örnekleri

### 1. Sadece Ana Karakter
```bash
python src/generate_singer_image.py --method stable_diffusion --single
```
**Çıktı:** `assets/female_singer_main.jpg` (sarışın, mavi gözlü)

### 2. Tüm Varyasyonlar
```bash
python src/generate_singer_image.py --method stable_diffusion
```
**Çıktı:**
- `assets/female_singer_main_blonde_blue.jpg` (ana karakter)
- `assets/female_singer_brunette_blue_neutral.jpg`
- `assets/female_singer_black_blue_sad.jpg`
- `assets/female_singer_red_blue_happy.jpg`
- ... ve daha fazlası

### 3. Özel Varyasyonlar
```bash
python src/generate_singer_image.py \
  --method stable_diffusion \
  --hair-colors blonde brunette \
  --eye-colors blue green \
  --emotions neutral sad
```

### 4. Aynı Görüntüyü Tekrar Oluşturma
```bash
python src/generate_singer_image.py \
  --method stable_diffusion \
  --single \
  --seed 42
```

---

## 🎨 Saç Renkleri

Varsayılan seçenekler:
- `blonde` - Sarışın (ana karakter)
- `brunette` - Kahverengi
- `black` - Siyah
- `red` - Kızıl

Özel renkler:
```bash
--hair-colors blonde brunette black red silver
```

---

## 👁️ Göz Renkleri

Varsayılan:
- `blue` - Mavi (ana karakter)

Diğer seçenekler:
```bash
--eye-colors blue green brown hazel
```

---

## 😊 Duygular

Varsayılan:
- `neutral` - Nötr
- `sad` - Üzgün
- `happy` - Neşeli

Diğer seçenekler:
```bash
--emotions neutral sad happy surprised thoughtful
```

---

## 📁 Çıktı Dosyaları

Tüm görüntüler `assets/` klasörüne kaydedilir:

```
assets/
├── female_singer_main.jpg              # Ana karakter
├── female_singer_blonde_blue_neutral.jpg
├── female_singer_blonde_blue_sad.jpg
├── female_singer_blonde_blue_happy.jpg
├── female_singer_brunette_blue_neutral.jpg
└── ...
```

---

## ⚙️ Gelişmiş Ayarlar

### Model Seçimi (Stable Diffusion)

Farklı modeller deneyebilirsiniz:
- `runwayml/stable-diffusion-v1-5` (varsayılan)
- `stabilityai/stable-diffusion-2-1` (daha iyi kalite)
- `stabilityai/sd-turbo` (daha hızlı)

Script içinde `model` parametresini değiştirin.

### Çözünürlük

Varsayılan: 1024x1024 (yüksek kalite)
- Daha yüksek: 1536x1536 (daha fazla VRAM gerekir)
- Daha düşük: 512x512 (daha hızlı)

---

## 💡 İpuçları

1. **İlk Çalıştırma**: Modeller indirilecek (~4-7GB), internet gerekli
2. **GPU Kullanımı**: RTX 3070 ile ~10-30 saniye/görüntü
3. **CPU Kullanımı**: Çok daha yavaş (~5-10 dakika/görüntü)
4. **Seed Kullanımı**: Aynı seed ile aynı görüntüyü tekrar oluşturabilirsiniz
5. **Varyasyonlar**: Farklı saç renkleri ile aynı yüzü korumak için seed kullanın

---

## 🔧 Sorun Giderme

### Hata: "CUDA out of memory"
```bash
# Daha küçük model kullan veya batch size azalt
# Script içinde torch.float32 kullan (float16 yerine)
```

### Hata: "diffusers not installed"
```bash
pip install diffusers torch torchvision transformers accelerate
```

### Hata: "Hugging Face API key required"
```bash
# API key al: https://huggingface.co/settings/tokens
set HUGGINGFACE_API_KEY=your_key_here
```

### Görüntü Kalitesi Düşük
- Daha yüksek çözünürlük kullan (1024x1024 veya 1536x1536)
- Daha iyi model seç (stable-diffusion-2-1)
- Daha fazla step kullan (50-100)

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Hızlı Test
```bash
# Sadece ana karakteri oluştur
python src/generate_singer_image.py --method stable_diffusion --single
```

### Senaryo 2: Tüm Varyasyonlar
```bash
# Farklı saç renkleri, duygular
python src/generate_singer_image.py --method stable_diffusion
```

### Senaryo 3: Şarkıya Özel Duygu
```bash
# "Rainy City Blues" için üzgün ifade
python src/generate_singer_image.py \
  --method stable_diffusion \
  --single \
  --emotions sad
```

### Senaryo 4: Video İçin Hazırlık
```bash
# Ana karakter + farklı duygular
python src/generate_singer_image.py \
  --method stable_diffusion \
  --hair-colors blonde \
  --eye-colors blue \
  --emotions neutral sad happy
```

---

## 📚 Sonraki Adımlar

Görüntüleri oluşturduktan sonra:

1. **Video Oluşturma**: SadTalker ile video oluşturun
   ```bash
   python src/sadtalker_integration.py \
     --image assets/female_singer_main.jpg \
     --audio rainy_city_blues_lyrics_singing_vocal.wav
   ```

2. **Farklı Duygular**: Şarkının farklı bölümleri için farklı duygular kullanın

3. **Varyasyonlar**: Farklı saç renkleri ile farklı karakterler oluşturun

---

## 🎨 Örnek Prompt'lar

Script otomatik olarak şu prompt'u kullanır:
```
beautiful female singer, professional musician, 
blonde hair, blue eyes, professional photo, 
high quality, 4K resolution, studio lighting, 
portrait, looking at camera, neutral expression
```

Özelleştirmek için script içindeki `create_prompt()` fonksiyonunu düzenleyin.


