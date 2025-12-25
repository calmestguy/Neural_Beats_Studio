# AI Music Generator - Sosyal Medya İçin

RTX 3070 8GB için optimize edilmiş AI müzik üretici. MusicGen kullanarak sosyal medya için kısa müzik loop'ları üretir.

## 🎯 Özellikler

- **MusicGen Modeli**: Meta'nın açık kaynak müzik üretim modeli
- **Sosyal Medya Odaklı**: 10-30 saniyelik loop'lar için optimize
- **GPU Optimizasyonu**: RTX 3070 8GB için optimize edilmiş
- **Batch Üretim**: Toplu müzik üretimi
- **Prompt Mühendisliği**: Hazır sosyal medya prompt'ları
- **Gelişmiş Mastering**: Otomatik EQ, compression, reverb, normalizasyon
- **18 Müzik Türü**: Classical, Pop, Rock, Jazz, Metal, Blues, Latin, vb.
- **Prompt İyileştirme**: Otomatik prompt önerileri ve geliştirme araçları

## 📋 Gereksinimler

- Python 3.8+ (Python 3.11 veya 3.12 önerilir - 3.13 bazı paketlerle uyumluluk sorunları yaşayabilir)
- CUDA destekli GPU (RTX 3070 önerilir)
- ~5GB disk alanı (modeller için)

## 🚀 Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt
```

**Not**: İlk çalıştırmada modeller otomatik indirilecek (~300MB-1.5GB)

## 💻 Kullanım

### Tek müzik üretimi:

```bash
python src/generate.py --prompt "upbeat electronic dance music" --duration 30
```

### Batch üretim (sosyal medya için):

```bash
python src/batch_generate.py
```

### Gelişmiş mastering ile üretim:

```bash
# Otomatik mastering ile
python src/generate.py --prompt "your prompt" --duration 30 --master

# Mastering preset seçimi
python src/generate.py --prompt "your prompt" --master --master-preset bass_heavy

# Tür bazlı otomatik mastering
python src/generate_by_genre.py --genre rock --duration 30 --master
```

### Gelişmiş audio işleme:

```bash
# Manuel mastering
python src/advanced_mixing.py output/track.wav --bass-boost 3.0 --treble-boost 2.0

# Bas vurgulama (basit)
python src/post_process.py output/track.wav --bass-boost 8.0
```

### Model seçimi:

```bash
# Küçük model (hızlı, ~2GB VRAM)
python src/generate.py --model small --prompt "your prompt"

# Orta model (daha iyi kalite, ~6GB VRAM)
python src/generate.py --model medium --prompt "your prompt"

# Büyük model (en iyi kalite, ~12GB VRAM - 8GB için riskli)
python src/generate.py --model large --prompt "your prompt"
```

## 📁 Proje Yapısı

```
AI_Music/
├── src/
│   ├── generate.py          # Ana üretim scripti
│   ├── prompt_engineer.py   # Prompt kütüphanesi
│   └── batch_generate.py    # Toplu üretim
├── output/                  # Üretilen müzikler
├── requirements.txt
└── README.md
```

## 🎵 Müzik Türleri

Sistemde 18 farklı müzik türü mevcut:

### Sosyal Medya Kategorileri
- **energetic**: Enerjik, dans edilebilir müzikler
- **ambient**: Sakin, arka plan müzikleri
- **trending**: Viral, TikTok/Reels tarzı
- **emotional**: Duygusal, sinematik müzikler

### Türk Müziği
- **turkish_pop**: Türk pop müziği
- **turkish_traditional**: Geleneksel enstrümanlarla Türk müziği

### Klasik Müzik Türleri
- **classical**: Klasik orkestra müziği (Beethoven, Mozart, Bach tarzı)
- **jazz**: Caz müziği (swing, bebop, smooth jazz)
- **blues**: Blues müziği (Delta, Chicago blues)

### Modern Popüler Müzik
- **pop**: Pop müzik
- **rock**: Rock müzik (hard, soft, punk)
- **metal**: Metal müzik (heavy, death, black metal)
- **rap_hiphop**: Rap/Hip-Hop
- **electronic**: Elektronik müzik (house, techno, trance, EDM)
- **country**: Country müzik
- **reggae**: Reggae müziği
- **latin**: Latin müziği (salsa, tango, rumba)

### Kullanım:
```bash
# Tüm türleri listele
python src/generate_by_genre.py --list

