"""
Audio analizi ve benzer müzik üretimi
Müzik dosyasını analiz edip, enstrümanları ve türü tespit eder,
sonra benzer müzik üretir
"""

import numpy as np
import librosa
import scipy.io.wavfile as wavfile
from scipy import signal
import argparse
import os
import re
import tempfile
import subprocess

# Enstrüman frekans aralıkları (Hz)
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
    'synthesizer': (20, 20000),  # Geniş aralık
    'vocals': (85, 255),  # Temel frekans
    # Karadeniz enstrümanları
    'kemenche': (200, 3000),  # Karadeniz kemençesi - yüksek frekans, tiz ses
    'tulum': (100, 2000),  # Karadeniz tulumu - orta-yüksek frekans
    'davul': (50, 500),  # Davul - düşük-orta frekans
    'zurna': (500, 4000),  # Zurna - çok yüksek, keskin ses
    'baglama': (80, 2000),  # Bağlama - geniş aralık
    'accordion': (100, 3000),  # Akordeon - geniş aralık
}

# Müzik türü karakteristikleri
GENRE_CHARACTERISTICS = {
    'rock': {
        'tempo_range': (120, 180),
        'bass_prominent': True,
        'guitar_prominent': True,
        'drums_prominent': True,
        'energy': 'high'
    },
    'pop': {
        'tempo_range': (100, 140),
        'bass_prominent': True,
        'synthesizer_prominent': True,
        'energy': 'medium'
    },
    'jazz': {
        'tempo_range': (60, 200),
        'piano_prominent': True,
        'saxophone_prominent': True,
        'energy': 'variable'
    },
    'electronic': {
        'tempo_range': (120, 150),
        'bass_prominent': True,
        'synthesizer_prominent': True,
        'drums_prominent': True,
        'energy': 'high'
    },
    'classical': {
        'tempo_range': (40, 200),
        'strings_prominent': True,
        'piano_prominent': True,
        'energy': 'variable'
    },
    'blues': {
        'tempo_range': (60, 120),
        'guitar_prominent': True,
        'bass_prominent': True,
        'energy': 'medium'
    },
    'karadeniz': {
        'tempo_range': (80, 140),
        'kemenche_prominent': True,
        'tulum_prominent': True,
        'davul_prominent': True,
        'energy': 'high'
    },
    'turkish_folk': {
        'tempo_range': (70, 130),
        'baglama_prominent': True,
        'davul_prominent': True,
        'energy': 'variable'
    }
}

def is_youtube_url(url):
    """YouTube URL kontrolü"""
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in youtube_patterns:
        if re.search(pattern, url):
            return True
    return False

