# Makine Mühendisliği Öğrenci Portalı

Bu proje, makine mühendisi öğrencilerin tek yerden ulaşabileceği **güncel bağlantı portalı** sunar.

## Özellikler
- Sol menüde kategori bazlı sade gezinme:
  - Güncel Haberler
  - Staj Programları
  - Bitirme Projeleri
  - Yarışma Programları
  - Online Oturumlar
  - Fiziksel Oturumlar
- Mavi-beyaz, basit ve okunabilir arayüz.
- Kategoriye tıklandığında bağlantılar yeni sekmede açılır.
- İçerikler internetten RSS ile çekilir.
- Veriler **8 saatte bir** yenilenir.
- Her kategoride en fazla **50 bağlantı** tutulur.

## Kurulum
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

## Çalıştırma
```bash
python3 app.py
```

Ardından tarayıcıda:

`http://127.0.0.1:5000`

## Veri önbelleği
Bağlantılar şu dosyada saklanır:

`data/links_cache.json`
