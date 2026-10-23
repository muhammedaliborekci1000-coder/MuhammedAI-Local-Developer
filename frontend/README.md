# MuhammedAI Local Developer - Web UI Frontend

React + Monaco Editor ile Windsurf benzeri AI-powered code editor frontend.

## Özellikler

- ✅ Monaco Editor (VS Code editor engine)
- ✅ Interactive code editing
- ✅ File tree sidebar
- ✅ Multi-tab editing
- ✅ Terminal panel (mock)
- ✅ AI Assistant panel
- ✅ Status bar
- ✅ Syntax highlighting
- ✅ Dark theme (VS Code dark)
- ✅ Backend API entegrasyonu

## Kurulum

### Gereksinimler

- Node.js v18+ (v24.21.0 test edildi)
- npm veya yarn

### Adımlar

1. **Bağımlılıkları yükle:**
```bash
cd frontend
npm install
```

2. **Development sunucusunu başlat:**
```bash
npm run dev
```

Frontend `http://localhost:3000` adresinde çalışacaktır.

3. **Backend'i başlat:**
```bash
# Ana dizinde
python -m uvicorn app.ui.web_app:app --host 127.0.0.1 --port 8000
```

Backend `http://127.0.0.1:8000` adresinde çalışacaktır.

## Yapılandırma

### Vite Proxy

`vite.config.js` dosyasında backend API proxy yapılandırılmıştır:

```javascript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:8000',
    changeOrigin: true
  }
}
```

Bu sayede frontend'den `/api/*` istekleri otomatik olarak backend'e yönlendirilir.

## Proje Yapısı

```
frontend/
├── src/
│   ├── components/
│   │   ├── Editor.jsx          # Monaco Editor component
│   │   ├── FileTree.jsx        # File tree sidebar
│   │   ├── Terminal.jsx       # Terminal panel
│   │   ├── StatusBar.jsx      # Status bar
│   │   └── AIPanel.jsx        # AI Assistant panel
│   ├── App.jsx                # Main application
│   ├── App.css                # App styles
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html                 # HTML template
├── package.json               # Dependencies
└── vite.config.js             # Vite configuration
```

## Kullanım

### Dosya Açma

1. Sol taraftaki file tree'den bir dosyaya tıklayın
2. Dosya yeni bir tab'da açılır
3. Monaco Editor'da düzenleyebilirsiniz

### Tab Yönetimi

- **Tab açma:** File tree'den dosyaya tıklayın
- **Tab kapatma:** Tab üzerindeki × butonuna tıklayın
- **Tab değiştirme:** Tab'a tıklayın

### Terminal

- **Komut çalıştırma:** Terminal'e komut yazın ve Enter'a basın
- **Kullanılabilir komutlar:** `help`, `clear`, `ls`, `pwd`, `echo`, `date`, `python`, `npm`, `git`
- **Terminal kapatma:** Header'daki X butonuna tıklayın
- **Terminal collapse:** Header'daki chevron butonuna tıklayın

### AI Assistant

- **Soru sor:** AI panelinde metin kutusuna sorunuzu yazın
- **Gönder:** Send butonuna tıklayın veya Enter'a basın
- **Panel kapatma:** Header'daki X butonuna tıklayın

### Status Bar

- **Terminal toggle:** Terminal butonuna tıklayın
- **AI toggle:** AI Assistant butonuna tıklayın
- **Dosya bilgisi:** Aktif dosya yolu gösterilir
- **Dil bilgisi:** Python 3.11, UTF-8 encoding
- **Konum:** Satır ve sütun bilgisi

## Build

Production build oluşturmak için:

```bash
npm run build
```

Build çıktısı `dist/` dizininde oluşturulur.

## Preview

Production build'i preview etmek için:

```bash
npm run preview
```

## Backend API Entegrasyonu

Frontend şu backend endpoint'lerini kullanır:

- `GET /api/editor/file` - Dosya içeriğini al
- `POST /api/agent/run` - AI görevi çalıştır

## Notlar

- Terminal şu an mock çalışmaktadır (gerçek terminal entegrasyonu gerekli)
- AI Assistant backend API entegrasyonu hazırdır
- File tree şu an mock veri kullanmaktadır (gerçek dosya sistemi entegrasyonu gerekli)
- Monaco Editor tam özellikli çalışmaktadır

## Geliştirme

### Yeni Component Ekleme

1. `src/components/` dizinine yeni JSX dosyası oluşturun
2. Component'i `App.jsx`'e import edin
3. Gerekli stilleri `index.css`'e ekleyin

### Monaco Editor Ayarları

`Editor.jsx` dosyasında Monaco Editor ayarları değiştirilebilir:

```javascript
options={{
  minimap: { enabled: true },
  fontSize: 14,
  // ... diğer ayarlar
}}
```

## Sorun Giderme

### npm install başarısız olursa

```bash
# Cache temizle
npm cache clean --force

# node_modules sil ve tekrar yükle
rm -rf node_modules package-lock.json
npm install
```

### Backend bağlantı hatası

Backend'in çalıştığından emin olun:

```bash
python -m uvicorn app.ui.web_app:app --host 127.0.0.1 --port 8000
```

### Port çakışması

Farklı bir port kullanmak için `vite.config.js`'i düzenleyin:

```javascript
server: {
  port: 3001, // Farklı port
  // ...
}
```

## Lisans

MIT
