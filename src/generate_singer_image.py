"""
AI ile Kadın Şarkıcı Fotoğrafı Oluşturucu
Stable Diffusion kullanarak sarışın, mavi gözlü kadın şarkıcı ve varyasyonlarını oluşturur
"""

import os
import sys
import argparse
import json

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_prompt(base_description="beautiful female singer", hair_color="blonde", 
                 eye_color="blue", style="professional photo", emotion="neutral", 
                 with_microphone=False):
    """
    Stable Diffusion için prompt oluşturur
    """
    # Mikrofon ekleme
    mic_description = ""
    if with_microphone:
        mic_description = "singing into microphone, holding microphone, recording studio, microphone stand, professional recording setup,"
    
    prompt = f"""
    {base_description}, {hair_color} hair, {eye_color} eyes,
    {mic_description}
    {style}, high quality, 4K resolution, professional photography,
    studio lighting, portrait, looking at camera, {emotion} expression,
    elegant, beautiful face, clear skin, detailed eyes, realistic,
    photorealistic, 8k uhd, dslr, soft lighting, high quality, film grain,
    Fujifilm XT3, professional makeup, natural beauty
    """.strip().replace('\n', ' ')
    
    # Negatif prompt (istenmeyen özellikler)
    negative_prompt = """
    ugly, deformed, disfigured, poor quality, low quality, blurry,
    bad anatomy, bad proportions, extra limbs, cloned face, watermark,
    signature, text, error, cropped, jpeg artifacts, duplicate,
    morbid, mutilated, out of frame, extra fingers, mutated hands,
    poorly drawn hands, poorly drawn face, mutation, extra limb,
    ugly, disgusting, amputation, bad art, bad proportions
    """.strip().replace('\n', ' ')
    
    return prompt, negative_prompt

