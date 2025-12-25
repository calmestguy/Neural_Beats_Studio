"""
Gelişmiş prompt mühendisliği araçları
"""

from prompt_engineer import SOCIAL_MEDIA_PROMPTS

# Müzik türüne göre önerilen mastering preset'leri
GENRE_MASTERING_PRESETS = {
    'rock': 'bass_heavy',
    'metal': 'bass_heavy',
    'rap_hiphop': 'bass_heavy',
    'electronic': 'bass_heavy',
    'pop': 'default',
    'jazz': 'vocal',
    'blues': 'vocal',
    'classical': 'cinematic',
    'turkish_pop': 'default',
    'turkish_traditional': 'vocal',
    'karadeniz': 'folk_traditional',  # Yeni preset
    'country': 'vocal',
    'latin': 'default',
    'reggae': 'bass_heavy'
}

# Müzik türüne göre önerilen ek prompt'lar
GENRE_ENHANCEMENTS = {
    'rock': ['powerful', 'driving', 'energetic', 'gritty'],
    'metal': ['aggressive', 'brutal', 'intense', 'heavy'],
    'pop': ['catchy', 'commercial', 'radio-friendly', 'polished'],
    'jazz': ['sophisticated', 'smooth', 'improvised', 'swinging'],
    'electronic': ['punchy', 'driving', 'festival-ready', 'bass-heavy'],
    'classical': ['elegant', 'dramatic', 'orchestral', 'sophisticated'],
    'turkish_pop': ['melodic', 'emotional', 'modern', 'catchy'],
    'karadeniz': ['traditional', 'rhythmic', 'energetic', 'melodic', 'folk', 'authentic'],
    'blues': ['soulful', 'emotional', 'raw', 'authentic']
}

def enhance_prompt_for_genre(genre, base_prompt=None, add_emotion=None, add_instruments=None):
    """
    Müzik türüne göre prompt'u geliştirir
    
    Args:
        genre: Müzik türü
        base_prompt: Temel prompt (None ise genre'den alır)
        add_emotion: Eklemek istediğiniz duygu
        add_instruments: Eklemek istediğiniz enstrümanlar
    """
    if base_prompt is None:
        if genre in SOCIAL_MEDIA_PROMPTS:
            base_prompt = SOCIAL_MEDIA_PROMPTS[genre][0]
        else:
            base_prompt = f"{genre} music"
    
    # Genre enhancement'ları ekle
    if genre in GENRE_ENHANCEMENTS:
        enhancements = GENRE_ENHANCEMENTS[genre]
        base_prompt += f", {', '.join(enhancements[:2])}"
    
    # Ek duygu
    if add_emotion:
        base_prompt += f", {add_emotion}"
    
    # Ek enstrümanlar
    if add_instruments:
        if isinstance(add_instruments, list):
            base_prompt += f", {', '.join(add_instruments)}"
        else:
            base_prompt += f", {add_instruments}"
    
    return base_prompt

def get_mastering_preset_for_genre(genre):
    """Müzik türüne göre önerilen mastering preset'i döndürür"""
    return GENRE_MASTERING_PRESETS.get(genre, 'default')

def create_social_media_prompt(genre, platform='general', mood='energetic'):
    """
    Sosyal medya için optimize edilmiş prompt oluşturur
    
    Args:
        genre: Müzik türü
        platform: Platform ('tiktok', 'instagram', 'youtube', 'general')
        mood: Ruh hali ('energetic', 'calm', 'emotional', 'trendy')
    """
    base_prompt = enhance_prompt_for_genre(genre)
    
    platform_specifics = {
        'tiktok': ['viral', 'catchy hook', 'repetitive', 'addictive', 'short loop'],
        'instagram': ['trendy', 'modern', 'commercial', 'polished'],
        'youtube': ['engaging', 'dynamic', 'professional', 'high-quality'],
        'general': ['social media ready', 'catchy', 'modern']
    }
    
    mood_specifics = {
        'energetic': ['upbeat', 'driving', 'energetic', 'high-energy'],
        'calm': ['relaxed', 'peaceful', 'chill', 'ambient'],
        'emotional': ['emotional', 'melodic', 'touching', 'heartfelt'],
        'trendy': ['trending', 'viral', 'modern', 'current']
    }
    
    if platform in platform_specifics:
        base_prompt += f", {', '.join(platform_specifics[platform][:3])}"
    
    if mood in mood_specifics:
        base_prompt += f", {', '.join(mood_specifics[mood][:2])}"
    
    return base_prompt

def suggest_prompt_improvements(prompt):
    """
    Mevcut prompt'a iyileştirme önerileri sunar
    """
    suggestions = []
    
    # BPM kontrolü
    if 'BPM' not in prompt:
        suggestions.append("BPM ekleyin (örn: '120 BPM')")
    
    # Enstrüman kontrolü
    instruments = ['guitar', 'piano', 'drums', 'bass', 'synthesizer', 'strings']
    has_instrument = any(inst in prompt.lower() for inst in instruments)
    if not has_instrument:
        suggestions.append("Enstrümanlar ekleyin (örn: 'electric guitar, drums, bass')")
    
    # Duygu kontrolü
    emotions = ['emotional', 'energetic', 'melancholic', 'uplifting', 'dramatic']
    has_emotion = any(emotion in prompt.lower() for emotion in emotions)
    if not has_emotion:
        suggestions.append("Duygu ekleyin (örn: 'emotional', 'energetic')")
    
    # Production kontrolü
    production_terms = ['modern production', 'polished', 'commercial', 'professional']
    has_production = any(term in prompt.lower() for term in production_terms)
    if not has_production:
        suggestions.append("Production terimi ekleyin (örn: 'modern production')")
    
    return suggestions

if __name__ == '__main__':
    # Test
    print("🎵 Prompt Enhancement Test\n")
    
    # Genre-based enhancement
    enhanced = enhance_prompt_for_genre('rock', add_emotion='aggressive', add_instruments=['distorted guitar', 'heavy drums'])
    print(f"Enhanced Rock Prompt: {enhanced}\n")
    
    # Social media prompt
    sm_prompt = create_social_media_prompt('pop', platform='tiktok', mood='energetic')
    print(f"TikTok Pop Prompt: {sm_prompt}\n")
    
    # Suggestions
    test_prompt = "electronic music"
    suggestions = suggest_prompt_improvements(test_prompt)
    print(f"Suggestions for '{test_prompt}':")
    for suggestion in suggestions:
        print(f"  • {suggestion}")

