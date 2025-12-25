"""
Hızlı Video Oluşturma - D-ID API veya Alternatif
Kullanıcıya hızlı sonuç vermek için
"""

import os
import sys

# Windows encoding fix
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("="*70)
print("[VIDEO] SARKICI VOKAL VIDEOSU OLUSTURMA")
print("="*70)
print()

# Mevcut dosyaları kontrol et
audio_file = "rainy_city_blues_lyrics_singing_vocal.wav"
image_file = "assets/female_singer_main.jpg"
lyrics_file = "rainy_city_blues_lyrics.txt"

print("[FILES] Dosya Kontrolu:")
files_ok = True
for file, name in [(audio_file, "Vokal"), (image_file, "Fotoğraf"), (lyrics_file, "Şarkı Sözleri")]:
    if os.path.exists(file):
        print(f"   ✅ {name}: {file}")
    else:
        print(f"   ❌ {name}: {file} (BULUNAMADI)")
        files_ok = False

print()

if not files_ok:
    print("⚠️  Bazı dosyalar eksik! Lütfen kontrol edin.")
    sys.exit(1)

print("="*70)
print("[FAST] HIZLI COZUM: D-ID Web Arayuzu (Onerilen)")
print("="*70)
print()
print("1. https://www.d-id.com/ adresine gidin")
print("2. Ücretsiz hesap oluşturun (deneme kredisi var)")
print("3. 'Create Video' → 'Talking Avatar' seçin")
print(f"4. Image Upload: {image_file}")
print(f"5. Audio Upload: {audio_file}")
print("6. Settings: 4K resolution seçin")
print("7. 'Create' butonuna tıklayın")
print("8. Video hazır olunca indirin")
print()
print("Sure: ~5 dakika")
print("Maliyet: ~$0.10-0.50 (deneme kredisi var)")
print()
print("="*70)
print("[FREE] UCRETSIZ COZUM: SadTalker (Kurulum Devam Ediyor)")
print("="*70)
print()
print("SadTalker kurulumu başlatıldı. Kurulum tamamlandığında:")
print()
print(f"python src/sadtalker_integration.py \\")
print(f"  --image {image_file} \\")
print(f"  --audio {audio_file} \\")
print(f"  --lyrics {lyrics_file} \\")
print(f"  --resolution 4k")
print()
print("Kurulum: ~30 dakika (bir kez)")
print("Video olusturma: ~5-10 dakika")
print("Maliyet: Ucretsiz")
print()
print("="*70)
print("[TIP] ONERI")
print("="*70)
print()
print("Hızlı sonuç için: D-ID Web Arayüzü (5 dakika)")
print("Uzun vadeli kullanım için: SadTalker (ücretsiz)")
print()

