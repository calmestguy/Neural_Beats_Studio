"""
Şarkı sözlerinden duygusal müzik üretimi
MusicGen şarkı sözlerini direkt çeviremez, ama duyguyu analiz edip prompt'a çevirir
"""

import re
from generate import MusicGenerator
import argparse

# Duygusal kelime analizi (basit)
EMOTIONAL_KEYWORDS = {
    'sad': ['üzgün', 'ağlıyor', 'yok', 'kaybettim', 'ayrılık', 'hasret', 'acı', 'keder', 'hüzün', 'gözyaşı'],
    'happy': ['mutlu', 'sevinç', 'neşe', 'gülüyor', 'sevgi', 'aşk', 'mutluluk', 'heyecan'],
    'romantic': ['aşk', 'sevgili', 'kalp', 'romantik', 'tutku', 'özlem', 'hasret'],
    'melancholic': ['hüzün', 'melankoli', 'nostalji', 'geçmiş', 'anı', 'özlem'],
    'energetic': ['enerji', 'dans', 'hareket', 'coşku', 'heyecan']
}

def analyze_lyrics_emotion(lyrics):
    """
    Şarkı sözlerinden duyguyu analiz eder
    
    Args:
        lyrics: Şarkı sözleri (string)
    
    Returns:
        dict: Duygu analizi sonuçları
    """
    lyrics_lower = lyrics.lower()
    
    emotion_scores = {}
    for emotion, keywords in EMOTIONAL_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in lyrics_lower)
        if score > 0:
            emotion_scores[emotion] = score
    
    # En güçlü duyguyu bul
    dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0] if emotion_scores else 'emotional'
    
    return {
        'dominant_emotion': dominant_emotion,
        'scores': emotion_scores,
        'has_traditional_instruments': any(word in lyrics_lower for word in ['saz', 'bağlama', 'keman', 'klarnet', 'ney'])
    }

def lyrics_to_prompt(lyrics, include_traditional=False):
    """
    Şarkı sözlerinden müzik prompt'u oluşturur
    
    Args:
        lyrics: Şarkı sözleri
        include_traditional: Geleneksel enstrümanlar ekle
    
    Returns:
        str: Müzik prompt'u
    """
    analysis = analyze_lyrics_emotion(lyrics)
    
    # Temel prompt
    base_prompt = "Turkish pop music, instrumental"
    
    # Duygu ekle
    emotion_map = {
        'sad': 'melancholic, emotional, melancholic',
        'happy': 'uplifting, joyful, energetic',
        'romantic': 'romantic, emotional, melodic',
        'melancholic': 'melancholic, nostalgic, emotional',
        'energetic': 'energetic, upbeat, driving'
    }
    
    emotion_desc = emotion_map.get(analysis['dominant_emotion'], 'emotional, melodic')
    base_prompt += f", {emotion_desc}"
    
    # Enstrümanlar
    if include_traditional or analysis['has_traditional_instruments']:
        base_prompt += ", bağlama (saz), violin, clarinet, piano, strings"
    else:
        base_prompt += ", synthesizer, strings, piano"
    
    # Ek özellikler
    base_prompt += ", modern production, strong bass, 110 BPM"
    
    return base_prompt

def generate_from_lyrics(lyrics, output_dir='output', duration=30, model_size='small', 
                         include_traditional=True, auto_bass_boost=True, add_vocals=False,
                         vocal_volume=0.7, music_volume=0.8):
    """
    Şarkı sözlerinden müzik üretir
    
    Args:
        lyrics: Şarkı sözleri
        output_dir: Çıktı klasörü
        duration: Süre (saniye)
        model_size: Model boyutu
        include_traditional: Geleneksel enstrümanlar ekle
        auto_bass_boost: Otomatik bas vurgulama
        add_vocals: Vokal ekle (TTS kullanarak)
        vocal_volume: Vokal ses seviyesi
        music_volume: Müzik ses seviyesi
    """
    print("📝 Analyzing lyrics...")
    analysis = analyze_lyrics_emotion(lyrics)
    print(f"   Dominant emotion: {analysis['dominant_emotion']}")
    print(f"   Emotion scores: {analysis['scores']}")
    
    # Prompt oluştur
    prompt = lyrics_to_prompt(lyrics, include_traditional)
    print(f"\n🎵 Generated prompt: {prompt}\n")
    
    # Müzik üret
    generator = MusicGenerator(model_size=model_size)
    results = generator.generate([prompt], output_dir=output_dir, duration=duration)
    
    if not results:
        return None
    
    music_file = results[0]
    
    # Bas vurgulama
    if auto_bass_boost:
        from post_process import process_audio
        print("\n🔊 Applying bass enhancement...")
        music_file = process_audio(music_file, bass_boost_db=8.0)
    
    # Vokal ekleme
    if add_vocals:
        from add_vocals import mix_vocals_with_music
        print("\n🎤 Adding vocals...")
        final_file = mix_vocals_with_music(
            music_file, 
            lyrics, 
            vocal_volume=vocal_volume,
            music_volume=music_volume,
            lang='tr',
            slow_speech=True
        )
        return final_file if final_file else music_file
    
    return music_file

def main():
    parser = argparse.ArgumentParser(description='Şarkı Sözlerinden Müzik Üretimi')
    parser.add_argument('--lyrics', type=str, default=None,
                       help='Şarkı sözleri (string)')
    parser.add_argument('--lyrics-file', type=str, default=None,
                       help='Şarkı sözleri dosyası (alternatif)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='small',
                       choices=['small', 'medium', 'large'])
    parser.add_argument('--output', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--no-traditional', action='store_true',
                       help='Geleneksel enstrümanları ekleme')
    parser.add_argument('--no-bass-boost', action='store_true',
                       help='Otomatik bas vurgulamayı kapat')
    parser.add_argument('--add-vocals', action='store_true',
                       help='Şarkı sözlerini TTS ile ekle (NOT: Bu şarkı söylemez, konuşur)')
    parser.add_argument('--vocal-volume', type=float, default=0.7,
                       help='Vokal ses seviyesi (0-1, default: 0.7)')
    parser.add_argument('--music-volume', type=float, default=0.8,
                       help='Müzik ses seviyesi (0-1, default: 0.8)')
    
    args = parser.parse_args()
    
    # Şarkı sözlerini oku
    if args.lyrics_file:
        with open(args.lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.read()
    elif args.lyrics:
        lyrics = args.lyrics
    else:
        parser.error("Either --lyrics or --lyrics-file must be provided")
    
    # Üret
    result = generate_from_lyrics(
        lyrics,
        output_dir=args.output,
        duration=args.duration,
        model_size=args.model,
        include_traditional=not args.no_traditional,
        auto_bass_boost=not args.no_bass_boost,
        add_vocals=args.add_vocals,
        vocal_volume=args.vocal_volume,
        music_volume=args.music_volume
    )
    
    print(f"\n🎉 Music generated: {result}")

if __name__ == '__main__':
    main()