# Belirli bir türde müzik üret
python src/generate_by_genre.py --genre classical --duration 30
python src/generate_by_genre.py --genre rock --duration 30 --bass-boost
python src/generate_by_genre.py --genre jazz --duration 30 --model medium
```

## ⚠️ Önemli Notlar

1. **İlk Çalıştırma**: Modeller indirilecek, internet bağlantısı gerekir
2. **VRAM Yönetimi**: 8GB VRAM için `small` veya `medium` önerilir
3. **Kalite**: İlk denemelerde sonuçlar değişken olabilir, prompt mühendisliği önemli
4. **Süre**: GPU'da ~10-30 saniye/track, CPU'da çok daha yavaş

## 🔧 Sorun Giderme

**CUDA hatası**: GPU sürücülerinizi güncelleyin
**Out of memory**: `small` model kullanın veya batch size'ı düşürün
**Yavaş üretim**: GPU kullanıldığından emin olun (`nvidia-smi` ile kontrol)

## 📊 Performans

RTX 3070 8GB ile:
- **small model**: ~10-15 saniye/track
- **medium model**: ~20-30 saniye/track
- **large model**: VRAM yetersiz olabilir

## 🎚️ Mastering Preset'leri

- **default**: Dengeli mastering (genel kullanım)
- **bass_heavy**: Güçlü bas vurgusu (rock, metal, hip-hop için)
- **vocal**: Vokal odaklı (jazz, blues, country için)
- **cinematic**: Sinematik, dramatik (klasik, ambient için)

## 🎵 Audio Analizi ve Benzer Müzik Üretimi

Sistem artık mevcut müzik dosyalarını **veya YouTube linklerini** analiz edip benzer müzik üretebilir!

**Özellikler**:
- ✅ **YouTube Entegrasyonu**: Direkt YouTube link'inden analiz
- ✅ Tempo tespiti
- ✅ Enstrüman tespiti (bass, guitar, drums, piano, vb.)
- ✅ Müzik türü tahmini
- ✅ Enerji seviyesi analizi
- ✅ Otomatik prompt oluşturma
- ✅ Benzer müzik üretimi

**Kullanım**:
```bash
# YouTube link'inden analiz ve benzer müzik üretimi
python src/audio_analyzer.py "https://www.youtube.com/watch?v=..." --duration 30

# Yerel dosya ile
python src/audio_analyzer.py output/track.wav --duration 30 --similarity high

# Sadece analiz (müzik üretmeden)
python src/audio_analyzer.py "https://www.youtube.com/watch?v=..." --analyze-only

# Mastering ile
python src/audio_analyzer.py output/track.wav --master
```

**Benzerlik Seviyeleri**:
- `high`: Çok benzer, aynı karakteristikler
- `medium`: İlham alınmış, benzer vibe
- `low`: Sadece tür bazlı

## 🎯 Sonraki Adımlar

1. Farklı prompt'larla denemeler yapın
2. En iyi sonuçları not edin
3. Mastering preset'lerini deneyin
4. Prompt iyileştirme araçlarını kullanın (`src/prompt_enhancer.py`)
5. **Audio analizi ile benzer müzik üretin** (`src/audio_analyzer.py`)
6. Web arayüzü ekleyin (Gradio) - gelecekte

## 📝 Lisans

Bu proje eğitim amaçlıdır. MusicGen Meta tarafından geliştirilmiştir.

