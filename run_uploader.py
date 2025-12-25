"""
Neural Beats Studio - Social Media Uploader
Masa üstü uygulamasını başlatır
"""

import sys
from pathlib import Path

# src klasörünü path'e ekle
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from social_media_uploader import main
    
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"[ERROR] Modül yüklenemedi: {e}")
    print("[INFO] Gerekli paketler:")
    print("  - tkinter (genellikle Python ile birlikte gelir)")
    print("  - google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client")
    input("\nDevam etmek için Enter'a basın...")

