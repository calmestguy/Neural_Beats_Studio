# 🎬 FFmpeg Kurulum Rehberi (Windows)

## ⚠️ Neden Gerekli?

YouTube'dan indirilen audio dosyaları genelde `.webm` formatında olur. Bunları `.wav` formatına çevirmek için FFmpeg gerekli.

## 🚀 Hızlı Kurulum (Önerilen)

### Yöntem 1: Chocolatey ile (En Kolay)

```powershell
# Chocolatey yüklüyse
choco install ffmpeg
```

### Yöntem 2: Manuel Kurulum

1. **FFmpeg İndir**:
   - https://www.gyan.dev/ffmpeg/builds/ adresine git
   - "ffmpeg-release-essentials.zip" indir

2. **Kur**:
   - ZIP'i aç (örn: `C:\ffmpeg`)
   - `bin` klasörünü PATH'e ekle:
     - Windows Ayarlar → Sistem → Gelişmiş Sistem Ayarları
     - Ortam Değişkenleri → Path → Yeni
     - `C:\ffmpeg\bin` ekle

3. **Test Et**:
   ```powershell
   ffmpeg -version
   ```

### Yöntem 3: Winget ile (Windows 10/11)

```powershell
winget install ffmpeg
```

## ✅ Kurulum Kontrolü

```powershell
ffmpeg -version
ffprobe -version
```

Her iki komut da çalışıyorsa kurulum başarılı!

## 🔄 Alternatif: FFmpeg Olmadan

FFmpeg yoksa sistem şu an webm formatını direkt kullanamıyor. İki seçenek:

1. **FFmpeg kur** (önerilen)
2. **Manuel indirme**: YouTube'dan manuel olarak MP3/WAV indirip kullan

## 📝 Not

FFmpeg kurulumu sonrası sistemi yeniden başlatmanız gerekebilir (PATH güncellemesi için).