def download_youtube_audio(url, output_dir=None, max_duration=60, skip_seconds=5):
    """
    YouTube'dan audio indirir
    
    Args:
        url: YouTube URL
        output_dir: Çıktı klasörü (None ise temp)
        max_duration: Maksimum süre (saniye) - analiz için ilk 60 saniye yeterli
        skip_seconds: Başlangıçtan kaç saniye atla (reklamları atlamak için)
    
    Returns:
        str: İndirilen dosya yolu
    """
    print(f"📥 Downloading audio from YouTube: {url}")
    
    try:
        import yt_dlp
    except ImportError:
        print("❌ yt-dlp not installed. Installing...")
        print("   Run: pip install yt-dlp")
        return None
    
    # Çıktı klasörü
    if output_dir is None:
        output_dir = tempfile.gettempdir()
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    # Geçici dosya adı
    output_file = os.path.join(output_dir, "youtube_audio_temp.%(ext)s")
    
    # yt-dlp options
    output_file = os.path.join(output_dir, "youtube_audio_temp.%(ext)s")
    
    # FFmpeg kontrolü
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        has_ffmpeg = True
    except:
        has_ffmpeg = False
        print("   ⚠️  FFmpeg not found. Will try to use original format or pydub.")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
    }
    
    # FFmpeg varsa post-processor ekle
    if has_ffmpeg:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video bilgilerini al
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"   Title: {video_title}")
            if duration:
                print(f"   Duration: {duration}s")
            
            # İndir
            ydl.download([url])
            
            # İndirilen dosyayı bul
            # yt-dlp genelde .wav'a çevirir
            possible_extensions = ['wav', 'm4a', 'webm', 'mp3', 'opus']
            downloaded_file = None
            
            for ext in possible_extensions:
                temp_file = os.path.join(output_dir, f"youtube_audio_temp.{ext}")
                if os.path.exists(temp_file):
                    downloaded_file = temp_file
                    break
            
            if not downloaded_file:
                # Son çare: output_dir'deki son değiştirilen dosyayı bul
                files = [f for f in os.listdir(output_dir) if 'youtube_audio_temp' in f]
                if files:
                    # En son değiştirilen dosyayı al
                    files_with_time = [(f, os.path.getmtime(os.path.join(output_dir, f))) for f in files]
                    files_with_time.sort(key=lambda x: x[1], reverse=True)
                    downloaded_file = os.path.join(output_dir, files_with_time[0][0])
            
            if downloaded_file:
                file_ext = os.path.splitext(downloaded_file)[1].lower()
                
                # Webm/m4a/mp3 formatındaysa WAV'a çevir
                if file_ext in ['.webm', '.m4a', '.mp3', '.opus']:
                    wav_file = downloaded_file.replace(file_ext, '.wav')
                    print(f"   🔄 Converting {file_ext} to WAV...")
                    
                    # FFmpeg ile dönüştür (subprocess kullan)
                    try:
                        # FFmpeg yolunu bul
                        ffmpeg_cmd = None
                        
                        # 1. PATH'te ara
                        try:
                            result = subprocess.run(['ffmpeg', '-version'], 
                                                   capture_output=True, 
                                                   timeout=5)
                            if result.returncode == 0:
                                ffmpeg_cmd = 'ffmpeg'
                        except:
                            pass
                        
                        # 2. Winget kurulum yolu (Windows)
                        if not ffmpeg_cmd:
                            import glob
                            winget_pattern = os.path.expanduser(
                                r'~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin\ffmpeg.exe'
                            )
                            matches = glob.glob(winget_pattern)
                            if matches:
                                ffmpeg_cmd = matches[0]
                        
                        # 3. Common locations
                        if not ffmpeg_cmd:
                            common_paths = [
                                r'C:\ffmpeg\bin\ffmpeg.exe',
                                r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
                            ]
                            for path in common_paths:
                                if os.path.exists(path):
                                    ffmpeg_cmd = path
                                    break
                        
                        if not ffmpeg_cmd:
                            raise Exception("FFmpeg not found")
                        
                        # Dönüştür
                        cmd = [
                            ffmpeg_cmd,
                            '-i', downloaded_file,
                            '-acodec', 'pcm_s16le',
                            '-ar', '44100',
                            '-ac', '2',
                            '-y',  # Overwrite
                            wav_file
                        ]
                        
                        result = subprocess.run(cmd, 
                                              capture_output=True, 
                                              timeout=60,
                                              text=True)
                        
                        if result.returncode == 0 and os.path.exists(wav_file):
                            print(f"   ✅ Converted to WAV")
                            # Eski dosyayı sil
                            try:
                                os.remove(downloaded_file)
                            except:
                                pass
                            downloaded_file = wav_file
                        else:
                            print(f"   ⚠️  FFmpeg conversion failed: {result.stderr[:200]}")
                            # Pydub ile dene
                            try:
                                from pydub import AudioSegment
                                audio = AudioSegment.from_file(downloaded_file)
                                audio.export(wav_file, format='wav')
                                if os.path.exists(wav_file):
                                    try:
                                        os.remove(downloaded_file)
                                    except:
                                        pass
                                    downloaded_file = wav_file
                                    print(f"   ✅ Converted using pydub")
                            except Exception as e:
                                print(f"   ⚠️  Could not convert: {e}")
                                print(f"   → Trying to use original format (may fail)")
                    
                    except Exception as e:
                        print(f"   ⚠️  Conversion error: {e}")
                        print(f"   → Trying to use original format")
                
                # Maksimum süre sınırı ve reklam atlama (eğer belirtilmişse ve WAV ise)
                if max_duration and downloaded_file.endswith('.wav') and os.path.exists(downloaded_file):
                    try:
                        # Reklamları atla ve kısalt
                        y, sr = librosa.load(downloaded_file, sr=None, offset=skip_seconds, duration=max_duration)
                        # Kısaltılmış versiyonu kaydet
                        wavfile.write(downloaded_file, sr, (y * 32767).astype(np.int16))
                        print(f"   ⏩ Skipped first {skip_seconds}s (ads/intro)")
                    except Exception as e:
                        print(f"   ⚠️  Could not process duration limit: {e}")
                
                print(f"✅ Downloaded: {downloaded_file}")
                return downloaded_file
            else:
                print("❌ Could not find downloaded file")
                return None
                
    except Exception as e:
        print(f"❌ Error downloading from YouTube: {e}")
        print("   Make sure you have internet connection and yt-dlp is installed")
        return None

