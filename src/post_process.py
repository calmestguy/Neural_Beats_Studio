"""
Ses işleme ve bas vurgulama için post-processing
"""

import numpy as np
import scipy.io.wavfile as wavfile
from scipy import signal
import argparse
import os

def enhance_bass(audio, sample_rate, bass_boost_db=6.0, low_cutoff=60, high_cutoff=250):
    """
    Bas frekanslarını vurgular
    
    Args:
        audio: Audio array (numpy)
        sample_rate: Sample rate
        bass_boost_db: Bas boost miktarı (dB)
        low_cutoff: Alt kesim frekansı (Hz)
        high_cutoff: Üst kesim frekansı (Hz)
    """
    # Normalize et
    if np.max(np.abs(audio)) > 0:
        audio = audio.astype(np.float32) / np.max(np.abs(audio))
    
    # Bas frekanslarını filtrele ve boost et
    nyquist = sample_rate / 2
    low = low_cutoff / nyquist
    high = high_cutoff / nyquist
    
    # Bandpass filter (bas frekansları için)
    b, a = signal.butter(4, [low, high], btype='band')
    bass_freqs = signal.filtfilt(b, a, audio)
    
    # Bas'ı boost et
    bass_boost = 10 ** (bass_boost_db / 20)  # dB'den linear'a çevir
    enhanced_audio = audio + (bass_freqs * (bass_boost - 1))
    
    # Normalize et (clipping önleme)
    if np.max(np.abs(enhanced_audio)) > 0:
        enhanced_audio = enhanced_audio / np.max(np.abs(enhanced_audio))
    
    return enhanced_audio

def process_audio(input_file, output_file=None, bass_boost_db=6.0):
    """
    Audio dosyasını işler ve bas'ı vurgular
    """
    # Dosyayı oku
    sample_rate, audio = wavfile.read(input_file)
    
    # Mono'ya çevir (eğer stereo ise)
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)
    
    # Float32'ye çevir
    audio = audio.astype(np.float32)
    
    # Normalize et
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))
    
    # Bas enhancement
    enhanced_audio = enhance_bass(audio, sample_rate, bass_boost_db)
    
    # Int16'ya çevir
    audio_int16 = (enhanced_audio * 32767).astype(np.int16)
    
    # Çıktı dosya adı
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_bass_boosted.wav"
    
    # Kaydet
    wavfile.write(output_file, sample_rate, audio_int16)
    
    print(f"✅ Enhanced: {output_file}")
    print(f"   Bass boost: {bass_boost_db} dB")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Audio Post-Processing - Bas Enhancement')
    parser.add_argument('input', type=str, help='Input audio file')
    parser.add_argument('--output', type=str, default=None, help='Output file (optional)')
    parser.add_argument('--bass-boost', type=float, default=6.0, help='Bass boost in dB (default: 6.0)')
    
    args = parser.parse_args()
    
    process_audio(args.input, args.output, args.bass_boost)

if __name__ == '__main__':
    main()



