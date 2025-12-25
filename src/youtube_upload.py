"""
YouTube API ile Otomatik Video Yükleme
Müzik videolarını ülke, tür ve metadata ile YouTube'a yükler
"""

import os
import sys
import json
import argparse
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("[ERROR] Google API client libraries not installed!")
    print("[INFO] Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    try:
        # Python 3.7+ için reconfigure kullan
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        elif hasattr(sys.stdout, 'buffer'):
            # Eski Python versiyonları için codecs kullan
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        elif hasattr(sys.stderr, 'buffer'):
            import codecs
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except (AttributeError, TypeError, ValueError):
        # Encoding ayarı başarısız olursa devam et
        pass

# YouTube API scope
# youtube.upload: Video yükleme
# youtube.readonly: Video listeleme ve arama (duplicate kontrolü için)
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly'
]

def authenticate_youtube(credentials_file='credentials.json', token_file='token.json'):
    """
    YouTube API için OAuth2 authentication
    
    Args:
        credentials_file: Google Cloud credentials JSON dosyası
        token_file: Token cache dosyası
    
    Returns:
        YouTube API service object
    """
    creds = None
    
    # Token dosyası varsa yükle
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # Token yoksa veya geçersizse, yeni token al
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                print(f"[ERROR] Credentials file not found: {credentials_file}")
                print("[INFO] Download from Google Cloud Console:")
                print("   1. Go to: https://console.cloud.google.com/")
                print("   2. Create a project")
                print("   3. Enable YouTube Data API v3")
                print("   4. Create OAuth 2.0 credentials")
                print("   5. Download credentials.json")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Token'ı kaydet
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def detect_language_from_title(title):
    """
    Şarkı başlığından dil tespit eder ve çok dilli destek için ek diller döndürür
    
    Args:
        title: Şarkı başlığı
    
    Returns:
        (video_language, audio_language, additional_languages) tuple
        additional_languages: Global erişim için ek diller listesi
    """
    title_lower = title.lower()
    additional_languages = []
    
    # Türkçe karakterler varsa Türkçe
    turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü']
    if any(char in title for char in turkish_chars):
        # Türkiye için: Türkçe + İngilizce (global erişim)
        additional_languages = ['en']  # Global erişim için İngilizce
        return ('tr', 'tr', additional_languages)
    
    # Rusça karakterler varsa Rusça
    russian_chars = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    if any(char in title_lower for char in russian_chars):
        # Rusya için: Rusça + İngilizce (global erişim)
        additional_languages = ['en']  # Global erişim için İngilizce
        return ('ru', 'ru', additional_languages)
    
    # Korece karakterler varsa Korece
    korean_chars = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']
    if any(char in title for char in korean_chars):
        # Kore için: Korece + İngilizce (global erişim)
        additional_languages = ['en']  # Global erişim için İngilizce
        return ('ko', 'ko', additional_languages)
    
    # Avrupa dilleri için kontrol (Fransızca, Almanca, İspanyolca, İtalyanca)
    european_keywords = {
        'fr': ['le', 'la', 'les', 'un', 'une', 'de', 'et', 'à', 'pour'],
        'de': ['der', 'die', 'das', 'und', 'ist', 'mit', 'für'],
        'es': ['el', 'la', 'los', 'las', 'y', 'de', 'en', 'por'],
        'it': ['il', 'la', 'lo', 'gli', 'le', 'e', 'di', 'in', 'per']
    }
    
    for lang_code, keywords in european_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            # Avrupa için: Ana dil + İngilizce (global erişim)
            additional_languages = ['en']
            return (lang_code, lang_code, additional_languages)
    
    # Varsayılan: İngilizce (global) - ama Türkiye, Rusya, Avrupa, Kore için de erişilebilir
    # Global içerik için çok dilli destek
    additional_languages = ['tr', 'ru', 'de', 'fr', 'es', 'it', 'ko']  # Ana pazarlar için
    return ('en', 'en', additional_languages)