def get_audio_file(input_source, temp_dir=None):
    """
    Audio dosyasını alır (yerel dosya veya YouTube URL)
    
    Args:
        input_source: Yerel dosya yolu veya YouTube URL
        temp_dir: Geçici dosyalar için klasör
    
    Returns:
        str: Audio dosya yolu
    """
    if is_youtube_url(input_source):
        # YouTube'dan indir
        audio_file = download_youtube_audio(input_source, output_dir=temp_dir, max_duration=60)
        return audio_file
    else:
        # Yerel dosya
        if os.path.exists(input_source):
            return input_source
        else:
            print(f"❌ File not found: {input_source}")
            return None

def convert_to_wav_if_needed(audio_file):
    """Gerekirse audio dosyasını WAV'a çevirir"""
    file_ext = os.path.splitext(audio_file)[1].lower()
    
    if file_ext == '.wav':
        return audio_file
    
    # MP3, M4A, WebM gibi formatları WAV'a çevir
    if file_ext in ['.mp3', '.m4a', '.webm', '.opus', '.flac']:
        wav_file = audio_file.replace(file_ext, '.wav')
        
        # FFmpeg ile çevir
        try:
            import glob
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
            
            if ffmpeg_cmd:
                cmd = [
                    ffmpeg_cmd,
                    '-i', audio_file,
                    '-acodec', 'pcm_s16le',
                    '-ar', '44100',
                    '-ac', '2',
                    '-y',
                    wav_file
                ]
                result = subprocess.run(cmd, capture_output=True, timeout=60, text=True)
                if result.returncode == 0 and os.path.exists(wav_file):
                    return wav_file
        
        except Exception as e:
            print(f"   ⚠️  Could not convert {file_ext} to WAV: {e}")
    
    return audio_file

def analyze_audio_multiple_segments(audio_file, skip_seconds=5, num_segments=3):
    """
    Audio'yu birden fazla bölümden analiz eder (daha doğru sonuç için)
    """
    audio_file = convert_to_wav_if_needed(audio_file)
    
    # Toplam süreyi al
    try:
        y_full, sr = librosa.load(audio_file, sr=None)
        total_duration = len(y_full) / sr
    except:
        return None
    
    # Farklı bölümlerden analiz yap
    segment_duration = min(30, (total_duration - skip_seconds) / num_segments)
    all_instruments = []
    all_tempos = []
    all_genres = []
    
    for i in range(num_segments):
        offset = skip_seconds + (i * segment_duration)
        if offset + segment_duration > total_duration:
            break
        
        try:
            y_seg, sr = librosa.load(audio_file, sr=None, offset=offset, duration=segment_duration)
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y_seg, sr=sr)
            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
            else:
                tempo = float(tempo)
            all_tempos.append(int(round(tempo)))
            
            # Enstrüman tespiti
            stft = librosa.stft(y_seg)
            magnitude = np.abs(stft)
            frequency_bins = librosa.fft_frequencies(sr=sr)
            
            segment_instruments = []
            for inst, (low, high) in INSTRUMENT_FREQUENCIES.items():
                freq_mask = (frequency_bins >= low) & (frequency_bins <= high)
                if np.any(freq_mask):
                    energy = np.mean(magnitude[freq_mask, :])
                    if energy > 0.1:
                        segment_instruments.append(inst)
            
            all_instruments.extend(segment_instruments)
            
        except:
            continue
    
    # En sık görülen enstrümanları seç
    from collections import Counter
    instrument_counts = Counter(all_instruments)
    most_common = [inst for inst, count in instrument_counts.most_common(6)]
    
    # Ortalama tempo
    avg_tempo = int(round(np.mean(all_tempos))) if all_tempos else 120
    
    return {
        'instruments': most_common,
        'tempo': avg_tempo,
        'multiple_segments': True
    }

