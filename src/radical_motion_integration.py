"""
RADiCAL Motion Entegrasyonu - Audio-Driven Motion
Şarkıya göre vücut hareketi üretir
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

def create_motion_from_audio(api_key, audio_file, output_file=None):
    """
    RADiCAL Motion ile audio-driven motion üretir
    
    Args:
        api_key: RADiCAL Motion API key
        audio_file: Ses dosyası (şarkı vokal)
        output_file: Çıktı motion dosyası
    """
    print("[MOTION] Creating audio-driven motion with RADiCAL Motion...")
    print(f"   Audio: {audio_file}")
    
    # RADiCAL Motion API endpoint (örnek - gerçek API dokümantasyonuna göre güncellenmeli)
    url = "https://api.radicalmotion.ai/v1/motion/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Ses dosyasını yükle
    with open(audio_file, 'rb') as f:
        files = {'audio': f}
        data = {
            'motion_type': 'singing',  # Şarkı söyleme hareketi
            'intensity': 'medium',  # Hareket yoğunluğu
            'style': 'natural'  # Doğal hareket
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        motion_data = result.get('motion_data')
        
        # Motion dosyasını kaydet
        if output_file is None:
            base_name = os.path.splitext(audio_file)[0]
            output_file = f"{base_name}_motion.json"
        
        with open(output_file, 'w') as f:
            import json
            json.dump(motion_data, f, indent=2)
        
        print(f"[SUCCESS] Motion data saved: {output_file}")
        return output_file
    else:
        print(f"[ERROR] Motion generation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='RADiCAL Motion Audio-Driven Motion Oluşturucu',
        epilog='Örnek: python src/radical_motion_integration.py --audio vocal.wav'
    )
    parser.add_argument('--audio', type=str, required=True,
                       help='Ses dosyası (vokal)')
    parser.add_argument('--api-key', type=str, default=None,
                       help='RADiCAL Motion API key (veya RADICAL_API_KEY env)')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı motion dosyası')
    
    args = parser.parse_args()
    
    # API key
    api_key = args.api_key or os.getenv('RADICAL_API_KEY')
    if not api_key:
        parser.error("RADiCAL Motion API key required!")
    
    # Dosya kontrolü
    if not os.path.exists(args.audio):
        parser.error(f"Audio file not found: {args.audio}")
    
    # Motion oluştur
    result = create_motion_from_audio(api_key, args.audio, args.output)
    
    if result:
        print(f"\n[SUCCESS] Motion data created: {result}")
        print("[INFO] Bu motion data'yı 3D karakter ile kullanabilirsiniz")

if __name__ == '__main__':
    main()

