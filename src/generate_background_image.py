"""
Şarkıya uygun arka plan görüntüsü oluşturucu
Hugging Face API ile ortam görüntüleri oluşturur
"""

import os
import sys
import argparse
import requests
from PIL import Image
import io

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def analyze_lyrics_for_background(lyrics_file):
    """
    Şarkı sözlerinden arka plan prompt'u oluşturur
    """
    from analyze_environment import analyze_lyrics_environment, generate_background_prompt
    
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        lyrics = f.read()
    
    environment = analyze_lyrics_environment(lyrics)
    prompt = generate_background_prompt(environment)
    
    return prompt, environment

def generate_background_with_api(prompt, output_file, api_key=None):
    """
    Hugging Face API ile arka plan görüntüsü oluşturur
    """
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            print("[ERROR] Hugging Face API key required!")
            return None
    
    print(f"[GENERATE] Creating background image...")
    print(f"   Prompt: {prompt[:100]}...")
    
    try:
        from huggingface_hub import InferenceClient
        
        client = InferenceClient(token=api_key)
        
        # Daha basit bir model dene
        try:
            image = client.text_to_image(
                prompt=prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )
        except:
            # Alternatif model
            try:
                image = client.text_to_image(
                    prompt=prompt,
                    model="runwayml/stable-diffusion-v1-5"
                )
            except Exception as e:
                print(f"[ERROR] Model error: {e}")
                # Direkt API endpoint dene
                api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {api_key}"}
                payload = {"inputs": prompt}
                response = requests.post(api_url, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                else:
                    raise Exception(f"API error: {response.status_code}")
        
        # Kaydet
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        image.save(output_file, quality=95)
        print(f"[SUCCESS] Background image saved: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        print(f"[INFO] Alternatif: Manuel olarak arka plan görüntüsü oluşturabilirsiniz")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Şarkıya Uygun Arka Plan Görüntüsü Oluşturucu',
        epilog='Örnek: python src/generate_background_image.py --lyrics rainy_city_blues_lyrics.txt'
    )
    parser.add_argument('--lyrics', type=str, required=True,
                       help='Şarkı sözleri dosyası')
    parser.add_argument('--api-key', type=str, default=None,
                       help='Hugging Face API key (veya HUGGINGFACE_API_KEY env)')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı görüntü dosyası')
    
    args = parser.parse_args()
    
    # Ortam analizi ve prompt oluştur
    prompt, environment = analyze_lyrics_for_background(args.lyrics)
    
    print(f"\n[ENVIRONMENT] Tespit edilen ortam:")
    print(f"   Açıklama: {environment['description']}")
    print(f"   Ruh hali: {environment['mood']}")
    print(f"   Renkler: {environment['colors']}")
    print(f"\n[PROMPT] Oluşturulan prompt:")
    print(f"   {prompt}\n")
    
    # Çıktı dosyası
    if args.output is None:
        base_name = os.path.splitext(args.lyrics)[0]
        args.output = f"assets/{os.path.basename(base_name)}_background.jpg"
    
    # Görüntü oluştur
    api_key = args.api_key or os.getenv('HUGGINGFACE_API_KEY')
    result = generate_background_with_api(prompt, args.output, api_key)
    
    if result:
        print(f"\n[SUCCESS] Arka plan görüntüsü hazır: {result}")
        print(f"\n[INFO] Bu görüntüyü video oluştururken kullanın:")
        print(f"   python src/did_api_video.py \\")
        print(f"     --image assets/female_singer_main.jpg \\")
        print(f"     --audio rainy_city_blues_lyrics_singing_vocal.wav \\")
        print(f"     --background {result} \\")
        print(f"     --lyrics {args.lyrics}")

if __name__ == '__main__':
    main()

