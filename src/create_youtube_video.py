"""
YouTube Video Oluşturucu - Muzik + Gorsel
Muzik dosyalari ve goruntuleri eslestirip YouTube videolari olusturur
Statik goruntu + muzik = YouTube video olusturur
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def find_ffmpeg():
    """FFmpeg yolunu bulur"""
    # PATH'te ara
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, 
                               timeout=5)
        if result.returncode == 0:
            return 'ffmpeg'
    except:
        pass
    
    # Winget yolu (Windows)
    import glob
    winget_pattern = os.path.expanduser(
        r'~\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin\ffmpeg.exe'
    )
    matches = glob.glob(winget_pattern)
    if matches:
        return matches[0]
    
    # Common locations
    common_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def create_youtube_video(music_file, image_file, output_file=None, 
                         width=1920, height=1080, duration=None):
    """
    Statik görüntü + müzik = YouTube video oluşturur
    
    Args:
        music_file: Müzik dosyası yolu
        image_file: Görüntü dosyası yolu
        output_file: Çıktı video dosyası
        width: Video genişliği (default: 1920)
        height: Video yüksekliği (default: 1080)
        duration: Video süresi (saniye, None = müzik süresi)
    """
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("[ERROR] FFmpeg not found!")
        print("[INFO] Install FFmpeg: https://ffmpeg.org/download.html")
        return None
    
    # Çıktı dosyası
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(music_file))[0]
        output_file = f"output/youtube_{base_name}.mp4"
    
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # FFmpeg komutu: Statik görüntü + müzik = video
    cmd = [
        ffmpeg,
        '-loop', '1',  # Görüntüyü loop'la
        '-i', image_file,  # Görüntü
        '-i', music_file,  # Müzik
        '-c:v', 'libx264',  # Video codec
        '-tune', 'stillimage',  # Statik görüntü için optimize
        '-c:a', 'aac',  # Audio codec
        '-b:a', '192k',  # Audio bitrate
        '-pix_fmt', 'yuv420p',  # YouTube uyumlu
        '-shortest',  # En kısa dosyaya göre (müzik süresi)
        '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2',  # Çözünürlük + aspect ratio koruma
        '-y',  # Overwrite
        output_file
    ]
    
    if duration:
        # Duration belirtilmişse, shortest yerine -t kullan
        cmd = [
            ffmpeg,
            '-loop', '1',
            '-i', image_file,
            '-i', music_file,
            '-c:v', 'libx264',
            '-tune', 'stillimage',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-pix_fmt', 'yuv420p',
            '-t', str(duration),  # Belirtilen süre
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2',
            '-y',
            output_file
        ]
    
    print(f"[VIDEO] Creating YouTube video...")
    print(f"   Music: {music_file}")
    print(f"   Image: {image_file}")
    print(f"   Output: {output_file}")
    print(f"   Resolution: {width}x{height}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"[SUCCESS] YouTube video created: {output_file}")
            return output_file
        else:
            print(f"[ERROR] FFmpeg failed: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"[ERROR] FFmpeg timeout (10 minutes)")
        return None
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return None

def match_music_with_images(music_dir, image_dir):
    """
    Müzik dosyalarını görsellerle eşleştirir
    
    Args:
        music_dir: Müzik dosyaları klasörü
        image_dir: Görsel dosyaları klasörü
    
    Returns:
        List of tuples: [(music_file, image_file), ...]
    """
    music_dir = Path(music_dir)
    image_dir = Path(image_dir)
    
    if not music_dir.exists():
        print(f"[ERROR] Music directory not found: {music_dir}")
        return []
    
    if not image_dir.exists():
        print(f"[ERROR] Image directory not found: {image_dir}")
        return []
    
    # Müzik dosyalarını bul
    music_files = list(music_dir.glob("*.mp3")) + list(music_dir.glob("*.wav")) + \
                  list(music_dir.glob("*.m4a")) + list(music_dir.glob("*.flac"))
    
    matches = []
    
    for music_file in music_files:
        # Müzik dosyası adı (uzantısız)
        music_name = music_file.stem
        
        # Eşleşen görseli bul
        image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
        image_file = None
        
        for ext in image_extensions:
            potential_image = image_dir / f"{music_name}{ext}"
            if potential_image.exists():
                image_file = potential_image
                break
        
        if image_file:
            matches.append((music_file, image_file))
        else:
            print(f"[WARNING] Image not found for: {music_name}")
    
    return matches

def batch_create_youtube_videos(music_dir, image_dir, output_dir="output/youtube",
                                width=1920, height=1080):
    """
    Tüm müzikleri görsellerle eşleştirip YouTube videoları oluşturur
    
    Args:
        music_dir: Müzik dosyaları klasörü
        image_dir: Görsel dosyaları klasörü
        output_dir: Çıktı video klasörü
        width: Video genişliği
        height: Video yüksekliği
    
    Returns:
        List of created video files
    """
    matches = match_music_with_images(music_dir, image_dir)
    
    if not matches:
        print("[ERROR] No music-image pairs found!")
        return []
    
    print(f"[MATCHES] Found {len(matches)} music-image pairs")
    print()
    
    results = []
    
    for i, (music_file, image_file) in enumerate(matches, 1):
        print(f"[{i}/{len(matches)}] Processing: {music_file.name}")
        
        output_file = os.path.join(output_dir, f"{music_file.stem}_youtube.mp4")
        os.makedirs(output_dir, exist_ok=True)
        
        result = create_youtube_video(
            str(music_file),
            str(image_file),
            output_file,
            width=width,
            height=height
        )
        
        if result:
            results.append(result)
        print()
    
    print(f"[SUCCESS] Created {len(results)}/{len(matches)} YouTube videos")
    return results

def main():
    parser = argparse.ArgumentParser(
        description='YouTube Video Oluşturucu - Müzik + Görsel',
        epilog='Örnek: python src/create_youtube_video.py --music-dir "D:\\Neutral Beats Studio" --image-dir "D:\\Neutral Beats Studio\\Music Resim"'
    )
    parser.add_argument('--music-dir', type=str, 
                       default=r'D:\Neutral Beats Studio',
                       help='Müzik dosyaları klasörü')
    parser.add_argument('--image-dir', type=str,
                       default=r'D:\Neutral Beats Studio\Music Resim',
                       help='Görsel dosyaları klasörü')
    parser.add_argument('--output-dir', type=str,
                       default='output/youtube',
                       help='Çıktı video klasörü')
    parser.add_argument('--single', type=str, default=None,
                       help='Tek bir müzik dosyası işle (dosya adı)')
    parser.add_argument('--width', type=int, default=1920,
                       help='Video genişliği (default: 1920)')
    parser.add_argument('--height', type=int, default=1080,
                       help='Video yüksekliği (default: 1080)')
    
    args = parser.parse_args()
    
    if args.single:
        # Tek dosya işle
        music_file = os.path.join(args.music_dir, args.single)
        if not os.path.exists(music_file):
            print(f"[ERROR] Music file not found: {music_file}")
            return
        
        music_name = os.path.splitext(args.single)[0]
        image_file = None
        
        for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
            potential = os.path.join(args.image_dir, f"{music_name}{ext}")
            if os.path.exists(potential):
                image_file = potential
                break
        
        if not image_file:
            print(f"[ERROR] Image not found for: {args.single}")
            return
        
        output_file = os.path.join(args.output_dir, f"{music_name}_youtube.mp4")
        os.makedirs(args.output_dir, exist_ok=True)
        
        create_youtube_video(music_file, image_file, output_file,
                           width=args.width, height=args.height)
    else:
        # Toplu işle
        batch_create_youtube_videos(
            args.music_dir,
            args.image_dir,
            args.output_dir,
            width=args.width,
            height=args.height
        )

if __name__ == '__main__':
    main()