def analyze_audio(audio_file, skip_seconds=5, analysis_duration=90):
    """
    Audio dosyasını analiz eder (geliştirilmiş versiyon)
    
    Args:
        audio_file: Audio dosya yolu
        skip_seconds: Başlangıçtan kaç saniye atla (reklamları atlamak için)
        analysis_duration: Analiz edilecek süre (saniye) - daha uzun = daha iyi tespit
    
    Returns:
        dict: Analiz sonuçları
    """
    print(f"🔍 Analyzing audio: {audio_file}")
    print(f"   ⏱️  Analysis duration: {analysis_duration}s (skip first {skip_seconds}s)")
    
    # Gerekirse WAV'a çevir
    audio_file = convert_to_wav_if_needed(audio_file)
    
    # Önce tüm dosyayı yükle (süre kontrolü için)
    try:
        y_full, sr_full = librosa.load(audio_file, sr=None)
        total_duration = len(y_full) / sr_full
        print(f"   📊 Total duration: {total_duration:.1f}s")
        
        # Analiz süresini dosya uzunluğuna göre ayarla
        max_analysis = min(analysis_duration, total_duration - skip_seconds - 5)
        if max_analysis < 10:
            max_analysis = min(30, total_duration)
            skip_seconds = 0
        
        print(f"   🎯 Analyzing {max_analysis:.1f}s of audio...")
    except Exception as e:
        print(f"   ⚠️  Could not get file duration: {e}")
        max_analysis = analysis_duration
    
    # Audio yükle (daha uzun analiz için)
    try:
        y, sr = librosa.load(audio_file, sr=None, offset=skip_seconds, duration=max_analysis)
        print(f"   ✅ Loaded {len(y)/sr:.1f}s of audio")
    except Exception as e:
        print(f"   ⚠️  Error with offset, trying without: {e}")
        # Offset olmadan dene
        try:
            y, sr = librosa.load(audio_file, sr=None, duration=max_analysis)
            print(f"   ✅ Loaded {len(y)/sr:.1f}s of audio (no offset)")
        except Exception as e2:
            # Daha kısa süre dene
            try:
                y, sr = librosa.load(audio_file, sr=None, duration=30)
                print(f"   ✅ Loaded {len(y)/sr:.1f}s of audio (fallback)")
            except Exception as e3:
                print(f"❌ Error loading audio: {e3}")
                return None
    
    # Tempo analizi
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray):
        tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
    else:
        tempo = float(tempo)
    tempo = int(round(tempo))
    
    # Key detection (basit)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_idx = np.argmax(chroma_mean)
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    estimated_key = keys[key_idx]
    
    # Spektral analiz
    stft = librosa.stft(y)
    magnitude = np.abs(stft)
    frequency_bins = librosa.fft_frequencies(sr=sr)
    
    # Enstrüman tespiti (frekans analizi + spektral özellikler)
    detected_instruments = []
    instrument_scores = {}
    
    # Temel frekans analizi
    for instrument, (low_freq, high_freq) in INSTRUMENT_FREQUENCIES.items():
        # Frekans aralığındaki enerjiyi hesapla
        freq_mask = (frequency_bins >= low_freq) & (frequency_bins <= high_freq)
        if np.any(freq_mask):
            energy = np.mean(magnitude[freq_mask, :])
            instrument_scores[instrument] = energy
    
    # Spektral özellikler (daha gelişmiş tespit)
    mean_energy = np.mean(list(instrument_scores.values())) if instrument_scores else 0.1
    
    # Kemençe tespiti: Yüksek frekanslarda güçlü, harmonik zengin, karakteristik tını
    # Karadeniz kemençesi: 200-3000 Hz arası, özellikle 800-2000 Hz'de güçlü
    kemenche_range = (frequency_bins >= 800) & (frequency_bins <= 2500)
    if np.any(kemenche_range):
        kemenche_energy = np.mean(magnitude[kemenche_range, :])
        # Harmonik zenginlik kontrolü (spektral centroid)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        high_centroid = np.mean(spectral_centroids) > 2000  # Yüksek spektral centroid
        
        # Daha hassas tespit: Eğer yüksek frekanslarda güçlü enerji varsa ve violin tespit edildiyse, kemençe olabilir
        violin_detected = instrument_scores.get('violin', 0) > 0
        if kemenche_energy > mean_energy * 1.2 or (kemenche_energy > mean_energy * 1.0 and high_centroid) or violin_detected:
            instrument_scores['kemenche'] = instrument_scores.get('kemenche', 0) + kemenche_energy * 1.0
            # Eğer violin tespit edildiyse ama kemençe daha uygun olabilir
            if violin_detected and kemenche_energy > instrument_scores.get('violin', 0):
                instrument_scores['kemenche'] = instrument_scores.get('kemenche', 0) + kemenche_energy * 0.5
    
    # Tulum tespiti: Orta-yüksek frekanslarda karakteristik ses, sürekli ton
    tulum_range = (frequency_bins >= 400) & (frequency_bins <= 1800)
    if np.any(tulum_range):
        tulum_energy = np.mean(magnitude[tulum_range, :])
        # Tulum genelde sürekli ton üretir (düşük varyans)
        tulum_variance = np.var(magnitude[tulum_range, :])
        if tulum_energy > mean_energy * 1.2 and tulum_variance < np.var(magnitude) * 0.8:
            instrument_scores['tulum'] = instrument_scores.get('tulum', 0) + tulum_energy * 0.6
    
    # Zurna tespiti: Çok yüksek, keskin frekanslar
    zurna_range = (frequency_bins >= 1500) & (frequency_bins <= 5000)
    if np.any(zurna_range):
        zurna_energy = np.mean(magnitude[zurna_range, :])
        if zurna_energy > mean_energy * 1.4:
            instrument_scores['zurna'] = instrument_scores.get('zurna', 0) + zurna_energy * 0.5
    
    # Davul tespiti: Düşük frekanslarda güçlü vuruşlar, ritmik pattern
    davul_range = (frequency_bins >= 50) & (frequency_bins <= 300)
    if np.any(davul_range):
        davul_energy = np.mean(magnitude[davul_range, :])
        # Ritmik pattern kontrolü
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        rhythmic = len(onset_frames) > 10  # Yeterli vuruş varsa
        
        if davul_energy > mean_energy * 1.1 and rhythmic:
            instrument_scores['davul'] = instrument_scores.get('davul', 0) + davul_energy * 0.7
    
    # En yüksek enerjili enstrümanları seç
    sorted_instruments = sorted(instrument_scores.items(), key=lambda x: x[1], reverse=True)
    detected_instruments = [inst for inst, score in sorted_instruments[:6] if score > 0.1]
    
    # Müzik türü tahmini
    estimated_genre = estimate_genre(tempo, detected_instruments, instrument_scores)
    
    # Enerji seviyesi
    rms = librosa.feature.rms(y=y)[0]
    energy_level = 'high' if np.mean(rms) > 0.1 else 'medium' if np.mean(rms) > 0.05 else 'low'
    
    # Bas vurgusu
    bass_energy = instrument_scores.get('bass', 0) + instrument_scores.get('kick_drum', 0)
    bass_prominent = bass_energy > np.mean(list(instrument_scores.values()))
    
    analysis = {
        'tempo': tempo,
        'key': estimated_key,
        'instruments': detected_instruments,
        'instrument_scores': instrument_scores,
        'estimated_genre': estimated_genre,
        'energy_level': energy_level,
        'bass_prominent': bass_prominent,
        'duration': len(y) / sr
    }
    
    return analysis

