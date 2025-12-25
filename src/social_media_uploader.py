"""
Sosyal Medya Otomatik Yükleme Masa Üstü Uygulaması
YouTube, Instagram, Facebook, TikTok, Spotify için otomatik içerik yükleme
Futuristik Koyu Tema ile Modern UI
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
from pathlib import Path
import threading
import json
from datetime import datetime
import io
import contextlib

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

# Futuristik Koyu Tema Renkleri
THEME = {
    'bg_primary': '#0a0e27',      # Koyu lacivert (ana arka plan)
    'bg_secondary': '#141b2d',    # Biraz daha açık (paneller)
    'bg_tertiary': '#1a2332',    # Daha açık (input alanları)
    'accent_primary': '#00d4ff',  # Neon cyan (vurgu)
    'accent_secondary': '#7b2cbf', # Mor (ikincil vurgu)
    'accent_tertiary': '#ff006e', # Pembe (üçüncül vurgu)
    'text_primary': '#ffffff',    # Beyaz (ana metin)
    'text_secondary': '#b8c5d6',  # Açık gri (ikincil metin)
    'text_muted': '#6b7a8f',      # Gri (soluk metin)
    'success': '#00ff88',         # Yeşil (başarı)
    'warning': '#ffaa00',         # Turuncu (uyarı)
    'error': '#ff3366',           # Kırmızı (hata)
    'border': '#2a3441',          # Kenarlık
    'hover': '#1e2a3a',           # Hover efekti
}

# YouTube upload modülünü import et
try:
    import sys
    from pathlib import Path
    # src klasörünü path'e ekle
    src_path = Path(__file__).parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    from youtube_upload import authenticate_youtube, get_music_metadata, upload_video_to_youtube, is_video_already_uploaded
except ImportError as e:
    print(f"[WARNING] YouTube upload module not found: {e}")

# Platform uploader modüllerini import et
try:
    from platform_uploaders import (
        InstagramUploader, FacebookUploader, TikTokUploader, SpotifyUploader,
        get_platform_specs
    )
    PLATFORM_UPLOADERS_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Platform uploaders not found: {e}")
    PLATFORM_UPLOADERS_AVAILABLE = False

# Video oluşturma modülünü import et
try:
    from create_youtube_video import create_youtube_video
    CREATE_VIDEO_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] create_youtube_video module not found: {e}")
    CREATE_VIDEO_AVAILABLE = False
    create_youtube_video = None

class ModernButton(tk.Canvas):
    """Futuristik buton widget'ı"""
    def __init__(self, parent, text, command, width=200, height=40, 
                 bg_color=THEME['accent_primary'], hover_color=THEME['accent_secondary'],
                 text_color=THEME['text_primary'], font_size=11):
        super().__init__(parent, width=width, height=height, 
                        bg=THEME['bg_secondary'], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
        # Buton arka planı
        self.create_rectangle(2, 2, width-2, height-2, 
                             fill=bg_color, outline=bg_color, width=0, tags='bg')
        
        # Buton metni
        self.create_text(width//2, height//2, text=text, 
                        fill=text_color, font=('Segoe UI', font_size, 'bold'),
                        tags='text')
        
        # Event bindings
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
    
    def on_enter(self, event):
        self.is_hovered = True
        self.itemconfig('bg', fill=self.hover_color, outline=self.hover_color)
        self.config(cursor='hand2')
    
    def on_leave(self, event):
        self.is_hovered = False
        self.itemconfig('bg', fill=self.bg_color, outline=self.bg_color)
        self.config(cursor='')
    
    def on_click(self, event):
        self.itemconfig('bg', fill=THEME['bg_tertiary'])
    
    def on_release(self, event):
        if self.is_hovered:
            self.itemconfig('bg', fill=self.hover_color)
        else:
            self.itemconfig('bg', fill=self.bg_color)
        if self.command:
            self.command()

class SocialMediaUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neural Beats Studio - Social Media Uploader")
        self.root.geometry("1100x800")
        self.root.configure(bg=THEME['bg_primary'])
        
        # Seçili dosyalar
        self.selected_music_file = None
        self.selected_image_file = None
        self.selected_video_file = None
        
        # YouTube service
        self.youtube_service = None
        
        # Platform uploader instance'ları
        self.instagram_uploader = None
        self.facebook_uploader = None
        self.tiktok_uploader = None
        self.spotify_uploader = None
        
        # Tema stilini ayarla
        self.setup_theme()
        
        self.create_widgets()
    
    def setup_theme(self):
        """Modern koyu tema stilini ayarla"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame stilleri
        style.configure('Dark.TFrame', background=THEME['bg_primary'])
        style.configure('Panel.TFrame', background=THEME['bg_secondary'], 
                       relief='flat', borderwidth=0)
        
        # Label stilleri
        style.configure('Title.TLabel', background=THEME['bg_primary'], 
                       foreground=THEME['text_primary'], 
                       font=('Segoe UI', 20, 'bold'))
        style.configure('Subtitle.TLabel', background=THEME['bg_secondary'], 
                      foreground=THEME['text_secondary'], 
                      font=('Segoe UI', 10))
        style.configure('Dark.TLabel', background=THEME['bg_secondary'], 
                       foreground=THEME['text_primary'], 
                       font=('Segoe UI', 9))
        style.configure('Muted.TLabel', background=THEME['bg_secondary'], 
                       foreground=THEME['text_muted'], 
                       font=('Segoe UI', 8))
        
        # Entry stilleri
        style.configure('Dark.TEntry', fieldbackground=THEME['bg_tertiary'], 
                       foreground=THEME['text_primary'], 
                       borderwidth=1, relief='solid',
                       bordercolor=THEME['border'], insertcolor=THEME['accent_primary'])
        
        # Combobox stilleri
        style.configure('Dark.TCombobox', fieldbackground=THEME['bg_tertiary'], 
                       foreground=THEME['text_primary'], 
                       borderwidth=1, relief='solid',
                       bordercolor=THEME['border'])
        
        # Checkbutton stilleri
        style.configure('Dark.TCheckbutton', background=THEME['bg_secondary'], 
                       foreground=THEME['text_primary'], 
                       font=('Segoe UI', 9),
                       focuscolor='none')
        
        # Notebook stilleri
        style.configure('Dark.TNotebook', background=THEME['bg_primary'], 
                       borderwidth=0)
        style.configure('Dark.TNotebook.Tab', background=THEME['bg_secondary'], 
                       foreground=THEME['text_secondary'], 
                       padding=[20, 10], font=('Segoe UI', 9))
        style.map('Dark.TNotebook.Tab', 
                 background=[('selected', THEME['accent_primary'])],
                 foreground=[('selected', THEME['text_primary'])])
        
        # Progressbar stilleri
        style.configure('Dark.Horizontal.TProgressbar', 
                       background=THEME['accent_primary'], 
                       troughcolor=THEME['bg_tertiary'],
                       borderwidth=0, lightcolor=THEME['accent_primary'],
                       darkcolor=THEME['accent_primary'])
        
    def create_widgets(self):
        # Ana container (Canvas ile gradient efekti için)
        self.main_canvas = tk.Canvas(self.root, bg=THEME['bg_primary'], 
                                     highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", 
                                 command=self.main_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ana frame
        main_frame = ttk.Frame(self.main_canvas, style='Dark.TFrame')
        self.main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Başlık bölümü (gradient efekti simülasyonu)
        header_frame = tk.Canvas(main_frame, height=120, bg=THEME['bg_primary'], 
                                highlightthickness=0)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Başlık gradient arka planı
        header_frame.create_rectangle(0, 0, 1100, 120, 
                                     fill=THEME['bg_secondary'], outline='', tags='header_bg')
        
        # Başlık metni (neon efekti)
        title_label = header_frame.create_text(550, 40, 
                                              text="NEURAL BEATS STUDIO", 
                                              font=('Segoe UI', 28, 'bold'),
                                              fill=THEME['accent_primary'],
                                              tags='title')
        
        # Alt başlık
        subtitle_label = header_frame.create_text(550, 75, 
                                                text="Social Media Uploader • AI-Powered Content Distribution", 
                                                font=('Segoe UI', 11),
                                                fill=THEME['text_secondary'],
                                                tags='subtitle')
        
        # Dekoratif çizgiler
        header_frame.create_line(50, 100, 1050, 100, 
                                fill=THEME['accent_primary'], width=2, tags='line1')
        header_frame.create_line(50, 103, 1050, 103, 
                                fill=THEME['accent_secondary'], width=1, tags='line2')
        
        # Dosya seçimi bölümü - Modern Panel
        file_panel = tk.Canvas(main_frame, bg=THEME['bg_secondary'], 
                              highlightthickness=0, relief='flat')
        file_panel.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Panel başlığı
        file_title = tk.Label(file_panel, text="📁 DOSYA SEÇİMİ", 
                             bg=THEME['bg_secondary'], fg=THEME['accent_primary'],
                             font=('Segoe UI', 12, 'bold'))
        file_title.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Dosya seçim container
        file_container = ttk.Frame(file_panel, style='Panel.TFrame')
        file_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Müzik dosyası - Modern card
        music_card = tk.Frame(file_container, bg=THEME['bg_tertiary'], 
                            relief='flat', bd=0)
        music_card.pack(fill=tk.X, pady=8)
        
        ttk.Label(music_card, text="🎵 Müzik Dosyası", 
                 style='Dark.TLabel').pack(side=tk.LEFT, padx=15, pady=12)
        self.music_path_label = tk.Label(music_card, text="Seçilmedi", 
                                         bg=THEME['bg_tertiary'], 
                                         fg=THEME['text_muted'],
                                         font=('Segoe UI', 9))
        self.music_path_label.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        ModernButton(music_card, "Seç", self.select_music_file, 
                   width=80, height=32, bg_color=THEME['accent_primary'],
                   hover_color=THEME['accent_secondary']).pack(side=tk.RIGHT, padx=15)
        
        # Görsel dosyası - Modern card
        image_card = tk.Frame(file_container, bg=THEME['bg_tertiary'], 
                             relief='flat', bd=0)
        image_card.pack(fill=tk.X, pady=8)
        
        ttk.Label(image_card, text="🖼️ Görsel Dosyası", 
                 style='Dark.TLabel').pack(side=tk.LEFT, padx=15, pady=12)
        self.image_path_label = tk.Label(image_card, text="Seçilmedi", 
                                         bg=THEME['bg_tertiary'], 
                                         fg=THEME['text_muted'],
                                         font=('Segoe UI', 9))
        self.image_path_label.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        ModernButton(image_card, "Seç", self.select_image_file, 
                   width=80, height=32, bg_color=THEME['accent_primary'],
                   hover_color=THEME['accent_secondary']).pack(side=tk.RIGHT, padx=15)
        
        # Video dosyası - Modern card
        video_card = tk.Frame(file_container, bg=THEME['bg_tertiary'], 
                             relief='flat', bd=0)
        video_card.pack(fill=tk.X, pady=8)
        
        ttk.Label(video_card, text="🎬 Video Dosyası (Opsiyonel)", 
                 style='Dark.TLabel').pack(side=tk.LEFT, padx=15, pady=12)
        self.video_path_label = tk.Label(video_card, text="Seçilmedi", 
                                         bg=THEME['bg_tertiary'], 
                                         fg=THEME['text_muted'],
                                         font=('Segoe UI', 9))
        self.video_path_label.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        ModernButton(video_card, "Seç", self.select_video_file, 
                   width=80, height=32, bg_color=THEME['accent_primary'],
                   hover_color=THEME['accent_secondary']).pack(side=tk.RIGHT, padx=15)
        
        # Metadata bölümü - Modern Panel
        metadata_panel = tk.Canvas(main_frame, bg=THEME['bg_secondary'], 
                                 highlightthickness=0, relief='flat')
        metadata_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Panel başlığı
        meta_title = tk.Label(metadata_panel, text="📝 METADATA", 
                             bg=THEME['bg_secondary'], fg=THEME['accent_primary'],
                             font=('Segoe UI', 12, 'bold'))
        meta_title.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Metadata container
        meta_container = ttk.Frame(metadata_panel, style='Panel.TFrame')
        meta_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Başlık
        ttk.Label(meta_container, text="Başlık:", style='Dark.TLabel').pack(anchor=tk.W, padx=15, pady=(10, 5))
        self.title_entry = ttk.Entry(meta_container, style='Dark.TEntry', font=('Segoe UI', 10))
        self.title_entry.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Açıklama
        ttk.Label(meta_container, text="Açıklama:", style='Dark.TLabel').pack(anchor=tk.W, padx=15, pady=(5, 5))
        desc_frame = tk.Frame(meta_container, bg=THEME['bg_tertiary'])
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        self.description_text = scrolledtext.ScrolledText(desc_frame, height=5, 
                                                          bg=THEME['bg_tertiary'],
                                                          fg=THEME['text_primary'],
                                                          insertbackground=THEME['accent_primary'],
                                                          font=('Segoe UI', 9),
                                                          relief='flat', bd=1,
                                                          highlightthickness=1,
                                                          highlightbackground=THEME['border'],
                                                          highlightcolor=THEME['accent_primary'])
        self.description_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tür/Genre
        ttk.Label(meta_container, text="Tür/Genre:", style='Dark.TLabel').pack(anchor=tk.W, padx=15, pady=(5, 5))
        self.genre_entry = ttk.Entry(meta_container, style='Dark.TEntry', font=('Segoe UI', 10))
        self.genre_entry.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Etiketler
        ttk.Label(meta_container, text="Etiketler (virgülle ayırın):", style='Dark.TLabel').pack(anchor=tk.W, padx=15, pady=(5, 5))
        self.tags_entry = ttk.Entry(meta_container, style='Dark.TEntry', font=('Segoe UI', 10))
        self.tags_entry.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # Platform seçimi - Modern Panel
        platform_panel = tk.Canvas(main_frame, bg=THEME['bg_secondary'], 
                                  highlightthickness=0, relief='flat')
        platform_panel.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Panel başlığı
        platform_title = tk.Label(platform_panel, text="🌐 PLATFORM SEÇİMİ", 
                                 bg=THEME['bg_secondary'], fg=THEME['accent_primary'],
                                 font=('Segoe UI', 12, 'bold'))
        platform_title.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Platform container
        platform_container = ttk.Frame(platform_panel, style='Panel.TFrame')
        platform_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.youtube_var = tk.BooleanVar(value=True)
        self.instagram_var = tk.BooleanVar()
        self.facebook_var = tk.BooleanVar()
        self.tiktok_var = tk.BooleanVar()
        self.spotify_var = tk.BooleanVar()
        
        # Platform checkboxes - Modern grid
        platforms_row1 = tk.Frame(platform_container, bg=THEME['bg_secondary'])
        platforms_row1.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Checkbutton(platforms_row1, text="▶️ YouTube", 
                       variable=self.youtube_var, style='Dark.TCheckbutton').pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(platforms_row1, text="📷 Instagram", 
                       variable=self.instagram_var, style='Dark.TCheckbutton').pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(platforms_row1, text="👥 Facebook", 
                       variable=self.facebook_var, style='Dark.TCheckbutton').pack(side=tk.LEFT, padx=15)
        
        platforms_row2 = tk.Frame(platform_container, bg=THEME['bg_secondary'])
        platforms_row2.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Checkbutton(platforms_row2, text="🎵 TikTok", 
                       variable=self.tiktok_var, style='Dark.TCheckbutton').pack(side=tk.LEFT, padx=15)
        ttk.Checkbutton(platforms_row2, text="🎧 Spotify", 
                       variable=self.spotify_var, style='Dark.TCheckbutton').pack(side=tk.LEFT, padx=15)
        
        # Ayarlar - Modern Panel
        settings_panel = tk.Canvas(main_frame, bg=THEME['bg_secondary'], 
                                  highlightthickness=0, relief='flat')
        settings_panel.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Panel başlığı
        settings_title = tk.Label(settings_panel, text="⚙️ AYARLAR", 
                                 bg=THEME['bg_secondary'], fg=THEME['accent_primary'],
                                 font=('Segoe UI', 12, 'bold'))
        settings_title.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Settings container
        settings_container = ttk.Frame(settings_panel, style='Panel.TFrame')
        settings_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Gizlilik durumu
        privacy_row = tk.Frame(settings_container, bg=THEME['bg_secondary'])
        privacy_row.pack(fill=tk.X, padx=15, pady=8)
        
        ttk.Label(privacy_row, text="🔒 Gizlilik:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.privacy_var = tk.StringVar(value="private")
        privacy_combo = ttk.Combobox(privacy_row, textvariable=self.privacy_var,
                                    values=["private", "unlisted", "public"], 
                                    state="readonly", width=15, style='Dark.TCombobox')
        privacy_combo.pack(side=tk.LEFT, padx=5)
        
        # Çocuklara özel değil
        self.made_for_kids_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(privacy_row, text="Made for Kids: No", 
                       variable=self.made_for_kids_var, style='Dark.TCheckbutton').pack(side=tk.LEFT, padx=20)
        
        # Duplicate kontrolü
        self.check_duplicate_var = tk.BooleanVar(value=True)
        duplicate_row = tk.Frame(settings_container, bg=THEME['bg_secondary'])
        duplicate_row.pack(fill=tk.X, padx=15, pady=8)
        ttk.Checkbutton(duplicate_row, text="🔄 Duplicate kontrolü (Aynı videoyu tekrar yükleme)", 
                       variable=self.check_duplicate_var, style='Dark.TCheckbutton').pack(side=tk.LEFT)
        
        # YouTube API durumu
        youtube_row = tk.Frame(settings_container, bg=THEME['bg_secondary'])
        youtube_row.pack(fill=tk.X, padx=15, pady=8)
        
        ttk.Label(youtube_row, text="▶️ YouTube API:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.youtube_status_label = tk.Label(youtube_row, text="❌ Bağlanmadı", 
                                            bg=THEME['bg_secondary'], fg=THEME['error'],
                                            font=('Segoe UI', 9, 'bold'))
        self.youtube_status_label.pack(side=tk.LEFT, padx=5)
        ModernButton(youtube_row, "Bağlan", self.connect_youtube, 
                    width=100, height=32, bg_color=THEME['accent_primary'],
                    hover_color=THEME['success']).pack(side=tk.LEFT, padx=10)
        
        # Platform API durumları
        if PLATFORM_UPLOADERS_AVAILABLE:
            platform_row = tk.Frame(settings_container, bg=THEME['bg_secondary'])
            platform_row.pack(fill=tk.X, padx=15, pady=8)
            
            ttk.Label(platform_row, text="🌐 Diğer Platformlar:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 10))
            self.platform_status_label = tk.Label(platform_row, 
                                                 text="⚠️ API credentials gerekli", 
                                                 bg=THEME['bg_secondary'], fg=THEME['warning'],
                                                 font=('Segoe UI', 9, 'bold'))
            self.platform_status_label.pack(side=tk.LEFT, padx=5)
            ModernButton(platform_row, "API Ayarları", self.open_platform_settings, 
                        width=130, height=32, bg_color=THEME['accent_secondary'],
                        hover_color=THEME['accent_tertiary']).pack(side=tk.LEFT, padx=10)
        
        # Platform uploader instance'ları
        self.instagram_uploader = None
        self.facebook_uploader = None
        self.tiktok_uploader = None
        self.spotify_uploader = None
        
        # Log alanı - Modern Panel
        log_panel = tk.Canvas(main_frame, bg=THEME['bg_secondary'], 
                             highlightthickness=0, relief='flat')
        log_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Panel başlığı
        log_title = tk.Label(log_panel, text="📊 LOG & İLERLEME", 
                            bg=THEME['bg_secondary'], fg=THEME['accent_primary'],
                            font=('Segoe UI', 12, 'bold'))
        log_title.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Progress bar
        progress_container = tk.Frame(log_panel, bg=THEME['bg_secondary'])
        progress_container.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="⚡ Hazır")
        progress_label = tk.Label(progress_container, textvariable=self.progress_var,
                                 bg=THEME['bg_secondary'], fg=THEME['text_primary'],
                                 font=('Segoe UI', 10, 'bold'))
        progress_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_container, mode='indeterminate',
                                           style='Dark.Horizontal.TProgressbar',
                                           length=1050)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Log text area
        log_container = tk.Frame(log_panel, bg=THEME['bg_tertiary'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.log_text = scrolledtext.ScrolledText(log_container, height=12,
                                                 bg=THEME['bg_tertiary'],
                                                 fg=THEME['text_primary'],
                                                 insertbackground=THEME['accent_primary'],
                                                 font=('Consolas', 9),
                                                 relief='flat', bd=1,
                                                 highlightthickness=1,
                                                 highlightbackground=THEME['border'],
                                                 highlightcolor=THEME['accent_primary'])
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Butonlar - Modern Action Bar
        button_panel = tk.Frame(main_frame, bg=THEME['bg_primary'])
        button_panel.pack(fill=tk.X, padx=20, pady=20)
        
        button_container = tk.Frame(button_panel, bg=THEME['bg_primary'])
        button_container.pack()
        
        ModernButton(button_container, "📥 Metadata'yı Doldur", 
                    self.fill_metadata_from_music, 
                    width=200, height=45, 
                    bg_color=THEME['accent_secondary'],
                    hover_color=THEME['accent_tertiary']).pack(side=tk.LEFT, padx=10)
        
        ModernButton(button_container, "🚀 YÜKLE", 
                    self.start_upload, 
                    width=220, height=50, font_size=13,
                    bg_color=THEME['accent_primary'],
                    hover_color=THEME['success']).pack(side=tk.LEFT, padx=10)
        
        ModernButton(button_container, "🗑️ Temizle", 
                    self.clear_all, 
                    width=150, height=45,
                    bg_color=THEME['bg_tertiary'],
                    hover_color=THEME['error'],
                    text_color=THEME['text_secondary']).pack(side=tk.LEFT, padx=10)
        
        # Scroll region güncelleme
        main_frame.update_idletasks()
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        
        # Mouse wheel binding
        def on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.main_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
    def log(self, message):
        """Log mesajı ekle"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def select_music_file(self):
        """Müzik dosyası seç"""
        file = filedialog.askopenfilename(
            title="Müzik Dosyası Seç",
            filetypes=[("Audio files", "*.mp3 *.wav *.m4a"), ("All files", "*.*")]
        )
        if file:
            self.selected_music_file = file
            self.music_path_label.config(text=Path(file).name, fg=THEME['success'])
            self.log(f"Müzik dosyası seçildi: {Path(file).name}")
            
    def select_image_file(self):
        """Görsel dosyası seç"""
        file = filedialog.askopenfilename(
            title="Görsel Dosyası Seç",
            filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        if file:
            self.selected_image_file = file
            self.image_path_label.config(text=Path(file).name, fg=THEME['success'])
            self.log(f"Görsel dosyası seçildi: {Path(file).name}")
            
    def select_video_file(self):
        """Video dosyası seç"""
        file = filedialog.askopenfilename(
            title="Video Dosyası Seç",
            filetypes=[("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*")]
        )
        if file:
            self.selected_video_file = file
            self.video_path_label.config(text=Path(file).name, fg=THEME['success'])
            self.log(f"Video dosyası seçildi: {Path(file).name}")
            
    def fill_metadata_from_music(self):
        """Müzik dosyasından metadata doldur (otomatik dil tespiti ile)"""
        if not self.selected_music_file:
            messagebox.showwarning("Uyarı", "Lütfen önce bir müzik dosyası seçin!")
            return
            
        try:
            metadata = get_music_metadata(self.selected_music_file)
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, metadata['title'])
            
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(1.0, metadata['description'])
            
            self.tags_entry.delete(0, tk.END)
            self.tags_entry.insert(0, ", ".join(metadata['tags']))
            
            # Dil bilgisini göster
            video_lang = metadata.get('video_language', 'en')
            audio_lang = metadata.get('audio_language', 'en')
            self.log(f"Metadata müzik dosyasından dolduruldu")
            self.log(f"Tespit edilen dil: Video={video_lang}, Audio={audio_lang}")
            if metadata.get('additional_languages'):
                self.log(f"Ek diller (global erişim): {', '.join(metadata['additional_languages'])}")
            
            messagebox.showinfo("Başarılı", 
                             f"Metadata başarıyla dolduruldu!\n"
                             f"Tespit edilen dil: {video_lang.upper()}")
        except Exception as e:
            self.log(f"Hata: {e}")
            messagebox.showerror("Hata", f"Metadata doldurulamadı: {e}")
            
    def connect_youtube(self):
        """YouTube API'ye bağlan"""
        self.log("YouTube API'ye bağlanılıyor...")
        self.progress_bar.start()
        
        def connect():
            try:
                self.youtube_service = authenticate_youtube()
                if self.youtube_service:
                    self.root.after(0, lambda: self.youtube_status_label.config(
                        text="✅ Bağlandı", fg=THEME['success']))
                    self.root.after(0, lambda: self.log("YouTube API'ye bağlandı!"))
                    messagebox.showinfo("Başarılı", "YouTube API'ye başarıyla bağlandı!")
                else:
                    self.root.after(0, lambda: self.log("YouTube API bağlantısı başarısız"))
                    messagebox.showerror("Hata", "YouTube API'ye bağlanılamadı!")
            except Exception as e:
                self.root.after(0, lambda: self.log(f"YouTube bağlantı hatası: {e}"))
                messagebox.showerror("Hata", f"YouTube bağlantı hatası: {e}")
            finally:
                self.root.after(0, lambda: self.progress_bar.stop())
                
        threading.Thread(target=connect, daemon=True).start()
        
    def start_upload(self):
        """Yükleme işlemini başlat"""
        # Validasyon
        if not self.selected_music_file:
            messagebox.showwarning("Uyarı", "Lütfen bir müzik dosyası seçin!")
            return
            
        if not self.title_entry.get():
            messagebox.showwarning("Uyarı", "Lütfen bir başlık girin!")
            return
            
        # Platform kontrolü
        platforms = []
        if self.youtube_var.get():
            if not self.youtube_service:
                messagebox.showwarning("Uyarı", "YouTube için önce API'ye bağlanın!")
                return
            platforms.append("youtube")
        if self.instagram_var.get():
            platforms.append("instagram")
        if self.facebook_var.get():
            platforms.append("facebook")
        if self.tiktok_var.get():
            platforms.append("tiktok")
        if self.spotify_var.get():
            platforms.append("spotify")
            
        if not platforms:
            messagebox.showwarning("Uyarı", "Lütfen en az bir platform seçin!")
            return
            
        # Yükleme işlemini thread'de başlat
        def upload():
            self.progress_bar.start()
            self.progress_var.set("Yükleniyor...")
            
            try:
                # Metadata topla
                title = self.title_entry.get()
                description = self.description_text.get(1.0, tk.END).strip()
                tags = [tag.strip() for tag in self.tags_entry.get().split(",") if tag.strip()]
                privacy = self.privacy_var.get()
                
                # Her platform için yükle
                for platform in platforms:
                    self.log(f"\n[{platform.upper()}] Yükleniyor...")
                    self.upload_to_platform(platform, title, description, tags, privacy)
                    
                self.root.after(0, lambda: messagebox.showinfo(
                    "Başarılı", "Tüm platformlara yükleme tamamlandı!"))
                self.root.after(0, lambda: self.progress_var.set("Tamamlandı"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Hata", f"Yükleme hatası: {e}"))
                self.log(f"Hata: {e}")
            finally:
                self.root.after(0, lambda: self.progress_bar.stop())
                
        threading.Thread(target=upload, daemon=True).start()
        
    def upload_to_platform(self, platform, title, description, tags, privacy):
        """Belirli bir platforma yükle"""
        if platform == "youtube":
            self.upload_to_youtube(title, description, tags, privacy)
        elif platform == "instagram":
            self.upload_to_instagram(title, description, tags)
        elif platform == "facebook":
            self.upload_to_facebook(title, description, tags)
        elif platform == "tiktok":
            self.upload_to_tiktok(title, description, tags)
        elif platform == "spotify":
            self.upload_to_spotify(title, description, tags)
            
    def upload_to_youtube(self, title, description, tags, privacy):
        """YouTube'a yükle"""
        if not self.youtube_service:
            self.log("[YOUTUBE] ❌ Hata: API'ye bağlı değil!")
            return
        
        # Duplicate kontrolü - önce başlığa göre kontrol et (video dosyası oluşturulmadan önce)
        if self.check_duplicate_var.get():
            if is_video_already_uploaded(self.youtube_service, title, None):
                self.log(f"[YOUTUBE] ⚠️ Video zaten yüklenmiş: {title}")
                self.root.after(0, lambda: messagebox.showinfo(
                    "Bilgi", f"Bu video zaten yüklenmiş:\n\n{title}\n\nYükleme atlandı."))
                return
            
        # Video dosyası yoksa, müzik + görsel'den video oluştur
        video_file = self.selected_video_file
        if not video_file and self.selected_music_file and self.selected_image_file:
            if not CREATE_VIDEO_AVAILABLE or create_youtube_video is None:
                self.log("[YOUTUBE] ❌ Hata: Video oluşturma modülü bulunamadı!")
                self.log("[YOUTUBE] FFmpeg kurulu olmalı ve create_youtube_video.py mevcut olmalı")
                self.root.after(0, lambda: messagebox.showerror(
                    "Hata", "Video oluşturma modülü bulunamadı!\n\n"
                    "FFmpeg kurulu olmalı ve create_youtube_video.py dosyası mevcut olmalı."))
                return
            
            self.log("[YOUTUBE] 🎬 Video oluşturuluyor (müzik + görsel)...")
            self.root.after(0, lambda: self.progress_var.set("🎬 Video oluşturuluyor..."))
            
            # Output dizini oluştur
            output_dir = Path("output/youtube")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Video dosya adı
            music_name = Path(self.selected_music_file).stem
            video_file = str(output_dir / f"{music_name}_youtube.mp4")
            
            # Video oluştur
            try:
                created_video = create_youtube_video(
                    self.selected_music_file,
                    self.selected_image_file,
                    video_file,
                    width=1920,
                    height=1080
                )
                
                if not created_video:
                    self.log("[YOUTUBE] ❌ Video oluşturulamadı!")
                    self.root.after(0, lambda: messagebox.showerror(
                        "Hata", "Video oluşturulamadı!\n\n"
                        "FFmpeg kurulu olmalı ve çalışır durumda olmalı."))
                    return
                
                video_file = created_video
                self.log(f"[YOUTUBE] ✅ Video oluşturuldu: {Path(video_file).name}")
                
                # Oluşturulan video dosyasını seçili olarak işaretle
                self.selected_video_file = video_file
                
            except Exception as e:
                self.log(f"[YOUTUBE] ❌ Video oluşturma hatası: {e}")
                import traceback
                self.log(f"[YOUTUBE] Traceback: {traceback.format_exc()}")
                self.root.after(0, lambda: messagebox.showerror(
                    "Hata", f"Video oluşturma hatası:\n\n{e}"))
                return
            
        if not video_file:
            self.log("[YOUTUBE] ❌ Hata: Video dosyası bulunamadı!")
            self.log("[YOUTUBE] Lütfen video dosyası seçin veya müzik + görsel seçin")
            self.root.after(0, lambda: messagebox.showwarning(
                "Uyarı", "Video dosyası bulunamadı!\n\n"
                "Lütfen:\n"
                "1. Video dosyası seçin, VEYA\n"
                "2. Müzik + Görsel dosyalarını seçin (otomatik video oluşturulur)"))
            return
            
        try:
            metadata = get_music_metadata(self.selected_music_file)
            
            # Made for Kids ayarı
            made_for_kids = self.made_for_kids_var.get()
            
            self.log(f"[YOUTUBE] 📤 Video yükleniyor: {Path(video_file).name}")
            self.root.after(0, lambda: self.progress_var.set("📤 YouTube'a yükleniyor..."))
            
            # YouTube upload fonksiyonunu çağır ve stdout/stderr'i yakala
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                try:
                    video_id = upload_video_to_youtube(
                        self.youtube_service,
                        video_file,
                        title,
                        description,
                        tags,
                        category_id='10',
                        privacy_status=privacy,
                        for_kids=made_for_kids,  # False = Not made for kids
                        video_language=metadata.get('video_language', 'en'),
                        audio_language=metadata.get('audio_language', 'en'),
                        check_duplicate=False  # Zaten yukarıda kontrol ettik
                    )
                except Exception as upload_error:
                    # Exception'ı yakala ve log'la
                    import traceback
                    error_trace = traceback.format_exc()
                    self.log(f"[YOUTUBE] ❌ Exception: {upload_error}")
                    self.log(f"[YOUTUBE] Traceback: {error_trace}")
                    video_id = None
            
            # Yakalanan çıktıyı log'a yaz
            captured_output = stdout_capture.getvalue()
            captured_errors = stderr_capture.getvalue()
            
            if captured_output:
                for line in captured_output.strip().split('\n'):
                    if line.strip():
                        # Progress mesajlarını özel işle
                        if 'Progress:' in line:
                            progress_pct = line.split('Progress:')[1].strip() if 'Progress:' in line else ''
                            self.root.after(0, lambda p=progress_pct: self.progress_var.set(f"📤 Yükleniyor... {p}"))
                        self.log(f"[YOUTUBE] {line}")
            
            if captured_errors:
                for line in captured_errors.strip().split('\n'):
                    if line.strip():
                        self.log(f"[YOUTUBE] ⚠️ {line}")
            
            if video_id:
                self.log(f"[YOUTUBE] ✅ Başarılı! Video ID: {video_id}")
                self.log(f"[YOUTUBE] 🔗 URL: https://www.youtube.com/watch?v={video_id}")
                self.root.after(0, lambda: messagebox.showinfo(
                    "Başarılı", f"Video başarıyla yüklendi!\n\n"
                    f"Video ID: {video_id}\n\n"
                    f"URL: https://www.youtube.com/watch?v={video_id}"))
            else:
                self.log("[YOUTUBE] ❌ Yükleme başarısız!")
                # Detaylı hata mesajı varsa göster
                error_msg = "Video yükleme başarısız oldu!"
                error_details = []
                
                # Hata mesajlarını topla
                all_output = captured_output + captured_errors
                if all_output:
                    error_lines = [line.strip() for line in all_output.split('\n') 
                                 if '[ERROR]' in line or 'error' in line.lower()]
                    if error_lines:
                        error_details = error_lines
                
                if error_details:
                    error_msg += "\n\nDetaylar:\n" + "\n".join(error_details[:5])  # İlk 5 hata satırı
                
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Hata", msg))
        except Exception as e:
            self.log(f"[YOUTUBE] ❌ Hata: {e}")
            import traceback
            self.log(f"[YOUTUBE] Traceback: {traceback.format_exc()}")
            self.root.after(0, lambda: messagebox.showerror(
                "Hata", f"YouTube yükleme hatası:\n\n{e}"))
            
    def open_platform_settings(self):
        """Platform API ayarları penceresi"""
        if not PLATFORM_UPLOADERS_AVAILABLE:
            messagebox.showwarning("Uyarı", "Platform uploader modülleri bulunamadı!")
            return
        
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Platform API Ayarları")
        settings_window.geometry("600x500")
        
        # Notebook (tabbed interface)
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Instagram tab
        instagram_frame = ttk.Frame(notebook, padding="10")
        notebook.add(instagram_frame, text="Instagram")
        self.create_platform_settings_tab(instagram_frame, "instagram")
        
        # Facebook tab
        facebook_frame = ttk.Frame(notebook, padding="10")
        notebook.add(facebook_frame, text="Facebook")
        self.create_platform_settings_tab(facebook_frame, "facebook")
        
        # TikTok tab
        tiktok_frame = ttk.Frame(notebook, padding="10")
        notebook.add(tiktok_frame, text="TikTok")
        self.create_platform_settings_tab(tiktok_frame, "tiktok")
        
        # Spotify tab
        spotify_frame = ttk.Frame(notebook, padding="10")
        notebook.add(spotify_frame, text="Spotify")
        self.create_platform_settings_tab(spotify_frame, "spotify")
        
        # Butonlar
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Kaydet", 
                  command=lambda: self.save_platform_settings(settings_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", 
                  command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_platform_settings_tab(self, parent, platform):
        """Platform ayarları tab'ı oluştur"""
        ttk.Label(parent, text=f"{platform.upper()} API Ayarları", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Access Token
        ttk.Label(parent, text="Access Token:").pack(anchor=tk.W, pady=5)
        token_entry = ttk.Entry(parent, width=60, show="*")
        token_entry.pack(fill=tk.X, pady=5)
        
        # Platform-specific fields
        if platform == "instagram":
            ttk.Label(parent, text="Instagram Business Account ID:").pack(anchor=tk.W, pady=5)
            account_id_entry = ttk.Entry(parent, width=60)
            account_id_entry.pack(fill=tk.X, pady=5)
        elif platform == "facebook":
            ttk.Label(parent, text="Facebook Page ID (opsiyonel):").pack(anchor=tk.W, pady=5)
            page_id_entry = ttk.Entry(parent, width=60)
            page_id_entry.pack(fill=tk.X, pady=5)
        elif platform == "tiktok":
            ttk.Label(parent, text="App ID:").pack(anchor=tk.W, pady=5)
            app_id_entry = ttk.Entry(parent, width=60)
            app_id_entry.pack(fill=tk.X, pady=5)
            ttk.Label(parent, text="App Secret:").pack(anchor=tk.W, pady=5)
            app_secret_entry = ttk.Entry(parent, width=60, show="*")
            app_secret_entry.pack(fill=tk.X, pady=5)
        
        # Video gereksinimleri bilgisi
        specs = get_platform_specs(platform)
        if specs:
            info_text = "Video Gereksinimleri:\n"
            for key, spec in specs.items():
                info_text += f"\n{key.upper()}:\n"
                info_text += f"  Format: {', '.join(spec['format'])}\n"
                info_text += f"  Çözünürlük: {spec['resolution'][0]}x{spec['resolution'][1]}\n"
                info_text += f"  Max Süre: {spec['max_duration']} saniye\n"
                info_text += f"  Max Boyut: {spec['max_size_mb']} MB\n"
            
            info_label = ttk.Label(parent, text=info_text, justify=tk.LEFT)
            info_label.pack(anchor=tk.W, pady=10)
        
        # Store entries for later access
        parent.token_entry = token_entry
        if platform == "instagram":
            parent.account_id_entry = account_id_entry
        elif platform == "facebook":
            parent.page_id_entry = page_id_entry
        elif platform == "tiktok":
            parent.app_id_entry = app_id_entry
            parent.app_secret_entry = app_secret_entry
    
    def save_platform_settings(self, window):
        """Platform ayarlarını kaydet"""
        # TODO: Ayarları dosyaya kaydet ve uploader'ları initialize et
        messagebox.showinfo("Bilgi", "Ayarlar kaydedildi! (Gelecekte implement edilecek)")
        window.destroy()
    
    def upload_to_instagram(self, title, description, tags):
        """Instagram'a yükle"""
        if not PLATFORM_UPLOADERS_AVAILABLE:
            self.log("[INSTAGRAM] Platform uploader modülleri bulunamadı!")
            return
        
        if not self.instagram_uploader:
            self.log("[INSTAGRAM] API credentials ayarlanmamış! Lütfen API Ayarları'ndan yapılandırın.")
            messagebox.showwarning("Uyarı", "Instagram API credentials gerekli!\nLütfen API Ayarları'ndan yapılandırın.")
            return
        
        video_file = self.selected_video_file
        if not video_file:
            self.log("[INSTAGRAM] Video dosyası bulunamadı!")
            return
        
        try:
            # Instagram için caption oluştur
            caption = f"{title}\n\n{description}\n\n{' '.join(['#' + tag.replace(' ', '') for tag in tags])}"
            
            reel_id = self.instagram_uploader.upload_reel(
                video_file=video_file,
                caption=caption
            )
            
            if reel_id:
                self.log(f"[INSTAGRAM] Başarılı! Reel ID: {reel_id}")
            else:
                self.log("[INSTAGRAM] Yükleme başarısız!")
        except Exception as e:
            self.log(f"[INSTAGRAM] Hata: {e}")
        
    def upload_to_facebook(self, title, description, tags):
        """Facebook'a yükle"""
        if not PLATFORM_UPLOADERS_AVAILABLE:
            self.log("[FACEBOOK] Platform uploader modülleri bulunamadı!")
            return
        
        if not self.facebook_uploader:
            self.log("[FACEBOOK] API credentials ayarlanmamış! Lütfen API Ayarları'ndan yapılandırın.")
            messagebox.showwarning("Uyarı", "Facebook API credentials gerekli!\nLütfen API Ayarları'ndan yapılandırın.")
            return
        
        video_file = self.selected_video_file
        if not video_file:
            self.log("[FACEBOOK] Video dosyası bulunamadı!")
            return
        
        try:
            video_id = self.facebook_uploader.upload_video(
                video_file=video_file,
                title=title,
                description=description,
                privacy="PUBLIC"
            )
            
            if video_id:
                self.log(f"[FACEBOOK] Başarılı! Video ID: {video_id}")
            else:
                self.log("[FACEBOOK] Yükleme başarısız!")
        except Exception as e:
            self.log(f"[FACEBOOK] Hata: {e}")
        
    def upload_to_tiktok(self, title, description, tags):
        """TikTok'a yükle"""
        if not PLATFORM_UPLOADERS_AVAILABLE:
            self.log("[TIKTOK] Platform uploader modülleri bulunamadı!")
            return
        
        if not self.tiktok_uploader:
            self.log("[TIKTOK] API credentials ayarlanmamış! Lütfen API Ayarları'ndan yapılandırın.")
            messagebox.showwarning("Uyarı", "TikTok API credentials gerekli!\nLütfen API Ayarları'ndan yapılandırın.")
            return
        
        video_file = self.selected_video_file
        if not video_file:
            self.log("[TIKTOK] Video dosyası bulunamadı!")
            return
        
        try:
            video_id = self.tiktok_uploader.upload_video(
                video_file=video_file,
                title=title,
                description=description,
                privacy_level="PUBLIC_TO_EVERYONE"
            )
            
            if video_id:
                self.log(f"[TIKTOK] Başarılı! Video ID: {video_id}")
            else:
                self.log("[TIKTOK] Yükleme başarısız!")
        except Exception as e:
            self.log(f"[TIKTOK] Hata: {e}")
        
    def upload_to_spotify(self, title, description, tags):
        """Spotify'a yükle (podcast video)"""
        if not PLATFORM_UPLOADERS_AVAILABLE:
            self.log("[SPOTIFY] Platform uploader modülleri bulunamadı!")
            return
        
        if not self.spotify_uploader:
            self.log("[SPOTIFY] API credentials ayarlanmamış! Lütfen API Ayarları'ndan yapılandırın.")
            messagebox.showwarning("Uyarı", 
                                 "Spotify API credentials gerekli!\n"
                                 "Not: Spotify'a müzik yüklemek için distributor gerekir.\n"
                                 "API sadece podcast video için kullanılabilir.")
            return
        
        video_file = self.selected_video_file
        if not video_file:
            self.log("[SPOTIFY] Video dosyası bulunamadı!")
            return
        
        # Spotify için episode ID gerekli
        episode_id = tk.simpledialog.askstring(
            "Spotify Episode ID", 
            "Podcast Episode ID girin:"
        )
        
        if not episode_id:
            self.log("[SPOTIFY] Episode ID girilmedi!")
            return
        
        try:
            success = self.spotify_uploader.upload_podcast_video(
                video_file=video_file,
                episode_id=episode_id,
                title=title,
                description=description
            )
            
            if success:
                self.log(f"[SPOTIFY] Başarılı! Episode ID: {episode_id}")
            else:
                self.log("[SPOTIFY] Yükleme başarısız!")
        except Exception as e:
            self.log(f"[SPOTIFY] Hata: {e}")
        
    def clear_all(self):
        """Tüm alanları temizle"""
        self.selected_music_file = None
        self.selected_image_file = None
        self.selected_video_file = None
        self.music_path_label.config(text="Seçilmedi", fg=THEME['text_muted'])
        self.image_path_label.config(text="Seçilmedi", fg=THEME['text_muted'])
        self.video_path_label.config(text="Seçilmedi", fg=THEME['text_muted'])
        self.title_entry.delete(0, tk.END)
        self.description_text.delete(1.0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.log("Temizlendi")

def main():
    root = tk.Tk()
    app = SocialMediaUploaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

