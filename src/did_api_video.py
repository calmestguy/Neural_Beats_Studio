"""
D-ID API ile Programatik Video Oluşturucu
API key ile otomatik video oluşturma
"""

import os
import sys
import time
import requests
import base64
import argparse

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def upload_image_to_did(api_key, image_path):
    """
    D-ID API'ye fotoğraf yükler
    """
    print(f"[UPLOAD] Uploading image: {image_path}")
    
    url = "https://api.d-id.com/images"
    headers = {
        "Authorization": f"Basic {api_key}",
    }
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 201:
        result = response.json()
        image_id = result.get('id')
        image_url = result.get('url')  # Image URL'ini al
        print(f"[SUCCESS] Image uploaded: {image_id}")
        print(f"   Image URL: {image_url}")
        return image_id, image_url
    else:
        print(f"[ERROR] Image upload failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None, None

def upload_audio_to_did(api_key, audio_path):
    """
    D-ID API'ye ses dosyası yükler
    """
    print(f"[UPLOAD] Uploading audio: {audio_path}")
    
    url = "https://api.d-id.com/audios"
    headers = {
        "Authorization": f"Basic {api_key}",
    }
    
    with open(audio_path, 'rb') as f:
        files = {'audio': f}
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 201:
        result = response.json()
        audio_url = result.get('url')
        print(f"[SUCCESS] Audio uploaded: {audio_url}")
        return audio_url
    else:
        print(f"[ERROR] Audio upload failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def upload_background_image(api_key, background_path):
    """
    Arka plan görüntüsünü D-ID'ye yükler
    """
    if not background_path or not os.path.exists(background_path):
        return None
    
    print(f"[UPLOAD] Uploading background image: {background_path}")
    
    url = "https://api.d-id.com/images"
    headers = {
        "Authorization": f"Basic {api_key}",
    }
    
    with open(background_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 201:
        result = response.json()
        bg_url = result.get('url')
        print(f"[SUCCESS] Background uploaded: {bg_url}")
        return bg_url
    else:
        print(f"[WARNING] Background upload failed: {response.status_code}")
        return None

def create_video_with_did(api_key, image_url, audio_url, resolution="1024", 
                          background_url=None, output_name="singing_video"):
    """
    D-ID API ile video oluşturur (arka plan desteği ile)
    """
    print(f"[VIDEO] Creating video with D-ID API...")
    print(f"   Resolution: {resolution}")
    if background_url:
        print(f"   Background: {background_url[:50]}...")
    
    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "source_url": image_url,  # Image URL kullan
        "script": {
            "type": "audio",
            "audio_url": audio_url,
            "reduce_noise": True
        },
        "config": {
            "result_format": "mp4",
            "resolution": resolution,  # 1024=HD, 4096=4K
            "face_enhance": True,
            "motion_factor": 1.0
        }
    }
    
    # Arka plan ekle (D-ID API'de background desteği)
    if background_url:
        # D-ID API'de background için farklı yöntemler
        # Yöntem 1: presenter API kullan (daha iyi arka plan desteği)
        # Yöntem 2: config içinde background_image_url
        payload["config"]["background"] = background_url
        # Alternatif: presenter API endpoint'i kullanılabilir
        print(f"   [INFO] Background will be added via config")
    
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        result = response.json()
        talk_id = result.get('id')
        status_url = result.get('status_url')
        print(f"[SUCCESS] Video creation started!")
        print(f"   Talk ID: {talk_id}")
        print(f"   Status URL: {status_url}")
        return talk_id, status_url
    else:
        print(f"[ERROR] Video creation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None, None

def check_video_status(api_key, talk_id):
    """
    Video durumunu kontrol eder
    """
    url = f"https://api.d-id.com/talks/{talk_id}"
    headers = {
        "Authorization": f"Basic {api_key}",
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        status = result.get('status')
        result_url = result.get('result_url')
        return status, result_url
    else:
        print(f"[ERROR] Status check failed: {response.status_code}")
        return None, None

def download_video(video_url, output_path):
    """
    Video'yu indirir
    """
    print(f"[DOWNLOAD] Downloading video...")
    
    response = requests.get(video_url, stream=True)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[SUCCESS] Video downloaded: {output_path}")
        return output_path
    else:
        print(f"[ERROR] Download failed: {response.status_code}")
        return None

def create_singing_video_did(api_key, image_path, audio_path, output_dir="output", 
                             resolution="1024", background_path=None, lyrics_file=None,
                             wait_for_completion=True):
    """
    Tam süreç: Fotoğraf ve ses yükle, ortam analizi yap, arka plan ekle, video oluştur, indir
    """
    print("="*70)
    print("D-ID API ILE VIDEO OLUSTURMA (ORTAM DESTEKLİ)")
    print("="*70)
    print()
    
    # Ortam analizi (şarkı sözlerinden)
    background_url = None
    if lyrics_file and os.path.exists(lyrics_file):
        from analyze_environment import analyze_lyrics_environment, generate_background_prompt
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.read()
        
        environment = analyze_lyrics_environment(lyrics)
        print(f"[ENVIRONMENT] Tespit edilen ortam:")
        print(f"   Açıklama: {environment['description']}")
        print(f"   Ruh hali: {environment['mood']}")
        print(f"   Renkler: {environment['colors']}")
        
        # Arka plan görüntüsü varsa yükle
        if background_path and os.path.exists(background_path):
            background_url = upload_background_image(api_key, background_path)
        else:
            print(f"[INFO] Arka plan görüntüsü bulunamadı, arka plan olmadan devam ediliyor")
            print(f"       Arka plan eklemek için: --background path/to/background.jpg")
    
    # 1. Fotoğraf yükle
    image_id, image_url = upload_image_to_did(api_key, image_path)
    if not image_id or not image_url:
        return None
    
    # 2. Ses yükle
    audio_url = upload_audio_to_did(api_key, audio_path)
    if not audio_url:
        return None
    
    # 3. Video oluştur (arka plan ile)
    talk_id, status_url = create_video_with_did(api_key, image_url, audio_url, 
                                                 resolution=resolution,
                                                 background_url=background_url)
    if not talk_id:
        return None
    
    if not wait_for_completion:
        print(f"\n[INFO] Video oluşturuluyor. Talk ID: {talk_id}")
        print(f"       Durum kontrolü için: python src/did_api_video.py --check {talk_id}")
        return talk_id
    
    # 4. Video hazır olana kadar bekle
    print(f"\n[WAIT] Video oluşturuluyor, lütfen bekleyin...")
    print("       (Bu işlem 2-5 dakika sürebilir)")
    
    max_wait = 300  # 5 dakika
    wait_time = 0
    check_interval = 10  # Her 10 saniyede bir kontrol
    
    while wait_time < max_wait:
        time.sleep(check_interval)
        wait_time += check_interval
        
        status, result_url = check_video_status(api_key, talk_id)
        
        if status == "done":
            print(f"[SUCCESS] Video hazır!")
            
            # 5. Video indir
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_did_video.mp4")
            os.makedirs(output_dir, exist_ok=True)
            
            return download_video(result_url, output_path)
        elif status == "error":
            print(f"[ERROR] Video oluşturma hatası!")
            return None
        else:
            print(f"   [WAIT] Durum: {status} ({wait_time}s/{max_wait}s)")
    
    print(f"[TIMEOUT] Video oluşturma zaman aşımına uğradı")
    print(f"          Durum kontrolü için: python src/did_api_video.py --check {talk_id}")
    return None

def main():
    parser = argparse.ArgumentParser(
        description='D-ID API ile Şarkıcı Video Oluşturucu',
        epilog='Örnek: python src/did_api_video.py --image assets/female_singer_main.jpg --audio rainy_city_blues_lyrics_singing_vocal.wav'
    )
    parser.add_argument('--image', type=str, required=True,
                       help='Fotoğraf dosyası')
    parser.add_argument('--audio', type=str, required=True,
                       help='Ses dosyası (vokal)')
    parser.add_argument('--api-key', type=str, default=None,
                       help='D-ID API key (veya D_ID_API_KEY env)')
    parser.add_argument('--output-dir', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--resolution', type=str, default='1024',
                       choices=['512', '1024', '2048', '4096'],
                       help='Video çözünürlüğü (1024=HD, 4096=4K)')
    parser.add_argument('--no-wait', action='store_true',
                       help='Video hazır olana kadar bekleme (sadece başlat)')
    parser.add_argument('--check', type=str, default=None,
                       help='Video durumunu kontrol et (talk_id)')
    parser.add_argument('--background', type=str, default=None,
                       help='Arka plan görüntüsü (şarkıya uygun ortam)')
    parser.add_argument('--lyrics', type=str, default=None,
                       help='Şarkı sözleri dosyası (otomatik ortam tespiti için)')
    
    args = parser.parse_args()
    
    # API key
    api_key = args.api_key or os.getenv('D_ID_API_KEY')
    if not api_key:
        parser.error("D-ID API key required! Use --api-key or set D_ID_API_KEY environment variable")
    
    # Durum kontrolü
    if args.check:
        status, result_url = check_video_status(api_key, args.check)
        if status == "done" and result_url:
            print(f"[SUCCESS] Video hazır!")
            output_path = os.path.join(args.output_dir, f"video_{args.check}.mp4")
            os.makedirs(args.output_dir, exist_ok=True)
            download_video(result_url, output_path)
        else:
            print(f"   Status: {status}")
        return
    
    # Dosya kontrolü
    if not os.path.exists(args.image):
        parser.error(f"Image file not found: {args.image}")
    if not os.path.exists(args.audio):
        parser.error(f"Audio file not found: {args.audio}")
    
    # Video oluştur
    result = create_singing_video_did(
        api_key,
        args.image,
        args.audio,
        args.output_dir,
        args.resolution,
        args.background,
        args.lyrics,
        not args.no_wait
    )
    
    if result:
        print(f"\n[SUCCESS] Video oluşturuldu: {result}")
    else:
        print(f"\n[ERROR] Video oluşturulamadı")

if __name__ == '__main__':
    main()

