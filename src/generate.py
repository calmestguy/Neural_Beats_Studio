"""
AI Music Generator - MusicGen ile müzik üretimi (Transformers kullanarak)
Sosyal medya için kısa loop'lar üretir
"""

import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile as wavfile
import os
from datetime import datetime
import argparse
import numpy as np

class MusicGenerator:
    def __init__(self, model_size='small', device=None):
        """
        Args:
            model_size: 'small' (300M), 'medium' (1.5B), 'large' (3.3B)
                       RTX 3070 için 'small' veya 'medium' önerilir
            device: 'cuda', 'cpu' veya None (otomatik seçim)
        """
        # GPU kontrolü ve otomatik seçim
        if device is None:
            if torch.cuda.is_available():
                self.device = 'cuda'
                gpu_name = torch.cuda.get_device_name(0)
                vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
                print(f"🎮 GPU detected: {gpu_name} ({vram_gb:.1f}GB VRAM)")
            else:
                self.device = 'cpu'
                print("💻 Using CPU (GPU not available)")
        else:
            self.device = device if torch.cuda.is_available() and device == 'cuda' else 'cpu'
        
        print(f"Using device: {self.device}")
        
        # VRAM kontrolü - 8GB için small/medium uygun
        if model_size == 'large' and torch.cuda.is_available():
            vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
            if vram_gb < 12:
                print(f"⚠️  Large model {vram_gb:.1f}GB VRAM için riskli. Medium'a geçiliyor...")
                model_size = 'medium'
        
        model_name = f'facebook/musicgen-{model_size}'
        print(f"Loading {model_name}...")
        
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        self.model = self.model.to(self.device)
        
        # GPU optimizasyonları
        if self.device == 'cuda':
            self.model = self.model.half()  # FP16 - daha hızlı ve daha az VRAM
            print("   ⚡ Using FP16 precision for faster generation")
        
        self.sample_rate = self.model.config.audio_encoder.sampling_rate
        print("✅ Model loaded!")
    
    def generate(self, descriptions, output_dir='output', duration=30, 
                 auto_master=False, master_preset='default',
                 guidance_scale=3.0, num_generations=1, seed=None):
        """
        Müzik üretir
        
        Args:
            descriptions: List[str] - Müzik açıklamaları
            output_dir: Çıktı klasörü
            duration: Süre (saniye)
            auto_master: Otomatik mastering uygula
            master_preset: Mastering preset ('default', 'bass_heavy', 'vocal', 'cinematic')
            guidance_scale: Guidance scale (1.0-10.0, yüksek = prompt'a daha sadık)
            num_generations: Her prompt için kaç farklı versiyon üret (en iyisini seçmek için)
            seed: Random seed (reproducible results için)
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n🎵 Generating {len(descriptions)} track(s)...")
        if num_generations > 1:
            print(f"   🔄 Generating {num_generations} variations per prompt (best will be selected)")
        
        # Seed ayarla (reproducible results)
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
            print(f"   🎲 Using seed: {seed}")
        
        # GPU memory temizliği
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Prompt'ları işle
        inputs = self.processor(
            text=descriptions,
            padding=True,
            return_tensors="pt",
        ).to(self.device)
        
        # Üretim
        all_audio_values = []
        with torch.no_grad():
            for gen_idx in range(num_generations):
                if num_generations > 1:
                    print(f"   Generating variation {gen_idx + 1}/{num_generations}...")
                
                audio_values = self.model.generate(
                    **inputs, 
                    do_sample=True, 
                    guidance_scale=guidance_scale,
                    max_new_tokens=int(duration * self.sample_rate / self.model.config.audio_encoder.hop_length)
                )
                all_audio_values.append(audio_values)
        
        # En iyi versiyonu seç (basit: en yüksek enerji)
        if num_generations > 1:
            print("   🎯 Selecting best variation...")
            best_indices = []
            for desc_idx in range(len(descriptions)):
                best_energy = -1
                best_idx = 0
                for gen_idx in range(num_generations):
                    audio = all_audio_values[gen_idx][desc_idx].cpu().numpy()
                    if len(audio.shape) > 1:
                        audio = np.mean(audio, axis=0) if audio.shape[0] > 1 else audio[0]
                    energy = np.mean(np.abs(audio))
                    if energy > best_energy:
                        best_energy = energy
                        best_idx = gen_idx
                best_indices.append(best_idx)
                print(f"      Track {desc_idx + 1}: Selected variation {best_idx + 1}")
            
            # En iyi versiyonları seç
            audio_values = torch.stack([
                all_audio_values[best_indices[i]][i] 
                for i in range(len(descriptions))
            ])
        else:
            audio_values = all_audio_values[0]
        
        # Kaydet
        results = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Audio değerlerini işle (shape: [batch, channels, samples])
        audio_values = audio_values.cpu().numpy()
        
        for idx, (desc, audio) in enumerate(zip(descriptions, audio_values)):
            # Eğer stereo ise mono'ya çevir (ortalamasını al)
            if len(audio.shape) > 1 and audio.shape[0] > 1:
                audio = np.mean(audio, axis=0)
            elif len(audio.shape) > 1:
                audio = audio[0]
            
            # Audio'yu normalize et ve int16'ya çevir
            if np.max(np.abs(audio)) > 0:
                audio_normalized = audio / np.max(np.abs(audio))
            else:
                audio_normalized = audio
            audio_int16 = (audio_normalized * 32767).astype(np.int16)
            
            filename = f"{output_dir}/track_{timestamp}_{idx:02d}.wav"
            wavfile.write(filename, self.sample_rate, audio_int16)
            
            results.append(filename)
            print(f"✅ Saved: {filename}")
            print(f"   Description: {desc}")
        
        # Otomatik mastering
        if auto_master and results:
            from advanced_mixing import process_audio_advanced
            
            mastering_presets = {
                'default': {'bass_boost': 2.0, 'mid_boost': 0, 'treble_boost': 1.0, 'compression': True, 'reverb': True},
                'bass_heavy': {'bass_boost': 4.0, 'mid_boost': 0, 'treble_boost': 0.5, 'compression': True, 'reverb': False},
                'vocal': {'bass_boost': 1.0, 'mid_boost': 2.0, 'treble_boost': 1.5, 'compression': True, 'reverb': True},
                'cinematic': {'bass_boost': 3.0, 'mid_boost': 1.0, 'treble_boost': 2.0, 'compression': True, 'reverb': True},
                'folk_traditional': {'bass_boost': 2.5, 'mid_boost': 1.5, 'treble_boost': 2.0, 'compression': True, 'reverb': True}  # Karadeniz için
            }
            
            preset = mastering_presets.get(master_preset, mastering_presets['default'])
            
            print("\n🎚️  Applying automatic mastering...")
            mastered_results = []
            for result_file in results:
                mastered = process_audio_advanced(
                    result_file,
                    bass_boost=preset['bass_boost'],
                    mid_boost=preset['mid_boost'],
                    treble_boost=preset['treble_boost'],
                    compression=preset['compression'],
                    reverb=preset['reverb'],
                    stereo_widen=False
                )
                mastered_results.append(mastered)
            return mastered_results
        
        return results

def main():
    parser = argparse.ArgumentParser(description='AI Music Generator')
    parser.add_argument('--model', type=str, default='small',
                       choices=['small', 'medium', 'large'],
                       help='Model size (small/medium/large)')
    parser.add_argument('--prompt', type=str, required=True,
                       help='Müzik açıklaması (örn: "upbeat electronic dance music")')
    parser.add_argument('--duration', type=int, default=30,
                       help='Süre (saniye)')
    parser.add_argument('--output', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--master', action='store_true',
                       help='Otomatik mastering uygula')
    parser.add_argument('--master-preset', type=str, default='default',
                       choices=['default', 'bass_heavy', 'vocal', 'cinematic'],
                       help='Mastering preset')
    
    args = parser.parse_args()
    
    generator = MusicGenerator(model_size=args.model)
    results = generator.generate(
        [args.prompt], 
        output_dir=args.output, 
        duration=args.duration,
        auto_master=args.master,
        master_preset=args.master_preset
    )
    print(f"\n🎉 {len(results)} track generated!")

if __name__ == '__main__':
    main()
