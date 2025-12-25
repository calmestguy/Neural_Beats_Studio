"""
Çok detaylı audio analizi - Daha iyi müzik üretimi için
Melodik yapı, ritim pattern'leri, dinamikler, spektral özellikler
"""

import numpy as np
import librosa
import scipy.io.wavfile as wavfile
from scipy import signal
import os
from collections import Counter
import json

# Enstrüman frekans aralıkları (daha detaylı)
INSTRUMENT_FREQUENCIES = {
    'bass': (20, 250),
    'kick_drum': (20, 100),
    'snare_drum': (100, 300),
    'hi_hat': (2000, 15000),
    'guitar': (80, 2000),
    'electric_guitar': (80, 5000),
    'piano': (27, 4186),
    'violin': (196, 2637),
    'cello': (65, 987),
    'trumpet': (165, 1175),
    'saxophone': (110, 880),
    'synthesizer': (20, 20000),
    'vocals': (85, 255),
    # Karadeniz enstrümanları (daha hassas)
    'kemenche': (200, 3000),  # Karadeniz kemençesi
    'tulum': (100, 2000),  # Karadeniz tulumu
    'davul': (50, 500),  # Davul
    'zurna': (500, 4000),  # Zurna
    'baglama': (80, 2000),  # Bağlama
    'accordion': (100, 3000),  # Akordeon
}

def analyze_melodic_structure(y, sr):
    """
    Melodik yapı analizi
    - Scale (major/minor)
    - Key detection (daha hassas)
    - Chord progression
    - Melodic contour
    """
    print("   🎼 Analyzing melodic structure...")
    
    # Chroma features (12 perde sınıfı)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    
    # Key detection (Krumhansl-Schmuckler algorithm benzeri)
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Major ve minor profile'ları (basitleştirilmiş)
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    
    # Her key için correlation hesapla
    best_key = None
    best_mode = None
    best_correlation = -1
    
    for i, key in enumerate(keys):
        # Major için
        rotated_major = np.roll(major_profile, i)
        corr_major = np.corrcoef(chroma_mean, rotated_major)[0, 1]
        
        # Minor için
        rotated_minor = np.roll(minor_profile, i)
        corr_minor = np.corrcoef(chroma_mean, rotated_minor)[0, 1]
        
        if corr_major > best_correlation:
            best_correlation = corr_major
            best_key = key
            best_mode = 'major'
        
        if corr_minor > best_correlation:
            best_correlation = corr_minor
            best_key = key
            best_mode = 'minor'
    
    # Melodic contour (pitch over time)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_times = librosa.frames_to_time(np.arange(pitches.shape[1]), sr=sr)
    
    # Dominant pitch'leri bul
    pitch_values = []
    for t in range(pitches.shape[1]):
        col = pitches[:, t]
        idx = np.argmax(col)
        if magnitudes[idx, t] > 0.1:
            pitch_values.append(pitches[idx, t])
    
    # Melodic direction (ascending/descending/stable)
    if len(pitch_values) > 10:
        pitch_diff = np.diff(pitch_values)
        ascending = np.sum(pitch_diff > 0) / len(pitch_diff)
        descending = np.sum(pitch_diff < 0) / len(pitch_diff)
        
        if ascending > 0.4:
            melodic_direction = 'ascending'
        elif descending > 0.4:
            melodic_direction = 'descending'
        else:
            melodic_direction = 'stable'
    else:
        melodic_direction = 'stable'
    
    return {
        'key': best_key,
        'mode': best_mode,
        'key_confidence': float(best_correlation),
        'melodic_direction': melodic_direction,
        'chroma_mean': chroma_mean.tolist()
    }

