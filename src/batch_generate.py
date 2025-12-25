"""
Sosyal medya için batch üretim
"""

from generate import MusicGenerator
from prompt_engineer import SOCIAL_MEDIA_PROMPTS, get_prompt
import json

def batch_generate_social_media(output_dir='output/social_media', model_size='small'):
    """Sosyal medya için çeşitli müzikler üretir"""
    generator = MusicGenerator(model_size=model_size)
    
    all_prompts = []
    for category, prompts in SOCIAL_MEDIA_PROMPTS.items():
        all_prompts.extend(prompts[:2])  # Her kategoriden 2 tane
    
    print(f"📦 Generating {len(all_prompts)} tracks for social media...")
    results = generator.generate(all_prompts, output_dir=output_dir, duration=30)
    
    # Metadata kaydet
    metadata = {
        'tracks': [
            {'file': r, 'prompt': p} 
            for r, p in zip(results, all_prompts)
        ]
    }
    
    with open(f'{output_dir}/metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(results)} tracks!")
    return results

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='small', choices=['small', 'medium', 'large'])
    args = parser.parse_args()
    batch_generate_social_media(model_size=args.model)

