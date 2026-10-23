# MuhammedAI Local Developer - Kullanım Kılavuzu

## İçindekiler
1. [Giriş](#giriş)
2. [Sistem Gereksinimleri](#sistem-gereksinimleri)
3. [Kurulum](#kurulum)
4. [İlk Çalıştırma](#ilk-çalıştırma)
5. [Ollama Kurulumu](#ollama-kurulumu)
6. [Kullanım](#kullanım)
7. [Sorun Giderme](#sorun-giderme)
8. [Gelişmiş Ayarlar](#gelişmiş-ayarlar)

---

## Giriş

MuhammedAI Local Developer, Windsurf/Cursor benzeri yerel bir AI kod asistanıdır. Uygulama tamamen yerel olarak çalışır ve Ollama AI modelini kullanır.

**Özellikler:**
- Yerel AI modeli ile kod yazma ve analiz
- WebSocket tabanlı gerçek zamanlı sohbet
- Proje yapısı analizi
- Dosya yönetimi
- Kullanıcı onayı gerektiren işlemler
- Tamamen masaüstü uygulaması

---

## Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi:** Windows 10 veya 11 (64-bit)
- **RAM:** 8 GB (önerilen: 16 GB)
- **Depolama:** 10 GB boş alan
- **İşlemci:** Intel i5 veya eşdeğeri

### Önerilen Gereksinimler
- **RAM:** 16 GB veya üzeri
- **GPU:** NVIDIA GPU (CUDA desteği ile daha hızlı)
- **Depolama:** SSD

---

## Kurulum

### 1. Uygulamayı Çalıştırma

Uygulama paketlenmiş olarak gelir, ek kurulum gerekmez:

1. Masaüstündeki **MuhammedAI** kısayoluna çift tıklayın
2. Veya doğrudan EXE'yi çalıştırın:
   ```
   dist\MuhammedAI\MuhammedAI.exe
   ```

### 2. WebView2 Gereksinimi

Uygulama Windows WebView2 kullanır. Çoğu Windows 11 sistemde yüklüdür.

Eğer WebView2 yoksa, şu adresten indirin:
https://developer.microsoft.com/en-us/microsoft-edge/webview2/

---

## İlk Çalıştırma

### Uygulamayı Başlatma

1. **MuhammedAI.exe**'yi çalıştırın
2. Uygulama otomatik olarak bir yerel sunucu başlatır (http://127.0.0.1:8000)
3. Masaüstü penceresi açılır
4. Tarayıcı benzeri arayüz yüklenir

### Port Çakışması

Eğer 8000 portu kullanımdaysa, uygulama otomatik olarak 8001, 8002... gibi alternatif portları dener.

---

## Ollama Kurulumu

MuhammedAI Local Developer, Ollama AI modelini kullanır.

### 1. Ollama'yı İndirin

Windows için Ollama'yı indirin:
https://ollama.com/download/windows

### 2. Ollama'yı Kurun

İndirilen `.exe` dosyasını çalıştırın ve kurulumu tamamlayın.

### 3. Modeli İndirin

Varsayılan model: `qwen3:4b`

Komut satırını açın (CMD) ve şu komutu çalıştırın:
```cmd
ollama pull qwen3:4b
```

Alternatif modeller:
```cmd
ollama pull llama3:8b
ollama pull mistral:7b
```

### 4. Ollama'yı Başlatın

Ollama genellikle otomatik başlar. Başlamazsa:
```cmd
ollama serve
```

### 5. Bağlantıyı Kontrol Edin

Uygulama içinde Ollama bağlantısı otomatik kontrol edilir.

---

## Kullanım

### Arayüz

Uygulama arayüzü üç ana bölümden oluşur:

1. **Sol Panel (Proje Ağacı):** Proje dosyalarını gösterir
2. **Orta Panel (Sohbet):** AI ile sohbet eder
3. **Sağ Panel (Kod):** Kod düzenleme ve görüntüleme

### Görev Gönderme

1. Sohbet kutusuna görevinizi yazın
2. "Gönder" butonuna tıklayın
3. AI görevi analiz eder ve gerekirse onay ister

### Onay Mekanizması

Güvenli işlemler için onay gereklidir:
- Dosya silme
- Terminal komutları çalıştırma
- Proje dışına dosya yazma

Onay istendiğinde:
- **Onayla:** İşlemi devam ettirir
- **Reddet:** İşlemi iptal eder

### Proje Analizi

Uygulama otomatik olarak proje yapısını analiz eder:
- Dosya ağacı
- Desteklenen uzantılar: `.py`, `.json`, `.yaml`, `.txt`, `.md`, `.toml`
- Yoksayılan dizinler: `.git`, `.venv`, `__pycache__`, `node_modules`

---

## Sorun Giderme

### Uygulama Açılmıyor

**Sorun:** EXE çalışmıyor

**Çözüm:**
1. WebView2 kurulu mu kontrol edin
2. Antivirüs engelliyor mu kontrol edin
3. Windows Defender'dan izin verin

### Ollama Bağlanamıyor

**Sorun:** "Ollama connected: false" hatası

**Çözüm:**
1. Ollama çalışıyor mu kontrol edin: `ollama list`
2. Ollama servisini başlatın: `ollama serve`
3. Model indirilmiş mi kontrol edin: `ollama list`
4. Port 11434 kullanımda mı kontrol edin

### Port Çakışması

**Sorun:** "Port kullanımda" hatası

**Çözüm:**
1. Uygulama otomatik olarak alternatif port dener
2. Manuel olarak portu değiştirmek için `desktop_app.py`'yi düzenleyin

### Yavaş Performans

**Sorun:** AI yanıtları yavaş

**Çözüm:**
1. Daha küçük model kullanın: `qwen3:4b`
2. GPU varsa CUDA destekli model kullanın
3. RAM'i artırın
4. Arka plan uygulamalarını kapatın

### Template Hatası

**Sorun:** "Templates dizini bulunamadı"

**Çözüm:**
1. EXE'yi dist dizininden çalıştırın
2. `_internal` klasörü var mı kontrol edin
3. EXE'yi yeniden paketleyin: `python build_exe.py --onedir`

---

## Gelişmiş Ayarlar

### Model Değiştirme

Varsayılan modeli değiştirmek için:

1. `app/core/config.py` dosyasını açın
2. `DEFAULT_MODEL` satırını bulun
3. Model adını değiştirin:
   ```python
   DEFAULT_MODEL = "llama3:8b"
   ```

### Proje Kökü Değiştirme

Varsayılan proje kökü EXE'nin bulunduğu dizindir.

Değiştirmek için:
1. Ortam değişkeni ayarlayın:
   ```cmd
   set MUHAMMEDAI_PROJECT_ROOT=C:\Proje\Yolu
   ```
2. Veya `desktop_app.py`'yi düzenleyin

### Log Dosyaları

Log dosyaları şu konumda:
```
C:\Users\KullanıcıAdı\.muhammedai\desktop_app.log
```

### Port Değiştirme

Varsayılan port: 8000

Değiştirmek için `desktop_app.py`'yi düzenleyin:
```python
PORT = 8080  # İstenilen port
```

---

## Teknik Destek

### Log Dosyaları

Sorun bildirirken log dosyasını ekleyin:
```
C:\Users\KullanıcıAdı\.muhammedai\desktop_app.log
```

### Sistem Bilgileri

Sorun bildirirken şu bilgileri ekleyin:
- Windows sürümü
- RAM miktarı
- Ollama sürümü
- Kullanılan model
- Hata mesajı

---

## Lisans ve Güvenlik

- Uygulama tamamen yerel olarak çalışır
- Verileriniz internete gönderilmez
- Ollama modeli yerel olarak çalışır
- Kodunuz ve verileriniz güvende

---

## Güncellemeler

Uygulamayı güncellemek için:

1. Yeni sürümü indirin
2. Eski `dist\MuhammedAI` klasörünü silin
3. Yeni sürümü paketleyin: `python build_exe.py --onedir`
4. Kısayolu güncelleyin: `python create_shortcut.py`

---

## İletişim

Sorular ve geri bildirimler için proje sayfasını ziyaret edin.

---

**Versiyon:** 1.0.0  
**Son Güncelleme:** 2026-10-21  
**Platform:** Windows 10/11 (64-bit)