def is_video_already_uploaded(service, title, video_file=None):
    """
    Aynı başlıklı veya dosya adlı video zaten yüklenmiş mi kontrol eder
    
    Args:
        service: YouTube API service object
        title: Video başlığı
        video_file: Video dosyası yolu (opsiyonel, dosya adı kontrolü için)
    
    Returns:
        True if already uploaded, False otherwise
    """
    try:
        # Başlığa göre kontrol - channels().list kullanarak kendi videolarımızı al
        # search().list yerine channels().list kullanıyoruz çünkü daha güvenilir
        try:
            # Önce channel ID'yi al
            channels_response = service.channels().list(
                part='contentDetails',
                mine=True
            ).execute()
            
            if not channels_response.get('items'):
                # Channel bilgisi alınamadı, search ile dene
                request = service.search().list(
                    part='snippet',
                    forMine=True,
                    q=title,
                    type='video',
                    maxResults=50
                )
                response = request.execute()
            else:
                # Uploads playlist ID'yi al
                uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                
                # Playlist'teki videoları al
                playlist_items = service.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=50
                ).execute()
                
                # Başlık kontrolü
                for item in playlist_items.get('items', []):
                    video_title = item['snippet'].get('title', '').lower()
                    if video_title == title.lower():
                        return True
                
                # Dosya adına göre kontrol (eğer video_file verilmişse)
                if video_file:
                    file_name = Path(video_file).stem
                    clean_name = file_name.replace('_youtube', '').replace('_yt', '').lower()
                    
                    for item in playlist_items.get('items', []):
                        video_title = item['snippet'].get('title', '').lower()
                        if clean_name in video_title or video_title in clean_name:
                            return True
                
                return False
                
        except HttpError as http_err:
            # Eğer channels().list çalışmazsa, search().list ile dene
            if 'insufficientPermissions' in str(http_err) or '403' in str(http_err):
                print(f"[WARNING] Duplicate kontrolü için yeterli izin yok. "
                      f"Token'ı yeniden oluşturmanız gerekebilir (youtube.readonly scope'u ile)")
                # İzin yoksa False döndür (yükleme devam etsin)
                return False
            
            # Diğer hatalar için search().list dene
            request = service.search().list(
                part='snippet',
                forMine=True,
                q=title,
                type='video',
                maxResults=50
            )
            response = request.execute()
            
            # Başlık kontrolü
            for item in response.get('items', []):
                if item['snippet']['title'].lower() == title.lower():
                    return True
            
            return False
        
    except Exception as e:
        print(f"[WARNING] Could not check for duplicates: {e}")
        # Hata durumunda False döndür (yükleme devam etsin, duplicate kontrolü atlanır)
        return False

def get_music_metadata(music_file):
    """
    Müzik dosyasından metadata çıkarır (isim, tür tahmini, çok dilli açıklama, vb.)
    
    Args:
        music_file: Müzik dosyası yolu
    
    Returns:
        Dict with metadata
    """
    music_name = Path(music_file).stem
    
    # Gelişmiş copyright notice (İngilizce)
    copyright_notice = "\n\n" + "=" * 80 + "\n" + \
                       "Copyright © Neural Beats Studio. All rights reserved.\n" + \
                       "This music is generated by Neural Beats Studio using AI technology.\n" + \
                       "Unauthorized reproduction, distribution, or commercial use is prohibited.\n" + \
                       "For licensing inquiries, please contact Neural Beats Studio.\n" + \
                       "=" * 80 + "\n"
    
    # Dil tespiti (gelişmiş)
    lang_result = detect_language_from_title(music_name)
    if len(lang_result) == 3:
        video_lang, audio_lang, additional_languages = lang_result
    else:
        # Eski format için geriye dönük uyumluluk
        video_lang, audio_lang = lang_result[:2]
        additional_languages = []
    
    # Çok dilli açıklama oluştur
    description_parts = [f"🎵 {music_name}"]
    
    # Ana dil açıklaması
    language_descriptions = {
        'tr': 'Neural Beats Studio tarafından AI teknolojisi ile oluşturulmuş müzik.',
        'ru': 'Музыка, созданная Neural Beats Studio с использованием технологий ИИ.',
        'ko': 'Neural Beats Studio가 AI 기술을 사용하여 생성한 음악.',
        'en': 'Music generated by Neural Beats Studio using AI technology.',
        'de': 'Musik, die von Neural Beats Studio mit KI-Technologie generiert wurde.',
        'fr': 'Musique générée par Neural Beats Studio utilisant la technologie IA.',
        'es': 'Música generada por Neural Beats Studio usando tecnología de IA.',
        'it': 'Musica generata da Neural Beats Studio utilizzando la tecnologia AI.'
    }
    
    main_desc = language_descriptions.get(video_lang, language_descriptions['en'])
    description_parts.append(f"\n{main_desc}")
    
    # Global erişim için İngilizce açıklama ekle (ana dil İngilizce değilse)
    if video_lang != 'en':
        description_parts.append(f"\n\n🌍 {language_descriptions['en']}")
    
    # Copyright notice ekle
    description_parts.append(copyright_notice)
    
    # Hashtag'ler (çok dilli)
    hashtags = ['#AIMusic', '#NeuralBeatsStudio', '#GeneratedMusic', '#MusicProduction']
    if video_lang == 'tr':
        hashtags.extend(['#TürkçeMüzik', '#AIMüzik'])
    elif video_lang == 'ru':
        hashtags.extend(['#РусскаяМузыка', '#ИИМузыка'])
    elif video_lang == 'ko':
        hashtags.extend(['#한국음악', '#AI음악'])
    
    description_parts.append("\n" + " ".join(hashtags))
    
    # Etiketler
    tags = ['music', 'generated music', 'neural beats studio', 'ai music', 'electronic music']
    if video_lang != 'en':
        tags.append(f'{video_lang} music')
    
    metadata = {
        'title': music_name,
        'description': '\n'.join(description_parts),
        'tags': tags,
        'category_id': '10',  # Music
        'video_language': video_lang,
        'audio_language': audio_lang,
        'additional_languages': additional_languages
    }
    
    return metadata

