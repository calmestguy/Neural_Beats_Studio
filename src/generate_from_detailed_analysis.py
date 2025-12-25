"""
Detaylı analiz sonuçlarını kullanarak müzik üretimi
"""

import argparse
from detailed_audio_analyzer import detailed_analyze_audio, detailed_analysis_to_prompt
from generate import MusicGenerator

def generate_from_detailed_analysis(audio_file, output_dir='output', duration=30,
                                    model_size='medium', guidance_scale=3.5,
                                    num_generations=3, auto_master=True, seed=None):
    """
    Detaylı analiz yapıp, sonuçlara göre müzik üretir
    """
    print("="*70)
    print("🎵 GENERATE FROM DETAILED ANALYSIS")
    print("="*70)
    
    # 1. Detaylı analiz
    print("\n📊 Step 1: Detailed Analysis")
    analysis = detailed_analyze_audio(audio_file, skip_seconds=5, analysis_duration=120)
    
    if analysis is None:
        print("❌ Analysis failed!")
        return None
    
    # 2. Prompt oluştur
    print("\n📝 Step 2: Generate Prompt")
    prompt = detailed_analysis_to_prompt(analysis)
    
    # Prompt'u iyileştir (Karadeniz için)
    if analysis['estimated_genre'] == 'karadeniz':
        # Yanlış tespit edilen enstrümanları temizle
        prompt = prompt.replace('saxophone', '')
        prompt = prompt.replace('cello', '')
        prompt = prompt.replace('trumpet', '')
        prompt = prompt.replace('kick_drum', 'drums')
        prompt = prompt.replace('snare_drum', '')
        # Çift boşlukları temizle
        prompt = ' '.join(prompt.split())
        # Virgül düzenle
        prompt = prompt.replace(', ,', ',')
        prompt = prompt.replace('  ', ' ')
    
    print(f"\n✨ Refined Prompt:")
    print(f"{prompt}\n")
    
    # 3. Müzik üret
    print("\n🎵 Step 3: Generate Music")
    generator = MusicGenerator(model_size=model_size)
    results = generator.generate(
        [prompt],
        output_dir=output_dir,
        duration=duration,
        auto_master=auto_master,
        master_preset='folk_traditional',
        guidance_scale=guidance_scale,
        num_generations=num_generations,
        seed=seed
    )
    
    if results:
        print("\n" + "="*70)
        print("✅ GENERATION COMPLETE!")
        print("="*70)
        print(f"\n🎵 Output: {results[0]}\n")
        return results[0]
    else:
        print("\n❌ Generation failed!")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Detaylı Analiz ile Müzik Üretimi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek kullanım:
  python generate_from_detailed_analysis.py "path/to/audio.mp3"
  python generate_from_detailed_analysis.py "path/to/audio.mp3" --model medium --variations 3
        """
    )
    parser.add_argument('audio_file', type=str,
                       help='Audio dosyası yolu')
    parser.add_argument('--output', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--duration', type=int, default=30,
                       help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='medium',
                       choices=['small', 'medium', 'large'],
                       help='Model boyutu')
    parser.add_argument('--guidance', type=float, default=3.5,
                       help='Guidance scale')
    parser.add_argument('--variations', type=int, default=3,
                       help='Kaç versiyon üret')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed')
    parser.add_argument('--no-master', action='store_true',
                       help='Mastering uygulama')
    
    args = parser.parse_args()
    
    generate_from_detailed_analysis(
        args.audio_file,
        output_dir=args.output,
        duration=args.duration,
        model_size=args.model,
        guidance_scale=args.guidance,
        num_generations=args.variations,
        auto_master=not args.no_master,
        seed=args.seed
    )

if __name__ == '__main__':
    main()

