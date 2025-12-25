# 🎤 Vokal Ekleme - Önemli Notlar

## ⚠️ Gerçekçi Beklentiler

**Şarkı sözlerini müziğe eklemek mümkün, AMA:**

1. **Bu şarkı söylemez, konuşur**: TTS (Text-to-Speech) kullanıyoruz, bu yüzden çıktı şarkı gibi değil, konuşma gibi olacak.

2. **Profesyonel şarkı kalitesi değil**: Gerçek şarkı söyleyen AI modelleri (Suno AI, Musicfy) var ama bunlar ayrı servisler ve ücretli.

3. **İnternet gerekli**: Google TTS kullanıyoruz, bu yüzden internet bağlantısı gerekli.

## 🎯 Kullanım

### Otomatik (Şarkı sözlerinden müzik + vokal):
```bash
python src/lyrics_to_music.py --lyrics-file example_lyrics.txt --add-vocals --duration 30
```

### Manuel (Mevcut müziğe vokal ekle):
```bash
python src/add_vocals.py output/music.wav --lyrics-file lyrics.txt --vocal-volume 0.7
```

## 🔧 Parametreler

- `--vocal-volume`: Vokal ses seviyesi (0-1, default: 0.7)
- `--music-volume`: Müzik ses seviyesi (0-1, default: 0.8)
- `--lang`: Dil kodu ('tr' = Türkçe, 'en' = İngilizce)
- `--fast`: Hızlı konuşma (varsayılan: yavaş, şarkı için daha uygun)

## 💡 Daha İyi Sonuçlar İçin

1. **Şarkı sözlerini kısa tutun**: Çok uzun sözler müziğe sığmayabilir
2. **Vokal ses seviyesini ayarlayın**: Müziğin üzerinde duyulacak şekilde
3. **Yavaş konuşma kullanın**: `--fast` kullanmayın, daha şarkı gibi olur

## 🚀 Gelecek İyileştirmeler

- Coqui TTS entegrasyonu (daha kaliteli, offline)
- Pitch shifting (nota ayarlama)
- Reverb/echo efektleri
- Gerçek şarkı söyleyen AI entegrasyonu (Suno API, vb.)

## ⚠️ Sınırlamalar

- TTS şarkı söylemez, sadece konuşur
- Melodi/nota takibi yok
- Duygusal tonlama sınırlı
- İnternet bağlantısı gerekli (Google TTS için)



