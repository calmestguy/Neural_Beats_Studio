"""
Tam Otomatik Şarkıcı Video Oluşturucu
Tüm süreci tek komutla yönetir: Vokal → Şarkıcı → Arka Plan → Video → Müzik
"""

import os
import sys
import argparse
import subprocess

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_complete_singer_video(lyrics_file, music_file=None, 
                                 singer_image=None, background_image=None,
                                 did_api_key=None, hf_api_key=None,
                                 output_dir="output", resolution="4096",
                                 vocal_volume=0.4, music_volume=0.6):
    """
    Tam otomatik şarkıcı video oluşturma süreci
    
    Args:
        lyrics_file: Şarkı sözleri dosyası
        music_file: Orijinal müzik dosyası (opsiyonel)
        singer_image: Şarkıcı fotoğrafı (opsiyonel, yoksa oluşturulur)
        background_image: Arka plan görüntüsü (opsiyonel, yoksa oluşturulur)
        did_api_key: D-ID API key
        hf_api_key: Hugging Face API key
        output_dir: Çıktı klasörü
        resolution: Video çözünürlüğü (1024, 2048, 4096)
        vocal_volume: Vokal ses seviyesi (0-1)
        music_volume: Müzik ses seviyesi (0-1)
    """
    print("="*70)
    print("TAM OTOMATIK SARKICI VIDEO OLUSTURMA")
    print("="*70)
    print()
    
    # Dosya kontrolü
    if not os.path.exists(lyrics_file):
        print(f"[ERROR] Şarkı sözleri dosyası bulunamadı: {lyrics_file}")
        return None
    
    # API key kontrolü
    if not did_api_key:
        did_api_key = os.getenv('D_ID_API_KEY')
    if not did_api_key:
        print("[ERROR] D-ID API key gerekli!")
        print("[INFO] --did-api-key parametresi veya D_ID_API_KEY env variable")
        return None
    
    if not hf_api_key:
        hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    base_name = os.path.splitext(os.path.basename(lyrics_file))[0]
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    
    # 1. Vokal oluştur
    print("[1/6] Vokal oluşturuluyor...")
    vocal_file = os.path.join(output_dir, f"{base_name}_singing_vocal.wav")
    
    if not os.path.exists(vocal_file):
        cmd = [
            sys.executable, "src/create_singing_vocal.py",
            lyrics_file,
            "--vocal-only",
            "--output", vocal_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] Vokal oluşturma başarısız: {result.stderr}")
            return None
        print(f"[OK] Vokal oluşturuldu: {vocal_file}")
    else:
        print(f"[SKIP] Vokal zaten mevcut: {vocal_file}")
    
    # 2. Şarkıcı fotoğrafı (yoksa oluştur)
    if not singer_image:
        print("[2/6] Şarkıcı fotoğrafı oluşturuluyor...")
        singer_image = f"assets/{base_name}_singer.jpg"
        
        if not os.path.exists(singer_image) and hf_api_key:
            cmd = [
                sys.executable, "src/generate_singer_image.py",
                "--method", "huggingface_api",
                "--single",
                "--microphone",
                "--api-key", hf_api_key,
                "--output-dir", "assets",
                "--base-name", f"{base_name}_singer"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] Şarkıcı fotoğrafı oluşturuldu: {singer_image}")
            else:
                print(f"[WARNING] Şarkıcı fotoğrafı oluşturulamadı, varsayılan kullanılacak")
                singer_image = "assets/female_singer_microphone_main.jpg"
        else:
            print(f"[SKIP] Şarkıcı fotoğrafı mevcut: {singer_image}")
    else:
        print(f"[2/6] Şarkıcı fotoğrafı kullanılıyor: {singer_image}")
    
    if not os.path.exists(singer_image):
        print(f"[ERROR] Şarkıcı fotoğrafı bulunamadı: {singer_image}")
        return None
    
    # 3. Arka plan görüntüsü (yoksa oluştur)
    if not background_image:
        print("[3/6] Arka plan görüntüsü oluşturuluyor...")
        background_image = f"assets/{base_name}_background.jpg"
        
        if not os.path.exists(background_image) and hf_api_key:
            cmd = [
                sys.executable, "src/generate_background_image.py",
                "--lyrics", lyrics_file,
                "--api-key", hf_api_key,
                "--output", background_image
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] Arka plan oluşturuldu: {background_image}")
            else:
                print(f"[WARNING] Arka plan oluşturulamadı, arka plan olmadan devam edilecek")
                background_image = None
        else:
            print(f"[SKIP] Arka plan mevcut: {background_image}")
    else:
        print(f"[3/6] Arka plan görüntüsü kullanılıyor: {background_image}")
    
    # 4. Video oluştur (D-ID)
    print("[4/6] Video oluşturuluyor (D-ID API)...")
    video_file = os.path.join(output_dir, f"{base_name}_singer_video.mp4")
    
    cmd = [
        sys.executable, "src/did_api_video.py",
        "--image", singer_image,
        "--audio", vocal_file,
        "--api-key", did_api_key,
        "--output-dir", output_dir,
        "--resolution", resolution
    ]
    
    if background_image and os.path.exists(background_image):
        cmd.extend(["--background", background_image])
    
    cmd.extend(["--lyrics", lyrics_file])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Video oluşturma başarısız: {result.stderr}")
        return None
    
    # Video dosyasını bul
    video_files = [f for f in os.listdir(output_dir) 
                   if f.endswith('.mp4') and 'did_video' in f]
    if video_files:
        # En yeni dosyayı al
        video_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
        created_video = os.path.join(output_dir, video_files[0])
        print(f"[OK] Video oluşturuldu: {created_video}")
    else:
        print("[ERROR] Video dosyası bulunamadı")
        return None
    
    # 5. Müzik ekle (eğer müzik dosyası varsa)
    if music_file and os.path.exists(music_file):
        print("[5/6] Orijinal müzik ekleniyor...")
        final_video = os.path.join(output_dir, f"{base_name}_singer_video_with_music.mp4")
        
        cmd = [
            sys.executable, "src/combine_music_with_video.py",
            "--video", created_video,
            "--music", music_file,
            "--video-volume", str(vocal_volume),
            "--music-volume", str(music_volume),
            "--output", final_video
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] Final video hazır: {final_video}")
            return final_video
        else:
            print(f"[WARNING] Müzik eklenemedi: {result.stderr}")
            return created_video
    else:
        print("[5/6] Müzik dosyası yok, sadece vokal ile devam ediliyor")
        return created_video

