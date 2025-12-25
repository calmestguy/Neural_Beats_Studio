"""
Ready Player Me Entegrasyonu - Tam Vücut 3D Avatar
"""

import os
import sys
import requests
import argparse

# Windows konsol encoding sorununu çöz
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_avatar(api_key, gender="female", body_type="fullbody", 
                 hair_color="blonde", hair_style="long_wavy"):
    """
    Ready Player Me ile tam vücut avatar oluşturur
    
    Args:
        api_key: Ready Player Me API key
        gender: "female" veya "male"
        body_type: "fullbody" (tam vücut)
        hair_color: Saç rengi ("blonde", "brunette", "black", "red")
        hair_style: Saç stili ("long_wavy", "short", "curly", vb.)
    """
    print("[AVATAR] Creating full-body avatar with Ready Player Me...")
    
    url = "https://api.readyplayer.me/v1/avatars"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "gender": gender,
        "bodyType": body_type,
        "assets": {
            "hair": {
                "color": hair_color,
                "style": hair_style
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        avatar_id = result.get('id')
        avatar_url = result.get('url')
        
        print(f"[SUCCESS] Avatar created!")
        print(f"   Avatar ID: {avatar_id}")
        print(f"   Avatar URL: {avatar_url}")
        return avatar_id, avatar_url
    else:
        print(f"[ERROR] Avatar creation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None, None

def get_avatar_glb(avatar_id, api_key):
    """
    Avatar'ın 3D modelini (GLB formatında) alır
    """
    url = f"https://api.readyplayer.me/v1/avatars/{avatar_id}.glb"
    headers = {"X-API-KEY": api_key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        output_file = f"assets/avatar_{avatar_id}.glb"
        os.makedirs("assets", exist_ok=True)
        
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f"[SUCCESS] Avatar 3D model saved: {output_file}")
        return output_file
    else:
        print(f"[ERROR] Failed to get avatar model: {response.status_code}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Ready Player Me Tam Vücut Avatar Oluşturucu',
        epilog='Örnek: python src/ready_player_me_integration.py --gender female --hair-color blonde'
    )
    parser.add_argument('--api-key', type=str, default=None,
                       help='Ready Player Me API key (veya READY_PLAYER_ME_API_KEY env)')
    parser.add_argument('--gender', type=str, default='female',
                       choices=['female', 'male'],
                       help='Cinsiyet')
    parser.add_argument('--hair-color', type=str, default='blonde',
                       choices=['blonde', 'brunette', 'black', 'red', 'brown'],
                       help='Saç rengi')
    parser.add_argument('--hair-style', type=str, default='long_wavy',
                       help='Saç stili')
    parser.add_argument('--download-model', action='store_true',
                       help='3D modeli (GLB) indir')
    
    args = parser.parse_args()
    
    # API key
    api_key = args.api_key or os.getenv('READY_PLAYER_ME_API_KEY')
    if not api_key:
        parser.error("Ready Player Me API key required!")
    
    # Avatar oluştur
    avatar_id, avatar_url = create_avatar(
        api_key,
        args.gender,
        "fullbody",
        args.hair_color,
        args.hair_style
    )
    
    if avatar_id and args.download_model:
        get_avatar_glb(avatar_id, api_key)

if __name__ == '__main__':
    main()