def analyze_rhythm_pattern(y, sr, tempo):
    """
    Ritim pattern analizi
    - Time signature
    - Beat pattern (strong/weak)
    - Groove
    - Rhythmic complexity
    """
    print("   🥁 Analyzing rhythm pattern...")
    
    # Beat tracking
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    
    # Time signature detection (basit: 4/4, 3/4, 2/4)
    if len(beat_times) > 4:
        beat_intervals = np.diff(beat_times)
        avg_interval = np.mean(beat_intervals)
        
        # Strong beats (daha yüksek enerji)
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr)
        
        # Beat'lerdeki enerji
        rms = librosa.feature.rms(y=y)[0]
        rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
        
        beat_energies = []
        for beat_time in beat_times:
            idx = np.argmin(np.abs(rms_times - beat_time))
            beat_energies.append(rms[idx])
        
        # Strong beat pattern (4/4 için her 4'te bir güçlü)
        if len(beat_energies) >= 4:
            # Her 4 beat'te bir pattern
            pattern_4_4 = []
            for i in range(0, len(beat_energies), 4):
                if i + 3 < len(beat_energies):
                    pattern_4_4.append(beat_energies[i:i+4])
            
            if pattern_4_4:
                avg_pattern = np.mean(pattern_4_4, axis=0)
                # İlk beat genelde en güçlü
                if avg_pattern[0] > avg_pattern[1] * 1.2:
                    time_signature = '4/4'
                else:
                    time_signature = 'unknown'
            else:
                time_signature = '4/4'  # Default
        else:
            time_signature = '4/4'
    else:
        time_signature = '4/4'
    
    # Rhythmic complexity (onset density)
    onset_density = len(onset_times) / (len(y) / sr)
    
    if onset_density > 3:
        rhythmic_complexity = 'high'
    elif onset_density > 1.5:
        rhythmic_complexity = 'medium'
    else:
        rhythmic_complexity = 'low'
    
    # Groove (syncopation detection - basit)
    # Karadeniz müziği için özel: genelde güçlü, düzenli ritim
    if tempo >= 80 and tempo <= 120:
        if rhythmic_complexity == 'high':
            groove_type = 'energetic, driving'
        else:
            groove_type = 'steady, traditional'
    else:
        groove_type = 'variable'
    
    return {
        'time_signature': time_signature,
        'rhythmic_complexity': rhythmic_complexity,
        'onset_density': float(onset_density),
        'groove_type': groove_type,
        'beat_count': len(beat_times)
    }

def analyze_dynamics(y, sr):
    """
    Dinamik analiz
    - Loudness contour
    - Dynamic range
    - Energy distribution
    """
    print("   🔊 Analyzing dynamics...")
    
    # RMS energy over time
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    
    # Dynamic range
    dynamic_range = np.max(rms) - np.min(rms)
    avg_rms = np.mean(rms)
    
    # Energy distribution (beginning, middle, end)
    third = len(rms) // 3
    energy_beginning = np.mean(rms[:third])
    energy_middle = np.mean(rms[third:2*third])
    energy_end = np.mean(rms[2*third:])
    
    # Energy contour (increasing/decreasing/stable)
    if energy_end > energy_beginning * 1.2:
        energy_contour = 'increasing'
    elif energy_beginning > energy_end * 1.2:
        energy_contour = 'decreasing'
    else:
        energy_contour = 'stable'
    
    # Overall energy level
    if avg_rms > 0.1:
        energy_level = 'high'
    elif avg_rms > 0.05:
        energy_level = 'medium'
    else:
        energy_level = 'low'
    
    return {
        'dynamic_range': float(dynamic_range),
        'avg_rms': float(avg_rms),
        'energy_level': energy_level,
        'energy_contour': energy_contour,
        'energy_beginning': float(energy_beginning),
        'energy_middle': float(energy_middle),
        'energy_end': float(energy_end)
    }