def generate_with_stable_diffusion(prompt, negative_prompt, output_file, 
                                   model="runwayml/stable-diffusion-v1-5",
                                   steps=50, guidance_scale=7.5, seed=None):
    """
    Stable Diffusion ile görüntü oluşturur
    """
    try:
        from diffusers import StableDiffusionPipeline
        import torch
    except ImportError:
        print("[ERROR] diffusers not installed!")
        print("[INFO] Install with: pip install diffusers torch torchvision transformers accelerate")
        return None
    
    print(f"[GENERATE] Creating image with Stable Diffusion...")
    print(f"   Model: {model}")
    print(f"   Prompt: {prompt[:100]}...")
    
    # GPU kontrolü
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"   Device: {device}")
    
    try:
        # Pipeline yükle
        print("[LOAD] Loading Stable Diffusion model (first time may take a while)...")
        pipe = StableDiffusionPipeline.from_pretrained(
            model,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,  # Hızlandırmak için
            requires_safety_checker=False
        )
        pipe = pipe.to(device)
        
        # Optimizasyonlar
        if device == "cuda":
            pipe.enable_attention_slicing()
            pipe.enable_memory_efficient_attention()
        
        # Görüntü oluştur
        print("[GENERATE] Generating image...")
        generator = torch.Generator(device=device)
        if seed:
            generator.manual_seed(seed)
        
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
            height=1024,
            width=1024
        ).images[0]
        
        # Kaydet
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        image.save(output_file, quality=95)
        
        print(f"[SUCCESS] Image saved: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        return None

def generate_with_huggingface_api(prompt, negative_prompt, output_file, 
                                  api_key=None, model="stabilityai/stable-diffusion-2-1"):
    """
    Hugging Face Inference API kullanarak görüntü oluşturur
    (API key gerektirir, ücretsiz tier var)
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
    
    print(f"[GENERATE] Creating image with Hugging Face API...")
    print(f"   Model: {model}")
    print(f"   Prompt: {prompt[:100]}...")
    
    try:
        # InferenceClient ile dene
        client = InferenceClient(token=api_key)
        
        # Daha yaygın bir model dene
        try_model = "stabilityai/stable-diffusion-xl-base-1.0"
        
        try:
            print(f"[TRY] Trying model: {try_model}")
            image = client.text_to_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                model=try_model
            )
        except:
            # Alternatif: Direkt API endpoint
            print(f"[TRY] Using direct API endpoint...")
            api_url = f"https://api-inference.huggingface.co/models/{try_model}"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": negative_prompt,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
            else:
                # Daha basit bir model dene
                print(f"[TRY] Trying simpler model: runwayml/stable-diffusion-v1-5")
                simple_model = "runwayml/stable-diffusion-v1-5"
                api_url = f"https://api-inference.huggingface.co/models/{simple_model}"
                response = requests.post(api_url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                else:
                    raise Exception(f"API error: {response.status_code} - {response.text}")
        
        # Kaydet
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        image.save(output_file, quality=95)
        
        print(f"[SUCCESS] Image saved: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] API generation failed: {e}")
        print(f"[INFO] Trying alternative method...")
        
        # Alternatif: requests ile direkt API
        try:
            api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {api_key}"}
            
            payload = {
                "inputs": prompt
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
                image.save(output_file, quality=95)
                print(f"[SUCCESS] Image saved: {output_file}")
                return output_file
            else:
                print(f"[ERROR] API returned status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None
        except Exception as e2:
            print(f"[ERROR] Alternative method also failed: {e2}")
            return None

def generate_singer_variations(base_name="female_singer", output_dir="assets", 
                               hair_colors=["blonde", "brunette", "black", "red"],
                               eye_colors=["blue"], emotions=["neutral", "sad", "happy"],
                               method="stable_diffusion", api_key=None):
    """
    Farklı varyasyonlar oluşturur
    """
    print(f"[VARIANTS] Generating singer variations...")
    print(f"   Hair colors: {hair_colors}")
    print(f"   Eye colors: {eye_colors}")
    print(f"   Emotions: {emotions}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    # Ana karakter (sarışın, mavi gözlü)
    main_prompt, main_negative = create_prompt(
        base_description="beautiful female singer, professional musician",
        hair_color="blonde",
        eye_color="blue",
        style="professional photo, studio portrait",
        emotion="neutral"
    )
    
    main_file = os.path.join(output_dir, f"{base_name}_main_blonde_blue.jpg")
    
    if method == "stable_diffusion":
        result = generate_with_stable_diffusion(main_prompt, main_negative, main_file)
    else:
        result = generate_with_huggingface_api(main_prompt, main_negative, main_file, api_key)
    
    if result:
        generated_files.append(result)
        print(f"[MAIN] Main character created: {result}")
    
    # Varyasyonlar
    for hair in hair_colors:
        for eye in eye_colors:
            for emotion in emotions:
                if hair == "blonde" and eye == "blue" and emotion == "neutral":
                    continue  # Ana karakter zaten oluşturuldu
                
                prompt, negative = create_prompt(
                    base_description="beautiful female singer, professional musician, same face",
                    hair_color=hair,
                    eye_color=eye,
                    style="professional photo, studio portrait",
                    emotion=emotion
                )
                
                variant_file = os.path.join(
                    output_dir, 
                    f"{base_name}_{hair}_{eye}_{emotion}.jpg"
                )
                
                if method == "stable_diffusion":
                    result = generate_with_stable_diffusion(prompt, negative, variant_file)
                else:
                    result = generate_with_huggingface_api(prompt, negative, variant_file, api_key)
                
                if result:
                    generated_files.append(result)
    
    print(f"\n[SUCCESS] Generated {len(generated_files)} images")
    return generated_files

def main():
    parser = argparse.ArgumentParser(
        description='AI ile Kadın Şarkıcı Fotoğrafı Oluşturucu',
        epilog='Örnek: python src/generate_singer_image.py --method stable_diffusion'
    )
    parser.add_argument('--method', type=str, 
                       choices=['stable_diffusion', 'huggingface_api'],
                       default='stable_diffusion',
                       help='Görüntü oluşturma yöntemi')
    parser.add_argument('--api-key', type=str, default=None,
                       help='Hugging Face API key (veya HUGGINGFACE_API_KEY env)')
    parser.add_argument('--output-dir', type=str, default='assets',
                       help='Çıktı klasörü')
    parser.add_argument('--base-name', type=str, default='female_singer',
                       help='Temel dosya adı')
    parser.add_argument('--hair-colors', type=str, nargs='+',
                       default=['blonde', 'brunette', 'black', 'red'],
                       help='Saç renkleri')
    parser.add_argument('--eye-colors', type=str, nargs='+',
                       default=['blue'],
                       help='Göz renkleri')
    parser.add_argument('--emotions', type=str, nargs='+',
                       default=['neutral', 'sad', 'happy'],
                       help='Duygular')
    parser.add_argument('--single', action='store_true',
                       help='Sadece ana karakteri oluştur (varyasyonlar olmadan)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed (aynı görüntü için)')
    parser.add_argument('--microphone', action='store_true',
                       help='Mikrofon karşısında şarkı söyleyen şarkıcı')
    
    args = parser.parse_args()
    
    if args.single:
        # Sadece ana karakter
        prompt, negative = create_prompt(
            base_description="beautiful female singer, professional musician",
            hair_color="blonde",
            eye_color="blue",
            style="professional photo, studio portrait",
            emotion="neutral",
            with_microphone=args.microphone
        )
        
        output_file = os.path.join(args.output_dir, f"{args.base_name}_main.jpg")
        
        if args.method == "stable_diffusion":
            generate_with_stable_diffusion(prompt, negative, output_file, seed=args.seed)
        else:
            api_key = args.api_key or os.getenv('HUGGINGFACE_API_KEY')
            generate_with_huggingface_api(prompt, negative, output_file, api_key)
    else:
        # Tüm varyasyonlar
        api_key = args.api_key or os.getenv('HUGGINGFACE_API_KEY')
        generate_singer_variations(
            args.base_name,
            args.output_dir,
            args.hair_colors,
            args.eye_colors,
            args.emotions,
            args.method,
            api_key
        )

if __name__ == '__main__':
    main()

