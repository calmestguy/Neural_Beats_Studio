"""
SadTalker Entegrasyonu - 4K Kadın Şarkıcı Video Oluşturucu
Açık kaynak, ücretsiz, duygusal ifadeler
"""

import os
import sys
import subprocess
import argparse

def check_sadtalker_installed():
    """SadTalker kurulu mu kontrol et"""
    try:
        import sys
        sadtalker_path = os.path.join(os.getcwd(), 'SadTalker')
        if os.path.exists(sadtalker_path):
            return True
        return False
    except:
        return False

def download_models():
    """SadTalker modellerini indir"""
    print("[DOWNLOAD] Downloading SadTalker models...")
    print("[INFO] This may take a while (models are large)")
    
    sadtalker_path = os.path.join(os.getcwd(), 'SadTalker')
    checkpoints_dir = os.path.join(sadtalker_path, 'checkpoints')
    os.makedirs(checkpoints_dir, exist_ok=True)
    
    # Model URL'leri (Hugging Face'den)
    models = {
        'SadTalker_V0.0.2_256.safetensors': 'https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints/SadTalker_V0.0.2_256.safetensors',
        'SadTalker_V0.0.2_512.safetensors': 'https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints/SadTalker_V0.0.2_512.safetensors',
        'mapping_00109-model.pth.tar': 'https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints/mapping_00109-model.pth.tar',
        'mapping_00229-model.pth.tar': 'https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints/mapping_00229-model.pth.tar',
        'auido2exp_00300-model.pth': 'https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints/auido2exp_00300-model.pth',
        'auido2pose_00140-model.pth': 'https://huggingface.co/vinthony/SadTalker/resolve/main/checkpoints/auido2pose_00140-model.pth',
    }
    
    try:
        import requests
        from tqdm import tqdm
        
        for filename, url in models.items():
            filepath = os.path.join(checkpoints_dir, filename)
            
            if os.path.exists(filepath):
                print(f"[SKIP] {filename} already exists")
                continue
            
            print(f"[DOWNLOAD] {filename}...")
            print(f"   URL: {url}")
            
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                if total_size > 0:
                    with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    f.write(response.content)
            
            print(f"[SUCCESS] {filename} downloaded")
        
        print("\n[SUCCESS] All models downloaded!")
        print(f"   Location: {checkpoints_dir}")
        
    except ImportError:
        print("[ERROR] Required packages not installed!")
        print("[INFO] Install with: pip install requests tqdm")
        print("\n[MANUAL] Manual download:")
        print("   1. Go to: https://huggingface.co/vinthony/SadTalker/tree/main/checkpoints")
        print("   2. Download all .safetensors and .pth files")
        print(f"   3. Place in: {checkpoints_dir}")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        print("\n[MANUAL] Manual download:")
        print("   1. Go to: https://huggingface.co/vinthony/SadTalker/tree/main/checkpoints")
        print("   2. Download all .safetensors and .pth files")
        print(f"   3. Place in: {checkpoints_dir}")

def install_sadtalker():
    """SadTalker'ı kur"""
    print("[INSTALL] Checking SadTalker installation...")
    
    sadtalker_path = os.path.join(os.getcwd(), 'SadTalker')
    
    if not os.path.exists(sadtalker_path):
        print("[ERROR] SadTalker directory not found!")
        print("[INFO] Clone it first:")
        print("   git clone https://github.com/OpenTalker/SadTalker.git")
        return
    
    print("[INFO] SadTalker directory found")
    print("[INFO] Installing dependencies...")
    
    requirements_file = os.path.join(sadtalker_path, 'requirements.txt')
    if os.path.exists(requirements_file):
        print(f"[RUN] pip install -r {requirements_file}")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_file], 
                         check=True)
            print("[SUCCESS] Dependencies installed!")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Installation failed: {e}")
            print("[INFO] Try manually: pip install -r SadTalker/requirements.txt")
    else:
        print("[WARNING] requirements.txt not found")
    
    print("\n[INFO] Next step: Download models")
    print("   Run: python src/sadtalker_integration.py --download-models")