def upload_video_to_youtube(service, video_file, title, description, tags, 
                            category_id='10', privacy_status='private',
                            thumbnail_file=None, for_kids=False,
                            video_language='en', audio_language='en',
                            check_duplicate=True):
    """
    Video'yu YouTube'a yükler
    
    Args:
        service: YouTube API service object
        video_file: Video dosyası yolu
        title: Video başlığı
        description: Video açıklaması
        tags: Video etiketleri (list)
        category_id: Video kategorisi (10=Music)
        privacy_status: Gizlilik durumu (private, unlisted, public)
        thumbnail_file: Thumbnail görüntüsü (opsiyonel)
    
    Returns:
        Video ID if successful, None otherwise
    """
    print(f"[UPLOAD] Uploading video to YouTube...")
    print(f"   Title: {title}")
    print(f"   File: {video_file}")
    print(f"   Privacy: {privacy_status}")
    
    if not os.path.exists(video_file):
        print(f"[ERROR] Video file not found: {video_file}")
        return None
    
    # Duplicate kontrolü (başlık ve dosya adına göre)
    if check_duplicate:
        if is_video_already_uploaded(service, title, video_file):
            print(f"[SKIP] Video already uploaded: {title}")
            return None
    
    # Video metadata
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id,
            'defaultLanguage': video_language,
            'defaultAudioLanguage': audio_language
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': for_kids  # False = Not made for kids (çocuklara özel değil)
        }
    }
    
    # Video yükleme
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True,
                           mimetype='video/*')
    
    try:
        insert_request = service.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        video_id = None
        response = None
        
        # Resumable upload
        while response is None:
            status, response = insert_request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"   Progress: {progress}%")
        
        if 'id' in response:
            video_id = response['id']
            print(f"[SUCCESS] Video uploaded! Video ID: {video_id}")
            print(f"   URL: https://www.youtube.com/watch?v={video_id}")
            
            # Thumbnail yükle (varsa)
            if thumbnail_file and os.path.exists(thumbnail_file):
                print(f"[THUMBNAIL] Uploading thumbnail...")
                try:
                    service.thumbnails().set(
                        videoId=video_id,
                        media_body=MediaFileUpload(thumbnail_file)
                    ).execute()
                    print(f"[SUCCESS] Thumbnail uploaded!")
                except HttpError as e:
                    print(f"[WARNING] Thumbnail upload failed: {e}")
            
            return video_id
        else:
            print(f"[ERROR] Upload failed: {response}")
            return None
            
    except HttpError as e:
        error_details = f"[ERROR] YouTube API error: {e}"
        # Detaylı hata mesajı
        if hasattr(e, 'content'):
            try:
                import json
                error_json = json.loads(e.content.decode('utf-8'))
                if 'error' in error_json:
                    error_info = error_json['error']
                    error_code = error_info.get('code', 'N/A')
                    error_details += f"\n   Error Code: {error_code}"
                    error_details += f"\n   Error Message: {error_info.get('message', 'N/A')}"
                    if 'errors' in error_info:
                        for err in error_info['errors']:
                            reason = err.get('reason', 'N/A')
                            message = err.get('message', 'N/A')
                            error_details += f"\n   - {message} (reason: {reason})"
                            
                            # Özel hata mesajları
                            if reason == 'uploadLimitExceeded':
                                error_details += "\n\n   ⚠️ YOUTUBE GÜNLÜK YÜKLEME LİMİTİ AŞILDI!"
                                error_details += "\n   YouTube'un günlük video yükleme limiti var:"
                                error_details += "\n   - Yeni kanallar: 15 video/gün"
                                error_details += "\n   - Doğrulanmış kanallar: 50+ video/gün"
                                error_details += "\n   Çözüm:"
                                error_details += "\n   1. 24 saat bekleyin"
                                error_details += "\n   2. Kanalınızı doğrulayın (https://www.youtube.com/verify)"
                                error_details += "\n   3. Videoları daha sonra yükleyin"
                            
                            elif reason == 'insufficientPermissions':
                                error_details += "\n\n   ⚠️ YETKİ HATASI!"
                                error_details += "\n   Token'ı yeniden oluşturmanız gerekiyor."
                                error_details += "\n   token.json dosyasını silin ve tekrar bağlanın."
            except:
                pass
        print(error_details)
        return None
    except Exception as e:
        error_details = f"[ERROR] Unexpected error during upload: {e}"
        import traceback
        error_details += f"\n   Traceback: {traceback.format_exc()}"
        print(error_details)
        return None