def analyze_spectral_features(y, sr):
    """
    Spektral özellikler
    - Harmonic content
    - Spectral centroid
    - Spectral rolloff
    - Zero crossing rate
    """
    print("   📊 Analyzing spectral features...")
    
    # Harmonic and percussive separation
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    # Harmonic ratio
    harmonic_energy = np.sum(y_harmonic ** 2)
    percussive_energy = np.sum(y_percussive ** 2)
    total_energy = harmonic_energy + percussive_energy
    
    if total_energy > 0:
        harmonic_ratio = harmonic_energy / total_energy
    else:
        harmonic_ratio = 0.5
    
    # Spectral centroid (brightness)
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    avg_centroid = np.mean(spectral_centroids)
    
    # Spectral rolloff (high frequency content)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    avg_rolloff = np.mean(spectral_rolloff)
    
    # Zero crossing rate (noisiness)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    avg_zcr = np.mean(zcr)
    
    # Brightness classification
    if avg_centroid > 3000:
        brightness = 'bright'
    elif avg_centroid > 2000:
        brightness = 'medium'
    else:
        brightness = 'dark'
    
    return {
        'harmonic_ratio': float(harmonic_ratio),
        'spectral_centroid': float(avg_centroid),
        'spectral_rolloff': float(avg_rolloff),
        'zero_crossing_rate': float(avg_zcr),
        'brightness': brightness
    }

def analyze_karadeniz_characteristics(y, sr, tempo, instrument_scores):
    """
    Karadeniz müziği için özel karakteristik analiz
    - Kemençe karakteristikleri
    - Tulum karakteristikleri
    - Karadeniz ritim pattern'leri
    """
    print("   🎵 Analyzing Karadeniz characteristics...")
    
    characteristics = {
        'has_kemenche': False,
        'has_tulum': False,
        'has_davul': False,
        'kemenche_style': None,
        'tulum_style': None,
        'rhythm_style': None
    }
    
    # Kemençe tespiti ve karakteristikleri
    if instrument_scores.get('kemenche', 0) > 0.1:
        characteristics['has_kemenche'] = True
        
        # Kemençe stili (vibrato, glissando detection)
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        frequency_bins = librosa.fft_frequencies(sr=sr)
        
        # Kemençe frekans aralığı (800-2500 Hz)
        kemenche_range = (frequency_bins >= 800) & (frequency_bins <= 2500)
        if np.any(kemenche_range):
            kemenche_spectrum = magnitude[kemenche_range, :]
            
            # Vibrato detection (frequency modulation)
            # Basit: spektral centroid'in zaman içinde değişimi
            centroid_over_time = []
            for t in range(kemenche_spectrum.shape[1]):
                col = kemenche_spectrum[:, t]
                if np.sum(col) > 0:
                    weighted_freq = np.sum(frequency_bins[kemenche_range] * col) / np.sum(col)
                    centroid_over_time.append(weighted_freq)
            
            if len(centroid_over_time) > 10:
                centroid_variance = np.var(centroid_over_time)
                if centroid_variance > 50000:  # Yüksek varyans = vibrato
                    characteristics['kemenche_style'] = 'with vibrato, expressive'
                else:
                    characteristics['kemenche_style'] = 'melodic, clear'
            else:
                characteristics['kemenche_style'] = 'melodic'
    
    # Tulum tespiti
    if instrument_scores.get('tulum', 0) > 0.1:
        characteristics['has_tulum'] = True
        
        # Tulum: sürekli ton, düşük varyans
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        frequency_bins = librosa.fft_frequencies(sr=sr)
        
        tulum_range = (frequency_bins >= 400) & (frequency_bins <= 1800)
        if np.any(tulum_range):
            tulum_spectrum = magnitude[tulum_range, :]
            tulum_energy_variance = np.var(np.mean(tulum_spectrum, axis=0))
            
            if tulum_energy_variance < np.var(np.mean(magnitude, axis=0)) * 0.5:
                characteristics['tulum_style'] = 'sustained, drone-like'
            else:
                characteristics['tulum_style'] = 'melodic, dynamic'
    
    # Davul tespiti
    if instrument_scores.get('davul', 0) > 0.1:
        characteristics['has_davul'] = True
    
    # Karadeniz ritim stili
    if tempo >= 85 and tempo <= 110:
        if characteristics['has_davul']:
            characteristics['rhythm_style'] = 'traditional Karadeniz rhythm, strong beat, driving'
        else:
            characteristics['rhythm_style'] = 'moderate tempo, steady'
    else:
        characteristics['rhythm_style'] = 'variable tempo'
    
    return characteristics

