"""
Gerçek şarkı söyleyen AI kadın vokal oluşturucu
Bark TTS kullanarak şarkı modunda vokal üretir
"""

import os
import sys
import numpy as np
from scipy.io.wavfile import write as write_wav
import argparse

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    from bark import SAMPLE_RATE, generate_audio, preload_models
    BARK_AVAILABLE = True
except ImportError:
    BARK_AVAILABLE = False
    print("⚠️  Bark TTS not installed. Installing...")
    print("   Run: pip install bark")

def format_lyrics_for_singing(lyrics_text):
    """
    Şarkı sözlerini Bark TTS'in şarkı modu için formatlar
    Bark, [SINGING] etiketi ile şarkı modunu aktif eder
    """
    # Şarkı sözlerini satırlara böl
    lines = [line.strip() for line in lyrics_text.split('\n') if line.strip()]
    
    # Verse, Chorus gibi bölümleri koru ama şarkı moduna çevir
    formatted = []
    for line in lines:
        # Bölüm başlıklarını atla veya yorum olarak bırak
        if line.startswith('[') and line.endswith(']'):
            continue
        
        # Her satırı şarkı moduna çevir
        if line.strip():
            formatted.append(f"♪ [SINGING] {line.strip()} ♪")
    
    # Tüm satırları birleştir
    return "\n".join(formatted)

def create_singing_vocal(lyrics_file, output_file=None, voice_preset="v2/en_speaker_9", 
                        sample_rate=22050):
    """
    Şarkı sözlerinden gerçek şarkı söyleyen AI kadın vokal oluşturur
    
    Args:
        lyrics_file: Şarkı sözleri dosyası
        output_file: Çıktı dosyası (None ise otomatik)
        voice_preset: Ses preset'i (kadın sesi için v2/en_speaker_9)
        sample_rate: Sample rate (Bark için 22050)
    """
    if not BARK_AVAILABLE:
        print("[ERROR] Bark TTS not available. Please install: pip install bark")
        return None
    
    print("[VOCAL] Creating singing vocal with Bark TTS...")
    print(f"   Voice preset: {voice_preset} (Female voice)")
    
    # Şarkı sözlerini oku
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        lyrics = f.read()
    
    # Şarkı modu için formatla
    formatted_lyrics = format_lyrics_for_singing(lyrics)
    print(f"\n[LYRICS] Formatted lyrics for singing mode:")
    print("="*60)
    print(formatted_lyrics[:200] + "..." if len(formatted_lyrics) > 200 else formatted_lyrics)
    print("="*60)
    
    try:
        # PyTorch 2.6 uyumluluk sorunu için monkey patch
        import torch
        original_load = torch.load
        
        def patched_load(*args, **kwargs):
            # weights_only=False yaparak eski davranışı geri getir
            if 'weights_only' not in kwargs:
                kwargs['weights_only'] = False
            return original_load(*args, **kwargs)
        
        # Geçici olarak torch.load'u değiştir
        torch.load = patched_load
        
        try:
            # Modelleri yükle (ilk çalıştırmada indirilecek)
            print("\n[MODELS] Loading Bark models (first time may take a while)...")
            preload_models()
            
            # Şarkı söyleyen vokal üret
            print("\n[GENERATE] Generating singing vocal...")
            print("   This may take a few minutes...")
            
            audio_array = generate_audio(
                formatted_lyrics,
                history_prompt=voice_preset,  # Kadın sesi
                text_temp=0.7,  # Daha melodik için
                waveform_temp=0.7
            )
        finally:
            # torch.load'u geri yükle
            torch.load = original_load
        
        # Çıktı dosyası
        if output_file is None:
            base_name = os.path.splitext(lyrics_file)[0]
            output_file = f"{base_name}_singing_vocal.wav"
        
        # Kaydet
        write_wav(output_file, sample_rate, audio_array)
        
        print(f"\n[SUCCESS] Singing vocal created: {output_file}")
        print(f"   Duration: {len(audio_array) / sample_rate:.2f} seconds")
        
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Error generating vocal: {e}")
        print("\n[TIPS] Troubleshooting:")
        print("   1. Make sure you have internet connection (first time)")
        print("   2. Check if Bark models are downloaded")
        print("   3. Try a shorter lyrics text")
        return None

