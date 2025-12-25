"""
Orijinal müzik ile şarkı söyleyen video'yu birleştirir
Video'ya orijinal müziği ekler
"""

import os
import sys
import subprocess
import argparse

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

def combine_video_with_music(video_file, music_file, output_file=None, 
                             video_volume=0.3, music_volume=0.7):
    """
    Video'ya orijinal müziği ekler
    
    Args:
        video_file: Şarkı söyleyen video (vokal içeriyor)
        music_file: Orijinal müzik dosyası
        output_file: Çıktı dosyası
        video_volume: Video ses seviyesi (vokal için düşük)
        music_volume: Müzik ses seviyesi (yüksek)
    """
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        print("[ERROR] FFmpeg not found!")
        print("[INFO] Install FFmpeg: https://ffmpeg.org/download.html")
        return None
    
    print(f"[COMBINE] Combining video with original music...")
    print(f"   Video: {video_file}")
    print(f"   Music: {music_file}")
    print(f"   Video volume: {video_volume} (vocal)")
    print(f"   Music volume: {music_volume} (background)")
    
    if not os.path.exists(video_file):
        print(f"[ERROR] Video file not found: {video_file}")
        return None
    
    if not os.path.exists(music_file):
        print(f"[ERROR] Music file not found: {music_file}")
        return None
    
    # Çıktı dosyası
    if output_file is None:
        base_name = os.path.splitext(video_file)[0]
        output_file = f"{base_name}_with_music.mp4"
    
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # FFmpeg komutu: Video sesini düşür, müziği ekle
    cmd = [
        ffmpeg,
        '-i', video_file,  # Video (vokal içeriyor)
        '-i', music_file,  # Orijinal müzik
        '-filter_complex', 
        f'[0:a]volume={video_volume}[vocal];[1:a]volume={music_volume}[music];[vocal][music]amix=inputs=2:duration=first:dropout_transition=2[out]',
        '-map', '0:v',  # Video stream
        '-map', '[out]',  # Mixed audio
        '-c:v', 'copy',  # Video codec (kopyala, yeniden encode etme)
        '-c:a', 'aac',  # Audio codec
        '-b:a', '192k',  # Audio bitrate
        '-shortest',  # En kısa dosyaya göre
        '-y',  # Overwrite
        output_file
    ]
    
    print(f"\n[RUN] Running FFmpeg...")
    print(f"   Command: {' '.join(cmd[:5])} ...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"[SUCCESS] Combined video saved: {output_file}")
            return output_file
        else:
            print(f"[ERROR] FFmpeg failed: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"[ERROR] FFmpeg timeout (5 minutes)")
        return None
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Video ile Orijinal Müziği Birleştirici',
        epilog='Örnek: python src/combine_music_with_video.py --video output/female_singer_main_did_video.mp4 --music "output/Rainy City Blues.mp3"'
    )
    parser.add_argument('--video', type=str, required=True,
                       help='Şarkı söyleyen video dosyası')
    parser.add_argument('--music', type=str, required=True,
                       help='Orijinal müzik dosyası')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı video dosyası')
    parser.add_argument('--video-volume', type=float, default=0.3,
                       help='Video ses seviyesi (vokal, 0-1, default: 0.3)')
    parser.add_argument('--music-volume', type=float, default=0.7,
                       help='Müzik ses seviyesi (0-1, default: 0.7)')
    
    args = parser.parse_args()
    
    result = combine_video_with_music(
        args.video,
        args.music,
        args.output,
        args.video_volume,
        args.music_volume
    )
    
    if result:
        print(f"\n[SUCCESS] Final video with music: {result}")

if __name__ == '__main__':
    main()