def convert_to_wav_if_needed(audio_file):
    """
    MP3/WebM dosyalarını WAV'a çevirir (FFmpeg ile)
    """
    if not os.path.exists(audio_file):
        return None
    
    # Zaten WAV ise
    if audio_file.lower().endswith('.wav'):
        return audio_file
    
    # WAV'a çevir
    import tempfile
    import subprocess
    import glob
    
    temp_dir = os.path.join(os.path.dirname(audio_file) or '.', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    wav_file = os.path.join(temp_dir, os.path.basename(audio_file).rsplit('.', 1)[0] + '.wav')
    
    # FFmpeg yolunu bul
    ffmpeg_cmd = None
    
    # PATH'te ara
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, 
                               timeout=5)
        if result.returncode == 0:
            ffmpeg_cmd = 'ffmpeg'
    except:
        pass
    
    # Winget yolu
    if not ffmpeg_cmd:
        winget_pattern = os.path.expanduser(
            r'~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin\ffmpeg.exe'
        )
        matches = glob.glob(winget_pattern)
        if matches:
            ffmpeg_cmd = matches[0]
    
    # Program Files yolu
    if not ffmpeg_cmd:
        program_files_patterns = [
            r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
            r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
        ]
        for pattern in program_files_patterns:
            if os.path.exists(pattern):
                ffmpeg_cmd = pattern
                break
    
    # FFmpeg ile çevir
    if ffmpeg_cmd:
        try:
            result = subprocess.run(
                [ffmpeg_cmd, '-i', audio_file, '-y', '-acodec', 'pcm_s16le', '-ar', '44100', wav_file],
                capture_output=True,
                check=True,
                timeout=60
            )
            if os.path.exists(wav_file):
                print(f"   ✅ Converted to WAV: {wav_file}")
                return wav_file
        except Exception as e:
            print(f"   ⚠️  FFmpeg conversion failed: {e}")
    else:
        print(f"   ⚠️  FFmpeg not found, trying direct load...")
    
    return audio_file  # Orijinal dosyayı döndür

