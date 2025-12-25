# 🎬 4K Kadın Şarkıcı Video Oluşturma - Hızlı Rehber

## 🎯 İhtiyacınız Olan

1. **Ses dosyası** (vokal) - Zaten var: `rainy_city_blues_lyrics_singing_vocal.wav`
2. **Kadın şarkıcı fotoğrafı** - İnternetten bulabilirsiniz veya kendi fotoğrafınızı kullanabilirsiniz
3. **Video oluşturma aracı** - Aşağıdaki seçeneklerden biri

---

## ⚡ En Hızlı Çözüm: D-ID (5 Dakika)

### Adımlar:

1. **D-ID Hesabı Oluştur**
   - https://www.d-id.com/ adresine gidin
   - Ücretsiz hesap oluşturun (deneme kredisi var)

2. **API Key Alın**
   - Dashboard'dan API key'inizi kopyalayın

3. **Ses Dosyasını Upload Edin**
   - D-ID platformunda ses dosyanızı yükleyin
   - Veya direkt URL kullanın

4. **Avatar Seçin**
   - Kadın şarkıcı avatar'ı seçin
   - Duygusal ifadeleri ayarlayın

5. **Video Oluşturun**
   - "Create Video" butonuna tıklayın
   - 4K çözünürlük seçin
   - İndirin

**Süre:** ~5 dakika  
**Maliyet:** ~$0.10-0.50 per video (deneme kredisi var)

---

## 🆓 Ücretsiz Çözüm: SadTalker (30 Dakika Kurulum)

### Kurulum:

```bash
# 1. SadTalker'ı klonla
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Modelleri indir
# GitHub sayfasındaki linklerden checkpoint'leri indirin
# checkpoints/ klasörüne yerleştirin
```

### Kullanım:

```bash
# Proje dizinine dön
cd ..

# Kadın şarkıcı fotoğrafı hazırla (örn: assets/female_singer.jpg)
# Sonra çalıştır:

python src/sadtalker_integration.py \
  --image assets/female_singer.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --lyrics rainy_city_blues_lyrics.txt \
  --resolution 4k
```

**Süre:** İlk kurulum ~30 dakika, sonraki kullanımlar ~5-10 dakika  
**Maliyet:** Ücretsiz

---

## 🎨 Kadın Şarkıcı Fotoğrafı Nereden Bulunur?

1. **Unsplash/Pexels** (Ücretsiz, telif hakkı yok):
   - https://unsplash.com/s/photos/female-singer
   - https://www.pexels.com/search/woman-singer/

2. **Kendi Fotoğrafınız**:
   - Kendi fotoğrafınızı kullanabilirsiniz
   - Veya AI ile oluşturabilirsiniz (Midjourney, DALL-E)

3. **AI Avatar Oluşturucu**:
   - https://www.thispersondoesnotexist.com/ (rastgele)
   - https://generated.photos/ (AI generated)

**Önemli:** Fotoğraf yüz net görünmeli, iyi ışıklandırılmış olmalı

---

## 📋 Adım Adım: D-ID ile (Önerilen)

### 1. D-ID'ye Giriş Yapın
```
https://www.d-id.com/
→ Sign Up (ücretsiz)
```

### 2. API Key Alın
```
Dashboard → API Keys → Create New Key
→ Key'i kopyalayın
```

### 3. Video Oluşturun
```
Create → Talking Avatar
→ Avatar seçin (kadın şarkıcı)
→ Audio upload: rainy_city_blues_lyrics_singing_vocal.wav
→ Settings: 4K resolution
→ Create Video
```

### 4. İndirin
```
Video hazır olunca → Download
→ 4K MP4 formatında indirin
```

---

## 📋 Adım Adım: SadTalker ile (Ücretsiz)

### 1. SadTalker Kurun
```bash
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
pip install -r requirements.txt
```

### 2. Modelleri İndirin
- GitHub sayfasından checkpoint'leri indirin
- `checkpoints/` klasörüne yerleştirin

### 3. Kadın Şarkıcı Fotoğrafı Hazırlayın
- Unsplash'tan indirin veya kendi fotoğrafınızı kullanın
- `assets/female_singer.jpg` olarak kaydedin

### 4. Video Oluşturun
```bash
cd ..  # Proje dizinine dön

python src/sadtalker_integration.py \
  --image assets/female_singer.jpg \
  --audio rainy_city_blues_lyrics_singing_vocal.wav \
  --lyrics rainy_city_blues_lyrics.txt \
  --resolution 4k \
  --output output/singing_video.mp4
```

---

## 🎭 Duygusal İfadeler

Şarkı sözlerinizden otomatik duygu tespiti yapılır:

- **"Rainy City Blues"** → `sad` (üzgün, melankolik)
- **Neşeli şarkılar** → `happy` (mutlu, neşeli)
- **Sürprizli şarkılar** → `surprised` (şaşkın)

Manuel olarak da belirtebilirsiniz:
```bash
--emotion sad  # veya happy, surprised, angry, neutral
```

---

## ⚙️ Çözünürlük Seçenekleri

- `512` - Hızlı, düşük kalite
- `1024` - Orta kalite
- `4k` - En yüksek kalite (önerilen)

---

## 💡 İpuçları

1. **Fotoğraf Kalitesi**: Yüksek çözünürlüklü, net fotoğraf kullanın
2. **Işıklandırma**: İyi aydınlatılmış yüz fotoğrafları daha iyi sonuç verir
3. **Pozisyon**: Yüz tam görünmeli, yan profil değil
4. **Ses Kalitesi**: Temiz, gürültüsüz ses dosyası kullanın
5. **Duygu**: Şarkı sözlerine uygun duygu seçin

---

## 🚀 Hemen Başlayın

### D-ID ile (En Hızlı):
1. https://www.d-id.com/ → Sign Up
2. Avatar seç → Audio upload
3. 4K video oluştur → İndir

### SadTalker ile (Ücretsiz):
1. `git clone https://github.com/OpenTalker/SadTalker.git`
2. Kurulum yap
3. `python src/sadtalker_integration.py --help` ile başla

---

## 📞 Yardım

Sorun yaşarsanız:
- D-ID: https://docs.d-id.com/
- SadTalker: https://github.com/OpenTalker/SadTalker/issues


