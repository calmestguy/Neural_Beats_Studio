# 🔑 API Key Kurulumu

Hugging Face API key'iniz kaydedildi ve kullanıma hazır!

## ✅ Oluşturulan Görüntüler

1. **Ana Karakter**: `assets/female_singer_main.jpg` (sarışın, mavi gözlü, nötr)
2. **Varyasyonlar**:
   - `assets/female_singer_main_blonde_blue.jpg` (ana karakter)
   - `assets/female_singer_blonde_blue_sad.jpg` (sarışın, üzgün)
   - `assets/female_singer_brunette_blue_neutral.jpg` (kahverengi saç, nötr)
   - `assets/female_singer_brunette_blue_sad.jpg` (kahverengi saç, üzgün)

## 🚀 Sonraki Adımlar

### 1. Video Oluşturma (SadTalker ile)

```bash
python src/sadtalker_integration.py \
  --image assets/female_singer_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --lyrics rainy_city_blues_lyrics.txt \
  --resolution 4k
```

### 2. Daha Fazla Varyasyon Oluşturma

```bash
# Tüm saç renkleri ve duygular
python src/generate_singer_image.py \
  --method huggingface_api \
  --api-key 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
```

### 3. Şarkıya Özel Duygu

```bash
# Rainy City Blues için üzgün ifade
python src/generate_singer_image.py \
  --method huggingface_api \
  --api-key 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 \
  --single \
  --emotions sad
```

## 📝 API Key Kullanımı

API key'iniz script'te kullanılıyor. Gelecekte kullanmak için:

**Yöntem 1: Komut satırında**
```bash
python src/generate_singer_image.py --api-key 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
```

**Yöntem 2: Environment Variable (Önerilen)**
```bash
set HUGGINGFACE_API_KEY=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
python src/generate_singer_image.py --method huggingface_api
```

## 🎨 Oluşturulan Görüntüleri Kullanma

Görüntüler `assets/` klasöründe. Bunları:
- SadTalker ile video oluşturmak için kullanabilirsiniz
- D-ID ile video oluşturmak için kullanabilirsiniz
- Farklı şarkılar için farklı duygular seçebilirsiniz

## 💡 İpuçları

1. **Aynı Yüz**: Farklı varyasyonlarda aynı yüzü korumak için `--seed` parametresi kullanın
2. **Duygular**: Şarkının ruh haline göre duygu seçin
3. **Kalite**: Hugging Face API yüksek kalite görüntüler üretir


