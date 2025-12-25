"""
Manuel prompt oluşturucu - Analiz sonuçlarını gösterir, kullanıcı prompt'u düzenleyebilir
"""

from audio_analyzer import analyze_audio, convert_to_wav_if_needed
from generate import MusicGenerator
import argparse
import os

def interactive_prompt_creation(audio_file, output_dir='output', duration=30, 
                                model_size='small', auto_master=False):
    """
    İnteraktif prompt oluşturma - analiz sonuçlarını gösterir, kullanıcı düzenleyebilir
    """
    print(f"🔍 Analyzing: {audio_file}\n")
    
    # Analiz
    audio_file = convert_to_wav_if_needed(audio_file)
    analysis = analyze_audio(audio_file, skip_seconds=0, analysis_duration=60)
    
    if not analysis:
        return None
    
    # Sonuçları göster
    print("\n" + "="*60)
    print("📊 ANALİZ SONUÇLARI")
    print("="*60)
    print(f"Tempo: {analysis['tempo']} BPM")
    print(f"Key: {analysis['key']}")
    print(f"Tahmin Edilen Tür: {analysis['estimated_genre']}")
    print(f"Tespit Edilen Enstrümanlar: {', '.join(analysis['instruments'])}")
    print(f"Enerji Seviyesi: {analysis['energy_level']}")
    print(f"Bas Vurgulu: {analysis['bass_prominent']}")
    print("="*60)
    
    # Önerilen prompt
    from audio_analyzer import analysis_to_prompt
    suggested_prompt = analysis_to_prompt(analysis, similarity_level='high')
    
    print("\n💡 ÖNERİLEN PROMPT:")
    print(f"   {suggested_prompt}\n")
    
    print("⚠️  Bu prompt'u düzenlemek ister misiniz?")
    print("   (Şimdilik önerilen prompt kullanılıyor)")
    print("   (Gelecekte interaktif düzenleme eklenebilir)\n")
    
    # Müzik üret
    generator = MusicGenerator(model_size=model_size)
    results = generator.generate(
        [suggested_prompt],
        output_dir=output_dir,
        duration=duration,
        auto_master=auto_master,
        master_preset='default'
    )
    
    if results:
        print(f"\n✅ Music generated: {results[0]}")
        return results[0]
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Manuel Prompt Oluşturucu')
    parser.add_argument('audio_file', type=str, help='Audio dosyası')
    parser.add_argument('--output', type=str, default='output', help='Çıktı klasörü')
    parser.add_argument('--duration', type=int, default=30, help='Süre (saniye)')
    parser.add_argument('--model', type=str, default='small', choices=['small', 'medium', 'large'])
    parser.add_argument('--master', action='store_true', help='Otomatik mastering')
    
    args = parser.parse_args()
    
    interactive_prompt_creation(
        args.audio_file,
        output_dir=args.output,
        duration=args.duration,
        model_size=args.model,
        auto_master=args.master
    )

if __name__ == '__main__':
    main()



