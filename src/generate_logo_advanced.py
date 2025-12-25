"""
Gelişmiş logo oluşturucu - Daha spesifik prompt'lar ile
"""

import os
import sys
import argparse

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def generate_logo_advanced(prompt, output_file, api_key=None):
    """Gelişmiş logo oluşturma"""
    try:
        from huggingface_hub import InferenceClient
        import requests
        from PIL import Image
        import io
    except ImportError as e:
        print(f"[ERROR] Required packages not installed: {e}")
        return None
    
    if not api_key:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            print("[ERROR] Hugging Face API key required!")
            return None
    
    print(f"[GENERATE] Creating advanced logo...")
    
    try:
        client = InferenceClient(token=api_key)
        model = "stabilityai/stable-diffusion-xl-base-1.0"
        
        image = client.text_to_image(
            prompt=prompt,
            model=model
        )
        
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        image.save(output_file, quality=95)
        
        print(f"[SUCCESS] Logo saved: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Gelişmiş Logo Oluşturucu')
    parser.add_argument('--style', type=str, default='icon', 
                       choices=['icon', 'geometric', 'wave', 'note'],
                       help='Logo stili')
    parser.add_argument('--api-key', type=str, default=None)
    parser.add_argument('--output', type=str, default=None)
    
    args = parser.parse_args()
    
    # Çok spesifik prompt'lar
    prompts = {
        'icon': """
        minimalist music icon logo, single music note symbol, 
        clean geometric shape, monochrome gray, white background,
        professional, simple, elegant, 1024x1024, centered,
        suitable for profile picture, no text, icon only
        """,
        'geometric': """
        geometric music logo, abstract sound wave pattern,
        minimalist design, gray and white, clean lines,
        professional logo, square format, centered,
        modern, sleek, simple geometric shapes
        """,
        'wave': """
        sound wave logo, audio waveform visualization,
        minimalist, monochrome gray, white background,
        clean design, professional, square format,
        modern, simple wave pattern
        """,
        'note': """
        stylized music note logo, minimalist design,
        single note symbol, geometric style,
        gray tones, white background, clean,
        professional, square format, centered
        """
    }
    
    prompt = prompts.get(args.style, prompts['icon'])
    prompt = prompt.strip().replace('\n', ' ')
    
    if args.output is None:
        output_file = f"assets/neural_beats_logo_{args.style}.png"
    else:
        output_file = args.output
    
    generate_logo_advanced(prompt, output_file, args.api_key)

if __name__ == '__main__':
    main()

