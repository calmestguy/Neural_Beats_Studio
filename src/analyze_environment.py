"""
Şarkı sözlerinden uygun ortam/arka plan tespiti
"""

def analyze_lyrics_environment(lyrics):
    """
    Şarkı sözlerinden uygun ortam/arka plan tespit eder
    """
    lyrics_lower = lyrics.lower()
    
    # Ortam anahtar kelimeleri
    environments = {
        'rainy_city_night': {
            'keywords': ['rain', 'rainy', 'city', 'streetlights', 'neon', 'asphalt', 
                        'puddles', 'night', 'nighttime', 'urban', 'street'],
            'description': 'Rainy city night, urban street, neon lights, wet asphalt, streetlights',
            'mood': 'melancholic, atmospheric, cinematic',
            'colors': 'dark, blue, neon, wet reflections'
        },
        'studio': {
            'keywords': ['studio', 'recording', 'microphone', 'music'],
            'description': 'Professional music studio, modern, clean',
            'mood': 'professional, clean, focused',
            'colors': 'warm, professional lighting'
        },
        'concert_stage': {
            'keywords': ['stage', 'concert', 'performance', 'audience', 'spotlight'],
            'description': 'Concert stage, spotlight, audience, live performance',
            'mood': 'energetic, live, performance',
            'colors': 'stage lighting, dynamic'
        },
        'cozy_indoor': {
            'keywords': ['home', 'room', 'cozy', 'warm', 'fireplace', 'indoor'],
            'description': 'Cozy indoor space, warm lighting, intimate',
            'mood': 'intimate, warm, cozy',
            'colors': 'warm, golden, soft lighting'
        },
        'nature_outdoor': {
            'keywords': ['nature', 'forest', 'mountain', 'beach', 'outdoor', 'sunset', 'sunrise'],
            'description': 'Natural outdoor setting, scenic, beautiful',
            'mood': 'peaceful, natural, scenic',
            'colors': 'natural, vibrant, outdoor lighting'
        },
        'bar_club': {
            'keywords': ['bar', 'club', 'nightclub', 'drinks', 'nightlife'],
            'description': 'Bar or nightclub, dim lighting, social atmosphere',
            'mood': 'social, nightlife, energetic',
            'colors': 'dim, colorful, neon bar lights'
        },
        'car_interior': {
            'keywords': ['car', 'drive', 'driving', 'road', 'travel', 'journey', 'vehicle', 'interior'],
            'description': 'Car interior, driving at night, road ahead, windshield view',
            'mood': 'contemplative, moving, journey',
            'colors': 'dark interior, streetlights, warm dashboard lights'
        },
        'window_rainy_night': {
            'keywords': ['window', 'rain', 'rainy', 'night', 'outside', 'view', 'looking'],
            'description': 'Window view, rainy night, looking outside, reflections',
            'mood': 'melancholic, contemplative, peaceful',
            'colors': 'dark, blue, rain drops, window reflections'
        },
        'cozy_room_window': {
            'keywords': ['room', 'window', 'cozy', 'warm', 'indoor', 'home', 'inside'],
            'description': 'Cozy room with window, warm lighting, intimate space',
            'mood': 'intimate, warm, cozy, peaceful',
            'colors': 'warm, golden, soft indoor lighting'
        }
    }
    
    # Her ortam için skor hesapla
    scores = {}
    for env_name, env_data in environments.items():
        score = sum(1 for keyword in env_data['keywords'] if keyword in lyrics_lower)
        if score > 0:
            scores[env_name] = score
    
    # En yüksek skorlu ortamı seç
    if scores:
        best_env = max(scores.items(), key=lambda x: x[1])[0]
        return environments[best_env]
    else:
        # Varsayılan: studio
        return environments['studio']

def generate_background_prompt(environment_data):
    """
    Ortam verilerinden arka plan prompt'u oluşturur
    """
    return f"{environment_data['description']}, {environment_data['mood']}, {environment_data['colors']}, high quality, 4K, cinematic"

def get_background_image_url(environment_name):
    """
    Ortam adına göre arka plan görüntüsü URL'i döndürür
    (D-ID'nin hazır arka planları veya kullanıcının yüklediği görüntüler)
    """
    # D-ID'de hazır arka planlar varsa buraya eklenebilir
    # Şimdilik kullanıcının kendi arka planını yüklemesi gerekecek
    return None