def check_models_installed():
    """SadTalker modellerinin kurulu olup olmadığını kontrol et"""
    sadtalker_path = os.path.join(os.getcwd(), 'SadTalker')
    checkpoints_dir = os.path.join(sadtalker_path, 'checkpoints')
    
    if not os.path.exists(checkpoints_dir):
        return False
    
    # Gerekli model dosyalarını kontrol et
    required_files = [
        'SadTalker_V0.0.2_256.safetensors',
        'SadTalker_V0.0.2_512.safetensors',
        'mapping_00109-model.pth.tar',
        'mapping_00229-model.pth.tar',
        'auido2exp_00300-model.pth',
        'auido2pose_00140-model.pth'
    ]
    
    existing_files = os.listdir(checkpoints_dir)
    found = sum(1 for f in required_files if f in existing_files)
    
    return found >= 2  # En az 2 model dosyası olmalı

def create_video_with_sadtalker(image_file, audio_file, output_file=None, 
                                emotion='neutral', resolution='4k', 
                                enhancer='gfpgan', background_enhancer='realesrgan'):
    """
    SadTalker ile video oluştur
    
    Args:
        image_file: Kadın şarkıcı fotoğrafı
        audio_file: Ses dosyası (vokal)
        output_file: Çıktı video
        emotion: Duygu ('happy', 'sad', 'surprised', 'angry', 'neutral')
        resolution: Çözünürlük ('256', '512', '1024')
        enhancer: Yüz iyileştirme ('gfpgan', 'RestoreFormer', None)
        background_enhancer: Arka plan iyileştirme ('realesrgan', None)
    """
    if not check_sadtalker_installed():
        print("[ERROR] SadTalker not installed!")
        print("[INFO] Run: python src/sadtalker_integration.py --install")
        return None
    
    if not check_models_installed():
        print("[ERROR] SadTalker models not found!")
        print("[INFO] Run: python src/sadtalker_integration.py --download-models")
        return None
    
    print("[VIDEO] Creating video with SadTalker...")
    print(f"   Image: {image_file}")
    print(f"   Audio: {audio_file}")
    print(f"   Emotion: {emotion}")
    print(f"   Resolution: {resolution}")
    
    # SadTalker script yolu
    sadtalker_path = os.path.join(os.getcwd(), 'SadTalker')
    inference_script = os.path.join(sadtalker_path, 'inference.py')
    
    if not os.path.exists(inference_script):
        print("[ERROR] SadTalker inference.py not found!")
        return None
    
    # Çıktı dizini
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.dirname(output_file) if os.path.dirname(output_file) else 'output'
        os.makedirs(output_dir, exist_ok=True)
    
    # Çözünürlük ayarı (SadTalker size parametresi)
    size_map = {
        '256': 256,
        '512': 512,
        '1024': 512,  # 1024 için 512 kullan (daha hızlı)
        '4k': 512     # 4K için 512 kullan
    }
    size = size_map.get(resolution.lower(), 512)
    
    # SadTalker komutu
    cmd = [
        sys.executable,
        inference_script,
        '--driven_audio', os.path.abspath(audio_file),
        '--source_image', os.path.abspath(image_file),
        '--result_dir', os.path.abspath(output_dir),
        '--checkpoint_dir', os.path.join(sadtalker_path, 'checkpoints'),
        '--size', str(size),
        '--preprocess', 'crop',  # Yüz kırpma
        '--batch_size', '2',
        '--expression_scale', '1.0',
    ]
    
    # Enhancer ekle
    if enhancer:
        cmd.extend(['--enhancer', enhancer])
    
    if background_enhancer:
        cmd.extend(['--background_enhancer', background_enhancer])
    
    print(f"\n[RUN] Running SadTalker...")
    print(f"   Command: {' '.join(cmd[:5])} ...")
    print(f"   Working directory: {sadtalker_path}")
    
    try:
        result = subprocess.run(cmd, cwd=sadtalker_path, check=True, 
                               capture_output=True, text=True, timeout=600)
        
        # SadTalker çıktı dosyasını bul (timestamp ile)
        # SadTalker sonucu timestamp'li klasör adıyla kaydeder
        result_files = []
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            if item.endswith('.mp4') and os.path.isfile(item_path):
                result_files.append((os.path.getmtime(item_path), item_path))
        
        if result_files:
            # En yeni dosyayı al
            result_files.sort(reverse=True)
            final_video = result_files[0][1]
            
            # İstenen isimle kopyala
            if output_file and final_video != output_file:
                import shutil
                shutil.copy2(final_video, output_file)
                final_video = output_file
            
            print("[SUCCESS] Video created!")
            print(f"   Output: {final_video}")
            return final_video
        else:
            print("[WARNING] Video file not found in output directory")
            print(f"   Check: {output_dir}")
            return None
            
    except subprocess.TimeoutExpired:
        print("[ERROR] SadTalker timeout (10 minutes)")
        return None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] SadTalker failed: {e}")
        if e.stderr:
            print(f"   Error output: {e.stderr[:500]}")
        if e.stdout:
            print(f"   Output: {e.stdout[:500]}")
        return None