def mix_vocal_with_music(vocal_file, music_file, output_file=None, 
                        vocal_volume=0.8, music_volume=0.7):
    """
    Şarkı söyleyen vokali müzikle karıştırır
    """
    try:
        import librosa
        import soundfile as sf
    except ImportError:
        print("[ERROR] librosa or soundfile not available")
        return None
    
    print(f"\n[MIX] Mixing vocal with music...")
    print(f"   Vocal: {vocal_file}")
    print(f"   Music: {music_file}")
    
    # Vokali yükle
    vocal, vocal_sr = librosa.load(vocal_file, sr=None)
    
    # Müziği yükle
    music, music_sr = librosa.load(music_file, sr=None)
    
    # Sample rate'leri eşitle
    target_sr = max(vocal_sr, music_sr)
    if vocal_sr != target_sr:
        vocal = librosa.resample(vocal, orig_sr=vocal_sr, target_sr=target_sr)
    if music_sr != target_sr:
        music = librosa.resample(music, orig_sr=music_sr, target_sr=target_sr)
    
    # Süreleri eşitle (kısa olanı uzat)
    if len(vocal) < len(music):
        # Vokali uzat (sessizlik ekle)
        silence = np.zeros(len(music) - len(vocal))
        vocal = np.concatenate([vocal, silence])
    elif len(music) < len(vocal):
        # Müziği uzat (loop veya sessizlik)
        music = np.pad(music, (0, len(vocal) - len(music)), mode='constant')
    
    # Karıştır
    mixed = (vocal * vocal_volume + music * music_volume)
    
    # Normalize
    if np.max(np.abs(mixed)) > 0:
        mixed = mixed / np.max(np.abs(mixed))
    
    # Çıktı dosyası
    if output_file is None:
        base_name = os.path.splitext(music_file)[0]
        output_file = f"{base_name}_with_singing_vocal.wav"
    
    # Kaydet
    sf.write(output_file, mixed, target_sr)
    
    print(f"[SUCCESS] Mixed track saved: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(
        description='Gerçek Şarkı Söyleyen AI Kadın Vokal Oluşturucu',
        epilog='Örnek: python src/create_singing_vocal.py rainy_city_blues_lyrics.txt --music output/Rainy\\ City\\ Blues.mp3'
    )
    parser.add_argument('lyrics_file', type=str, help='Şarkı sözleri dosyası')
    parser.add_argument('--music', type=str, default=None, 
                       help='Müzik dosyası (vokali müzikle karıştırmak için)')
    parser.add_argument('--output', type=str, default=None, help='Çıktı dosyası')
    parser.add_argument('--voice', type=str, default='v2/en_speaker_9',
                       help='Ses preset\'i (kadın sesi için v2/en_speaker_9)')
    parser.add_argument('--vocal-volume', type=float, default=0.8,
                       help='Vokal ses seviyesi (0-1)')
    parser.add_argument('--music-volume', type=float, default=0.7,
                       help='Müzik ses seviyesi (0-1)')
    parser.add_argument('--vocal-only', action='store_true',
                       help='Sadece vokal üret, müzikle karıştırma')
    
    args = parser.parse_args()
    
    # Şarkı söyleyen vokal oluştur
    vocal_file = create_singing_vocal(
        args.lyrics_file,
        output_file=args.output if args.vocal_only else None,
        voice_preset=args.voice
    )
    
    if not vocal_file:
        return
    
    # Müzikle karıştır (eğer belirtilmişse)
    if args.music and not args.vocal_only:
        final_file = mix_vocal_with_music(
            vocal_file,
            args.music,
            output_file=args.output,
            vocal_volume=args.vocal_volume,
            music_volume=args.music_volume
        )
        
        if final_file:
            print(f"\n[SUCCESS] Final track with singing vocal: {final_file}")
    else:
        print(f"\n[SUCCESS] Singing vocal created: {vocal_file}")

if __name__ == '__main__':
    main()