def estimate_genre(tempo, instruments, instrument_scores):
    """Müzik türü tahmini"""
    scores = {}
    
    # Önce Karadeniz müziği kontrolü (öncelikli)
    if any(inst in ['kemenche', 'tulum', 'zurna', 'davul'] for inst in instruments):
        karadeniz_score = 0
        if 'kemenche' in instruments:
            karadeniz_score += 3  # Kemençe çok karakteristik
        if 'tulum' in instruments:
            karadeniz_score += 2
        if 'davul' in instruments:
            karadeniz_score += 1
        if 'zurna' in instruments:
            karadeniz_score += 1
        
        tempo_min, tempo_max = GENRE_CHARACTERISTICS['karadeniz']['tempo_range']
        if tempo_min <= tempo <= tempo_max:
            karadeniz_score += 2
        
        if karadeniz_score >= 3:  # Eşik değer
            return 'karadeniz'
    
    for genre, characteristics in GENRE_CHARACTERISTICS.items():
        if genre == 'karadeniz':  # Zaten kontrol ettik
            continue
            
        score = 0
        
        # Tempo uyumu
        tempo_min, tempo_max = characteristics['tempo_range']
        if tempo_min <= tempo <= tempo_max:
            score += 2
        
        # Enstrüman uyumu
        if characteristics.get('bass_prominent') and 'bass' in instruments:
            score += 1
        if characteristics.get('guitar_prominent') and any('guitar' in inst for inst in instruments):
            score += 1
        if characteristics.get('piano_prominent') and 'piano' in instruments:
            score += 1
        if characteristics.get('synthesizer_prominent') and 'synthesizer' in instruments:
            score += 1
        if characteristics.get('kemenche_prominent') and 'kemenche' in instruments:
            score += 3
        if characteristics.get('tulum_prominent') and 'tulum' in instruments:
            score += 2
        if characteristics.get('davul_prominent') and 'davul' in instruments:
            score += 1
        if characteristics.get('baglama_prominent') and 'baglama' in instruments:
            score += 2
        
        scores[genre] = score
    
    # En yüksek skorlu türü döndür
    if scores:
        best_genre = max(scores.items(), key=lambda x: x[1])[0]
        if scores[best_genre] > 0:
            return best_genre
    
    return 'unknown'

