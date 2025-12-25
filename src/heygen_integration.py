"""
HeyGen API Entegrasyonu - Tam Vücut Şarkıcı Avatar
Saç fizik simülasyonu, vücut hareketleri, gerçekçi lip-sync
"""

import os
import sys
import requests
import time
import argparse

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def upload_media_to_heygen(api_key, file_path, media_type="image"):
    """
    HeyGen'e görüntü veya ses dosyası yükler
    
    Args:
        api_key: HeyGen API key
        file_path: Dosya yolu
        media_type: "image" veya "audio"
    """
    print(f"[UPLOAD] Uploading {media_type} to HeyGen...")
    
    url = "https://api.heygen.com/v1/media.upload"
    headers = {
        "X-Api-Key": api_key
    }
    
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, f'application/{media_type}')}
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        result = response.json()
        media_id = result.get('data', {}).get('media_id')
        print(f"[SUCCESS] {media_type.capitalize()} uploaded: {media_id}")
        return media_id
    else:
        print(f"[ERROR] Upload failed: {response.status_code} - {response.text}")
        return None

def create_video_with_heygen(api_key, avatar_id, audio_file, 
                             background_image=None, output_name="singing_video"):
    """
    HeyGen ile tam vücut şarkıcı video oluşturur
    
    Args:
        api_key: HeyGen API key
        avatar_id: HeyGen avatar ID (tam vücut avatar)
        audio_file: Ses dosyası (vokal)
        background_image: Arka plan görüntüsü (opsiyonel)
        output_name: Çıktı video adı
    """
    print("[VIDEO] Creating full-body singing video with HeyGen...")
    
    # Ses dosyasını yükle
    audio_id = upload_media_to_heygen(api_key, audio_file, "audio")
    if not audio_id:
        return None
    
    # Arka plan yükle (varsa)
    background_id = None
    if background_image and os.path.exists(background_image):
        background_id = upload_media_to_heygen(api_key, background_image, "image")
    
    # Video oluştur
    url = "https://api.heygen.com/v1/video.generate"
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "avatar_id": avatar_id,
        "voice_id": "default",  # Veya özel ses ID
        "audio_id": audio_id,
        "background": background_id if background_id else None,
        "video_inputs": [],
        "caption": False,
        "dimension": {
            "width": 1920,
            "height": 1080
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        video_id = result.get('data', {}).get('video_id')
        print(f"[SUCCESS] Video creation started!")
        print(f"   Video ID: {video_id}")
        return video_id
    else:
        print(f"[ERROR] Video creation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def check_video_status(api_key, video_id):
    """Video durumunu kontrol eder"""
    url = f"https://api.heygen.com/v1/video.get?video_id={video_id}"
    headers = {"X-Api-Key": api_key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        status = result.get('data', {}).get('status')
        video_url = result.get('data', {}).get('video_url')
        return status, video_url
    else:
        return None, None

def download_video(video_url, output_path):
    """Video'yu indirir"""
    print(f"[DOWNLOAD] Downloading video...")
    
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"[SUCCESS] Video downloaded: {output_path}")
        return output_path
    else:
        print(f"[ERROR] Download failed: {response.status_code}")
        return None

def list_avatars(api_key):
    """Mevcut avatarları listeler"""
    url = "https://api.heygen.com/v1/avatar.list"
    headers = {"X-Api-Key": api_key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        avatars = result.get('data', {}).get('avatars', [])
        
        print("[AVATARS] Available avatars:")
        print()
        for avatar in avatars:
            avatar_id = avatar.get('avatar_id')
            name = avatar.get('name', 'Unknown')
            avatar_type = avatar.get('type', 'Unknown')
            print(f"  - {name} ({avatar_type})")
            print(f"    ID: {avatar_id}")
            print()
        
        return avatars
    else:
        print(f"[ERROR] Failed to list avatars: {response.status_code}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description='HeyGen ile Tam Vücut Şarkıcı Video Oluşturucu',
        epilog='Örnek: python src/heygen_integration.py --avatar-id YOUR_AVATAR_ID --audio vocal.wav'
    )
    parser.add_argument('--avatar-id', type=str, required=True,
                       help='HeyGen avatar ID (tam vücut avatar)')
    parser.add_argument('--audio', type=str, required=True,
                       help='Ses dosyası (vokal)')
    parser.add_argument('--background', type=str, default=None,
                       help='Arka plan görüntüsü (opsiyonel)')
    parser.add_argument('--api-key', type=str, default=None,
                       help='HeyGen API key (veya HEYGEN_API_KEY env)')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı video dosyası')
    parser.add_argument('--list-avatars', action='store_true',
                       help='Mevcut avatarları listele')
    parser.add_argument('--check', type=str, default=None,
                       help='Video durumunu kontrol et (video_id)')
    
    args = parser.parse_args()
    
    # API key
    api_key = args.api_key or os.getenv('HEYGEN_API_KEY')
    if not api_key:
        parser.error("HeyGen API key required! Use --api-key or set HEYGEN_API_KEY environment variable")
    
    # Avatar listesi
    if args.list_avatars:
        list_avatars(api_key)
        return
    
    # Video durum kontrolü
    if args.check:
        status, video_url = check_video_status(api_key, args.check)
        if status == "completed" and video_url:
            print(f"[SUCCESS] Video hazır!")
            output_path = args.output or f"output/video_{args.check}.mp4"
            download_video(video_url, output_path)
        else:
            print(f"   Status: {status}")
        return
    
    # Dosya kontrolü
    if not os.path.exists(args.audio):
        parser.error(f"Audio file not found: {args.audio}")
    
    # Video oluştur
    video_id = create_video_with_heygen(
        api_key,
        args.avatar_id,
        args.audio,
        args.background,
        args.output or "singing_video"
    )
    
    if not video_id:
        return
    
    # Video hazır olana kadar bekle
    print(f"\n[WAIT] Video oluşturuluyor, lütfen bekleyin...")
    print("       (Bu işlem 3-10 dakika sürebilir)")
    
    max_wait = 600  # 10 dakika
    wait_time = 0
    check_interval = 15  # Her 15 saniyede bir kontrol
    
    while wait_time < max_wait:
        time.sleep(check_interval)
        wait_time += check_interval
        
        status, video_url = check_video_status(api_key, video_id)
        
        if status == "completed":
            print(f"[SUCCESS] Video hazır!")
            
            output_path = args.output or f"output/heygen_singing_video_{video_id}.mp4"
            return download_video(video_url, output_path)
        elif status == "failed":
            print(f"[ERROR] Video oluşturma hatası!")
            return None
        elif status:
            print(f"[INFO] Status: {status}... ({wait_time}s)")
    
    print(f"[ERROR] Timeout (10 dakika)")
    print(f"[INFO] Video ID: {video_id}")
    print(f"       Durum kontrolü için: python src/heygen_integration.py --check {video_id}")

if __name__ == '__main__':
    main()

