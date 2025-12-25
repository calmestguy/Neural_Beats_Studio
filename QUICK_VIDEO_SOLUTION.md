# 🎬 Hızlı Video Çözümü

SadTalker kurulumu uzun sürebilir. İşte hızlı alternatifler:

## ⚡ En Hızlı: D-ID Web Arayüzü (5 Dakika)

1. **D-ID'ye Git**: https://www.d-id.com/
2. **Sign Up** (ücretsiz, deneme kredisi var)
3. **Create Video** → **Talking Avatar**
4. **Upload Image**: `assets/female_singer_main.jpg` yükle
5. **Upload Audio**: `rainy_city_blues_lyrics_singing_vocal.wav` yükle
6. **Settings**: 4K resolution seç
7. **Create** → Video hazır olunca indir

**Süre**: ~5 dakika  
**Maliyet**: ~$0.10-0.50 (deneme kredisi var)

---

## 🆓 Ücretsiz: SadTalker Kurulumu (30 Dakika - Bir Kez)

SadTalker kurulumu devam ediyor. Alternatif olarak manuel kurulum:

```bash
# 1. SadTalker'ı klonla
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Modelleri indir (GitHub sayfasından)
# checkpoints/ klasörüne yerleştir

# 4. Video oluştur
cd ..
python src/sadtalker_integration.py \
  --image assets/female_singer_main.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --lyrics rainy_city_blues_lyrics.txt \
  --resolution 4k
```

---

## 🎯 Şu An Yapabilecekleriniz

1. **D-ID ile Hızlı Test** (önerilen - 5 dakika)
2. **SadTalker Kurulumunu Bekle** (ücretsiz ama uzun)
3. **Alternatif Araçlar**: Wav2Lip, HeyGen, vb.


