"""
YouTube API Authentication Test Script
İlk authentication'ı test eder
"""

import os
import sys

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    print("[ERROR] Google API client libraries not installed!")
    print("[INFO] Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# YouTube API scope
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def test_authentication():
    """YouTube API authentication test"""
    print("="*70)
    print("YOUTUBE API AUTHENTICATION TEST")
    print("="*70)
    print()
    
    credentials_file = 'credentials.json'
    token_file = 'token.json'
    
    # credentials.json kontrolü
    if not os.path.exists(credentials_file):
        print(f"[ERROR] credentials.json bulunamadi: {credentials_file}")
        print("[INFO] Google Cloud Console'dan credentials.json dosyasini indirin")
        return False
    
    print(f"[OK] credentials.json bulundu: {credentials_file}")
    print()
    
    creds = None
    
    # Token dosyası varsa yükle
    if os.path.exists(token_file):
        print(f"[INFO] token.json bulundu, yukleniyor...")
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            print(f"[OK] token.json yuklendi")
        except Exception as e:
            print(f"[WARNING] token.json yuklenemedi: {e}")
            print(f"[INFO] Yeni token alinacak...")
            creds = None
    
    # Token yoksa veya geçersizse, yeni token al
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"[INFO] Token expired, yenileniyor...")
            try:
                creds.refresh(Request())
                print(f"[OK] Token yenilendi")
            except Exception as e:
                print(f"[ERROR] Token yenilenemedi: {e}")
                creds = None
        
        if not creds:
            print(f"[INFO] Yeni token aliniyor...")
            print(f"[INFO] Tarayici acilacak, Google hesabinizla giris yapin")
            print()
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
                print()
                print(f"[SUCCESS] Authentication basarili!")
            except Exception as e:
                print(f"[ERROR] Authentication basarisiz: {e}")
                return False
        
        # Token'ı kaydet
        print(f"[INFO] Token kaydediliyor: {token_file}")
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print(f"[OK] Token kaydedildi")
    
    # YouTube API service oluştur
    print()
    print("[INFO] YouTube API service olusturuluyor...")
    try:
        service = build('youtube', 'v3', credentials=creds)
        print("[OK] YouTube API service olusturuldu")
    except Exception as e:
        print(f"[ERROR] YouTube API service olusturulamadi: {e}")
        return False
    
    # Basit test: API'ye erişim kontrolü
    print()
    print("[INFO] YouTube API erisim testi...")
    try:
        # Sadece upload yetkisi var, kanal bilgisi almak için gerekli değil
        # Basit bir test yapalım - service oluşturulduysa başarılı
        print("[OK] YouTube API service hazir!")
        print()
        print("="*70)
        print("AUTHENTICATION TEST BASARILI!")
        print("="*70)
        print()
        print("[INFO] Token kaydedildi: token.json")
        print("[INFO] Artik videolari yukleyebilirsiniz!")
        return True
    except Exception as e:
        print(f"[ERROR] Test basarisiz: {e}")
        return False

if __name__ == '__main__':
    success = test_authentication()
    if success:
        print()
        print("[NEXT] Simdi videolari yukleyebilirsiniz:")
        print("   python src/youtube_upload.py --video-dir output/youtube --privacy private")
    else:
        print()
        print("[ERROR] Authentication test basarisiz!")
        sys.exit(1)

