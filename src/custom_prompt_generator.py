"""
Özel prompt oluşturucu - Kullanıcı enstrümanları ve özellikleri manuel belirler
"""

from generate import MusicGenerator
import argparse

def create_custom_prompt(instruments, genre, tempo=None, style=None, mood=None, additional=None, 
                        prompt_style='detailed'):
    """
    Özel prompt oluşturur (geliştirilmiş versiyon)
    
    Args:
        instruments: List[str] - Enstrüman listesi
        genre: str - Müzik türü
        tempo: int - BPM (opsiyonel)
        style: str - Stil (opsiyonel)
        mood: str - Ruh hali (opsiyonel)
        additional: str - Ek özellikler (opsiyonel)
        prompt_style: 'detailed' (detaylı) veya 'concise' (kısa)
    """
    prompt_parts = []
    
    # Karadeniz müziği için özel, detaylı prompt
    if genre == 'karadeniz':
        # Ana tür tanımı
        prompt_parts.append("Turkish Black Sea folk music, Karadeniz müziği")
        
        # Enstrümanlar - öncelik sırasına göre
        if instruments:
            primary_instruments = []
            secondary_instruments = []
            
            for inst in instruments:
                inst_lower = inst.lower()
                # Öncelikli enstrümanlar
                if inst_lower in ['kemençe', 'kemenche', 'tulum', 'davul']:
                    inst_map = {
                        'kemençe': 'kemenche (Karadeniz kemençesi, traditional 3-string fiddle)',
                        'kemenche': 'kemenche (Karadeniz kemençesi, traditional 3-string fiddle)',
                        'tulum': 'tulum (Karadeniz bagpipe, traditional wind instrument)',
                        'davul': 'davul (traditional Turkish drum)',
                    }
                    primary_instruments.append(inst_map.get(inst_lower, inst))
                else:
                    inst_map = {
                        'zurna': 'zurna (traditional Turkish wind instrument)',
                        'bağlama': 'bağlama (saz, traditional Turkish string instrument)',
                        'baglama': 'bağlama (saz)',
                        'saz': 'bağlama (saz)',
                        'klarnet': 'clarinet',
                        'keman': 'violin',
                        'gitar': 'guitar',
                        'bass': 'bass guitar',
                        'drums': 'drums',
                        'vocals': 'vocals',
                    }
                    secondary_instruments.append(inst_map.get(inst_lower, inst))
            
            if primary_instruments:
                prompt_parts.append(', '.join(primary_instruments))
            if secondary_instruments:
                prompt_parts.append(', '.join(secondary_instruments))
        
        # Karadeniz karakteristik özellikler
        prompt_parts.append("traditional Karadeniz rhythm patterns")
        prompt_parts.append("characteristic Black Sea melodic structure")
        prompt_parts.append("folk music arrangement")
        
        # Tempo ve ritim
        if tempo:
            prompt_parts.append(f"{tempo} BPM")
        else:
            prompt_parts.append("moderate tempo")
        
        # Stil ve ruh hali
        if style:
            prompt_parts.append(style)
        else:
            prompt_parts.append("traditional style")
        
        if mood:
            mood_parts = mood.split(',') if ',' in mood else [mood]
            prompt_parts.extend([m.strip() for m in mood_parts])
        else:
            prompt_parts.append("energetic, rhythmic, joyful")
        
        # Ek özellikler
        if additional:
            prompt_parts.append(additional)
        else:
            prompt_parts.append("strong rhythmic foundation")
            prompt_parts.append("melodic lead instruments")
        
        # Production
        if prompt_style == 'detailed':
            prompt_parts.append("professional production, clear instrument separation")
            prompt_parts.append("balanced mix, authentic traditional sound")
        else:
            prompt_parts.append("professional quality")
    
    else:
        # Diğer türler için standart prompt
        if genre == 'turkish_folk':
            prompt_parts.append("Turkish folk music")
        else:
            prompt_parts.append(f"{genre} music")
        
        # Enstrümanlar
        if instruments:
            instrument_list = []
            for inst in instruments:
                inst_map = {
                    'kemençe': 'kemenche',
                    'kemenche': 'kemenche',
                    'tulum': 'tulum',
                    'davul': 'drum',
                    'zurna': 'zurna',
                    'bağlama': 'bağlama',
                    'baglama': 'bağlama',
                    'saz': 'bağlama',
                    'klarnet': 'clarinet',
                    'keman': 'violin',
                    'gitar': 'guitar',
                    'bass': 'bass',
                    'piyano': 'piano',
                    'drums': 'drums',
                }
                instrument_list.append(inst_map.get(inst.lower(), inst))
            prompt_parts.append(', '.join(instrument_list))
        
        # Tempo
        if tempo:
            prompt_parts.append(f"{tempo} BPM")
        
        # Stil ve mood
        if style:
            prompt_parts.append(style)
        if mood:
            prompt_parts.append(mood)
        if additional:
            prompt_parts.append(additional)
        
        prompt_parts.append("professional quality")
    
    return ', '.join(prompt_parts)

