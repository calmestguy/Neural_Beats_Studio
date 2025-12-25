"""
Sosyal Medya Platformları için Upload Modülleri
Instagram, Facebook, TikTok, Spotify API entegrasyonları
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Tuple

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        elif hasattr(sys.stdout, 'buffer'):
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except (AttributeError, TypeError, ValueError):
        pass

class InstagramUploader:
    """
    Instagram Graph API ile video yükleme
    Facebook Graph API üzerinden Instagram'a erişim
    """
    
    # Instagram video gereksinimleri
    REELS_SPECS = {
        'format': ['mp4', 'mov'],
        'resolution': (1080, 1920),  # 9:16 aspect ratio
        'max_duration': 90,  # seconds
        'max_size_mb': 100
    }
    
    POST_SPECS = {
        'format': ['mp4', 'mov'],
        'resolution': (1080, 1080),  # 1:1 aspect ratio
        'max_duration': 60,  # seconds
        'max_size_mb': 100
    }
    
    def __init__(self, access_token: str, instagram_account_id: str):
        """
        Args:
            access_token: Facebook/Instagram Graph API access token
            instagram_account_id: Instagram Business Account ID
        """
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def upload_reel(self, video_file: str, caption: str, 
                   thumbnail_url: Optional[str] = None) -> Optional[str]:
        """
        Instagram Reels yükle
        
        Args:
            video_file: Video dosyası yolu
            caption: Video açıklaması
            thumbnail_url: Thumbnail URL (opsiyonel)
        
        Returns:
            Media container ID if successful, None otherwise
        """
        if not os.path.exists(video_file):
            print(f"[INSTAGRAM] Video dosyası bulunamadı: {video_file}")
            return None
        
        # Video format kontrolü
        if not self._check_video_format(video_file, self.REELS_SPECS):
            print(f"[INSTAGRAM] Video formatı uygun değil (Reels: 1080x1920, MP4/MOV)")
            return None
        
        try:
            # 1. Adım: Video yükle
            upload_url = f"{self.base_url}/{self.instagram_account_id}/media"
            
            with open(video_file, 'rb') as video:
                files = {'video_file': video}
                data = {
                    'media_type': 'REELS',
                    'caption': caption,
                    'access_token': self.access_token
                }
                if thumbnail_url:
                    data['cover_url'] = thumbnail_url
                
                response = requests.post(upload_url, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                
                if 'id' in result:
                    container_id = result['id']
                    print(f"[INSTAGRAM] Video yüklendi! Container ID: {container_id}")
                    
                    # 2. Adım: Publish
                    publish_url = f"{self.base_url}/{self.instagram_account_id}/media_publish"
                    publish_data = {
                        'creation_id': container_id,
                        'access_token': self.access_token
                    }
                    
                    publish_response = requests.post(publish_url, data=publish_data)
                    publish_response.raise_for_status()
                    publish_result = publish_response.json()
                    
                    if 'id' in publish_result:
                        reel_id = publish_result['id']
                        print(f"[INSTAGRAM] Reel yayınlandı! Reel ID: {reel_id}")
                        return reel_id
                
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[INSTAGRAM] Hata: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"[INSTAGRAM] API Hatası: {error_data}")
                except:
                    pass
            return None
    
    def _check_video_format(self, video_file: str, specs: Dict) -> bool:
        """Video format kontrolü (basit)"""
        ext = Path(video_file).suffix.lower().lstrip('.')
        return ext in specs['format']
    
    @staticmethod
    def get_required_permissions() -> list:
        """Gerekli Facebook API izinleri"""
        return [
            'instagram_basic',
            'instagram_content_publish',
            'pages_read_engagement',
            'pages_show_list'
        ]


class FacebookUploader:
    """
    Facebook Graph API ile video yükleme
    """
    
    # Facebook video gereksinimleri
    VIDEO_SPECS = {
        'format': ['mp4', 'mov'],
        'resolution': (1280, 720),  # 16:9 aspect ratio (minimum)
        'max_duration': 240,  # seconds (4 minutes)
        'max_size_mb': 1024  # 1 GB
    }
    
    def __init__(self, access_token: str, page_id: Optional[str] = None):
        """
        Args:
            access_token: Facebook Graph API access token
            page_id: Facebook Page ID (opsiyonel, kullanıcı için None)
        """
        self.access_token = access_token
        self.page_id = page_id
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def upload_video(self, video_file: str, title: str, description: str,
                    privacy: str = 'PUBLIC') -> Optional[str]:
        """
        Facebook'a video yükle
        
        Args:
            video_file: Video dosyası yolu
            title: Video başlığı
            description: Video açıklaması
            privacy: Gizlilik durumu (PUBLIC, FRIENDS, etc.)
        
        Returns:
            Video ID if successful, None otherwise
        """
        if not os.path.exists(video_file):
            print(f"[FACEBOOK] Video dosyası bulunamadı: {video_file}")
            return None
        
        # Video format kontrolü
        if not self._check_video_format(video_file, self.VIDEO_SPECS):
            print(f"[FACEBOOK] Video formatı uygun değil (MP4/MOV, min 1280x720)")
            return None
        
        try:
            # Upload endpoint
            if self.page_id:
                upload_url = f"{self.base_url}/{self.page_id}/videos"
            else:
                upload_url = f"{self.base_url}/me/videos"
            
            with open(video_file, 'rb') as video:
                files = {'source': video}
                data = {
                    'title': title,
                    'description': description,
                    'privacy': {'value': privacy},
                    'access_token': self.access_token
                }
                
                response = requests.post(upload_url, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                
                if 'id' in result:
                    video_id = result['id']
                    print(f"[FACEBOOK] Video yüklendi! Video ID: {video_id}")
                    return video_id
                
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[FACEBOOK] Hata: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"[FACEBOOK] API Hatası: {error_data}")
                except:
                    pass
            return None
    
    def _check_video_format(self, video_file: str, specs: Dict) -> bool:
        """Video format kontrolü"""
        ext = Path(video_file).suffix.lower().lstrip('.')
        return ext in specs['format']
    
    @staticmethod
    def get_required_permissions() -> list:
        """Gerekli Facebook API izinleri"""
        return [
            'pages_manage_posts',
            'pages_read_engagement',
            'pages_show_list',
            'user_videos'
        ]


class TikTokUploader:
    """
    TikTok Creative API ile video yükleme
    """
    
    # TikTok video gereksinimleri
    VIDEO_SPECS = {
        'format': ['mp4', 'mov'],
        'resolution': (1080, 1920),  # 9:16 aspect ratio
        'max_duration': 60,  # seconds (60 saniye, bazı hesaplar için daha uzun)
        'max_size_mb': 287  # ~287 MB
    }
    
    def __init__(self, access_token: str, app_id: str, app_secret: str):
        """
        Args:
            access_token: TikTok Creative API access token
            app_id: TikTok App ID
            app_secret: TikTok App Secret
        """
        self.access_token = access_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open-api.tiktok.com"
    
    def upload_video(self, video_file: str, title: str, description: str,
                    privacy_level: str = 'PUBLIC_TO_EVERYONE') -> Optional[str]:
        """
        TikTok'a video yükle
        
        Args:
            video_file: Video dosyası yolu
            title: Video başlığı
            description: Video açıklaması
            privacy_level: Gizlilik seviyesi
        
        Returns:
            Video ID if successful, None otherwise
        """
        if not os.path.exists(video_file):
            print(f"[TIKTOK] Video dosyası bulunamadı: {video_file}")
            return None
        
        # Video format kontrolü
        if not self._check_video_format(video_file, self.VIDEO_SPECS):
            print(f"[TIKTOK] Video formatı uygun değil (1080x1920, MP4/MOV)")
            return None
        
        try:
            # 1. Adım: Video yükleme URL'i al
            init_url = f"{self.base_url}/share/video/upload/"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            init_data = {
                'source_info': {
                    'source': 'FILE_UPLOAD'
                },
                'post_info': {
                    'title': title,
                    'description': description,
                    'privacy_level': privacy_level,
                    'disable_duet': False,
                    'disable_comment': False,
                    'disable_stitch': False
                }
            }
            
            init_response = requests.post(init_url, json=init_data, headers=headers)
            init_response.raise_for_status()
            init_result = init_response.json()
            
            if 'data' in init_result and 'upload_url' in init_result['data']:
                upload_url = init_result['data']['upload_url']
                publish_id = init_result['data'].get('publish_id')
                
                # 2. Adım: Video dosyasını yükle
                with open(video_file, 'rb') as video:
                    upload_response = requests.put(upload_url, data=video)
                    upload_response.raise_for_status()
                
                # 3. Adım: Yayınla
                if publish_id:
                    publish_url = f"{self.base_url}/share/video/publish/"
                    publish_data = {
                        'publish_id': publish_id
                    }
                    
                    publish_response = requests.post(
                        publish_url, json=publish_data, headers=headers
                    )
                    publish_response.raise_for_status()
                    publish_result = publish_response.json()
                    
                    if 'data' in publish_result and 'share_id' in publish_result['data']:
                        video_id = publish_result['data']['share_id']
                        print(f"[TIKTOK] Video yüklendi! Video ID: {video_id}")
                        return video_id
                
                return None
            else:
                print(f"[TIKTOK] Upload URL alınamadı: {init_result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"[TIKTOK] Hata: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"[TIKTOK] API Hatası: {error_data}")
                except:
                    pass
            return None
    
    def _check_video_format(self, video_file: str, specs: Dict) -> bool:
        """Video format kontrolü"""
        ext = Path(video_file).suffix.lower().lstrip('.')
        return ext in specs['format']
    
    @staticmethod
    def get_required_permissions() -> list:
        """Gerekli TikTok API izinleri"""
        return [
            'video.upload',
            'video.publish'
        ]


class SpotifyUploader:
    """
    Spotify for Creators API ile podcast video yükleme
    Not: Spotify müzik yükleme için farklı bir süreç gerektirir (distributor gerekli)
    """
    
    # Spotify podcast video gereksinimleri
    PODCAST_VIDEO_SPECS = {
        'format': ['mp4', 'mov'],
        'resolution': (1920, 1080),  # 16:9 aspect ratio
        'max_duration': 3600,  # seconds (1 hour)
        'max_size_mb': 500
    }
    
    def __init__(self, access_token: str):
        """
        Args:
            access_token: Spotify API access token
        """
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1"
    
    def upload_podcast_video(self, video_file: str, episode_id: str,
                             title: str, description: str) -> bool:
        """
        Spotify podcast episode'una video ekle
        
        Args:
            video_file: Video dosyası yolu
            episode_id: Podcast episode ID
            title: Video başlığı
            description: Video açıklaması
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(video_file):
            print(f"[SPOTIFY] Video dosyası bulunamadı: {video_file}")
            return False
        
        # Video format kontrolü
        if not self._check_video_format(video_file, self.PODCAST_VIDEO_SPECS):
            print(f"[SPOTIFY] Video formatı uygun değil (MP4/MOV, 1920x1080)")
            return False
        
        try:
            # Spotify podcast video yükleme endpoint'i
            upload_url = f"{self.base_url}/episodes/{episode_id}/video"
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'video/mp4'
            }
            
            with open(video_file, 'rb') as video:
                response = requests.post(upload_url, data=video, headers=headers)
                response.raise_for_status()
                
                print(f"[SPOTIFY] Video yüklendi! Episode ID: {episode_id}")
                return True
                
        except requests.exceptions.RequestException as e:
            print(f"[SPOTIFY] Hata: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"[SPOTIFY] API Hatası: {error_data}")
                except:
                    pass
            return False
    
    def _check_video_format(self, video_file: str, specs: Dict) -> bool:
        """Video format kontrolü"""
        ext = Path(video_file).suffix.lower().lstrip('.')
        return ext in specs['format']
    
    @staticmethod
    def get_required_permissions() -> list:
        """Gerekli Spotify API izinleri"""
        return [
            'user-read-email',
            'user-library-read',
            'user-library-modify',
            'user-modify-playback-state'
        ]
    
    @staticmethod
    def note_about_music_upload():
        """
        Önemli Not: Spotify'a müzik yüklemek için:
        - Spotify for Artists hesabı gerekir
        - Müzik distributor (DistroKid, CD Baby, vb.) gerekir
        - Doğrudan API ile müzik yükleme mümkün değil
        """
        return """
        ⚠️ SPOTIFY MÜZİK YÜKLEME NOTU:
        
        Spotify'a müzik yüklemek için doğrudan API desteği yoktur.
        Bunun yerine bir müzik distributor kullanmanız gerekir:
        
        1. DistroKid (https://distrokid.com/)
        2. CD Baby (https://cdbaby.com/)
        3. TuneCore (https://www.tunecore.com/)
        4. Ditto Music (https://www.dittomusic.com/)
        
        Bu distributor'lar Spotify, Apple Music, Amazon Music gibi
        platformlara otomatik olarak müzik dağıtır.
        """


def get_platform_specs(platform: str) -> Dict:
    """
    Platform video gereksinimlerini döndür
    
    Args:
        platform: Platform adı (instagram, facebook, tiktok, spotify)
    
    Returns:
        Platform video gereksinimleri dict
    """
    specs = {
        'instagram': {
            'reels': InstagramUploader.REELS_SPECS,
            'post': InstagramUploader.POST_SPECS
        },
        'facebook': {
            'video': FacebookUploader.VIDEO_SPECS
        },
        'tiktok': {
            'video': TikTokUploader.VIDEO_SPECS
        },
        'spotify': {
            'podcast': SpotifyUploader.PODCAST_VIDEO_SPECS
        }
    }
    
    return specs.get(platform.lower(), {})

