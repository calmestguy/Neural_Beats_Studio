"""
Şarkı sözlerini müziğe ekleme
TTS (Text-to-Speech) kullanarak vokal ekler
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
import argparse
import os
import re

# TTS için alternatifler:
# 1. gTTS (Google TTS) - Ücretsiz, basit ama şarkı değil
# 2. pyttsx3 - Offline, basit
# 3. Coqui TTS - Daha kaliteli ama kurulumu zor
# 4. ElevenLabs API - Ücretli, en kaliteli

try:
    from gtts import gTTS
    import io
    from pydub import AudioSegment
    from pydub.playback import play
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️  gTTS not installed. Installing...")
    print("   Run: pip install gtts pydub")

def split_lyrics_by_lines(lyrics):
    """Şarkı sözlerini satırlara böler"""
    lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
    return lines

def text_to_speech_gtts(text, lang='tr', slow=False):
    """
    Google TTS kullanarak metni sese çevirir
    
    Args:
        text: Metin
        lang: Dil kodu ('tr' = Türkçe)
        slow: Yavaş konuşma
    
    Returns:
        bytes: Audio data
    """
    if not GTTS_AVAILABLE:
        raise ImportError("gTTS not available. Install with: pip install gtts pydub")
    
    tts = gTTS(text=text, lang=lang, slow=slow)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    return audio_buffer

def adjust_speech_timing(speech_audio, target_duration, sample_rate):
    """
    Konuşma hızını ayarlar (şarkı için daha yavaş/yumuşak)
    """
    current_duration = len(speech_audio) / sample_rate
    
    if current_duration < target_duration:
        # Yavaşlat (stretch)
        stretch_factor = target_duration / current_duration
        # Basit time-stretching (daha iyi için librosa.time_stretch kullanılabilir)
        indices = np.linspace(0, len(speech_audio) - 1, int(len(speech_audio) * stretch_factor))
        stretched = np.interp(indices, np.arange(len(speech_audio)), speech_audio)
        return stretched.astype(speech_audio.dtype)
    else:
        # Hızlandır
        speed_factor = current_duration / target_duration
        indices = np.linspace(0, len(speech_audio) - 1, int(len(speech_audio) / speed_factor))
        sped_up = np.interp(indices, np.arange(len(speech_audio)), speech_audio)
        return sped_up.astype(speech_audio.dtype)

def mix_vocals_with_music(music_file, lyrics, output_file=None, 
                          vocal_volume=0.7, music_volume=0.8, 
                          lang='tr', slow_speech=True):
    """
    Şarkı sözlerini müziğe ekler
    
    Args:
        music_file: Müzik dosyası
        lyrics: Şarkı sözleri
        output_file: Çıktı dosyası
        vocal_volume: Vokal ses seviyesi (0-1)
        music_volume: Müzik ses seviyesi (0-1)
        lang: Dil kodu
        slow_speech: Yavaş konuşma (şarkı için daha uygun)
    """
    print("🎤 Generating speech from lyrics...")
    
    # Müziği yükle
    music_sr, music_audio = wavfile.read(music_file)
    
    # Mono'ya çevir
    if len(music_audio.shape) > 1:
        music_audio = np.mean(music_audio, axis=1)
    
    music_audio = music_audio.astype(np.float32)
    if np.max(np.abs(music_audio)) > 0:
        music_audio = music_audio / np.max(np.abs(music_audio))
    
    music_duration = len(music_audio) / music_sr
    
    # TTS ile konuşma üret
    if not GTTS_AVAILABLE:
        print("❌ gTTS not available. Please install: pip install gtts pydub")
        return None
    
    try:
        # Tüm sözleri birleştir
        full_text = ' '.join(split_lyrics_by_lines(lyrics))
        
        # TTS üret
        audio_buffer = text_to_speech_gtts(full_text, lang=lang, slow=slow_speech)
        
        # AudioSegment ile yükle
        audio_segment = AudioSegment.from_mp3(audio_buffer)
        speech_sr = audio_segment.frame_rate
        speech_audio = np.array(audio_segment.get_array_of_samples())
        
        # Mono'ya çevir
        if audio_segment.channels > 1:
            speech_audio = speech_audio.reshape(-1, audio_segment.channels)
            speech_audio = np.mean(speech_audio, axis=1)
        
        speech_audio = speech_audio.astype(np.float32)
        if np.max(np.abs(speech_audio)) > 0:
            speech_audio = speech_audio / np.max(np.abs(speech_audio))
        
        # Sample rate'leri eşitle
        if speech_sr != music_sr:
            # Resample
            num_samples = int(len(speech_audio) * music_sr / speech_sr)
            speech_audio = signal.resample(speech_audio, num_samples)
        
        # Süreyi ayarla
        speech_duration = len(speech_audio) / music_sr
        if speech_duration > music_duration:
            # Kısalt
            speech_audio = speech_audio[:int(music_duration * music_sr)]
        elif speech_duration < music_duration:
            # Uzat (sessizlik ekle veya loop)
            silence = np.zeros(int((music_duration - speech_duration) * music_sr))
            speech_audio = np.concatenate([speech_audio, silence])
        
        # Mix
        print("🎵 Mixing vocals with music...")
        mixed = (music_audio * music_volume + speech_audio * vocal_volume)
        
        # Normalize
        if np.max(np.abs(mixed)) > 0:
            mixed = mixed / np.max(np.abs(mixed))
        
        # Kaydet
        if output_file is None:
            base_name = os.path.splitext(music_file)[0]
            output_file = f"{base_name}_with_vocals.wav"
        
        audio_int16 = (mixed * 32767).astype(np.int16)
        wavfile.write(output_file, music_sr, audio_int16)
        
        print(f"✅ Saved: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   TTS generation failed. Make sure you have internet connection for gTTS.")
        return None

def main():
    parser = argparse.ArgumentParser(description='Şarkı Sözlerini Müziğe Ekleme')
    parser.add_argument('music_file', type=str, help='Müzik dosyası')
    parser.add_argument('--lyrics', type=str, default=None, help='Şarkı sözleri')
    parser.add_argument('--lyrics-file', type=str, default=None, help='Şarkı sözleri dosyası')
    parser.add_argument('--output', type=str, default=None, help='Çıktı dosyası')
    parser.add_argument('--vocal-volume', type=float, default=0.7, help='Vokal ses seviyesi (0-1)')
    parser.add_argument('--music-volume', type=float, default=0.8, help='Müzik ses seviyesi (0-1)')
    parser.add_argument('--lang', type=str, default='tr', help='Dil kodu (tr=en)')
    parser.add_argument('--fast', action='store_true', help='Hızlı konuşma (varsayılan: yavaş)')
    
    args = parser.parse_args()
    
    # Şarkı sözlerini oku
    if args.lyrics_file:
        with open(args.lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.read()
    elif args.lyrics:
        lyrics = args.lyrics
    else:
        parser.error("Either --lyrics or --lyrics-file must be provided")
    
    result = mix_vocals_with_music(
        args.music_file,
        lyrics,
        output_file=args.output,
        vocal_volume=args.vocal_volume,
        music_volume=args.music_volume,
        lang=args.lang,
        slow_speech=not args.fast
    )
    
    if result:
        print(f"\n🎉 Final track: {result}")

if __name__ == '__main__':
    main()



