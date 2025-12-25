"""
Neural Beats Studio için logo/profil resmi oluşturucu
"""

import os
import sys
import argparse

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def generate_logo_with_huggingface(prompt, output_file, api_key=None):
    """
    Hugging Face API ile logo oluşturur
    """
    try:
        from huggingface_hub import InferenceClient
        import requests
        from PIL import Image
        import io
    except ImportError as e:
        print(f"[ERROR] Required packages not installed: {e}")
        print("[INFO] Install with: pip install huggingface_hub requests pillow")
        return None
    
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            print("[ERROR] Hugging Face API key required!")
            print("[INFO] Get free API key from: https://huggingface.co/settings/tokens")
            print("[INFO] Set as environment variable: HUGGINGFACE_API_KEY")
            return None
    
    print(f"[GENERATE] Creating logo with Hugging Face API...")
    print(f"   Prompt: {prompt[:100]}...")
    
    try:
        client = InferenceClient(token=api_key)
        
        # Stable Diffusion XL kullan
        model = "stabilityai/stable-diffusion-xl-base-1.0"
        
        print(f"[TRY] Using model: {model}")
        
        try:
            image = client.text_to_image(
                prompt=prompt,
                model=model
            )
        except Exception as e:
            print(f"[WARNING] InferenceClient failed: {e}")
            print("[TRY] Using direct API endpoint...")
            
            # Alternatif: Direkt API endpoint
            api_url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
            else:
                print(f"[ERROR] API returned status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
        
        # Kaydet
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        image.save(output_file, quality=95)
        
        print(f"[SUCCESS] Logo saved: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Logo generation failed: {e}")
        return None

def create_neural_beats_logo_prompt(style="minimalist", type="profile"):
    """
    Neural Beats Studio için logo prompt'u oluşturur
    
    Args:
        style: Stil ('minimalist', 'modern', 'tech', 'music')
        type: Tip ('profile', 'banner', 'full')
    """
    
    base_prompt = "professional logo design"
    
    # Stil ekle
    style_prompts = {
        'minimalist': "minimalist, clean, simple, elegant",
        'modern': "modern, sleek, contemporary, stylish",
        'tech': "tech-inspired, futuristic, digital, AI-themed",
        'music': "music-themed, sound waves, audio visual, rhythmic"
    }
    
    style_desc = style_prompts.get(style, style_prompts['minimalist'])
    
    # Tip ekle
    if type == "profile":
        # Profil resmi için kare format, merkezi logo (text-free, sadece sembol)
        prompt = f"""
        {base_prompt}, {style_desc},
        square format, centered icon symbol logo,
        music note symbol, sound wave pattern, audio visual element,
        neutral color palette, monochrome gray tones, white or transparent background,
        professional, clean, high quality, 1024x1024,
        suitable for social media profile picture,
        minimalist design, no text, icon only, geometric shapes,
        modern, sleek, simple symbol
        """.strip().replace('\n', ' ')
    elif type == "banner":
        # Banner için geniş format
        prompt = f"""
        {base_prompt}, {style_desc},
        wide banner format, 16:9 ratio,
        "Neural Beats Studio" text,
        neutral color palette, gray tones,
        professional, clean, high quality,
        suitable for YouTube banner, social media header
        """.strip().replace('\n', ' ')
    else:
        # Full logo
        prompt = f"""
        {base_prompt}, {style_desc},
        "Neural Beats Studio" branding,
        neutral color palette, gray tones,
        professional, clean, high quality,
        versatile logo design
        """.strip().replace('\n', ' ')
    
    # Negatif prompt
    negative_prompt = """
    ugly, distorted, low quality, blurry, pixelated,
    complex, cluttered, busy design, too many elements,
    bright colors, neon, flashy, unprofessional,
    text, letters, words, typography, writing,
    realistic photo, 3d render, illustration,
    human, person, face, character
    """.strip().replace('\n', ' ')
    
    return prompt, negative_prompt

def main():
    parser = argparse.ArgumentParser(
        description='Neural Beats Studio Logo Oluşturucu',
        epilog='Örnek: python src/generate_logo.py --type profile --style minimalist'
    )
    parser.add_argument('--type', type=str, 
                       choices=['profile', 'banner', 'full'],
                       default='profile',
                       help='Logo tipi (default: profile)')
    parser.add_argument('--style', type=str,
                       choices=['minimalist', 'modern', 'tech', 'music'],
                       default='minimalist',
                       help='Logo stili (default: minimalist)')
    parser.add_argument('--api-key', type=str, default=None,
                       help='Hugging Face API key (veya HUGGINGFACE_API_KEY env)')
    parser.add_argument('--output', type=str, default=None,
                       help='Çıktı dosyası')
    
    args = parser.parse_args()
    
    # Prompt oluştur
    prompt, negative_prompt = create_neural_beats_logo_prompt(
        style=args.style,
        type=args.type
    )
    
    # Çıktı dosyası
    if args.output is None:
        output_file = f"assets/neural_beats_studio_{args.type}_{args.style}.png"
    else:
        output_file = args.output
    
    print(f"[LOGO] Creating Neural Beats Studio logo...")
    print(f"   Type: {args.type}")
    print(f"   Style: {args.style}")
    print(f"   Output: {output_file}")
    print()
    
    # Logo oluştur
    result = generate_logo_with_huggingface(
        prompt,
        output_file,
        args.api_key
    )
    
    if result:
        print(f"\n[SUCCESS] Logo created: {result}")
        print(f"[INFO] You can now use this as your profile picture!")
    else:
        print(f"\n[ERROR] Logo creation failed")

if __name__ == '__main__':
    main()