def detailed_analyze_audio(audio_file, skip_seconds=5, analysis_duration=120):
    """
    Çok detaylı audio analizi
    """
    print("="*70)
    print("🔍 DETAILED AUDIO ANALYSIS")
    print("="*70)
    print(f"\n📁 Analyzing: {audio_file}")
    
    # MP3/WebM ise WAV'a çevir
    audio_file = convert_to_wav_if_needed(audio_file)
    if audio_file is None:
        print("❌ Could not process audio file")
        return None
    
    # Audio yükle
    try:
        y, sr = librosa.load(audio_file, sr=None, offset=skip_seconds, duration=analysis_duration)
        print(f"   ✅ Loaded {len(y)/sr:.1f}s of audio")
    except Exception as e:
        print(f"   ⚠️  Error with offset, trying without: {e}")
        try:
            y, sr = librosa.load(audio_file, sr=None, duration=analysis_duration)
            print(f"   ✅ Loaded {len(y)/sr:.1f}s of audio (no offset)")
        except Exception as e2:
            try:
                y, sr = librosa.load(audio_file, sr=None, duration=60)
                print(f"   ✅ Loaded {len(y)/sr:.1f}s of audio (fallback)")
            except Exception as e3:
                print(f"❌ Error loading audio: {e3}")
                return None
    
    print(f"\n📊 Analysis Components:")
    
    # 1. Tempo analizi
    print("\n1️⃣  TEMPO ANALYSIS")
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray):
        tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
    else:
        tempo = float(tempo)
    tempo = int(round(tempo))
    print(f"   ⏱️  Tempo: {tempo} BPM")
    
    # 2. Melodik yapı
    print("\n2️⃣  MELODIC STRUCTURE")
    melodic = analyze_melodic_structure(y, sr)
    print(f"   🎹 Key: {melodic['key']} {melodic['mode']} (confidence: {melodic['key_confidence']:.2f})")
    print(f"   📈 Melodic direction: {melodic['melodic_direction']}")
    
    # 3. Ritim pattern
    print("\n3️⃣  RHYTHM PATTERN")
    rhythm = analyze_rhythm_pattern(y, sr, tempo)
    print(f"   🥁 Time signature: {rhythm['time_signature']}")
    print(f"   🎯 Rhythmic complexity: {rhythm['rhythmic_complexity']}")
    print(f"   🎵 Groove: {rhythm['groove_type']}")
    
    # 4. Dinamikler
    print("\n4️⃣  DYNAMICS")
    dynamics = analyze_dynamics(y, sr)
    print(f"   🔊 Energy level: {dynamics['energy_level']}")
    print(f"   📊 Dynamic range: {dynamics['dynamic_range']:.3f}")
    print(f"   📈 Energy contour: {dynamics['energy_contour']}")
    
    # 5. Spektral özellikler
    print("\n5️⃣  SPECTRAL FEATURES")
    spectral = analyze_spectral_features(y, sr)
    print(f"   🎨 Brightness: {spectral['brightness']}")
    print(f"   🎵 Harmonic ratio: {spectral['harmonic_ratio']:.2f}")
    print(f"   📊 Spectral centroid: {spectral['spectral_centroid']:.0f} Hz")
    
    # 6. Enstrüman tespiti (detaylı)
    print("\n6️⃣  INSTRUMENT DETECTION")
    stft = librosa.stft(y)
    magnitude = np.abs(stft)
    frequency_bins = librosa.fft_frequencies(sr=sr)
    
    instrument_scores = {}
    for instrument, (low_freq, high_freq) in INSTRUMENT_FREQUENCIES.items():
        freq_mask = (frequency_bins >= low_freq) & (frequency_bins <= high_freq)
        if np.any(freq_mask):
            energy = np.mean(magnitude[freq_mask, :])
            instrument_scores[instrument] = energy
    
    # Karadeniz enstrümanları için özel tespit
    mean_energy = np.mean(list(instrument_scores.values()))
    
    # Kemençe (daha hassas)
    kemenche_range = (frequency_bins >= 800) & (frequency_bins <= 2500)
    if np.any(kemenche_range):
        kemenche_energy = np.mean(magnitude[kemenche_range, :])
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        high_centroid = np.mean(spectral_centroids) > 2000
        
        if kemenche_energy > mean_energy * 1.3 or (kemenche_energy > mean_energy * 1.1 and high_centroid):
            instrument_scores['kemenche'] = instrument_scores.get('kemenche', 0) + kemenche_energy * 0.8
    
    # Tulum
    tulum_range = (frequency_bins >= 400) & (frequency_bins <= 1800)
    if np.any(tulum_range):
        tulum_energy = np.mean(magnitude[tulum_range, :])
        tulum_variance = np.var(magnitude[tulum_range, :])
        if tulum_energy > mean_energy * 1.2 and tulum_variance < np.var(magnitude) * 0.8:
            instrument_scores['tulum'] = instrument_scores.get('tulum', 0) + tulum_energy * 0.6
    
    # Davul
    davul_range = (frequency_bins >= 50) & (frequency_bins <= 300)
    if np.any(davul_range):
        davul_energy = np.mean(magnitude[davul_range, :])
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        rhythmic = len(onset_frames) > 10
        
        if davul_energy > mean_energy * 1.1 and rhythmic:
            instrument_scores['davul'] = instrument_scores.get('davul', 0) + davul_energy * 0.7
    
    # Enstrümanları sırala
    sorted_instruments = sorted(instrument_scores.items(), key=lambda x: x[1], reverse=True)
    detected_instruments = [inst for inst, score in sorted_instruments[:8] if score > 0.1]
    
    print(f"   🎸 Detected instruments (top {len(detected_instruments)}):")
    for i, (inst, score) in enumerate(sorted_instruments[:8]):
        if score > 0.1:
            print(f"      {i+1}. {inst}: {score:.3f}")
    
    # 7. Karadeniz karakteristikleri
    print("\n7️⃣  KARADENIZ CHARACTERISTICS")
    karadeniz = analyze_karadeniz_characteristics(y, sr, tempo, instrument_scores)
    if karadeniz['has_kemenche']:
        print(f"   ✅ Kemenche detected: {karadeniz['kemenche_style']}")
    if karadeniz['has_tulum']:
        print(f"   ✅ Tulum detected: {karadeniz['tulum_style']}")
    if karadeniz['has_davul']:
        print(f"   ✅ Davul detected")
    print(f"   🎵 Rhythm style: {karadeniz['rhythm_style']}")
    
    # 8. Genre tahmini
    print("\n8️⃣  GENRE ESTIMATION")
    # Basit genre tahmini
    if karadeniz['has_kemenche'] or karadeniz['has_tulum']:
        estimated_genre = 'karadeniz'
        genre_confidence = 0.9
    elif 'baglama' in detected_instruments:
        estimated_genre = 'turkish_folk'
        genre_confidence = 0.7
    else:
        estimated_genre = 'unknown'
        genre_confidence = 0.5
    
    print(f"   🎵 Estimated genre: {estimated_genre} (confidence: {genre_confidence:.2f})")
    
    # Tüm analiz sonuçlarını birleştir
    detailed_analysis = {
        'tempo': tempo,
        'melodic': melodic,
        'rhythm': rhythm,
        'dynamics': dynamics,
        'spectral': spectral,
        'instruments': detected_instruments,
        'instrument_scores': {k: float(v) for k, v in instrument_scores.items()},
        'karadeniz_characteristics': karadeniz,
        'estimated_genre': estimated_genre,
        'genre_confidence': genre_confidence,
        'duration': len(y) / sr
    }
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE")
    print("="*70)
    
    return detailed_analysis

