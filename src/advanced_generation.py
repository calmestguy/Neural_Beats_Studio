"""
Gelişmiş müzik üretimi - Tüm iyileştirmeleri birleştirir
"""

import argparse
from custom_prompt_generator import generate_with_custom_prompt
from prompt_enhancer import get_mastering_preset_for_genre

def advanced_generate(instruments, genre, output_dir='output', duration=30,
                     model_size='medium', tempo=None, style=None, mood=None,
                     additional=None, guidance_scale=3.5, num_generations=3,
                     auto_master=True, seed=None):
    """
    Gelişmiş müzik üretimi - Tüm iyileştirmeleri kullanır
    
    Args:
        instruments: List[str] - Enstrüman listesi
        genre: str - Müzik türü
        output_dir: str - Çıktı klasörü
        duration: int - Süre (saniye)
        model_size: str - Model boyutu ('small', 'medium', 'large')
        tempo: int - BPM
        style: str - Stil
        mood: str - Ruh hali
        additional: str - Ek özellikler
        guidance_scale: float - Guidance scale (3.5 = prompt'a daha sadık)
        num_generations: int - Kaç farklı versiyon üret (3 = en iyisini seç)
        auto_master: bool - Otomatik mastering
        seed: int - Random seed
    """
    print("="*70)
    print("🚀 ADVANCED MUSIC GENERATION")
    print("="*70)
    print(f"\n📋 Parameters:")
    print(f"   Genre: {genre}")
    print(f"   Instruments: {', '.join(instruments)}")
    print(f"   Model: {model_size}")
    print(f"   Duration: {duration}s")
    print(f"   Guidance Scale: {guidance_scale}")
    print(f"   Variations: {num_generations}")
    print(f"   Auto Master: {auto_master}")
    if tempo:
        print(f"   Tempo: {tempo} BPM")
    if seed:
        print(f"   Seed: {seed}")
    print()
    
    # Mastering preset belirle
    if auto_master:
        master_preset = get_mastering_preset_for_genre(genre)
        print(f"🎚️  Recommended mastering preset: {master_preset}\n")
    
    # Müzik üret
    result = generate_with_custom_prompt(
        instruments=instruments,
        genre=genre,
        output_dir=output_dir,
        duration=duration,
        model_size=model_size,
        tempo=tempo,
        style=style,
        mood=mood,
        additional=additional,
        auto_master=auto_master,
        guidance_scale=guidance_scale,
        num_generations=num_generations,
        seed=seed,
        prompt_style='detailed'
    )
    
    if result:
        print("\n" + "="*70)
        print("✅ GENERATION COMPLETE!")
        print("="*70)
        print(f"\n🎵 Output: {result}\n")
        return result
    else:
        print("\n❌ Generation failed!")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Gelişmiş Müzik Üretimi - Tüm İyileştirmeler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek kullanım:
  # Karadeniz müziği - 3 versiyon, en iyisini seç
  python advanced_generation.py --instruments "kemençe,tulum,davul,bass" --genre karadeniz --tempo 91 --variations 3
  
  # GPU ile hızlı üretim
  python advanced_generation.py --instruments "guitar,drums,bass" --genre rock --model medium --guidance 4.0
        """
    )
    parser.add_argument('--instruments', type=str, required=True,
                       help='Enstrümanlar (virgülle ayrılmış)')
    parser.add_argument('--genre', type=str, required=True,
                       help='Müzik türü')
    parser.add_argument('--tempo', type=int, default=None,
                       help='Tempo (BPM)')
    parser.add_argument('--style', type=str, default=None,
                       help='Stil')
    parser.add_argument('--mood', type=str, default=None,
                       help='Ruh hali')
    parser.add_argument('--additional', type=str, default=None,
                       help='Ek özellikler')
    parser.add_argument('--output', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--duration', type=int, default=30,
                       help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='medium',
                       choices=['small', 'medium', 'large'],
                       help='Model boyutu')
    parser.add_argument('--guidance', type=float, default=3.5,
                       help='Guidance scale (1.0-10.0, yüksek = prompt\'a daha sadık)')
    parser.add_argument('--variations', type=int, default=3,
                       help='Kaç farklı versiyon üret (en iyisini seçer)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed (reproducible results)')
    parser.add_argument('--no-master', action='store_true',
                       help='Mastering uygulama')
    
    args = parser.parse_args()
    
    instruments = [inst.strip() for inst in args.instruments.split(',')]
    
    advanced_generate(
        instruments=instruments,
        genre=args.genre,
        output_dir=args.output,
        duration=args.duration,
        model_size=args.model,
        tempo=args.tempo,
        style=args.style,
        mood=args.mood,
        additional=args.additional,
        guidance_scale=args.guidance,
        num_generations=args.variations,
        auto_master=not args.no_master,
        seed=args.seed
    )

if __name__ == '__main__':
    main()



