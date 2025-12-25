# ⚠️ YouTube Video Yükleme Limitleri

## 📊 Günlük Yükleme Limitleri

YouTube'un günlük video yükleme limitleri vardır:

### Yeni Kanallar (Doğrulanmamış)
- **Limit**: 15 video/gün
- **Açıklama**: İlk 24 saat içinde yeni oluşturulmuş kanallar için

### Doğrulanmış Kanallar
- **Limit**: 50+ video/gün (genellikle)
- **Açıklama**: Telefon numarası ile doğrulanmış kanallar için

### Premium/Partner Kanallar
- **Limit**: Daha yüksek limitler (kanal durumuna göre)

## 🔍 Limit Kontrolü

Eğer şu hatayı alıyorsanız:

```
The user has exceeded the number of videos they may upload.
reason: uploadLimitExceeded
```

Bu, günlük yükleme limitinizi aştığınız anlamına gelir.

## ✅ Çözümler

### 1. 24 Saat Bekleyin
- Limit her 24 saatte bir sıfırlanır
- Ertesi gün tekrar deneyin

### 2. Kanalınızı Doğrulayın
- https://www.youtube.com/verify adresine gidin
- Telefon numaranızı doğrulayın
- Doğrulanmış kanallar daha yüksek limitlere sahiptir

### 3. Videoları Yayınlamayın
- Videoları "Private" veya "Unlisted" olarak yükleyin
- Daha sonra toplu olarak "Public" yapabilirsiniz

### 4. Toplu Yükleme Planlaması
- Günlük limiti aşmamak için videoları planlayın
- Örneğin: Günde 10-15 video yükleyin

## 🔐 Yetki (Permission) Sorunları

Eğer şu hatayı alıyorsanız:

```
Insufficient Permission
reason: insufficientPermissions
```

### Çözüm: Token'ı Yeniden Oluşturun

1. **token.json dosyasını silin**:
   ```powershell
   Remove-Item token.json
   ```

2. **Uygulamayı tekrar çalıştırın**:
   ```powershell
   python src/social_media_uploader.py
   ```

3. **YouTube API'ye tekrar bağlanın**:
   - "Bağlan" butonuna tıklayın
   - Tarayıcıda tüm izinleri onaylayın
   - Özellikle şu izinleri onaylayın:
     - ✅ YouTube'a video yükleme
     - ✅ YouTube kanalınızı görüntüleme (duplicate kontrolü için)

## 📝 Notlar

- Limitler kanal durumuna göre değişir
- YouTube, limitleri zaman zaman günceller
- Çok fazla video yüklerseniz, YouTube geçici olarak limiti düşürebilir
- Toplu yükleme yaparken limitlere dikkat edin

## 🆘 Sorun Giderme

### "Upload limit exceeded" Hatası

1. **Kontrol edin**: Bugün kaç video yüklediniz?
2. **Bekleyin**: 24 saat sonra tekrar deneyin
3. **Doğrulayın**: Kanalınızı doğrulayın

### "Insufficient permissions" Hatası

1. **Token'ı silin**: `token.json` dosyasını silin
2. **Yeniden bağlanın**: Uygulamada "Bağlan" butonuna tıklayın
3. **İzinleri onaylayın**: Tüm izinleri onaylayın

### Duplicate Kontrolü Çalışmıyor

1. **Token'ı yenileyin**: `token.json` dosyasını silin ve yeniden bağlanın
2. **Scope kontrolü**: `youtube.readonly` scope'unun aktif olduğundan emin olun
3. **Manuel kontrol**: YouTube Studio'da videoları kontrol edin

## 🔗 İlgili Linkler

- [YouTube Kanal Doğrulama](https://www.youtube.com/verify)
- [YouTube API Quotas](https://developers.google.com/youtube/v3/getting-started#quota)
- [YouTube Upload Limits](https://support.google.com/youtube/answer/71673)