def detailed_analysis_to_prompt(analysis, similarity_level='high'):
    """
    Detaylı analiz sonuçlarını kullanarak çok spesifik prompt oluşturur
    """
    print("\n" + "="*70)
    print("📝 GENERATING DETAILED PROMPT")
    print("="*70)
    
    prompt_parts = []
    
    # 1. Genre ve stil
    if analysis['estimated_genre'] == 'karadeniz':
        prompt_parts.append("Turkish Black Sea folk music, Karadeniz müziği")
        prompt_parts.append("authentic traditional Karadeniz style")
    elif analysis['estimated_genre'] == 'turkish_folk':
        prompt_parts.append("Turkish folk music")
    else:
        prompt_parts.append(f"{analysis['estimated_genre']} music")
    
    # 2. Enstrümanlar (öncelik sırasına göre)
    instruments = analysis['instruments']
    if instruments:
        instrument_descriptions = {
            'kemenche': 'kemenche (Karadeniz kemençesi, traditional 3-string fiddle)',
            'tulum': 'tulum (Karadeniz bagpipe, traditional wind instrument)',
            'davul': 'davul (traditional Turkish drum)',
            'zurna': 'zurna (traditional Turkish wind instrument)',
            'baglama': 'bağlama (saz, traditional Turkish string instrument)',
            'bass': 'bass guitar',
            'guitar': 'guitar',
            'electric_guitar': 'electric guitar',
            'drums': 'drums',
            'piano': 'piano',
            'violin': 'violin',
            'vocals': 'vocals'
        }
        
        inst_list = []
        for inst in instruments[:6]:  # En fazla 6 enstrüman
            desc = instrument_descriptions.get(inst, inst)
            inst_list.append(desc)
        
        if inst_list:
            prompt_parts.append(', '.join(inst_list))
    
    # 3. Karadeniz karakteristikleri
    karadeniz = analysis['karadeniz_characteristics']
    if karadeniz['has_kemenche'] and karadeniz['kemenche_style']:
        prompt_parts.append(f"kemenche {karadeniz['kemenche_style']}")
    if karadeniz['has_tulum'] and karadeniz['tulum_style']:
        prompt_parts.append(f"tulum {karadeniz['tulum_style']}")
    if karadeniz['rhythm_style']:
        prompt_parts.append(karadeniz['rhythm_style'])
    
    # 4. Tempo
    prompt_parts.append(f"{analysis['tempo']} BPM")
    
    # 5. Ritim özellikleri
    rhythm = analysis['rhythm']
    prompt_parts.append(f"time signature {rhythm['time_signature']}")
    prompt_parts.append(f"{rhythm['rhythmic_complexity']} rhythmic complexity")
    prompt_parts.append(rhythm['groove_type'])
    
    # 6. Melodik özellikler
    melodic = analysis['melodic']
    prompt_parts.append(f"key of {melodic['key']} {melodic['mode']}")
    prompt_parts.append(f"{melodic['melodic_direction']} melodic contour")
    
    # 7. Dinamikler
    dynamics = analysis['dynamics']
    prompt_parts.append(f"{dynamics['energy_level']} energy")
    prompt_parts.append(f"{dynamics['energy_contour']} energy contour")
    
    # 8. Spektral özellikler
    spectral = analysis['spectral']
    prompt_parts.append(f"{spectral['brightness']} timbre")
    if spectral['harmonic_ratio'] > 0.6:
        prompt_parts.append("harmonic, melodic")
    else:
        prompt_parts.append("percussive, rhythmic")
    
    # 9. Production
    prompt_parts.append("professional production")
    prompt_parts.append("clear instrument separation")
    prompt_parts.append("balanced mix")
    prompt_parts.append("authentic sound")
    
    # Prompt'u birleştir
    detailed_prompt = ', '.join(prompt_parts)
    
    print(f"\n📝 Generated Prompt ({len(detailed_prompt)} characters):")
    print(f"\n{detailed_prompt}\n")
    
    return detailed_prompt

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Çok Detaylı Audio Analizi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek kullanım:
  python detailed_audio_analyzer.py "path/to/audio.mp3"
  python detailed_audio_analyzer.py "path/to/audio.mp3" --generate
        """
    )
    parser.add_argument('audio_file', type=str,
                       help='Audio dosyası yolu')
    parser.add_argument('--skip', type=int, default=5,
                       help='Başlangıçtan kaç saniye atla')
    parser.add_argument('--duration', type=int, default=120,
                       help='Analiz süresi (saniye)')
    parser.add_argument('--generate', action='store_true',
                       help='Analiz sonrası prompt oluştur')
    parser.add_argument('--output', type=str, default=None,
                       help='Analiz sonuçlarını JSON olarak kaydet')
    
    args = parser.parse_args()
    
    # Analiz yap
    analysis = detailed_analyze_audio(
        args.audio_file,
        skip_seconds=args.skip,
        analysis_duration=args.duration
    )
    
    if analysis is None:
        print("❌ Analysis failed!")
        return
    
    # JSON olarak kaydet
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Analysis saved to: {args.output}")
    
    # Prompt oluştur
    if args.generate:
        prompt = detailed_analysis_to_prompt(analysis)
        print(f"\n✅ Use this prompt for generation:")
        print(f"\n{prompt}\n")

if __name__ == '__main__':
    main()

