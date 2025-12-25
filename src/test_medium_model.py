"""
Medium model indirme durumunu kontrol eder ve hazır olunca test eder
"""

import os
import sys
from pathlib import Path
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch

def check_model_downloaded():
    """Model indirilmiş mi kontrol et"""
    try:
        cache_dir = Path.home() / '.cache' / 'huggingface' / 'hub' / 'models--facebook--musicgen-medium'
        
        if not cache_dir.exists():
            return False
        
        # pytorch_model.bin dosyasını kontrol et
        model_files = list(cache_dir.rglob('pytorch_model.bin'))
        if not model_files:
            return False
        
        # Dosya boyutunu kontrol et (8GB civarında olmalı)
        model_file = model_files[0]
        file_size_gb = model_file.stat().st_size / (1024**3)
        
        print(f"📦 Model file found: {model_file}")
        print(f"   Size: {file_size_gb:.2f} GB")
        
        # 7GB'dan büyükse indirme tamamlanmış sayılır
        if file_size_gb > 7.0:
            return True
        
        return False
    except Exception as e:
        print(f"⚠️  Error checking model: {e}")
        return False

def test_medium_model():
    """Medium modeli test et"""
    print("\n" + "="*60)
    print("🧪 Testing Medium Model")
    print("="*60 + "\n")
    
    try:
        print("📥 Loading processor...")
        processor = AutoProcessor.from_pretrained('facebook/musicgen-medium')
        print("✅ Processor loaded!")
        
        print("\n📥 Loading model (this may take a while)...")
        model = MusicgenForConditionalGeneration.from_pretrained('facebook/musicgen-medium')
        print("✅ Model loaded!")
        
        # Test prompt
        prompt = "Turkish Black Sea music (Karadeniz müziği), kemenche (Karadeniz kemençesi), tulum (Karadeniz bagpipe), drums, bass, 91 BPM, traditional Turkish Black Sea style, energetic, rhythmic, folk music, melodic, emotional, regional Turkish music, authentic Karadeniz sound, modern production, professional quality"
        
        print(f"\n🎵 Generating test music...")
        print(f"   Prompt: {prompt[:80]}...")
        
        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        print(f"   Using device: {device}")
        
        with torch.no_grad():
            audio_values = model.generate(
                **inputs,
                do_sample=True,
                guidance_scale=3.0,
                max_new_tokens=int(30 * model.config.audio_encoder.sampling_rate / model.config.audio_encoder.hop_length)
            )
        
        print("✅ Generation complete!")
        print("\n🎉 Medium model is working!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔍 Checking if medium model is downloaded...\n")
    
    if check_model_downloaded():
        print("✅ Model appears to be fully downloaded!")
        print("\n🧪 Starting test...")
        test_medium_model()
    else:
        print("⏳ Model is still downloading or not found.")
        print("   Please wait for the download to complete.")
        print("   You can check the download progress in the terminal where")
        print("   you ran the previous command.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())