def analysis_to_prompt(analysis, similarity_level='high'):
    """
    Analiz sonuçlarından prompt oluşturur (geliştirilmiş versiyon)
    
    Args:
        analysis: Analiz sonuçları
        similarity_level: Benzerlik seviyesi ('high', 'medium', 'low')
    """
    prompt_parts = []
    
    # Karadeniz müziği özel işleme
    is_karadeniz = (
        'kemenche' in analysis.get('instruments', []) or
        'tulum' in analysis.get('instruments', []) or
        analysis.get('estimated_genre') == 'karadeniz' or
        'karadeniz' in str(analysis.get('estimated_genre', '')).lower()
    )
    
    if is_karadeniz:
        prompt_parts.append("Turkish Black Sea music (Karadeniz müziği)")
        prompt_parts.append("traditional Karadeniz style")
        prompt_parts.append("energetic, rhythmic, folk music")
    
    # Müzik türü
    if not is_karadeniz:
        if analysis['estimated_genre'] != 'unknown':
            genre_name = analysis['estimated_genre']
            # Türkçe türler için özel işleme
            if genre_name == 'turkish_folk':
                prompt_parts.append("Turkish folk music")
            elif genre_name == 'turkish_pop':
                prompt_parts.append("Turkish pop music")
            else:
                prompt_parts.append(f"{genre_name} music")
        else:
            prompt_parts.append("music")
    
    # Enstrümanlar (daha iyi işleme)
    if analysis['instruments']:
        instrument_names = []
        seen_drums = False
        
        # Enstrüman isimlerini düzelt ve zenginleştir
        instrument_map = {
            'kemenche': 'kemenche (Karadeniz kemençesi)',
            'tulum': 'tulum (Karadeniz bagpipe)',
            'davul': 'davul (drum)',
            'zurna': 'zurna',
            'baglama': 'bağlama (saz)',
            'kick_drum': 'kick drum',
            'snare_drum': 'snare drum',
            'hi_hat': 'hi-hat',
            'electric_guitar': 'electric guitar',
            'synthesizer': 'synthesizer',
        }
        
        for inst in analysis['instruments']:
            if inst in ['kick_drum', 'snare_drum', 'hi_hat']:
                if not seen_drums:
                    instrument_names.append('drums')
                    seen_drums = True
            elif inst == 'electric_guitar':
                instrument_names.append('electric guitar')
            elif inst == 'guitar':
                instrument_names.append('guitar')
            elif inst == 'saxophone':
                instrument_names.append('saxophone')
            elif inst == 'violin':
                instrument_names.append('violin')
            elif inst == 'cello':
                instrument_names.append('cello')
            elif inst == 'trumpet':
                instrument_names.append('trumpet')
            elif inst == 'piano':
                instrument_names.append('piano')
            elif inst == 'bass':
                instrument_names.append('bass')
            elif inst == 'synthesizer':
                instrument_names.append('synthesizer')
            elif inst == 'kemenche':
                instrument_names.append('kemenche (Karadeniz kemençesi)')
            elif inst == 'tulum':
                instrument_names.append('tulum (Karadeniz tulumu)')
            elif inst == 'davul':
                instrument_names.append('davul')
            elif inst == 'zurna':
                instrument_names.append('zurna')
            elif inst == 'baglama':
                instrument_names.append('bağlama (saz)')
            elif inst == 'accordion':
                instrument_names.append('accordion')
            elif inst != 'vocals':  # Vocals'ı ayrı ekleyeceğiz
                instrument_names.append(inst.replace('_', ' '))
            
            # En fazla 5 enstrüman
            if len(instrument_names) >= 5:
                break
        
        if instrument_names:
            prompt_parts.append(', '.join(instrument_names))
    
    # Tempo
    prompt_parts.append(f"{analysis['tempo']} BPM")
    
    # Enerji seviyesi
    if analysis['energy_level'] == 'high':
        prompt_parts.append('energetic, powerful, driving')
    elif analysis['energy_level'] == 'low':
        prompt_parts.append('calm, relaxed, mellow')
    else:
        prompt_parts.append('moderate energy')
    
    # Bas vurgusu
    if analysis['bass_prominent']:
        prompt_parts.append('strong bass, deep bass line, prominent low end')
    
    # Key (eğer tespit edildiyse)
    if 'key' in analysis and analysis['key']:
        prompt_parts.append(f"key of {analysis['key']}")
    
    # Karadeniz müziği özel işleme
    if analysis['estimated_genre'] == 'karadeniz':
        prompt_parts = ['Turkish Black Sea music (Karadeniz müziği)']
        if 'kemenche' in analysis['instruments']:
            prompt_parts.append('kemenche (Karadeniz kemençesi)')
        if 'tulum' in analysis['instruments']:
            prompt_parts.append('tulum (Karadeniz bagpipe)')
        if 'davul' in analysis['instruments']:
            prompt_parts.append('davul (drum)')
        if 'zurna' in analysis['instruments']:
            prompt_parts.append('zurna')
        prompt_parts.append(f"{analysis['tempo']} BPM")
        prompt_parts.append('traditional Turkish Black Sea style, energetic, rhythmic, folk music')
        prompt_parts.append('melodic, emotional, regional Turkish music')
        if similarity_level == 'high':
            prompt_parts.append('authentic Karadeniz sound, traditional arrangement')
        prompt = ', '.join(prompt_parts)
        return prompt
    
    # Türk müziği ipuçları (eğer Türkçe karakteristikler varsa)
    if 'saxophone' in analysis['instruments'] and analysis['estimated_genre'] in ['blues', 'jazz']:
        prompt_parts.append('melodic, emotional')
    
    # Benzerlik seviyesi
    if similarity_level == 'high':
        prompt_parts.append('similar style, matching tempo and energy')
    elif similarity_level == 'medium':
        prompt_parts.append('inspired by, similar vibe and mood')
    
    # Production
    prompt_parts.append('modern production, professional quality')
    
    prompt = ', '.join(prompt_parts)
    return prompt

