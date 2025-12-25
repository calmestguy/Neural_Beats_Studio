"""
Müzik türüne göre müzik üretimi
"""

from generate import MusicGenerator
from prompt_engineer import SOCIAL_MEDIA_PROMPTS, get_prompt
import argparse

def list_genres():
    """Mevcut tüm müzik türlerini listeler"""
    print("\n🎵 Available Music Genres:\n")
    for genre, prompts in SOCIAL_MEDIA_PROMPTS.items():
        print(f"  • {genre.replace('_', ' ').title()}")
        print(f"    Example: {prompts[0][:80]}...")
    print()

def generate_by_genre(genre, output_dir='output', duration=30, model_size='small', 
                      prompt_index=0, auto_bass_boost=False, auto_master=False, 
                      master_preset=None):
    """
    Belirli bir türe göre müzik üretir
    
    Args:
        genre: Müzik türü (classical, pop, rock, vb.)
        output_dir: Çıktı klasörü
        duration: Süre (saniye)
        model_size: Model boyutu
        prompt_index: Hangi prompt varyasyonunu kullan (0, 1, 2...)
        auto_bass_boost: Otomatik bas vurgulama
    """
    if genre not in SOCIAL_MEDIA_PROMPTS:
        print(f"❌ Genre '{genre}' not found!")
        print(f"Available genres: {', '.join(SOCIAL_MEDIA_PROMPTS.keys())}")
        return None
    
    prompts = SOCIAL_MEDIA_PROMPTS[genre]
    
    if prompt_index >= len(prompts):
        print(f"⚠️  Prompt index {prompt_index} not available. Using index 0.")
        prompt_index = 0
    
    prompt = prompts[prompt_index]
    print(f"🎵 Genre: {genre.replace('_', ' ').title()}")
    print(f"📝 Prompt: {prompt}\n")
    
    # Mastering preset belirle
    if master_preset is None:
        from prompt_enhancer import get_mastering_preset_for_genre
        master_preset = get_mastering_preset_for_genre(genre)
        print(f"   Recommended mastering preset: {master_preset}")
    
    # Müzik üret
    generator = MusicGenerator(model_size=model_size)
    results = generator.generate(
        [prompt], 
        output_dir=output_dir, 
        duration=duration,
        auto_master=auto_master,
        master_preset=master_preset
    )
    
    if not results:
        return None
    
    music_file = results[0]
    
    # Bas vurgulama (eğer mastering kullanılmıyorsa)
    if auto_bass_boost and not auto_master:
        from post_process import process_audio
        print("\n🔊 Applying bass enhancement...")
        music_file = process_audio(music_file, bass_boost_db=8.0)
    
    return music_file

def main():
    parser = argparse.ArgumentParser(description='Müzik Türüne Göre Müzik Üretimi')
    parser.add_argument('--genre', type=str, default=None,
                       help='Müzik türü (classical, pop, rock, vb.)')
    parser.add_argument('--list', action='store_true',
                       help='Mevcut tüm türleri listele')
    parser.add_argument('--duration', type=int, default=30,
                       help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='small',
                       choices=['small', 'medium', 'large'])
    parser.add_argument('--output', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--prompt-index', type=int, default=0,
                       help='Prompt varyasyonu (0, 1, 2...)')
    parser.add_argument('--bass-boost', action='store_true',
                       help='Otomatik bas vurgulama (mastering ile çakışır)')
    parser.add_argument('--master', action='store_true',
                       help='Otomatik mastering uygula')
    parser.add_argument('--master-preset', type=str, default=None,
                       choices=['default', 'bass_heavy', 'vocal', 'cinematic'],
                       help='Mastering preset (None = genre-based auto)')
    
    args = parser.parse_args()
    
    if args.list:
        list_genres()
        return
    
    if not args.genre:
        parser.error("--genre is required (or use --list to see available genres)")
    
    result = generate_by_genre(
        args.genre,
        output_dir=args.output,
        duration=args.duration,
        model_size=args.model,
        prompt_index=args.prompt_index,
        auto_bass_boost=args.bass_boost,
        auto_master=args.master,
        master_preset=args.master_preset
    )
    
    if result:
        print(f"\n🎉 Music generated: {result}")

if __name__ == '__main__':
    main()

