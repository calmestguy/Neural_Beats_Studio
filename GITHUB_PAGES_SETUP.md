# GitHub Pages Kurulum Rehberi

## 🔓 Repository'yi Public Yapma

GitHub Pages, **private repository'lerde ücretsiz çalışmaz**. Repository'yi public yapmanız gerekiyor.

### Adımlar:

1. **Repository Settings'e gidin:**
   - https://github.com/calmestguy/Neural_Beats_Studio/settings

2. **"General" sekmesine gidin** (sol menüden)

3. **En alta kaydırın** - "Danger Zone" bölümünü bulun

4. **"Change repository visibility"** seçeneğini bulun

5. **"Change visibility"** butonuna tıklayın

6. **"Make public"** seçeneğini seçin

7. **Repository adını yazarak onaylayın**

### ⚠️ Önemli Notlar:

- **Public repository** = Herkes kodu görebilir
- **Sensitive data kontrolü:** `credentials.json`, `token.json` gibi dosyalar `.gitignore`'da olmalı
- **API keys:** Kodda hardcoded API key'ler olmamalı

### ✅ Güvenlik Kontrolü:

Repository'yi public yapmadan önce kontrol edin:
- ✅ `credentials.json` → `.gitignore`'da olmalı
- ✅ `token.json` → `.gitignore`'da olmalı
- ✅ API keys → Kodda hardcoded olmamalı
- ✅ Şifreler → Kodda olmamalı

## 📄 GitHub Pages'i Aktif Etme

Repository public olduktan sonra:

1. **Settings → Pages** sayfasına gidin

2. **Source:** "Deploy from a branch" seçin

3. **Branch:** "master" (veya "main") seçin

4. **Folder:** "/docs" seçin

5. **Save** butonuna tıklayın

6. **1-2 dakika bekleyin** - Sayfa yayınlanacak

7. **URL:** `https://calmestguy.github.io/Neural_Beats_Studio/data-deletion.html`

## 🔒 Alternatif: Private Repository İçin

Eğer repository'yi public yapmak istemiyorsanız:

### Seçenek 1: Netlify (Ücretsiz)
1. https://www.netlify.com/ adresine gidin
2. GitHub ile giriş yapın
3. Repository'yi bağlayın
4. Build settings:
   - Publish directory: `docs`
   - Build command: (boş bırakın)
5. Deploy
6. URL: `https://neural-beats-studio.netlify.app/data-deletion.html`

### Seçenek 2: Vercel (Ücretsiz)
1. https://vercel.com/ adresine gidin
2. GitHub ile giriş yapın
3. Repository'yi import edin
4. Root directory: `docs`
5. Deploy
6. URL: `https://neural-beats-studio.vercel.app/data-deletion.html`

## ✅ Önerilen: Repository'yi Public Yap

**Neden?**
- ✅ En kolay ve hızlı
- ✅ Ücretsiz
- ✅ GitHub Pages otomatik çalışır
- ✅ Kod zaten açık kaynak olabilir

**Güvenlik:**
- `.gitignore` dosyası zaten sensitive dosyaları koruyor
- API keys kodda hardcoded değil
- Token'lar lokal dosyalarda

## 🚀 Sonuç

1. Repository'yi **public** yapın
2. GitHub Pages'i **aktif** edin
3. URL'yi Meta Developers'a **girin**

URL: `https://calmestguy.github.io/Neural_Beats_Studio/data-deletion.html`