def generate_similar_music(audio_source, output_dir='output', duration=30, 
                          model_size='small', similarity_level='high',
                          auto_master=False, cleanup_temp=True, skip_seconds=5,
                          manual_instruments=None, manual_genre=None):
    """
    Audio dosyasını analiz edip benzer müzik üretir
    
    Args:
        audio_source: Referans audio dosyası veya YouTube URL
        output_dir: Çıktı klasörü
        duration: Üretilecek müzik süresi
        model_size: Model boyutu
        similarity_level: Benzerlik seviyesi
        auto_master: Otomatik mastering
        cleanup_temp: Geçici dosyaları temizle (YouTube için)
    """
    # Audio dosyasını al (yerel veya YouTube)
    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # YouTube URL ise skip_seconds parametresini geç
    if is_youtube_url(audio_source):
        audio_file = download_youtube_audio(audio_source, output_dir=temp_dir, 
                                           max_duration=60, skip_seconds=skip_seconds)
    else:
        audio_file = get_audio_file(audio_source, temp_dir=temp_dir)
    
    if not audio_file:
        return None
    
    is_temp_file = audio_file.startswith(temp_dir) or 'youtube_audio_temp' in audio_file
    
    try:
        # Analiz (reklamları atla)
        analysis = analyze_audio(audio_file, skip_seconds=skip_seconds if is_youtube_url(audio_source) else 5)
        if not analysis:
            return None
        
        # Manuel düzeltmeler
        if manual_instruments:
            print(f"   🔧 Manual instruments override: {manual_instruments}")
            analysis['instruments'] = manual_instruments + [inst for inst in analysis['instruments'] 
                                                          if inst not in manual_instruments]
        
        if manual_genre:
            print(f"   🔧 Manual genre override: {manual_genre}")
            analysis['estimated_genre'] = manual_genre
        
        # Sonuçları göster
        print("\n📊 Analysis Results:")
        print(f"   Tempo: {analysis['tempo']} BPM")
        print(f"   Estimated Key: {analysis['key']}")
        print(f"   Estimated Genre: {analysis['estimated_genre']}")
        print(f"   Detected Instruments: {', '.join(analysis['instruments'][:6])}")
        print(f"   Energy Level: {analysis['energy_level']}")
        print(f"   Bass Prominent: {analysis['bass_prominent']}")
        
        # Prompt oluştur
        prompt = analysis_to_prompt(analysis, similarity_level)
        print(f"\n🎵 Generated Prompt: {prompt}\n")
        
        # Müzik üret
        from generate import MusicGenerator
        generator = MusicGenerator(model_size=model_size)
        results = generator.generate(
            [prompt],
            output_dir=output_dir,
            duration=duration,
            auto_master=auto_master,
            master_preset='default'
        )
        
        if results:
            print(f"\n✅ Similar music generated: {results[0]}")
            return results[0]
        
        return None
    
    finally:
        # Geçici dosyaları temizle
        if cleanup_temp and is_temp_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
                print(f"🧹 Cleaned up temporary file: {audio_file}")
            except:
                pass

