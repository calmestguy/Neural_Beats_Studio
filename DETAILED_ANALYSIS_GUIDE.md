# 🔍 Detaylı Audio Analizi Rehberi

## ✅ Yapılan İyileştirmeler

### 1. **Çok Detaylı Analiz Sistemi** 📊

Yeni sistem şu analizleri yapıyor:

#### 🎼 Melodik Yapı Analizi
- **Key Detection**: Hassas key tespiti (Krumhansl-Schmuckler algoritması benzeri)
- **Mode Detection**: Major/minor tespiti
- **Melodic Contour**: Melodinin yönü (ascending/descending/stable)
- **Chroma Analysis**: 12 perde sınıfı analizi

#### 🥁 Ritim Pattern Analizi
- **Time Signature**: 4/4, 3/4, 2/4 tespiti
- **Rhythmic Complexity**: Düşük/orta/yüksek
- **Groove Type**: Enerjik, sakin, geleneksel
- **Beat Pattern**: Güçlü/zayıf vuruş analizi

#### 🔊 Dinamik Analiz
- **Energy Level**: Düşük/orta/yüksek
- **Dynamic Range**: Dinamik aralık
- **Energy Contour**: Artan/azalan/sabit enerji
- **Energy Distribution**: Başlangıç/orta/son enerji analizi

#### 📊 Spektral Özellikler
- **Harmonic Ratio**: Harmonik/percussive oranı
- **Spectral Centroid**: Parlaklık (brightness)
- **Spectral Rolloff**: Yüksek frekans içeriği
- **Zero Crossing Rate**: Gürültü seviyesi

#### 🎸 Enstrüman Tespiti (Geliştirilmiş)
- **Frekans Analizi**: Her enstrüman için özel frekans aralıkları
- **Spektral Özellikler**: Vibrato, glissando tespiti
- **Karadeniz Enstrümanları**: Kemençe, tulum, davul için özel tespit
- **Enstrüman Skorları**: Her enstrüman için güven skoru

#### 🎵 Karadeniz Karakteristikleri
- **Kemençe Stili**: Vibrato, expressif, melodic
- **Tulum Stili**: Sürekli ton, drone-like, melodic
- **Ritim Stili**: Geleneksel Karadeniz ritim pattern'leri
- **Genre Confidence**: Genre tespit güven skoru

## 📝 Kullanım

### 1. Sadece Analiz Yapma

```bash
python src/detailed_audio_analyzer.py "path/to/audio.mp3" --generate
```

**Çıktı:**
- Tempo, key, mode
- Ritim pattern analizi
- Dinamik analiz
- Spektral özellikler
- Enstrüman tespiti
- Karadeniz karakteristikleri
- **Otomatik prompt oluşturma**

### 2. Analiz + Müzik Üretimi

```bash
python src/generate_from_detailed_analysis.py "path/to/audio.mp3" \
  --model medium \
  --variations 3 \
  --duration 30 \
  --guidance 3.5
```

**Adımlar:**
1. ✅ Detaylı analiz yapılır
2. ✅ Analiz sonuçlarından prompt oluşturulur
3. ✅ Prompt iyileştirilir (yanlış tespitler temizlenir)
4. ✅ Müzik üretilir (multiple generation + best selection)
5. ✅ Otomatik mastering uygulanır

## 🎯 Analiz Sonuçları Örneği

```
📊 Analysis Components:

1️⃣  TEMPO ANALYSIS
   ⏱️  Tempo: 91 BPM

2️⃣  MELODIC STRUCTURE
   🎹 Key: B minor (confidence: 0.52)
   📈 Melodic direction: ascending

3️⃣  RHYTHM PATTERN
   🥁 Time signature: 4/4
   🎯 Rhythmic complexity: medium
   🎵 Groove: steady, traditional

4️⃣  DYNAMICS
   🔊 Energy level: high
   📊 Dynamic range: 0.352
   📈 Energy contour: increasing

5️⃣  SPECTRAL FEATURES
   🎨 Brightness: bright
   🎵 Harmonic ratio: 0.91
   📊 Spectral centroid: 3593 Hz

6️⃣  INSTRUMENT DETECTION
   🎸 Detected instruments:
      1. davul: 27.862
      2. bass: 16.513
      3. vocals: 14.706
      4. kemenche: 12.345
      5. tulum: 8.901

7️⃣  KARADENIZ CHARACTERISTICS
   ✅ Kemenche detected: melodic, clear
   ✅ Tulum detected: melodic, dynamic
   ✅ Davul detected
   🎵 Rhythm style: traditional Karadeniz rhythm, strong beat, driving

8️⃣  GENRE ESTIMATION
   🎵 Estimated genre: karadeniz (confidence: 0.90)
```

