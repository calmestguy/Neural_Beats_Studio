"""
Gelişmiş audio mixing ve mastering
Reverb, EQ, compression, stereo widening vb.
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
import argparse
import os

def apply_reverb(audio, sample_rate, room_size=0.5, damping=0.5, wet_level=0.3):
    """
    Reverb (yankı) efekti ekler
    
    Args:
        audio: Audio array
        sample_rate: Sample rate
        room_size: Oda boyutu (0-1)
        damping: Sönümleme (0-1)
        wet_level: Reverb seviyesi (0-1)
    """
    # Basit reverb (impulse response simülasyonu)
    delay_samples = int(sample_rate * 0.03 * room_size)  # 30ms base delay
    decay = 1.0 - damping
    
    # Delay lines
    delays = [int(delay_samples * (1 + i * 0.3)) for i in range(3)]
    reverb_signal = np.zeros_like(audio)
    
    for delay in delays:
        if delay < len(audio):
            delayed = np.zeros_like(audio)
            delayed[delay:] = audio[:-delay] * (decay ** (delay / delay_samples))
            reverb_signal += delayed * 0.3
    
    # Mix
    wet = reverb_signal * wet_level
    dry = audio * (1 - wet_level)
    return dry + wet

def apply_eq(audio, sample_rate, bass_boost=0, mid_boost=0, treble_boost=0):
    """
    EQ (Equalizer) uygular
    
    Args:
        audio: Audio array
        sample_rate: Sample rate
        bass_boost: Bas boost (dB)
        mid_boost: Orta frekans boost (dB)
        treble_boost: Tiz boost (dB)
    """
    nyquist = sample_rate / 2
    
    # Bas (20-250 Hz)
    if bass_boost != 0:
        low = 250 / nyquist
        b, a = signal.butter(4, low, btype='low')
        bass = signal.filtfilt(b, a, audio)
        audio = audio + bass * (10 ** (bass_boost / 20) - 1)
    
    # Orta (250-4000 Hz)
    if mid_boost != 0:
        low = 250 / nyquist
        high = 4000 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        mid = signal.filtfilt(b, a, audio)
        audio = audio + mid * (10 ** (mid_boost / 20) - 1)
    
    # Tiz (4000+ Hz)
    if treble_boost != 0:
        high = 4000 / nyquist
        b, a = signal.butter(4, high, btype='high')
        treble = signal.filtfilt(b, a, audio)
        audio = audio + treble * (10 ** (treble_boost / 20) - 1)
    
    return audio

def apply_compression(audio, threshold=0.7, ratio=4.0, attack=0.003, release=0.1, sample_rate=32000):
    """
    Kompresyon uygular (dinamik aralık kontrolü)
    
    Args:
        audio: Audio array
        threshold: Eşik değeri (0-1)
        ratio: Kompresyon oranı (örn: 4:1)
        attack: Saldırı süresi (saniye)
        release: Bırakma süresi (saniye)
        sample_rate: Sample rate
    """
    # Basit kompresör
    compressed = np.copy(audio)
    
    attack_samples = int(attack * sample_rate)
    release_samples = int(release * sample_rate)
    
    envelope = np.abs(audio)
    gain_reduction = np.ones_like(audio)
    
    for i in range(1, len(audio)):
        if envelope[i] > threshold:
            # Kompresyon
            excess = envelope[i] - threshold
            reduced_excess = excess / ratio
            target_level = threshold + reduced_excess
            reduction = target_level / envelope[i] if envelope[i] > 0 else 1.0
            
            # Attack
            if gain_reduction[i-1] > reduction:
                gain_reduction[i] = gain_reduction[i-1] - (gain_reduction[i-1] - reduction) / attack_samples
            else:
                gain_reduction[i] = reduction
        else:
            # Release
            if gain_reduction[i-1] < 1.0:
                gain_reduction[i] = gain_reduction[i-1] + (1.0 - gain_reduction[i-1]) / release_samples
            else:
                gain_reduction[i] = 1.0
    
    return audio * gain_reduction

def apply_stereo_widening(audio, width=1.5):
    """
    Stereo genişletme (mono'yu stereo'ya çevirir ve genişletir)
    
    Args:
        audio: Mono audio array
        width: Genişlik (1.0 = normal, >1.0 = daha geniş)
    """
    # Basit stereo widening
    left = audio * (1.0 + width) / 2
    right = audio * (1.0 - width) / 2
    
    stereo = np.array([left, right]).T
    return stereo

def apply_limiter(audio, ceiling=0.95):
    """
    Limiter (peak kontrolü)
    
    Args:
        audio: Audio array
        ceiling: Maksimum seviye (0-1)
    """
    max_val = np.max(np.abs(audio))
    if max_val > ceiling:
        audio = audio * (ceiling / max_val)
    return audio

def normalize_audio(audio, target_lufs=-14.0):
    """
    Normalize (LUFS hedefleme - basit versiyon)
    
    Args:
        audio: Audio array
        target_lufs: Hedef LUFS seviyesi (genelde -14 to -16)
    """
    # Basit RMS normalizasyon
    rms = np.sqrt(np.mean(audio ** 2))
    if rms > 0:
        target_rms = 10 ** (target_lufs / 20)
        audio = audio * (target_rms / rms)
    
    # Peak kontrolü
    if np.max(np.abs(audio)) > 0.95:
        audio = audio * (0.95 / np.max(np.abs(audio)))
    
    return audio

def master_audio(audio, sample_rate, 
                 bass_boost=2.0, mid_boost=0, treble_boost=1.0,
                 compression=True, reverb=True, stereo_widen=True,
                 target_lufs=-14.0):
    """
    Tam mastering pipeline
    
    Args:
        audio: Audio array
        sample_rate: Sample rate
        bass_boost: Bas boost (dB)
        mid_boost: Orta boost (dB)
        treble_boost: Tiz boost (dB)
        compression: Kompresyon uygula
        reverb: Reverb ekle
        stereo_widen: Stereo genişletme
        target_lufs: Hedef LUFS seviyesi
    """
    print("🎚️  Mastering audio...")
    
    # 1. EQ
    if bass_boost != 0 or mid_boost != 0 or treble_boost != 0:
        print("   → Applying EQ...")
        audio = apply_eq(audio, sample_rate, bass_boost, mid_boost, treble_boost)
    
    # 2. Compression
    if compression:
        print("   → Applying compression...")
        audio = apply_compression(audio, threshold=0.7, ratio=4.0, sample_rate=sample_rate)
    
    # 3. Reverb
    if reverb:
        print("   → Adding reverb...")
        audio = apply_reverb(audio, sample_rate, room_size=0.3, wet_level=0.15)
    
    # 4. Normalize
    print("   → Normalizing...")
    audio = normalize_audio(audio, target_lufs=target_lufs)
    
    # 5. Limiter
    print("   → Applying limiter...")
    audio = apply_limiter(audio, ceiling=0.95)
    
    return audio

def process_audio_advanced(input_file, output_file=None,
                         bass_boost=2.0, mid_boost=0, treble_boost=1.0,
                         compression=True, reverb=True, stereo_widen=False,
                         target_lufs=-14.0):
    """
    Gelişmiş audio işleme
    
    Args:
        input_file: Giriş dosyası
        output_file: Çıktı dosyası
        bass_boost: Bas boost (dB)
        mid_boost: Orta boost (dB)
        treble_boost: Tiz boost (dB)
        compression: Kompresyon
        reverb: Reverb
        stereo_widen: Stereo genişletme
        target_lufs: Hedef LUFS
    """
    # Dosyayı oku
    sample_rate, audio = wavfile.read(input_file)
    
    # Mono'ya çevir (işleme için)
    is_stereo = len(audio.shape) > 1
    if is_stereo:
        audio_mono = np.mean(audio, axis=1)
    else:
        audio_mono = audio
    
    # Float32'ye çevir
    audio_mono = audio_mono.astype(np.float32)
    if np.max(np.abs(audio_mono)) > 0:
        audio_mono = audio_mono / np.max(np.abs(audio_mono))
    
    # Mastering
    processed = master_audio(
        audio_mono, sample_rate,
        bass_boost=bass_boost,
        mid_boost=mid_boost,
        treble_boost=treble_boost,
        compression=compression,
        reverb=reverb,
        stereo_widen=False,  # Önce mono işle
        target_lufs=target_lufs
    )
    
    # Stereo genişletme (eğer istenirse)
    if stereo_widen:
        print("   → Applying stereo widening...")
        processed = apply_stereo_widening(processed, width=1.3)
        is_stereo = True
    
    # Int16'ya çevir
    if is_stereo:
        audio_int16 = (processed * 32767).astype(np.int16)
    else:
        audio_int16 = (processed * 32767).astype(np.int16)
    
    # Çıktı dosya adı
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_mastered.wav"
    
    # Kaydet
    wavfile.write(output_file, sample_rate, audio_int16)
    
    print(f"✅ Mastered: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Gelişmiş Audio Mastering')
    parser.add_argument('input', type=str, help='Input audio file')
    parser.add_argument('--output', type=str, default=None, help='Output file')
    parser.add_argument('--bass-boost', type=float, default=2.0, help='Bass boost (dB)')
    parser.add_argument('--mid-boost', type=float, default=0, help='Mid boost (dB)')
    parser.add_argument('--treble-boost', type=float, default=1.0, help='Treble boost (dB)')
    parser.add_argument('--no-compression', action='store_true', help='Disable compression')
    parser.add_argument('--no-reverb', action='store_true', help='Disable reverb')
    parser.add_argument('--stereo-widen', action='store_true', help='Enable stereo widening')
    parser.add_argument('--target-lufs', type=float, default=-14.0, help='Target LUFS level')
    
    args = parser.parse_args()
    
    process_audio_advanced(
        args.input,
        output_file=args.output,
        bass_boost=args.bass_boost,
        mid_boost=args.mid_boost,
        treble_boost=args.treble_boost,
        compression=not args.no_compression,
        reverb=not args.no_reverb,
        stereo_widen=args.stereo_widen,
        target_lufs=args.target_lufs
    )

if __name__ == '__main__':
    main()



