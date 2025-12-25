# 🎮 Unreal Engine 5.7 İlk Adımlar

## ⚠️ Önemli: Launcher vs Editor

**Unreal Engine Launcher** (şu an açık olan):
- Proje yönetimi
- Örnek projeler
- Eğitimler
- **Edit menüsü YOK** (launcher'da)

**Unreal Engine Editor** (proje açıldığında):
- Gerçek editör
- Edit menüsü burada
- MetaHuman Creator burada

## 🚀 Adım 1: İlk Projenizi Oluşturun

### Launcher'da:

1. **Sol tarafta "Yeni Proje"** (mavi buton) tıklayın
2. **Template seçin**:
   - **"Oyun"** (Game) → **"Boş"** (Blank) veya
   - **"Film, Televizyon ve Canlı Etkinlikler"** → **"Boş"**
3. **Ayarlar**:
   - **Blueprint** veya **C++** (Blueprint önerilir - daha kolay)
   - **Target Platform**: Desktop
   - **Quality Preset**: Maximum
   - **Raytracing**: İsteğe bağlı (GPU güçlüyse)
4. **Proje Konumu**: Seçin
5. **Proje Adı**: Örn. "SingerAvatar" veya "NeutralBeatsStudio"
6. **Oluştur** butonuna tıklayın

**Not**: İlk proje oluşturma 5-10 dakika sürebilir (dosyalar indiriliyor).

---

## 🎨 Adım 2: Editor Açıldığında

Proje oluşturulduktan sonra **Unreal Engine Editor** açılacak. İşte Edit menüsü burada görünecek!

### Edit Menüsü Nerede?

1. **Editor açıldığında** üst menü çubuğunda:
   - **File** | **Edit** | **Window** | **Tools** | **Help**
2. **Edit** menüsüne tıklayın
3. **Plugins** seçeneğini bulun

---

## 🔌 Adım 3: MetaHuman Plugin'lerini Aktif Edin

### Editor'da:

1. **Edit** → **Plugins** tıklayın
2. Arama kutusuna **"MetaHuman"** yazın
3. Şu plugin'leri **Enable** yapın:
   - ✅ **MetaHuman**
   - ✅ **MetaHuman Performance**
   - ✅ **MetaHuman SDK**
4. **Restart** butonuna tıklayın (veya Editor'ı kapatıp tekrar açın)

---

## 🌐 Alternatif: Web-Based MetaHuman Creator (Daha Kolay)

Edit menüsünü bulmak zor geliyorsa, **web-based** versiyonu kullanabilirsiniz:

1. **Tarayıcıda** açın: https://metahuman.unrealengine.com/
2. **Sign In** (Epic Games hesabı ile)
3. **Create New** → Karakter oluşturun
4. **Download** → Unreal Engine projesi olarak indirin
5. İndirdiğiniz projeyi Unreal Engine'de açın

**Avantaj**: Daha kolay, Edit menüsüne gerek yok!

---

## 📋 Hızlı Kontrol Listesi

- [ ] Unreal Engine Launcher açık
- [ ] "Yeni Proje" butonuna tıklandı
- [ ] Template seçildi (Blank/Boş)
- [ ] Proje oluşturuldu
- [ ] Editor açıldı
- [ ] Edit menüsü görünüyor
- [ ] Plugins → MetaHuman aktif edildi

---

## 💡 İpuçları

### İlk Proje İçin:

- **Template**: "Blank" (Boş) - sadece temel
- **Blueprint**: Seçin (C++ yerine - daha kolay)
- **Starter Content**: İsteğe bağlı (test için yararlı)

### Performans:

- İlk açılış biraz yavaş olabilir (shader compilation)
- 5-10 dakika bekleyin
- Editor açıldıktan sonra daha hızlı olacak

---

## 🎯 Sonraki Adım

Proje oluşturulduktan ve Editor açıldıktan sonra:

1. **Edit** → **Plugins** → MetaHuman aktif edin
2. **Window** → **MetaHuman Creator** (veya web-based kullanın)
3. İlk karakterinizi oluşturun!

---

## ❓ Sorun mu Var?

### Editor Açılmıyor:

- Proje oluşturma tamamlandı mı kontrol edin
- Biraz bekleyin (ilk açılış yavaş olabilir)
- Hata mesajı varsa paylaşın

### Edit Menüsü Hala Görünmüyor:

- Editor açık olduğundan emin olun (Launcher değil)
- Üst menü çubuğuna bakın
- Tam ekran modundaysa menü çubuğu gizlenmiş olabilir

