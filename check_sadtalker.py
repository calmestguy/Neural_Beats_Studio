"""SadTalker kurulum durumu kontrolü"""
import sys

print("="*60)
print("SADTALKER KURULUM DURUMU")
print("="*60)
print()

packages = [
    "face_alignment",
    "kornia", 
    "imageio",
    "librosa",
    "scipy",
    "basicsr",
    "facexlib",
    "gradio",
    "gfpgan"
]

installed = []
missing = []

for pkg in packages:
    try:
        __import__(pkg)
        installed.append(pkg)
        print(f"[OK] {pkg}")
    except ImportError:
        missing.append(pkg)
        print(f"[BEKLENIYOR] {pkg}")

print()
print("="*60)
print(f"Kurulu: {len(installed)}/{len(packages)}")
print(f"Eksik: {len(missing)}/{len(packages)}")
print("="*60)

if len(missing) > 0:
    print("\n[INFO] Kurulum devam ediyor...")
    print("       Arka planda pip install calisiyor.")
    print("       Biraz bekleyin ve tekrar kontrol edin.")
else:
    print("\n[SUCCESS] Tum paketler kurulu!")
    print("         Simdi modelleri indirmeniz gerekiyor.")


