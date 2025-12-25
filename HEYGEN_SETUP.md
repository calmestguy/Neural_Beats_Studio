# 🎤 HeyGen Tam Vücut Avatar Kurulum Rehberi

## ✅ HeyGen Özellikleri

- ✅ **Tam Vücut Avatar**: Gövdenin yarısı görünür
- ✅ **Saç Fizik Simülasyonu**: Saçlar doğal hareket eder
- ✅ **Vücut Hareketleri**: El-kol hareketleri, duruş
- ✅ **Gerçekçi Lip-Sync**: Şarkı sözleri ile senkronize
- ✅ **Saç Özelleştirme**: Renk, stil seçimi
- ✅ **Yüksek Kalite**: 1080p-4K çözünürlük

## 🚀 Kurulum

### 1. HeyGen Hesabı Oluştur

1. **Website**: https://www.heygen.com/
2. **Sign Up** butonuna tıklayın
3. Ücretsiz deneme hesabı oluşturun

### 2. API Key Alın

1. Dashboard'a giriş yapın
2. **Settings** → **API Keys**
3. **Create New API Key** tıklayın
4. Key'i kopyalayın

### 3. Avatar Seçin

1. **Avatars** sekmesine gidin
2. **Full Body** avatarları filtreleyin
3. İstediğiniz avatar'ı seçin
4. **Avatar ID**'yi kopyalayın

**Önemli**: Tam vücut avatar seçtiğinizden emin olun!

### 4. Avatar Özelleştirme

- **Saç Rengi**: Blonde, brunette, black, red, vb.
- **Saç Stili**: Long, short, wavy, straight, vb.
- **Kıyafet**: Profesyonel, casual, vb.
- **Duruş**: Mikrofon karşısında, sahne, vb.

## 📋 Kullanım

### Avatar Listesi

```bash
python src/heygen_integration.py \
  --list-avatars \
  --api-key YOUR_HEYGEN_API_KEY
```

Bu komut mevcut avatarları listeler ve tam vücut avatarları gösterir.

### Video Oluşturma

```bash
python src/heygen_integration.py \
  --avatar-id YOUR_AVATAR_ID \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --background assets/rainy_city_blues_lyrics_background.jpg \
  --api-key YOUR_HEYGEN_API_KEY \
  --output output/singer_full_body_video.mp4
```

### Video Durum Kontrolü

```bash
python src/heygen_integration.py \
  --check VIDEO_ID \
  --api-key YOUR_HEYGEN_API_KEY
```

## 🎨 Tam Vücut Avatar Özellikleri

### Saç Fizik Simülasyonu

HeyGen avatarları saç fizik simülasyonu içerir:
- Saçlar doğal hareket eder
- Rüzgar efektleri
- Baş hareketleri ile senkronize

### Vücut Hareketleri

- El-kol hareketleri
- Mikrofon tutma pozisyonu
- Şarkı söylerken doğal duruş
- Gövde hareketleri

### Lip-Sync

- Şarkı sözleri ile mükemmel senkronizasyon
- Duygusal ifadeler
- Doğal dudak hareketleri

## 💰 Fiyatlandırma

- **Free Trial**: Sınırlı kullanım
- **Starter**: ~$24/month
- **Professional**: ~$89/month
- **Enterprise**: Özel fiyatlandırma

**Not**: API kullanımı için ayrı fiyatlandırma olabilir.

## 🔄 Alternatif: Animate Anyone (Ücretsiz)

Eğer HeyGen pahalı geliyorsa:

### Kurulum

```bash
git clone https://github.com/magic-research/AnimateAnyone.git
cd AnimateAnyone
pip install -r requirements.txt
```

### Kullanım

```bash
python inference.py \
  --source_image singer_full_body.jpg \
  --reference_video reference_dancing.mp4 \
  --audio singing_vocal.wav \
  --output output/singer_full_body_video.mp4
```

**Avantajlar:**
- Ücretsiz
- Tam kontrol
- Açık kaynak

**Dezavantajlar:**
- Kurulumu zor
- GPU gerekli (8GB+)
- Lip-sync ayrı eklenmeli

## 🎯 Öneriler

### En İyi Sonuç İçin:

1. **HeyGen Kullanın** (en kolay, en iyi)
2. **Tam Vücut Avatar** seçin
3. **Saç Fizik Aktif** edin
4. **Yüksek Kalite** ayarları kullanın
5. **Uygun Arka Plan** ekleyin

### Avatar Seçimi:

- **Müzik Temalı**: Mikrofon karşısında poz
- **Profesyonel**: Stüdyo ortamı
- **Sahne**: Konser ortamı
- **Casual**: Rahat, doğal

## 📊 Karşılaştırma

| Özellik | HeyGen | Animate Anyone |
|---------|--------|----------------|
| **Tam Vücut** | ✅✅✅ | ✅✅✅ |
| **Saç Fizik** | ✅✅✅ | ✅✅ |
| **Lip-Sync** | ✅✅✅ | ❌ |
| **Kurulum** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Maliyet** | Ücretli | Ücretsiz |
| **Kalite** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🎉 Sonuç

**HeyGen** tam vücut şarkıcı avatar için en iyi çözüm:
- Saç fizik simülasyonu
- Vücut hareketleri
- Gerçekçi lip-sync
- Kolay kullanım

**Alternatif**: Animate Anyone (ücretsiz ama zor)