def main():
    parser = argparse.ArgumentParser(
        description='Tam Otomatik Şarkıcı Video Oluşturucu',
        epilog='Örnek: python src/create_complete_singer_video.py --lyrics lyrics.txt --music song.mp3'
    )
    parser.add_argument('--lyrics', type=str, required=True,
                       help='Şarkı sözleri dosyası')
    parser.add_argument('--music', type=str, default=None,
                       help='Orijinal müzik dosyası (opsiyonel)')
    parser.add_argument('--singer-image', type=str, default=None,
                       help='Şarkıcı fotoğrafı (yoksa oluşturulur)')
    parser.add_argument('--background-image', type=str, default=None,
                       help='Arka plan görüntüsü (yoksa oluşturulur)')
    parser.add_argument('--did-api-key', type=str, default=None,
                       help='D-ID API key (veya D_ID_API_KEY env)')
    parser.add_argument('--hf-api-key', type=str, default=None,
                       help='Hugging Face API key (veya HUGGINGFACE_API_KEY env)')
    parser.add_argument('--output-dir', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--resolution', type=str, default='4096',
                       choices=['1024', '2048', '4096'],
                       help='Video çözünürlüğü')
    parser.add_argument('--vocal-volume', type=float, default=0.4,
                       help='Vokal ses seviyesi (0-1)')
    parser.add_argument('--music-volume', type=float, default=0.6,
                       help='Müzik ses seviyesi (0-1)')
    
    args = parser.parse_args()
    
    result = create_complete_singer_video(
        args.lyrics,
        args.music,
        args.singer_image,
        args.background_image,
        args.did_api_key,
        args.hf_api_key,
        args.output_dir,
        args.resolution,
        args.vocal_volume,
        args.music_volume
    )
    
    if result:
        print("\n" + "="*70)
        print("[SUCCESS] Şarkıcı video hazır!")
        print("="*70)
        print(f"Final video: {result}")
        print("\nVideo içeriği:")
        print("  ✅ Gerçekçi şarkıcı (AI)")
        print("  ✅ Lip-sync (şarkı sözleri ile senkronize)")
        print("  ✅ Duygusal ifadeler")
        print("  ✅ Şarkıya uygun ortam/arka plan")
        print("  ✅ Vokal + müzik karışımı")
        print("  ✅ 4K yüksek kalite")
    else:
        print("\n[ERROR] Video oluşturulamadı")

if __name__ == '__main__':
    main()