def main():
    parser = argparse.ArgumentParser(
        description='Audio Analizi ve Benzer Müzik Üretimi',
        epilog='Örnek: python audio_analyzer.py "https://www.youtube.com/watch?v=..." --duration 30'
    )
    parser.add_argument('audio_source', type=str, 
                       help='Referans audio dosyası veya YouTube URL')
    parser.add_argument('--output', type=str, default='output', help='Çıktı klasörü')
    parser.add_argument('--duration', type=int, default=30, help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='small', choices=['small', 'medium', 'large'])
    parser.add_argument('--similarity', type=str, default='high',
                       choices=['high', 'medium', 'low'],
                       help='Benzerlik seviyesi')
    parser.add_argument('--master', action='store_true', help='Otomatik mastering')
    parser.add_argument('--analyze-only', action='store_true',
                       help='Sadece analiz yap, müzik üretme')
    parser.add_argument('--keep-temp', action='store_true',
                       help='Geçici dosyaları sakla (YouTube için)')
    parser.add_argument('--skip-seconds', type=int, default=5,
                       help='Başlangıçtan kaç saniye atla (reklamları atlamak için, default: 5)')
    parser.add_argument('--manual-instruments', type=str, default=None,
                       help='Manuel enstrüman listesi (virgülle ayrılmış, örn: "kemenche,tulum,davul")')
    parser.add_argument('--manual-genre', type=str, default=None,
                       help='Manuel müzik türü (örn: "karadeniz", "turkish_folk")')
    
    args = parser.parse_args()
    
    # Manuel enstrümanları parse et
    manual_instruments = None
    if args.manual_instruments:
        manual_instruments = [inst.strip() for inst in args.manual_instruments.split(',')]
    
    if args.analyze_only:
        # Audio dosyasını al
        temp_dir = os.path.join(args.output, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        if is_youtube_url(args.audio_source):
            audio_file = download_youtube_audio(args.audio_source, output_dir=temp_dir, 
                                               max_duration=60, skip_seconds=args.skip_seconds)
        else:
            audio_file = get_audio_file(args.audio_source, temp_dir=temp_dir)
        
        if audio_file:
            analysis = analyze_audio(audio_file, skip_seconds=args.skip_seconds)
            if analysis:
                # Manuel düzeltmeler
                if manual_instruments:
                    analysis['instruments'] = manual_instruments + [inst for inst in analysis['instruments'] 
                                                                  if inst not in manual_instruments]
                if args.manual_genre:
                    analysis['estimated_genre'] = args.manual_genre
                
                print("\n📊 Analysis Results:")
                for key, value in analysis.items():
                    if key != 'instrument_scores':
                        print(f"   {key}: {value}")
            
            # Temizle
            if not args.keep_temp and (audio_file.startswith(temp_dir) or 'youtube_audio_temp' in audio_file):
                try:
                    os.remove(audio_file)
                except:
                    pass
    else:
        generate_similar_music(
            args.audio_source,
            output_dir=args.output,
            duration=args.duration,
            model_size=args.model,
            similarity_level=args.similarity,
            auto_master=args.master,
            cleanup_temp=not args.keep_temp,
            skip_seconds=args.skip_seconds,
            manual_instruments=manual_instruments,
            manual_genre=args.manual_genre
        )

if __name__ == '__main__':
    main()

