# 🎤 Şarkı Söyleyen AI Vokal Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Temel Kullanım (Vokal + Müzik)

```bash
python src/create_singing_vocal.py rainy_city_blues_lyrics.txt --music "output/Rainy City Blues.mp3"
```

Bu komut:
- Şarkı sözlerinden şarkı söyleyen AI kadın vokal oluşturur
- Vokali müzikle karıştırır
- Sonucu `output/Rainy City Blues_with_singing_vocal.wav` olarak kaydeder

### 2. Sadece Vokal (Müzik Olmadan)

```bash
python src/create_singing_vocal.py rainy_city_blues_lyrics.txt --vocal-only
```

Bu komut:
- Sadece vokal dosyası oluşturur
- `rainy_city_blues_lyrics_singing_vocal.wav` olarak kaydeder

### 3. Özel Çıktı Dosyası

```bash
python src/create_singing_vocal.py rainy_city_blues_lyrics.txt --music "output/Rainy City Blues.mp3" --output "my_song_with_vocal.wav"
```

## 📝 Şarkı Sözleri Dosyası Formatı

Şarkı sözleri dosyanız şu formatta olmalı:

```
[Verse]
Streetlights flicker like they're lost in time
Puddles ripple with a silent rhyme
My shadow stretches but it won't stay near

[Chorus]
And I walk
And I wander
Through the rain tonight
```

**Önemli Notlar:**
- `[Verse]`, `[Chorus]` gibi bölüm başlıkları otomatik atlanır
- Her satır şarkı modunda üretilir
- Çok uzun metinler otomatik kısaltılır (Bark limiti)

## 🎛️ Parametreler

### Ses Seviyeleri

```bash
# Vokal daha yüksek, müzik daha düşük
python src/create_singing_vocal.py rainy_city_blues_lyrics.txt \
  --music "output/Rainy City Blues.mp3" \
  --vocal-volume 0.9 \
  --music-volume 0.6
```

- `--vocal-volume`: Vokal ses seviyesi (0-1, varsayılan: 0.8)
- `--music-volume`: Müzik ses seviyesi (0-1, varsayılan: 0.7)

### Farklı Ses Preset'leri

```bash
# Farklı kadın sesi
python src/create_singing_vocal.py rainy_city_blues_lyrics.txt \
  --music "output/Rainy City Blues.mp3" \
  --voice "v2/en_speaker_8"
```

**Mevcut Kadın Ses Preset'leri:**
- `v2/en_speaker_9` (varsayılan) - Yumuşak, melodik
- `v2/en_speaker_8` - Daha güçlü
- `v2/en_speaker_6` - Farklı ton
- `v2/en_speaker_5` - Alternatif

## 📋 Tam Komut Örnekleri

### Örnek 1: Yeni Bir Şarkı İçin

```bash
# 1. Şarkı sözlerini hazırlayın (örn: my_song_lyrics.txt)
# 2. Müzik dosyanızı hazırlayın (örn: output/my_song.mp3)
# 3. Çalıştırın:

python src/create_singing_vocal.py my_song_lyrics.txt --music "output/my_song.mp3"
```

### Örnek 2: Sadece Vokal Test

```bash
# Önce vokali test edin, sonra müzikle karıştırın
python src/create_singing_vocal.py my_song_lyrics.txt --vocal-only

# Vokali dinleyin, beğenirseniz müzikle karıştırın
python src/create_singing_vocal.py my_song_lyrics.txt --music "output/my_song.mp3"
```

### Örnek 3: Farklı Ses ve Seviyeler

```bash
python src/create_singing_vocal.py rainy_city_blues_lyrics.txt \
  --music "output/Rainy City Blues.mp3" \
  --voice "v2/en_speaker_8" \
  --vocal-volume 0.85 \
  --music-volume 0.65 \
  --output "output/custom_mix.wav"
```

## ⚙️ Tüm Parametreler