## 📝 Oluşturulan Prompt Örneği

```
Turkish Black Sea folk music, Karadeniz müziği, 
authentic traditional Karadeniz style, 
davul (traditional Turkish drum), drums, bass guitar, vocals, 
kemenche melodic, clear, tulum melodic, dynamic, 
traditional Karadeniz rhythm, strong beat, driving, 
91 BPM, time signature 4/4, medium rhythmic complexity, 
steady, traditional, key of B minor, ascending melodic contour, 
high energy, increasing energy contour, bright timbre, 
harmonic, melodic, professional production, 
clear instrument separation, balanced mix, authentic sound
```

## 🔧 Parametreler

### `detailed_audio_analyzer.py`
- `--skip`: Başlangıçtan kaç saniye atla (default: 5)
- `--duration`: Analiz süresi (default: 120 saniye)
- `--generate`: Analiz sonrası prompt oluştur
- `--output`: Analiz sonuçlarını JSON olarak kaydet

### `generate_from_detailed_analysis.py`
- `--model`: Model boyutu (small/medium/large)
- `--duration`: Üretilecek müzik süresi (saniye)
- `--guidance`: Guidance scale (1.0-10.0)
- `--variations`: Kaç versiyon üret (en iyisini seçer)
- `--seed`: Random seed (reproducible results)
- `--no-master`: Mastering uygulama

## 🎵 Karadeniz Müziği için Özel Özellikler

### Kemençe Tespiti
- **Frekans Aralığı**: 800-2500 Hz
- **Karakteristikler**: Yüksek spektral centroid, vibrato tespiti
- **Stil**: "melodic, clear" veya "with vibrato, expressive"

### Tulum Tespiti
- **Frekans Aralığı**: 400-1800 Hz
- **Karakteristikler**: Düşük varyans (sürekli ton)
- **Stil**: "sustained, drone-like" veya "melodic, dynamic"

### Davul Tespiti
- **Frekans Aralığı**: 50-300 Hz
- **Karakteristikler**: Ritmik pattern, güçlü vuruşlar
- **Stil**: "traditional Turkish drum"

### Ritim Pattern
- **Tempo**: 85-110 BPM (Karadeniz için tipik)
- **Groove**: "traditional Karadeniz rhythm, strong beat, driving"
- **Complexity**: Medium (geleneksel Karadeniz müziği için)

## 📊 Analiz Sonuçlarını JSON Olarak Kaydetme

```bash
python src/detailed_audio_analyzer.py "audio.mp3" \
  --output analysis_results.json
```

**JSON Yapısı:**
```json
{
  "tempo": 91,
  "melodic": {
    "key": "B",
    "mode": "minor",
    "key_confidence": 0.52,
    "melodic_direction": "ascending"
  },
  "rhythm": {
    "time_signature": "4/4",
    "rhythmic_complexity": "medium",
    "groove_type": "steady, traditional"
  },
  "dynamics": {
    "energy_level": "high",
    "dynamic_range": 0.352,
    "energy_contour": "increasing"
  },
  "spectral": {
    "brightness": "bright",
    "harmonic_ratio": 0.91,
    "spectral_centroid": 3593.0
  },
  "instruments": ["davul", "bass", "vocals", "kemenche", "tulum"],
  "karadeniz_characteristics": {
    "has_kemenche": true,
    "has_tulum": true,
    "has_davul": true,
    "kemenche_style": "melodic, clear",
    "tulum_style": "melodic, dynamic",
    "rhythm_style": "traditional Karadeniz rhythm, strong beat, driving"
  },
  "estimated_genre": "karadeniz",
  "genre_confidence": 0.90
}
```

## 🎯 Sonuç

Artık sistem:
- ✅ **Çok daha detaylı analiz** yapıyor
- ✅ **Melodik yapıyı** tespit ediyor
- ✅ **Ritim pattern'lerini** analiz ediyor
- ✅ **Dinamikleri** ölçüyor
- ✅ **Spektral özellikleri** analiz ediyor
- ✅ **Karadeniz karakteristiklerini** tespit ediyor
- ✅ **Çok spesifik prompt'lar** oluşturuyor
- ✅ **Daha iyi müzik üretimi** sağlıyor

**Kullanmaya başlayın:**
```bash
python src/generate_from_detailed_analysis.py "your_audio.mp3"
```

