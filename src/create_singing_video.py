"""
4K Çözünürlükte Gerçekçi Kadın Şarkıcı Video Oluşturucu
D-ID API veya alternatif çözümler kullanarak şarkı söyleyen video oluşturur
"""

import os
import sys
import argparse
import json
import time

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def analyze_lyrics_emotion(lyrics):
    """
    Şarkı sözlerinden duyguyu analiz eder
    """
    lyrics_lower = lyrics.lower()
    
    # Duygusal kelimeler
    sad_words = ['rain', 'lonely', 'blues', 'faded', 'lost', 'crying', 'shadow', 'disappears']
    melancholic_words = ['rainy', 'night', 'whispers', 'secrets', 'quiet', 'cold']
    emotional_words = ['walk', 'wander', 'searching', 'pieces', 'déjà vu']
    
    sad_score = sum(1 for word in sad_words if word in lyrics_lower)
    melancholic_score = sum(1 for word in melancholic_words if word in lyrics_lower)
    emotional_score = sum(1 for word in emotional_words if word in lyrics_lower)
    
    # Dominant emotion
    if sad_score >= 3:
        emotion = 'sad'
        expression = 'melancholic, thoughtful, emotional'
    elif melancholic_score >= 2:
        emotion = 'melancholic'
        expression = 'contemplative, nostalgic, gentle'
    else:
        emotion = 'emotional'
        expression = 'expressive, heartfelt, sincere'
    
    return {
        'emotion': emotion,
        'expression': expression,
        'sad_score': sad_score,
        'melancholic_score': melancholic_score
    }

def create_video_with_did(lyrics_file, audio_file, api_key=None, output_file=None):
    """
    D-ID API kullanarak şarkı söyleyen video oluşturur
    
    D-ID: https://www.d-id.com/
    - API key gerektirir
    - Ücretli (ama deneme kredisi var)
    - 4K çözünürlük desteği
    - Duygusal ifadeler
    """
    try:
        import requests
    except ImportError:
        print("[ERROR] requests not installed. Install with: pip install requests")
        return None
    
    if not api_key:
        print("[ERROR] D-ID API key required!")
        print("[INFO] Get your API key from: https://www.d-id.com/api")
        print("[INFO] Set it as environment variable: D_ID_API_KEY")
        return None
    
    print("[VIDEO] Creating singing video with D-ID API...")
    
    # Şarkı sözlerini oku
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        lyrics = f.read()
    
    # Duygu analizi
    emotion_analysis = analyze_lyrics_emotion(lyrics)
    print(f"[EMOTION] Detected emotion: {emotion_analysis['emotion']}")
    print(f"[EXPRESSION] {emotion_analysis['expression']}")
    
    # D-ID API endpoint
    base_url = "https://api.d-id.com"
    
    # 1. Avatar seçimi (kadın şarkıcı)
    # D-ID'de mevcut avatarlar veya kendi avatar'ınızı yükleyebilirsiniz
    avatar_id = "amy-jcwCkr1grs"  # Örnek kadın avatar (değiştirilebilir)
    
    # 2. Video oluşturma isteği
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }
    
    # Şarkı sözlerini temizle (sadece metin)
    clean_lyrics = '\n'.join([line.strip() for line in lyrics.split('\n') 
                              if line.strip() and not line.strip().startswith('[')])
    
    # D-ID için script (duygusal ifadeler ekle)
    script = f"""
    {clean_lyrics}
    """
    
    # Video oluşturma payload
    payload = {
        "source_url": "https://d-id-public-bucket.s3.amazonaws.com/or-roman.jpg",  # Avatar URL
        "script": {
            "type": "audio",
            "audio_url": audio_file,  # Ses dosyası URL'i (upload etmeniz gerekebilir)
            "reduce_noise": True
        },
        "config": {
            "result_format": "mp4",
            "resolution": "4k",  # 4K çözünürlük
            "face_enhance": True,
            "motion_factor": 1.0
        }
    }
    
    print("[INFO] D-ID API entegrasyonu için:")
    print("   1. D-ID hesabı oluşturun: https://www.d-id.com/")
    print("   2. API key alın")
    print("   3. Ses dosyasını upload edin")
    print("   4. Video oluşturun")
    
    return None  # Şimdilik placeholder

def create_video_with_wav2lip(audio_file, video_file, output_file=None):
    """
    Wav2Lip kullanarak lip-sync video oluşturur
    Açık kaynak, ücretsiz ama kurulumu zor
    """
    print("[VIDEO] Wav2Lip entegrasyonu...")
    print("[INFO] Wav2Lip kurulumu için:")
    print("   1. GitHub: https://github.com/Rudrabha/Wav2Lip")
    print("   2. Model indir")
    print("   3. Kadın şarkıcı referans videosu hazırla")
    print("   4. Lip-sync uygula")
    
    return None  # Şimdilik placeholder

