# 🎨 Neural Beats Studio Logo Kullanım Rehberi

## ✅ Oluşturulan Logolar

### 1. PNG Logo (Profil Resmi)
- **Dosya**: `assets/neural_beats_studio_logo.png`
- **Kullanım**: Profil resmi, statik görüntüler
- **Platformlar**: Instagram, TikTok, YouTube, Twitter/X

### 2. MP4 Logo (Hareketli Logo)
- **Dosya**: `assets/neural_beats_studio_logo.mp4`
- **Kullanım**: Video içerikler, intro/outro, watermark
- **Platformlar**: YouTube, TikTok, Instagram Reels, Stories

## 📱 Platform Bazlı Kullanım

### Instagram
**Profil Resmi:**
- Dosya: `neural_beats_studio_logo.png`
- Boyut: 110x110 px (minimum), 1024x1024 px (önerilen)
- Format: PNG

**Stories/Reels:**
- Dosya: `neural_beats_studio_logo.mp4`
- Format: MP4
- Süre: Kısa loop (3-5 saniye)

### TikTok
**Profil Resmi:**
- Dosya: `neural_beats_studio_logo.png`
- Boyut: 200x200 px (minimum)

**Video Watermark:**
- Dosya: `neural_beats_studio_logo.mp4`
- Konum: Köşe (sağ alt veya sol üst)
- Opacity: %50-70 (görünür ama rahatsız etmeyen)

### YouTube
**Kanal İkonu:**
- Dosya: `neutral_beats_studio_logo.png`
- Boyut: 800x800 px (minimum), 1024x1024 px (önerilen)

**Video Intro/Outro:**
- Dosya: `neural_beats_studio_logo.mp4`
- Süre: 3-5 saniye
- Konum: Video başında veya sonunda

**Watermark:**
- Dosya: `neural_beats_studio_logo.png` (statik)
- Konum: Sağ alt köşe
- YouTube otomatik watermark özelliği kullanılabilir

### Twitter/X
**Profil Resmi:**
- Dosya: `neural_beats_studio_logo.png`
- Boyut: 400x400 px (minimum)

## 🎬 Video İçeriklerde Kullanım

### Intro Olarak
```bash
# Video başına logo ekleme (FFmpeg ile)
ffmpeg -i input_video.mp4 -i assets/neural_beats_studio_logo.mp4 \
  -filter_complex "[0:v][1:v]overlay=10:10:shortest=1" \
  -c:v libx264 -c:a copy output_with_logo.mp4
```

### Watermark Olarak
```bash
# Sağ alt köşeye logo ekleme
ffmpeg -i input_video.mp4 -i assets/neural_beats_studio_logo.png \
  -filter_complex "[0:v][1:v]overlay=W-w-10:H-h-10" \
  -c:v libx264 -c:a copy output_with_watermark.mp4
```

### Outro Olarak
```bash
# Video sonuna logo ekleme
ffmpeg -i input_video.mp4 -i assets/neural_beats_studio_logo.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1[outv]" \
  -map "[outv]" -c:v libx264 output_with_outro.mp4
```

## 🎨 Logo Özellikleri

### Tasarım Detayları
- **Ses Dalgası Grafikleri**: Mavi-cyan gradient, dinamik görünüm
- **Text**: "NEURAL BEATS STUDIO ENTERTAINMENT"
- **Renkler**: Mor tonları, mavi-cyan gradient, beyaz text
- **Stil**: Modern, profesyonel, müzik temalı

### Kullanım İpuçları
1. **Profil Resmi**: PNG versiyonunu kullanın
2. **Video İçerikler**: MP4 versiyonunu kullanın
3. **Watermark**: PNG versiyonunu kullanın (daha küçük, şeffaf)
4. **Intro/Outro**: MP4 versiyonunu kullanın

## 📋 Checklist

- [x] PNG logo oluşturuldu
- [x] MP4 logo oluşturuldu
- [ ] Instagram profil resmi yüklendi
- [ ] TikTok profil resmi yüklendi
- [ ] YouTube kanal ikonu yüklendi
- [ ] Twitter/X profil resmi yüklendi
- [ ] Video içeriklerde watermark kullanıldı

## 🎉 Hazır!

Logolarınız hazır ve kullanıma uygun. Sosyal medya hesaplarınıza yükleyebilir ve video içeriklerinizde kullanabilirsiniz!