def batch_upload_to_youtube(service, video_dir, music_dir=None, 
                           privacy_status='private', category_id='10'):
    """
    Klasördeki tüm videoları YouTube'a yükler
    
    Args:
        service: YouTube API service object
        video_dir: Video dosyaları klasörü
        music_dir: Müzik dosyaları klasörü (metadata için)
        privacy_status: Gizlilik durumu
        category_id: Video kategorisi
    """
    video_dir = Path(video_dir)
    video_files = list(video_dir.glob("*.mp4"))
    
    if not video_files:
        print(f"[ERROR] No video files found in: {video_dir}")
        return
    
    print(f"[BATCH] Found {len(video_files)} videos to upload")
    print()
    
    results = []
    
    for i, video_file in enumerate(video_files, 1):
        print(f"[{i}/{len(video_files)}] Processing: {video_file.name}")
        
        # Metadata oluştur
        if music_dir:
            music_name = video_file.stem.replace('_youtube', '')
            music_file = None
            for ext in ['.mp3', '.wav', '.m4a']:
                potential = Path(music_dir) / f"{music_name}{ext}"
                if potential.exists():
                    music_file = potential
                    break
            
            if music_file:
                metadata = get_music_metadata(music_file)
            else:
                metadata = get_music_metadata(video_file)
        else:
            metadata = get_music_metadata(video_file)
        
        # Video yükle
        video_id = upload_video_to_youtube(
            service,
            str(video_file),
            metadata['title'],
            metadata['description'],
            metadata['tags'],
            category_id=category_id,
            privacy_status=privacy_status,
            for_kids=False,  # Çocuklara özel değil
            video_language=metadata.get('video_language', 'en'),
            audio_language=metadata.get('audio_language', 'en'),
            check_duplicate=True
        )
        
        if video_id:
            results.append({
                'video_file': str(video_file),
                'video_id': video_id,
                'title': metadata['title']
            })
        print()
    
    print(f"[SUCCESS] Uploaded {len(results)}/{len(video_files)} videos")
    return results

def main():
    parser = argparse.ArgumentParser(
        description='YouTube API ile Otomatik Video Yükleme',
        epilog='Örnek: python src/youtube_upload.py --video output/youtube/video.mp4 --title "My Song"'
    )
    parser.add_argument('--video', type=str, default=None,
                       help='Tek video dosyası yükle')
    parser.add_argument('--video-dir', type=str, default=None,
                       help='Klasördeki tüm videoları yükle')
    parser.add_argument('--title', type=str, default=None,
                       help='Video başlığı (tek video için)')
    parser.add_argument('--description', type=str, default=None,
                       help='Video açıklaması (tek video için)')
    parser.add_argument('--tags', type=str, default=None,
                       help='Video etiketleri (virgülle ayrılmış)')
    parser.add_argument('--privacy', type=str, default='private',
                       choices=['private', 'unlisted', 'public'],
                       help='Gizlilik durumu (default: private)')
    parser.add_argument('--category', type=str, default='10',
                       help='Video kategorisi (10=Music, default: 10)')
    parser.add_argument('--music-dir', type=str, default=None,
                       help='Müzik dosyaları klasörü (metadata için)')
    parser.add_argument('--credentials', type=str, default='credentials.json',
                       help='Google Cloud credentials dosyası')
    parser.add_argument('--token', type=str, default='token.json',
                       help='Token cache dosyası')
    
    args = parser.parse_args()
    
    # YouTube API authentication
    print("[AUTH] Authenticating with YouTube API...")
    service = authenticate_youtube(args.credentials, args.token)
    if not service:
        return
    
    print("[SUCCESS] Authenticated!")
    print()
    
    # Tek video yükle
    if args.video:
        if not os.path.exists(args.video):
            print(f"[ERROR] Video file not found: {args.video}")
            return
        
        title = args.title or Path(args.video).stem
        description = args.description or f"🎵 {title}\n\nAI-generated music by Neural Beats Studio"
        tags = args.tags.split(',') if args.tags else ['AI Music', 'Neural Beats Studio']
        
        upload_video_to_youtube(
            service,
            args.video,
            title,
            description,
            tags,
            category_id=args.category,
            privacy_status=args.privacy
        )
    
    # Toplu yükleme
    elif args.video_dir:
        batch_upload_to_youtube(
            service,
            args.video_dir,
            music_dir=args.music_dir,
            privacy_status=args.privacy,
            category_id=args.category
        )
    
    else:
        parser.error("Either --video or --video-dir must be specified")

if __name__ == '__main__':
    main()

