"""
YouTube Tam İş Akışı: Video Oluştur + Yükle
Müzik ve görselleri eşleştir, video oluştur, YouTube'a yükle
"""

import os
import sys
import argparse
from pathlib import Path

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from create_youtube_video import (
    create_youtube_video,
    match_music_with_images,
    batch_create_youtube_videos
)

try:
    from youtube_upload import (
        authenticate_youtube,
        upload_video_to_youtube,
        batch_upload_to_youtube,
        get_music_metadata
    )
    YOUTUBE_UPLOAD_AVAILABLE = True
except ImportError:
    YOUTUBE_UPLOAD_AVAILABLE = False
    print("[WARNING] YouTube upload module not available. Install: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")

def complete_workflow(music_dir, image_dir, output_dir="output/youtube",
                     upload=False, privacy='private', category='10',
                     credentials_file='credentials.json', token_file='token.json',
                     width=1920, height=1080):
    """
    Tam iş akışı: Video oluştur + (opsiyonel) YouTube'a yükle
    
    Args:
        music_dir: Müzik dosyaları klasörü
        image_dir: Görsel dosyaları klasörü
        output_dir: Çıktı video klasörü
        upload: YouTube'a yükle (True/False)
        privacy: Gizlilik durumu (private/unlisted/public)
        category: Video kategorisi (10=Music)
        credentials_file: Google Cloud credentials dosyası
        token_file: Token cache dosyası
        width: Video genişliği
        height: Video yüksekliği
    """
    print("="*70)
    print("YOUTUBE TAM İŞ AKIŞI: Video Oluştur + Yükle")
    print("="*70)
    print()
    
    # 1. Videoları oluştur
    print("[1/2] Creating YouTube videos...")
    print(f"   Music dir: {music_dir}")
    print(f"   Image dir: {image_dir}")
    print(f"   Output dir: {output_dir}")
    print()
    
    videos = batch_create_youtube_videos(
        music_dir,
        image_dir,
        output_dir,
        width=width,
        height=height
    )
    
    if not videos:
        print("[ERROR] No videos created!")
        return []
    
    print()
    print(f"[SUCCESS] Created {len(videos)} videos")
    print()
    
    # 2. YouTube'a yükle (opsiyonel)
    if upload:
        if not YOUTUBE_UPLOAD_AVAILABLE:
            print("[ERROR] YouTube upload not available!")
            print("[INFO] Install required packages: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return videos
        
        print("[2/2] Uploading videos to YouTube...")
        print()
        
        # Authenticate
        service = authenticate_youtube(credentials_file, token_file)
        if not service:
            print("[ERROR] YouTube authentication failed!")
            return videos
        
        # Upload
        results = batch_upload_to_youtube(
            service,
            output_dir,
            music_dir=music_dir,
            privacy_status=privacy,
            category_id=category
        )
        
        if results:
            print()
            print(f"[SUCCESS] Uploaded {len(results)} videos to YouTube!")
            print()
            print("Video URLs:")
            for result in results:
                print(f"   {result['title']}: https://www.youtube.com/watch?v={result['video_id']}")
        else:
            print("[WARNING] No videos uploaded!")
    else:
        print("[SKIP] Upload skipped (use --upload to enable)")
        print()
        print("To upload videos manually:")
        print(f"   python src/youtube_upload.py --video-dir {output_dir} --privacy {privacy}")
    
    return videos

def main():
    parser = argparse.ArgumentParser(
        description='YouTube Tam İş Akışı: Video Oluştur + Yükle',
        epilog='Örnek: python src/youtube_complete_workflow.py --music-dir "D:\\Neutral Beats Studio" --image-dir "D:\\Neutral Beats Studio\\Music Resim" --upload'
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
    parser.add_argument('--upload', action='store_true',
                       help='YouTube\'a yükle (opsiyonel)')
    parser.add_argument('--privacy', type=str, default='private',
                       choices=['private', 'unlisted', 'public'],
                       help='Gizlilik durumu (default: private)')
    parser.add_argument('--category', type=str, default='10',
                       help='Video kategorisi (10=Music, default: 10)')
    parser.add_argument('--width', type=int, default=1920,
                       help='Video genişliği (default: 1920)')
    parser.add_argument('--height', type=int, default=1080,
                       help='Video yüksekliği (default: 1080)')
    parser.add_argument('--credentials', type=str, default='credentials.json',
                       help='Google Cloud credentials dosyası')
    parser.add_argument('--token', type=str, default='token.json',
                       help='Token cache dosyası')
    
    args = parser.parse_args()
    
    complete_workflow(
        args.music_dir,
        args.image_dir,
        args.output_dir,
        upload=args.upload,
        privacy=args.privacy,
        category=args.category,
        credentials_file=args.credentials,
        token_file=args.token,
        width=args.width,
        height=args.height
    )

if __name__ == '__main__':
    main()