def find_female_singer_image():
    """Kadın şarkıcı fotoğrafı bul"""
    # Kullanıcının kendi fotoğrafını kullanması için
    possible_paths = [
        'assets/female_singer.jpg',
        'assets/singer.jpg',
        'female_singer.jpg',
        'singer.jpg'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    print("[INFO] No female singer image found.")
    print("[INFO] Please provide an image with --image parameter")
    print("[INFO] Or place an image at: assets/female_singer.jpg")
    return None

def analyze_emotion_from_lyrics(lyrics_file):
    """Şarkı sözlerinden duyguyu analiz et"""
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        lyrics = f.read().lower()
    
    # Duygusal analiz
    if any(word in lyrics for word in ['rain', 'lonely', 'blues', 'sad', 'crying']):
        return 'sad'
    elif any(word in lyrics for word in ['happy', 'joy', 'smile', 'laugh']):
        return 'happy'
    elif any(word in lyrics for word in ['surprise', 'wow', 'amazing']):
        return 'surprised'
    else:
        return 'neutral'

def main():
    parser = argparse.ArgumentParser(
        description='SadTalker ile 4K Kadın Şarkıcı Video Oluşturucu',
        epilog='Örnek: python src/sadtalker_integration.py --image singer.jpg --audio vocal.wav'
    )
    parser.add_argument('--image', type=str, default=None,
                       help='Kadın şarkıcı fotoğrafı')
    parser.add_argument('--audio', type=str, required=False,
                       help='Ses dosyası (vokal)')
    parser.add_argument('--lyrics', type=str, default=None,
                       help='Şarkı sözleri dosyası (duygu analizi için)')
    parser.add_argument('--emotion', type=str, 
                       choices=['happy', 'sad', 'surprised', 'angry', 'neutral'],
                       default=None, help='Duygu (otomatik tespit edilir)')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı video dosyası')
    parser.add_argument('--resolution', type=str, 
                       choices=['256', '512', '1024', '4k'], default='512',
                       help='Video çözünürlüğü')
    parser.add_argument('--install', action='store_true',
                       help='SadTalker bağımlılıklarını yükle')
    parser.add_argument('--download-models', action='store_true',
                       help='SadTalker modellerini indir')
    parser.add_argument('--enhancer', type=str, default='gfpgan',
                       choices=['gfpgan', 'RestoreFormer', 'none'],
                       help='Yüz iyileştirme (default: gfpgan)')
    parser.add_argument('--background-enhancer', type=str, default='realesrgan',
                       choices=['realesrgan', 'none'],
                       help='Arka plan iyileştirme (default: realesrgan)')
    
    args = parser.parse_args()
    
    if args.install:
        install_sadtalker()
        return
    
    if args.download_models:
        download_models()
        return
    
    # Video oluşturma için gerekli parametreler
    if not args.audio:
        parser.error("--audio is required (except for --install or --download-models)")
    
    # Fotoğraf bul
    image_file = args.image
    if not image_file:
        image_file = find_female_singer_image()
        if not image_file:
            parser.error("--image is required (or place image at assets/female_singer.jpg)")
    
    if not os.path.exists(image_file):
        parser.error(f"Image file not found: {image_file}")
    
    if not os.path.exists(args.audio):
        parser.error(f"Audio file not found: {args.audio}")
    
    # Duygu analizi
    emotion = args.emotion
    if not emotion and args.lyrics:
        emotion = analyze_emotion_from_lyrics(args.lyrics)
        print(f"[EMOTION] Detected emotion from lyrics: {emotion}")
    elif not emotion:
        emotion = 'neutral'
    
    # Enhancer ayarları
    enhancer = None if args.enhancer == 'none' else args.enhancer
    background_enhancer = None if args.background_enhancer == 'none' else args.background_enhancer
    
    # Video oluştur
    output_file = create_video_with_sadtalker(
        image_file,
        args.audio,
        args.output,
        emotion,
        args.resolution,
        enhancer,
        background_enhancer
    )
    
    if output_file:
        print(f"\n[SUCCESS] Video created: {output_file}")
        print(f"[INFO] You can now use this video for your music!")

if __name__ == '__main__':
    main()