def generate_with_custom_prompt(instruments, genre, output_dir='output', duration=30,
                                model_size='small', tempo=None, style=None, mood=None,
                                additional=None, auto_master=False, guidance_scale=3.5,
                                num_generations=1, seed=None, prompt_style='detailed'):
    """
    Özel prompt ile müzik üretir (geliştirilmiş versiyon)
    
    Args:
        instruments: List[str] - Enstrüman listesi
        genre: str - Müzik türü
        output_dir: str - Çıktı klasörü
        duration: int - Süre (saniye)
        model_size: str - Model boyutu
        tempo: int - BPM
        style: str - Stil
        mood: str - Ruh hali
        additional: str - Ek özellikler
        auto_master: bool - Otomatik mastering
        guidance_scale: float - Guidance scale (1.0-10.0, yüksek = prompt'a daha sadık)
        num_generations: int - Kaç farklı versiyon üret (en iyisini seçmek için)
        seed: int - Random seed (reproducible results)
        prompt_style: str - 'detailed' veya 'concise'
    """
    prompt = create_custom_prompt(instruments, genre, tempo, style, mood, additional, prompt_style)
    
    print(f"🎵 Custom Prompt ({prompt_style}):")
    print(f"   {prompt}\n")
    
    if guidance_scale != 3.0:
        print(f"   ⚙️  Guidance scale: {guidance_scale}")
    if num_generations > 1:
        print(f"   🔄 Generating {num_generations} variations...")
    if seed is not None:
        print(f"   🎲 Seed: {seed}")
    
    generator = MusicGenerator(model_size=model_size)
    results = generator.generate(
        [prompt],
        output_dir=output_dir,
        duration=duration,
        auto_master=auto_master,
        master_preset='default',
        guidance_scale=guidance_scale,
        num_generations=num_generations,
        seed=seed
    )
    
    if results:
        print(f"\n✅ Music generated: {results[0]}")
        return results[0]
    
    return None

def main():
    parser = argparse.ArgumentParser(
        description='Özel Prompt ile Müzik Üretimi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek kullanım:
  python custom_prompt_generator.py --instruments "kemençe,tulum,davul" --genre karadeniz --tempo 91
  
Enstrümanlar (virgülle ayrılmış):
  kemençe, tulum, davul, zurna, bağlama, klarnet, keman, gitar, bass, piyano, drums
        """
    )
    parser.add_argument('--instruments', type=str, required=True,
                       help='Enstrümanlar (virgülle ayrılmış, örn: "kemençe,tulum,davul")')
    parser.add_argument('--genre', type=str, required=True,
                       help='Müzik türü (karadeniz, turkish_folk, pop, rock, vb.)')
    parser.add_argument('--tempo', type=int, default=None,
                       help='Tempo (BPM)')
    parser.add_argument('--style', type=str, default=None,
                       help='Stil (örn: "traditional", "modern", "fusion")')
    parser.add_argument('--mood', type=str, default=None,
                       help='Ruh hali (örn: "energetic", "melancholic", "joyful")')
    parser.add_argument('--additional', type=str, default=None,
                       help='Ek özellikler (virgülle ayrılmış)')
    parser.add_argument('--output', type=str, default='output',
                       help='Çıktı klasörü')
    parser.add_argument('--duration', type=int, default=30,
                       help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='small',
                       choices=['small', 'medium', 'large'])
    parser.add_argument('--master', action='store_true',
                       help='Otomatik mastering')
    
    args = parser.parse_args()
    
    # Enstrümanları parse et
    instruments = [inst.strip() for inst in args.instruments.split(',')]
    
    generate_with_custom_prompt(
        instruments,
        args.genre,
        output_dir=args.output,
        duration=args.duration,
        model_size=args.model,
        tempo=args.tempo,
        style=args.style,
        mood=args.mood,
        additional=args.additional,
        auto_master=args.master
    )

if __name__ == '__main__':
    main()

