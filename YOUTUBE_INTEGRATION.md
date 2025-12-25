# 🎵 YouTube Entegrasyonu

## ✅ Özellik

Sistem artık **YouTube linklerinden direkt müzik analizi yapabilir**! Manuel indirme gerekmez.

## 🚀 Kullanım

### YouTube Link ile Analiz ve Üretim

```bash
# YouTube link'inden benzer müzik üret
python src/audio_analyzer.py "https://www.youtube.com/watch?v=..." --duration 30

# Sadece analiz
python src/audio_analyzer.py "https://www.youtube.com/watch?v=..." --analyze-only

# Mastering ile
python src/audio_analyzer.py "https://www.youtube.com/watch?v=..." --master
```

### Yerel Dosya ile (Eski Yöntem)

```bash
# Yerel dosya ile
python src/audio_analyzer.py output/track.wav --duration 30
```

## 📋 Desteklenen Formatlar

### YouTube URL Formatları:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

### Yerel Dosya Formatları:
- `.wav`
- `.mp3`
- `.m4a`
- `.flac`
- Diğer librosa destekleyen formatlar

## ⚙️ Nasıl Çalışır?

1. **YouTube URL Tespiti**: Sistem otomatik olarak YouTube URL'si mi yoksa yerel dosya mı olduğunu anlar
2. **Audio İndirme**: `yt-dlp` ile YouTube'dan audio indirilir
3. **Geçici Kayıt**: İlk 60 saniye geçici olarak kaydedilir (analiz için yeterli)
4. **Analiz**: Audio analiz edilir
5. **Benzer Müzik**: MusicGen ile benzer müzik üretilir
6. **Temizlik**: Geçici dosya otomatik silinir (opsiyonel)

## 🔧 Parametreler

- `--keep-temp`: Geçici dosyaları sakla (debug için)
- `--analyze-only`: Sadece analiz, müzik üretme
- `--duration`: Üretilecek müzik süresi
- `--similarity`: Benzerlik seviyesi (`high`, `medium`, `low`)
- `--master`: Otomatik mastering

## ⚠️ Önemli Notlar

1. **İnternet Gerekli**: YouTube'dan indirme için internet bağlantısı gerekli
2. **FFmpeg Gerekli**: Audio dönüştürme için FFmpeg gerekli (yt-dlp ile birlikte gelir)
3. **Telif Hakları**: YouTube'dan indirilen içeriklerin telif haklarına dikkat edin
4. **Geçici Dosyalar**: Varsayılan olarak geçici dosyalar otomatik silinir

## 💡 İpuçları

1. **Kısa Videolar**: Analiz için ilk 60 saniye yeterli
2. **Temiz Audio**: Müzik videoları daha iyi sonuç verir (konuşma içermeyen)
3. **Geçici Dosyalar**: Debug için `--keep-temp` kullanın
4. **Hızlı Test**: `--analyze-only` ile önce analiz sonuçlarını kontrol edin

## 🐛 Sorun Giderme

### yt-dlp Bulunamadı
```bash
pip install yt-dlp
```

### FFmpeg Hatası
**Windows Kurulumu**:
1. Chocolatey: `choco install ffmpeg`
2. Winget: `winget install ffmpeg`
3. Manuel: https://www.gyan.dev/ffmpeg/builds/ adresinden indirip PATH'e ekle

Detaylı kurulum: `FFMPEG_INSTALL.md` dosyasına bakın.

**Linux/Mac**:
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

### İndirme Hatası
- İnternet bağlantınızı kontrol edin
- Video erişilebilir mi kontrol edin
- Video yaşı sınırlaması olabilir

## 📊 Örnek Kullanım

```bash
# Pop müziği analiz et ve benzer üret
python src/audio_analyzer.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --duration 30 \
  --similarity high \
  --master

# Sadece analiz
python src/audio_analyzer.py "https://www.youtube.com/watch?v=..." --analyze-only
```

## 🎯 Sonuç

Artık hem YouTube linkleri hem de yerel dosyalar kullanılabilir! 🎉