```bash
python src/create_singing_vocal.py <lyrics_file> [OPTIONS]

Zorunlu:
  lyrics_file              Şarkı sözleri dosyası (.txt)

Seçenekler:
  --music FILE            Müzik dosyası (vokali müzikle karıştırmak için)
  --output FILE           Çıktı dosyası (varsayılan: otomatik)
  --voice PRESET          Ses preset'i (varsayılan: v2/en_speaker_9)
  --vocal-volume FLOAT    Vokal ses seviyesi 0-1 (varsayılan: 0.8)
  --music-volume FLOAT    Müzik ses seviyesi 0-1 (varsayılan: 0.7)
  --vocal-only            Sadece vokal üret, müzikle karıştırma
```

## 🎵 Çıktı Dosyaları

### Vokal Dosyası
- **Konum**: Proje kök dizini
- **Format**: `{lyrics_filename}_singing_vocal.wav`
- **Örnek**: `rainy_city_blues_lyrics_singing_vocal.wav`

### Karışım Dosyası (Müzik + Vokal)
- **Konum**: `output/` klasörü
- **Format**: `{music_filename}_with_singing_vocal.wav`
- **Örnek**: `output/Rainy City Blues_with_singing_vocal.wav`

## ⚠️ Önemli Notlar

1. **İlk Çalıştırma**: Modeller otomatik indirilir (~90MB), internet gerekli
2. **İşlem Süresi**: CPU'da ~2-3 dakika, GPU'da daha hızlı
3. **Metin Uzunluğu**: Çok uzun şarkı sözleri otomatik kısaltılır
4. **Ses Kalitesi**: Bark TTS şarkı modu kullanır, profesyonel kalite değil ama şarkı gibi

## 🔧 Sorun Giderme

### Hata: "Bark TTS not available"
```bash
pip install bark
```

### Hata: "librosa or soundfile not available"
```bash
pip install librosa soundfile
```

### Vokal çok yavaş/garip
- `--voice` parametresini değiştirin
- Şarkı sözlerini kısaltın
- `text_temp` ve `waveform_temp` parametrelerini script içinde ayarlayın

### Müzik ve vokal senkronize değil
- Şarkı sözlerini müzik süresine göre ayarlayın
- Vokal dosyasını manuel olarak düzenleyin

## 💡 İpuçları

1. **Kısa Şarkılar**: Bark uzun metinlerde zorlanır, şarkıyı bölümlere ayırın
2. **Ses Testi**: Önce `--vocal-only` ile test edin
3. **Seviye Ayarı**: Vokal ve müzik seviyelerini dinleyerek ayarlayın
4. **Farklı Sesler**: Farklı `--voice` preset'lerini deneyin

## 📚 Örnek Kullanım Senaryoları

### Senaryo 1: Yeni Şarkı Üretimi
```bash
# 1. Müzik üret
python src/generate.py --prompt "blues music, melancholic, 75 BPM" --duration 30

# 2. Şarkı sözleri hazırla (my_song.txt)

# 3. Vokal ekle
python src/create_singing_vocal.py my_song.txt --music "output/track_xxx.wav"
```

### Senaryo 2: Mevcut Şarkıya Vokal Ekleme
```bash
# Mevcut müzik dosyanıza vokal ekleyin
python src/create_singing_vocal.py lyrics.txt --music "path/to/your/song.mp3"
```

### Senaryo 3: Sadece Vokal Üretimi (Başka Araçlarla Karıştırma)
```bash
# Vokali ayrı üretin, sonra DAW'da (Audacity, etc.) karıştırın
python src/create_singing_vocal.py lyrics.txt --vocal-only
```

## 🎯 Hızlı Referans

```bash
# EN BASIT KULLANIM
python src/create_singing_vocal.py lyrics.txt --music "song.mp3"

# SADECE VOKAL
python src/create_singing_vocal.py lyrics.txt --vocal-only

# ÖZELLEŞTİRİLMİŞ
python src/create_singing_vocal.py lyrics.txt \
  --music "song.mp3" \
  --voice "v2/en_speaker_8" \
  --vocal-volume 0.9 \
  --music-volume 0.6 \
  --output "final.wav"
```


