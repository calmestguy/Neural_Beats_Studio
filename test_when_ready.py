"""
Medium model indirme tamamlanınca otomatik test eder
Kullanım: python test_when_ready.py
"""

import time
import sys
from pathlib import Path
import sys
sys.path.insert(0, 'src')
from test_medium_model import check_model_downloaded, test_medium_model

def wait_and_test(check_interval=30):
    """Model indirilene kadar bekleyip test eder"""
    print("⏳ Waiting for medium model to download...")
    print(f"   Checking every {check_interval} seconds...")
    print("   (Press Ctrl+C to cancel)\n")
    
    check_count = 0
    while True:
        check_count += 1
        print(f"🔍 Check #{check_count}...", end=" ")
        
        if check_model_downloaded():
            print("✅ Model ready!")
            print("\n" + "="*60)
            print("🧪 Starting test with medium model...")
            print("="*60 + "\n")
            
            # Test et
            if test_medium_model():
                print("\n✅ Test completed successfully!")
                print("\n🎵 Now generating music with medium model...")
                
                # Müzik üret
                import sys
                sys.path.insert(0, 'src')
                from custom_prompt_generator import generate_with_custom_prompt
                result = generate_with_custom_prompt(
                    instruments=["kemençe", "tulum", "davul", "bass", "vocals"],
                    genre="karadeniz",
                    output_dir="output",
                    duration=30,
                    model_size="medium",
                    tempo=91,
                    style="traditional",
                    mood="energetic,rhythmic,melodic",
                    additional="strong bass,deep bass line",
                    auto_master=True
                )
                
                if result:
                    print(f"\n🎉 Music generated: {result}")
                    return 0
                else:
                    print("\n❌ Music generation failed")
                    return 1
            else:
                print("\n❌ Test failed")
                return 1
        else:
            print("⏳ Still downloading...")
        
        time.sleep(check_interval)

if __name__ == '__main__':
    try:
        sys.exit(wait_and_test())
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)

