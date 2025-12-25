# 🎵 Audio Analizi ve Benzer Müzik Üretimi Rehberi

## 🎯 Özellik

Sistem artık **mevcut müzik dosyalarını analiz edip benzer müzik üretebilir**!

## 🔍 Nasıl Çalışır?

1. **Audio Analizi**: Müzik dosyasını analiz eder
   - Tempo tespiti
   - Enstrüman tespiti (frekans analizi)
   - Müzik türü tahmini
   - Enerji seviyesi
   - Bas vurgusu

2. **Prompt Oluşturma**: Analiz sonuçlarından prompt oluşturur
   - Tespit edilen enstrümanlar
   - Tempo
   - Müzik türü
   - Enerji seviyesi

3. **Benzer Müzik Üretimi**: MusicGen ile benzer müzik üretir

## 📊 Analiz Edilen Özellikler

### Tempo
- BPM (Beats Per Minute) tespiti
- Müzik türüne göre uygun tempo aralığı

### Enstrümanlar
Tespit edilen enstrümanlar:
- **Bass**: 20-250 Hz
- **Drums**: Kick (20-100 Hz), Snare (100-300 Hz), Hi-hat (2-15 kHz)
- **Guitar**: 80-2000 Hz (akustik), 80-5000 Hz (elektrik)
- **Piano**: 27-4186 Hz
- **Strings**: Violin (196-2637 Hz), Cello (65-987 Hz)
- **Brass**: Trumpet (165-1175 Hz), Saxophone (110-880 Hz)
- **Synthesizer**: Geniş aralık (20-20000 Hz)

### Müzik Türü Tahmini
Karakteristiklere göre tahmin:
- **Rock**: Yüksek tempo, güçlü bas, gitar, davul
- **Pop**: Orta tempo, synthesizer, bas
- **Jazz**: Değişken tempo, piyano, saksafon
- **Electronic**: Yüksek tempo, synthesizer, bas, davul
- **Classical**: Değişken tempo, strings, piyano
- **Blues**: Düşük-orta tempo, gitar, bas

### Enerji Seviyesi
- **High**: Yüksek RMS enerjisi
- **Medium**: Orta RMS enerjisi
- **Low**: Düşük RMS enerjisi

## 🚀 Kullanım Örnekleri

### Örnek 1: Basit Analiz ve Üretim
```bash
python src/audio_analyzer.py output/track.wav --duration 30
```

### Örnek 2: Yüksek Benzerlik
```bash
python src/audio_analyzer.py output/track.wav --similarity high --master
```

### Örnek 3: Sadece Analiz
```bash
python src/audio_analyzer.py output/track.wav --analyze-only
```

### Örnek 4: Farklı Model
```bash
python src/audio_analyzer.py output/track.wav --model medium --duration 30
```

## 📈 Çıktı Örneği

```
🔍 Analyzing audio: output/track.wav

📊 Analysis Results:
   Tempo: 120 BPM
   Estimated Key: B
   Estimated Genre: rock
   Detected Instruments: kick_drum, bass, vocals, snare_drum, cello
   Energy Level: high
   Bass Prominent: True

🎵 Generated Prompt: rock music, drums, bass, vocals, drums, 120 BPM, 
   energetic, powerful, strong bass, deep bass line, similar style, 
   matching characteristics, modern production

🎵 Generating 1 track(s)...
✅ Similar music generated: output/track_20251130_132450_00.wav
```

## ⚙️ Parametreler

- `--similarity`: Benzerlik seviyesi (`high`, `medium`, `low`)
- `--duration`: Üretilecek müzik süresi (saniye)
- `--model`: Model boyutu (`small`, `medium`, `large`)
- `--master`: Otomatik mastering
- `--analyze-only`: Sadece analiz, müzik üretme

## 🎯 Benzerlik Seviyeleri

### High (Yüksek)
- Aynı tempo
- Aynı enstrümanlar
- Aynı enerji seviyesi
- "similar style, matching characteristics" eklenir

### Medium (Orta)
- Benzer tempo
- Benzer enstrümanlar
- "inspired by, similar vibe" eklenir

### Low (Düşük)
- Sadece müzik türü bazlı
- Temel karakteristikler

## ⚠️ Sınırlamalar

1. **Enstrüman Tespiti**: Frekans analizi bazlı, %100 doğru değil
2. **Müzik Türü**: Tahmin, kesin değil
3. **Tempo**: Bazen yanlış tespit edilebilir
4. **Karmaşık Müzikler**: Çok enstrümanlı müziklerde zorlanabilir

## 💡 İpuçları

1. **Temiz Audio**: Daha iyi analiz için temiz kayıtlar kullanın
2. **Uzunluk**: En az 10-15 saniye analiz için yeterli
3. **Benzerlik**: `high` seviyesi daha benzer sonuçlar verir
4. **Mastering**: Analiz sonrası mastering ekleyin

## 🔮 Gelecek İyileştirmeler

- [ ] Daha gelişmiş enstrüman tespiti (ML modeli)
- [ ] Akor tespiti
- [ ] Melodi analizi
- [ ] Daha doğru müzik türü tespiti
- [ ] Audio continuation (müziği devam ettirme)



