"""
Hareketli Arka Plan Video Oluşturucu
Şarkı sözlerine göre animasyonlu arka plan videoları oluşturur
Yağmur, araba hareketi, ışık animasyonları vb.
"""

import os
import sys
import subprocess
import argparse
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter
import random
import math

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def find_ffmpeg():
    """FFmpeg yolunu bulur"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, 
                               timeout=5)
        if result.returncode == 0:
            return 'ffmpeg'
    except:
        pass
    
    import glob
    winget_pattern = os.path.expanduser(
        r'~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin\ffmpeg.exe'
    )
    matches = glob.glob(winget_pattern)
    if matches:
        return matches[0]
    
    common_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def create_rain_effect(width, height, frame_count, intensity=0.5):
    """
    Yağmur efekti oluşturur
    """
    frames = []
    
    # Yağmur damlaları için particle system
    rain_drops = []
    num_drops = int(width * height * intensity * 0.0001)
    
    for _ in range(num_drops):
        rain_drops.append({
            'x': random.randint(0, width),
            'y': random.randint(-height, 0),
            'speed': random.uniform(5, 15),
            'length': random.randint(10, 30),
            'opacity': random.uniform(0.3, 0.8)
        })
    
    for frame_idx in range(frame_count):
        # Koyu mavi arka plan (gece)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = [20, 25, 40]  # Koyu mavi-gece rengi
        
        # Yağmur damlalarını çiz
        for drop in rain_drops:
            drop['y'] += drop['speed']
            
            # Ekranın dışına çıktıysa yukarıdan başlat
            if drop['y'] > height:
                drop['y'] = random.randint(-height, 0)
                drop['x'] = random.randint(0, width)
            
            # Yağmur çizgisi
            end_y = int(drop['y'] + drop['length'])
            color = (255, 255, 255, int(255 * drop['opacity']))
            
            # OpenCV ile çiz
            cv2.line(frame, 
                    (int(drop['x']), int(drop['y'])),
                    (int(drop['x']), min(end_y, height)),
                    (255, 255, 255),
                    1)
        
        frames.append(frame)
    
    return frames

def create_car_interior_effect(width, height, frame_count):
    """
    Gerçekçi araba içi hareket efekti oluşturur
    Gösterge paneli, direksiyon, ön cam, yağmur ve bulanık şehir ışıkları
    """
    frames = []
    
    # Gösterge paneli ve direksiyon için sabit öğeler
    dashboard_bottom = int(height * 0.65)  # Gösterge paneli alt sınırı (daha yukarı)
    windshield_top = int(height * 0.05)  # Ön cam üst sınırı (daha yukarı)
    windshield_bottom = int(height * 0.60)  # Ön cam alt sınırı (daha aşağı)
    
    # Şehir ışıkları (bokeh efektleri için) - ÇOK DAHA FAZLA
    city_lights = []
    for _ in range(80):  # 80 farklı ışık kaynağı (daha fazla)
        city_lights.append({
            'x': random.randint(0, width),
            'y': random.randint(windshield_top, windshield_bottom),
            'color': random.choice([
                (255, 255, 180),  # Sarı (sokak lambaları) - daha parlak
                (255, 120, 120),  # Kırmızı (trafik ışıkları, neon)
                (180, 220, 255),  # Mavi (neon, LED) - daha parlak
                (255, 255, 255),  # Beyaz (araç farları)
                (120, 255, 180),  # Yeşil (neon)
                (255, 200, 150),  # Turuncu (sokak lambaları)
            ]),
            'size': random.randint(25, 80),  # Daha büyük ışıklar
            'intensity': random.uniform(0.7, 1.0),
            'speed': random.uniform(0.3, 1.8)  # Hareket hızı
        })
    
    # Yağmur damlaları - DAHA GERÇEKÇİ
    rain_drops = []
    for _ in range(200):  # Daha fazla damla
        rain_drops.append({
            'x': random.randint(0, width),
            'y': random.randint(-height, windshield_bottom),
            'speed': random.uniform(10, 25),
            'length': random.randint(8, 20),  # Daha kısa (damla gibi)
            'opacity': random.uniform(0.5, 0.95),
            'width': random.randint(1, 3),  # Daha kalın
            'type': random.choice(['drop', 'streak'])  # Damla veya çizgi
        })
    
    for frame_idx in range(frame_count):
        # Araba içi arka plan (ÇOK KOYU - neredeyse siyah)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = [2, 2, 4]  # Neredeyse siyah
        
        # Gösterge paneli (alt kısım - daha belirgin)
        cv2.rectangle(frame,
                     (0, dashboard_bottom),
                     (width, height),
                     (15, 15, 18),
                     -1)
        
        # Gösterge paneli üst kenarı (hafif parlaklık)
        cv2.line(frame,
                (0, dashboard_bottom),
                (width, dashboard_bottom),
                (25, 25, 30),
                2)
        
        # Direksiyon (sol alt - daha detaylı)
        steering_wheel_x = int(width * 0.18)
        steering_wheel_y = int(height * 0.70)
        steering_radius = int(width * 0.10)
        
        # Direksiyon çemberi (dış)
        cv2.circle(frame,
                  (steering_wheel_x, steering_wheel_y),
                  steering_radius,
                  (35, 35, 40),
                  4)
        # Direksiyon çemberi (iç)
        cv2.circle(frame,
                  (steering_wheel_x, steering_wheel_y),
                  steering_radius - 8,
                  (25, 25, 30),
                  -1)
        
        # Direksiyon simidi (merkez)
        cv2.circle(frame,
                  (steering_wheel_x, steering_wheel_y),
                  12,
                  (40, 40, 45),
                  -1)
        
        # Direksiyon kolları (4 adet)
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x1 = int(steering_wheel_x + (steering_radius - 15) * math.cos(rad))
            y1 = int(steering_wheel_y + (steering_radius - 15) * math.sin(rad))
            x2 = int(steering_wheel_x + (steering_radius - 5) * math.cos(rad))
            y2 = int(steering_wheel_y + (steering_radius - 5) * math.sin(rad))
            cv2.line(frame, (x1, y1), (x2, y2), (35, 35, 40), 3)
        
        # Gösterge paneli ekranları (sağ alt - daha gerçekçi)
        screen_x = int(width * 0.65)
        screen_y = int(height * 0.72)
        screen_w = int(width * 0.30)
        screen_h = int(height * 0.20)
        
        # Ana ekran
        cv2.rectangle(frame,
                     (screen_x, screen_y),
                     (screen_x + screen_w, screen_y + screen_h),
                     (8, 8, 12),
                     -1)
        cv2.rectangle(frame,
                     (screen_x, screen_y),
                     (screen_x + screen_w, screen_y + screen_h),
                     (25, 25, 30),
                     2)
        
        # Ekran içi hafif parlaklık (gösterge paneli ışıkları)
        for i in range(3):
            x = screen_x + (i * screen_w // 3) + 20
            y = screen_y + screen_h // 2
            cv2.circle(frame, (x, y), 3, (50, 50, 60), -1)
        
        # Ön cam alanı (dışarıdaki manzara)
        scroll_offset = (frame_idx * 1.2) % (width * 2)
        
        # Şehir ışıkları (bokeh efektleri) - ÇOK DAHA BULANIK VE RENKLİ
        for light in city_lights:
            # Işıklar hareket ediyor (parallax)
            light_x = int((light['x'] - scroll_offset * light['speed']) % width)
            
            if windshield_top <= light['y'] <= windshield_bottom:
                # Bokeh efekti (ÇOK DAHA BULANIK)
                size = int(light['size'] * light['intensity'])
                color = tuple(int(c * light['intensity']) for c in light['color'])
                
                # Dış hale (çok büyük, çok şeffaf - bokeh efekti)
                overlay = frame.copy()
                # Çoklu hale katmanları (daha gerçekçi bokeh)
                for halo_size in [size + 40, size + 25, size + 15]:
                    cv2.circle(overlay,
                              (light_x, light['y']),
                              halo_size,
                              color,
                              -1)
                frame = cv2.addWeighted(frame, 0.5, overlay, 0.5, 0)
                
                # Orta hale
                overlay2 = frame.copy()
                cv2.circle(overlay2,
                          (light_x, light['y']),
                          size + 8,
                          color,
                          -1)
                frame = cv2.addWeighted(frame, 0.6, overlay2, 0.4, 0)
                
                # İç parlak nokta
                cv2.circle(frame,
                          (light_x, light['y']),
                          size,
                          color,
                          -1)
                cv2.circle(frame,
                          (light_x, light['y']),
                          max(size // 3, 3),
                          (255, 255, 255),
                          -1)
        
        # Yağmur damlaları (cam üzerinde) - DAHA GERÇEKÇİ
        for drop in rain_drops:
            drop['y'] += drop['speed']
            
            # Ekranın dışına çıktıysa yukarıdan başlat
            if drop['y'] > windshield_bottom:
                drop['y'] = random.randint(-height, windshield_top)
                drop['x'] = random.randint(0, width)
            
            # Cam alanı içindeyse çiz
            if windshield_top <= drop['y'] <= windshield_bottom:
                if drop['type'] == 'drop':
                    # Damla şeklinde (küçük daire)
                    cv2.circle(frame,
                              (int(drop['x']), int(drop['y'])),
                              drop['width'] + 1,
                              (255, 255, 255),
                              -1)
                else:
                    # Çizgi şeklinde
                    end_y = int(drop['y'] + drop['length'])
                    end_y = min(end_y, windshield_bottom)
                    cv2.line(frame,
                            (int(drop['x']), int(drop['y'])),
                            (int(drop['x']), end_y),
                            (255, 255, 255),
                            drop['width'])
        
        # Cam üzerinde su izleri (dikey çizgiler) - daha sık
        if frame_idx % 5 == 0:  # Her 5 frame'de bir
            for _ in range(8):  # Daha fazla su izi
                x = random.randint(0, width)
                start_y = random.randint(windshield_top, windshield_bottom - 40)
                end_y = start_y + random.randint(30, 70)
                end_y = min(end_y, windshield_bottom)
                
                # Su izi (hafif beyaz çizgi)
                cv2.line(frame,
                        (x, start_y),
                        (x, end_y),
                        (180, 180, 180),
                        1)
        
        frames.append(frame)
    
    return frames

def create_window_rainy_night(width, height, frame_count):
    """
    Gerçekçi pencere görünümü + yağmurlu gece
    Bulanık şehir ışıkları ve yağmur damlaları
    """
    frames = []
    
    # Pencere çerçevesi
    window_top = int(height * 0.15)
    window_bottom = int(height * 0.85)
    window_left = int(width * 0.1)
    window_right = int(width * 0.9)
    
    # Şehir ışıkları (bokeh efektleri)
    city_lights = []
    for _ in range(40):
        city_lights.append({
            'x': random.randint(window_left, window_right),
            'y': random.randint(window_top, window_bottom),
            'color': random.choice([
                (255, 255, 150),  # Sarı
                (255, 100, 100),  # Kırmızı
                (150, 200, 255),  # Mavi
                (255, 255, 255),  # Beyaz
                (100, 255, 150),  # Yeşil
            ]),
            'size': random.randint(20, 50),
            'intensity': random.uniform(0.5, 1.0),
            'speed': random.uniform(0.3, 1.5)
        })
    
    # Yağmur damlaları
    rain_drops = []
    for _ in range(150):
        rain_drops.append({
            'x': random.randint(window_left, window_right),
            'y': random.randint(-height, window_top),
            'speed': random.uniform(10, 25),
            'length': random.randint(15, 35),
            'opacity': random.uniform(0.5, 0.95),
            'width': random.randint(1, 2)
        })
    
    for frame_idx in range(frame_count):
        # İç mekan arka plan (çok koyu)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = [8, 8, 12]  # Çok koyu
        
        # Pencere camı alanı (dışarıdaki manzara)
        scroll_offset = (frame_idx * 1.2) % (width * 2)
        
        # Şehir ışıkları (bokeh - bulanık, renkli)
        for light in city_lights:
            light_x = int((light['x'] - scroll_offset * light['speed']) % width)
            if light_x < window_left:
                light_x += (window_right - window_left)
            
            if window_left <= light_x <= window_right and window_top <= light['y'] <= window_bottom:
                size = int(light['size'] * light['intensity'])
                color = tuple(int(c * light['intensity']) for c in light['color'])
                
                # Bokeh efekti (bulanık hale)
                overlay = frame.copy()
                cv2.circle(overlay,
                          (light_x, light['y']),
                          size + 15,
                          color,
                          -1)
                frame = cv2.addWeighted(frame, 0.6, overlay, 0.4, 0)
                
                # Parlak merkez
                cv2.circle(frame,
                          (light_x, light['y']),
                          size,
                          color,
                          -1)
                cv2.circle(frame,
                          (light_x, light['y']),
                          size // 2,
                          (255, 255, 255),
                          -1)
        
        # Yağmur damlaları (cam üzerinde)
        for drop in rain_drops:
            drop['y'] += drop['speed']
            
            if drop['y'] > window_bottom:
                drop['y'] = random.randint(-height, window_top)
                drop['x'] = random.randint(window_left, window_right)
            
            if window_left <= drop['x'] <= window_right and window_top <= drop['y'] <= window_bottom:
                end_y = int(drop['y'] + drop['length'])
                end_y = min(end_y, window_bottom)
                
                cv2.line(frame,
                        (int(drop['x']), int(drop['y'])),
                        (int(drop['x']), end_y),
                        (255, 255, 255),
                        drop['width'])
        
        # Su izleri (cam üzerinde dikey çizgiler)
        if frame_idx % 8 == 0:
            for _ in range(8):
                x = random.randint(window_left, window_right)
                start_y = random.randint(window_top, window_bottom - 40)
                end_y = start_y + random.randint(30, 60)
                end_y = min(end_y, window_bottom)
                
                cv2.line(frame,
                        (x, start_y),
                        (x, end_y),
                        (180, 180, 180),
                        1)
        
        # Pencere çerçevesi (kalın, koyu)
        frame_thickness = 8
        cv2.rectangle(frame,
                     (window_left, window_top),
                     (window_right, window_bottom),
                     (30, 30, 35),
                     frame_thickness)
        
        # İç çerçeve (ince)
        cv2.rectangle(frame,
                     (window_left + 5, window_top + 5),
                     (window_right - 5, window_bottom - 5),
                     (20, 20, 25),
                     2)
        
        frames.append(frame)
    
    return frames

def create_cozy_room_effect(width, height, frame_count):
    """
    Rahat oda + pencere görünümü
    """
    frames = []
    
    for frame_idx in range(frame_count):
        # Sıcak, rahat oda arka planı
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Sıcak altın-sarı tonlar
        base_color = [40, 35, 25]  # Sıcak kahverengi
        frame[:, :] = base_color
        
        # Pencere (üst kısım)
        window_top = int(height * 0.1)
        window_bottom = int(height * 0.5)
        window_left = int(width * 0.2)
        window_right = int(width * 0.8)
        
        # Pencere dışı (gece)
        frame[window_top:window_bottom, window_left:window_right] = [15, 20, 30]
        
        # Işık animasyonu (yanıp sönen)
        light_intensity = 0.5 + 0.3 * math.sin(frame_idx * 0.1)
        light_color = [int(255 * light_intensity), int(200 * light_intensity), int(150 * light_intensity)]
        
        # Pencere çerçevesi
        cv2.rectangle(frame,
                     (window_left, window_top),
                     (window_right, window_bottom),
                     (80, 70, 60),
                     3)
        
        frames.append(frame)
    
    return frames

def frames_to_video(frames, output_path, fps=30, audio_file=None):
    """
    Frame'leri video'ya dönüştürür
    """
    if not frames:
        return None
    
    height, width = frames[0].shape[:2]
    
    # Geçici video dosyası
    temp_video = output_path.replace('.mp4', '_temp.mp4')
    
    # FFmpeg ile video oluştur
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("[ERROR] FFmpeg not found!")
        print("[INFO] Install FFmpeg: https://ffmpeg.org/download.html")
        return None
    
    # Frame'leri geçici dizine kaydet
    temp_dir = os.path.join(os.path.dirname(output_path), 'temp_frames')
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"[FRAMES] Saving {len(frames)} frames...")
    for i, frame in enumerate(frames):
        frame_path = os.path.join(temp_dir, f'frame_{i:06d}.jpg')
        cv2.imwrite(frame_path, frame)
    
    # FFmpeg ile video oluştur
    print(f"[VIDEO] Creating video from frames...")
    
    # Önce sadece video oluştur (ses olmadan)
    cmd_video = [
        ffmpeg,
        '-y',  # Overwrite
        '-framerate', str(fps),
        '-i', os.path.join(temp_dir, 'frame_%06d.jpg'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '23',
        '-an',  # Ses yok (şimdilik)
        temp_video
    ]
    
    try:
        result = subprocess.run(cmd_video, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"[ERROR] FFmpeg video creation failed: {result.stderr}")
            return None
        
        # Eğer ses dosyası varsa, sonra ekle
        if audio_file and os.path.exists(audio_file):
            print(f"[AUDIO] Adding audio to video...")
            final_video = output_path
            cmd_audio = [
                ffmpeg,
                '-y',
                '-i', temp_video,
                '-i', audio_file,
                '-c:v', 'copy',  # Video'yu kopyala (yeniden encode etme)
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                final_video
            ]
            
            result = subprocess.run(cmd_audio, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                print(f"[WARNING] Audio addition failed: {result.stderr}")
                print(f"[INFO] Video without audio saved: {temp_video}")
                return temp_video
        else:
            final_video = output_path
            if os.path.exists(temp_video):
                if os.path.exists(final_video):
                    os.remove(final_video)
                os.rename(temp_video, final_video)
        
        # Geçici dosyaları temizle
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        if os.path.exists(final_video):
            return final_video
        else:
            return None
            
    except subprocess.TimeoutExpired:
        print(f"[ERROR] FFmpeg timeout (5 minutes)")
        return None
    except Exception as e:
        print(f"[ERROR] Error creating video: {e}")
        return None
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            # Geçici dosyaları temizle
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # Final dosyaya taşı
            if os.path.exists(temp_video):
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(temp_video, output_path)
                return output_path
        else:
            print(f"[ERROR] FFmpeg failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"[ERROR] Error creating video: {e}")
        return None

def create_animated_background(lyrics_file, audio_file, output_file=None, 
                               width=1920, height=1080, fps=30, duration=None):
    """
    Şarkı sözlerine göre animasyonlu arka plan video oluşturur
    """
    print("="*70)
    print("HAREKETLI ARKA PLAN VIDEO OLUSTURUCU")
    print("="*70)
    print()
    
    # Şarkı sözlerini analiz et
    from analyze_environment import analyze_lyrics_environment
    
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        lyrics = f.read()
    
    environment = analyze_lyrics_environment(lyrics)
    env_name = None
    
    # Ortam adını bul - önce car_interior kontrol et
    lyrics_lower = lyrics.lower()
    
    # Araba içi için özel kontrol
    if any(word in lyrics_lower for word in ['car', 'drive', 'driving', 'road', 'vehicle', 'interior']):
        env_name = 'car_interior'
    elif any(word in lyrics_lower for word in ['rain', 'rainy', 'window', 'night']):
        env_name = 'window_rainy_night'
    elif any(word in lyrics_lower for word in ['room', 'cozy', 'warm', 'home']):
        env_name = 'cozy_room_window'
    else:
        # Varsayılan: araba içi (en gerçekçi görünüm)
        env_name = 'car_interior'
    
    print(f"[ENVIRONMENT] Tespit edilen ortam: {env_name}")
    print(f"   Açıklama: {environment['description']}")
    print(f"   Ruh hali: {environment['mood']}")
    print()
    
    # Ses dosyası süresini al
    if duration is None and audio_file and os.path.exists(audio_file):
        try:
            import librosa
            audio_data, sr = librosa.load(audio_file, sr=None)
            duration = len(audio_data) / sr
        except:
            duration = 180  # Varsayılan 3 dakika
    
    if duration is None:
        duration = 180
    
    frame_count = int(duration * fps)
    print(f"[SETTINGS] Video ayarları:")
    print(f"   Çözünürlük: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Süre: {duration:.1f} saniye")
    print(f"   Frame sayısı: {frame_count}")
    print()
    
    # Animasyonlu arka plan oluştur
    print(f"[ANIMATION] Animasyonlu arka plan oluşturuluyor...")
    
    if env_name == 'car_interior':
        frames = create_car_interior_effect(width, height, frame_count)
    elif env_name == 'window_rainy_night':
        frames = create_window_rainy_night(width, height, frame_count)
    elif env_name == 'cozy_room_window':
        frames = create_cozy_room_effect(width, height, frame_count)
    elif env_name == 'rainy_city_night':
        frames = create_rain_effect(width, height, frame_count, intensity=0.6)
    else:
        # Varsayılan: araba içi (en gerçekçi)
        frames = create_car_interior_effect(width, height, frame_count)
    
    print(f"[SUCCESS] {len(frames)} frame oluşturuldu")
    print()
    
    # Video oluştur
    if output_file is None:
        base_name = os.path.splitext(lyrics_file)[0]
        output_file = f"output/{os.path.basename(base_name)}_animated_background.mp4"
    
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    result = frames_to_video(frames, output_file, fps, audio_file)
    
    if result:
        print(f"\n[SUCCESS] Hareketli arka plan video hazır: {result}")
        return result
    else:
        print(f"\n[ERROR] Video oluşturma başarısız")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Hareketli Arka Plan Video Oluşturucu',
        epilog='Örnek: python src/create_animated_background.py --lyrics rainy_city_blues_lyrics.txt --audio "output/Rainy City Blues.mp3"'
    )
    parser.add_argument('--lyrics', type=str, required=True,
                       help='Şarkı sözleri dosyası')
    parser.add_argument('--audio', type=str, required=True,
                       help='Ses dosyası (şarkı)')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı video dosyası')
    parser.add_argument('--width', type=int, default=1920,
                       help='Video genişliği (default: 1920)')
    parser.add_argument('--height', type=int, default=1080,
                       help='Video yüksekliği (default: 1080)')
    parser.add_argument('--fps', type=int, default=30,
                       help='Frame rate (default: 30)')
    parser.add_argument('--duration', type=float, default=None,
                       help='Video süresi (saniye, otomatik: ses dosyasından)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.lyrics):
        parser.error(f"Lyrics file not found: {args.lyrics}")
    
    if not os.path.exists(args.audio):
        parser.error(f"Audio file not found: {args.audio}")
    
    result = create_animated_background(
        args.lyrics,
        args.audio,
        args.output,
        args.width,
        args.height,
        args.fps,
        args.duration
    )
    
    if result:
        print(f"\n[SUCCESS] Final video: {result}")

if __name__ == '__main__':
    main()

