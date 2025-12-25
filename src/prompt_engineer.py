"""
Sosyal medya için optimize edilmiş prompt'lar
"""

SOCIAL_MEDIA_PROMPTS = {
    'energetic': [
        "upbeat electronic dance music, 128 BPM, energetic, catchy melody",
        "vibrant pop music, modern production, uplifting, commercial",
        "energetic house music, driving bass, festival vibe"
    ],
    'ambient': [
        "calm ambient music, atmospheric, peaceful, background",
        "chill lo-fi hip hop, relaxed, study music",
        "meditative ambient soundscape, ethereal, spacious"
    ],
    'trending': [
        "viral TikTok style music, catchy hook, repetitive, addictive",
        "Instagram Reels background music, trendy, modern",
        "YouTube Shorts music, energetic, short loop, engaging"
    ],
    'emotional': [
        "emotional piano ballad, melancholic, cinematic",
        "nostalgic synthwave, 80s vibe, dreamy",
        "inspiring orchestral music, epic, motivational"
    ],
    'turkish_pop': [
        "Turkish pop music style, melodic, emotional, modern production, strong bass, deep bass line, 110 BPM, synthesizer and strings",
        "Turkish pop instrumental, melodic synthesizer, emotional, modern arrangement, prominent bass, 105 BPM",
        "Turkish style pop music, melodic, modern production, deep bass, strings and synthesizer, 115 BPM"
    ],
    'turkish_traditional': [
        "Turkish pop music with traditional instruments, bağlama (saz), violin, clarinet, piano accompaniment, melodic, emotional, 110 BPM, modern production with traditional elements",
        "Turkish music style, bağlama, keman (violin), klarnet (clarinet), piano, emotional, melancholic, 105 BPM, traditional meets modern",
        "Turkish instrumental, saz (bağlama), violin, clarinet, piano, strings, emotional, melodic, 115 BPM, contemporary Turkish music"
    ],
    'classical': [
        "classical music, orchestral, symphonic, strings, woodwinds, brass, piano, elegant, sophisticated, 120 BPM, Beethoven style",
        "classical instrumental, chamber music, violin, cello, piano, strings ensemble, melodic, emotional, 100 BPM, Mozart style",
        "orchestral classical music, full symphony, strings, brass, woodwinds, dramatic, powerful, 110 BPM, Bach style"
    ],
    'pop': [
        "pop music, catchy melody, upbeat, commercial, modern production, synthesizer, drums, bass, 120 BPM, radio friendly",
        "pop instrumental, vibrant, uplifting, contemporary, electronic elements, strings, piano, 115 BPM, chart-topping style",
        "modern pop music, commercial, catchy hook, synthesizer, drums, bass guitar, energetic, 125 BPM"
    ],
    'rock': [
        "rock music, electric guitars, powerful drums, bass guitar, energetic, driving rhythm, 140 BPM, stadium rock",
        "hard rock, distorted guitars, heavy drums, bass, aggressive, powerful, 150 BPM, guitar solos",
        "soft rock, acoustic and electric guitars, melodic, emotional, 120 BPM, ballad style",
        "punk rock, fast tempo, raw energy, electric guitars, drums, 160 BPM, rebellious"
    ],
    'rap_hiphop': [
        "hip hop instrumental, heavy bass, drum machine, synthesizer, urban, street vibe, 90 BPM, trap style",
        "rap beat, deep 808 bass, hi-hats, snare, synthesizer, dark, atmospheric, 95 BPM",
        "hip hop music, boom bap drums, bass line, samples, old school, 88 BPM, classic hip hop"
    ],
    'electronic': [
        "electronic dance music, synthesizer, drum machine, bass, energetic, 128 BPM, house music",
        "techno music, repetitive beats, synthesizer, bass, industrial, 130 BPM, dark techno",
        "trance music, uplifting, synthesizer, bass, melodic, 138 BPM, progressive trance",
        "EDM, electronic, synthesizer, heavy bass, drops, festival vibe, 128 BPM, big room"
    ],
    'country': [
        "country music, acoustic guitar, banjo, fiddle, harmonica, rustic, folk, 110 BPM, American country",
        "country instrumental, acoustic guitar, steel guitar, fiddle, bass, drums, nostalgic, 105 BPM, traditional country",
        "country pop, acoustic and electric guitars, modern production, melodic, 115 BPM, contemporary country"
    ],
    'jazz': [
        "jazz music, piano, saxophone, double bass, drums, improvisation, swing, 120 BPM, classic jazz",
        "smooth jazz, saxophone, piano, bass, drums, relaxed, sophisticated, 100 BPM, contemporary jazz",
        "bebop jazz, fast tempo, saxophone, piano, double bass, drums, complex, 180 BPM, bebop style",
        "cool jazz, mellow, saxophone, piano, bass, drums, laid back, 110 BPM, West Coast jazz"
    ],
    'reggae': [
        "reggae music, slow tempo, heavy bass, off-beat rhythm, guitar, organ, 80 BPM, Bob Marley style",
        "reggae instrumental, bass heavy, skank guitar, drums, relaxed, laid back, 75 BPM, roots reggae",
        "dancehall reggae, bass, drums, synthesizer, energetic, 90 BPM, modern reggae"
    ],
    'metal': [
        "heavy metal, distorted electric guitars, powerful drums, bass, aggressive, fast, 160 BPM, power metal",
        "death metal, extreme distortion, blast beats, bass, dark, brutal, 200 BPM, technical death metal",
        "black metal, atmospheric, distorted guitars, fast drums, dark, 180 BPM, symphonic black metal",
        "metal music, guitar riffs, double bass drums, bass, powerful, 150 BPM, classic heavy metal"
    ],
    'blues': [
        "blues music, electric guitar, harmonica, bass, drums, melancholic, emotional, 100 BPM, Delta blues",
        "blues instrumental, slide guitar, harmonica, bass, slow tempo, sad, 90 BPM, traditional blues",
        "Chicago blues, electric guitar, harmonica, bass, drums, soulful, 110 BPM, electric blues"
    ],
    'latin': [
        "Latin music, salsa, percussion, brass, piano, energetic, danceable, 120 BPM, Cuban salsa",
        "Latin instrumental, bongo, conga, trumpet, piano, bass, festive, 115 BPM, rumba style",
        "tango music, bandoneon, violin, piano, bass, dramatic, passionate, 130 BPM, Argentine tango",
        "Latin pop, percussion, synthesizer, brass, modern, 125 BPM, reggaeton influence"
    ],
    'karadeniz': [
        "Turkish Black Sea music (Karadeniz müziği), kemenche (Karadeniz kemençesi), tulum (Karadeniz bagpipe), davul (drum), traditional Turkish Black Sea style, energetic, rhythmic, folk music, 90-100 BPM",
        "Karadeniz müziği, kemençe, tulum, davul, zurna, traditional arrangement, authentic Turkish Black Sea sound, melodic, emotional, regional Turkish music, 85-110 BPM",
        "Turkish Black Sea folk music, kemenche, tulum, davul, bass, traditional instruments, energetic, rhythmic, authentic Karadeniz style, 90-105 BPM"
    ]
}

def get_prompt(category='energetic', style='default'):
    """Kategoriye göre prompt döndürür"""
    prompts = SOCIAL_MEDIA_PROMPTS.get(category, SOCIAL_MEDIA_PROMPTS['energetic'])
    return prompts[0] if style == 'default' else prompts

def enhance_prompt(base_prompt, additions=None):
    """Prompt'u geliştirir"""
    if additions:
        return f"{base_prompt}, {', '.join(additions)}"
    return base_prompt