def create_video_with_sadtalker(audio_file, image_file, output_file=None):
    """
    SadTalker kullanarak konuşan video oluşturur
    Açık kaynak, ücretsiz, daha iyi kalite
    """
    print("[VIDEO] SadTalker entegrasyonu...")
    print("[INFO] SadTalker kurulumu için:")
    print("   1. GitHub: https://github.com/OpenTalker/SadTalker")
    print("   2. Model indir")
    print("   3. Kadın şarkıcı fotoğrafı hazırla")
    print("   4. Video oluştur")
    
    return None  # Şimdilik placeholder

def create_video_guide():
    """
    Video oluşturma rehberi
    """
    guide = """
# 4K Kadın Şarkıcı Video Oluşturma Rehberi

## Seçenek 1: D-ID API (Önerilen - En Kolay)

**Avantajlar:**
- Kolay kullanım
- 4K çözünürlük
- Duygusal ifadeler
- API entegrasyonu

**Dezavantajlar:**
- Ücretli (ama deneme kredisi var)
- API key gerektirir

**Kurulum:**
1. D-ID hesabı: https://www.d-id.com/
2. API key alın
3. Python script ile entegre edin

**Fiyat:** ~$0.10-0.50 per video

---

## Seçenek 2: Wav2Lip (Açık Kaynak - Ücretsiz)

**Avantajlar:**
- Ücretsiz
- Açık kaynak
- İyi lip-sync

**Dezavantajlar:**
- Kurulumu zor
- GPU gerekli
- Referans video gerekli

**Kurulum:**
```bash
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip
pip install -r requirements.txt
# Model indir
# Referans video hazırla
```

---

## Seçenek 3: SadTalker (Açık Kaynak - En İyi Kalite)

**Avantajlar:**
- Ücretsiz
- En iyi kalite
- Duygusal ifadeler
- Sadece fotoğraf gerekli

**Dezavantajlar:**
- Kurulumu zor
- GPU gerekli
- Model boyutu büyük

**Kurulum:**
```bash
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
pip install -r requirements.txt
# Model indir
```

---

## Seçenek 4: HeyGen (Alternatif Servis)

**Avantajlar:**
- Kolay kullanım
- API var
- İyi kalite

**Dezavantajlar:**
- Ücretli
- API key gerektirir

**Website:** https://www.heygen.com/

---

## Önerilen Yaklaşım

1. **Hızlı Test İçin:** D-ID API (kolay, hızlı)
2. **Ücretsiz Çözüm:** SadTalker (en iyi kalite)
3. **Profesyonel:** D-ID veya HeyGen (en kolay)

---

## Pratik Uygulama

### D-ID ile:
1. D-ID hesabı oluştur
2. API key al
3. Ses dosyasını upload et
4. Avatar seç (kadın şarkıcı)
5. Video oluştur

### SadTalker ile:
1. SadTalker kur
2. Kadın şarkıcı fotoğrafı bul/hazırla
3. Ses dosyasını hazırla
4. Video oluştur
"""
    
    print(guide)
    
    # Rehberi dosyaya kaydet
    with open("VIDEO_CREATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("\n[SUCCESS] Rehber kaydedildi: VIDEO_CREATION_GUIDE.md")

def main():
    parser = argparse.ArgumentParser(
        description='4K Çözünürlükte Gerçekçi Kadın Şarkıcı Video Oluşturucu',
        epilog='Örnek: python src/create_singing_video.py --lyrics lyrics.txt --audio vocal.wav --method did'
    )
    parser.add_argument('--lyrics', type=str, help='Şarkı sözleri dosyası')
    parser.add_argument('--audio', type=str, help='Ses dosyası (vokal)')
    parser.add_argument('--method', type=str, choices=['did', 'wav2lip', 'sadtalker', 'guide'],
                       default='guide', help='Video oluşturma yöntemi')
    parser.add_argument('--api-key', type=str, default=None,
                       help='D-ID API key (veya D_ID_API_KEY env variable)')
    parser.add_argument('--output', type=str, default=None, help='Çıktı video dosyası')
    parser.add_argument('--image', type=str, default=None,
                       help='SadTalker için referans fotoğraf')
    parser.add_argument('--video', type=str, default=None,
                       help='Wav2Lip için referans video')
    
    args = parser.parse_args()
    
    if args.method == 'guide':
        create_video_guide()
        return
    
    if not args.lyrics or not args.audio:
        parser.error("--lyrics and --audio are required (except for --method guide)")
    
    # API key kontrolü
    api_key = args.api_key or os.getenv('D_ID_API_KEY')
    
    if args.method == 'did':
        create_video_with_did(args.lyrics, args.audio, api_key, args.output)
    elif args.method == 'wav2lip':
        if not args.video:
            parser.error("--video is required for Wav2Lip method")
        create_video_with_wav2lip(args.audio, args.video, args.output)
    elif args.method == 'sadtalker':
        if not args.image:
            parser.error("--image is required for SadTalker method")
        create_video_with_sadtalker(args.audio, args.image, args.output)

if __name__ == '__main__':
    main()


