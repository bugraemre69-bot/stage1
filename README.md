# Makine Mühendisliği Öğrenci Rehberi

Bu proje, makine mühendisliği öğrencileri için tek yerden erişilebilen bir **güncel bağlantı portalı** sunar.

## Özellikler
- Sol menüde kategori bazlı gezinme:
  - Online Seminerler
  - Fiziksel Seminerler
  - Staj İlanları
  - Bitirme Projeleri
  - Online ve Ücretsiz Kurslar
- Mavi-beyaz, sade ve okunabilir arayüz.
- Ana ekranda **“Bugünün görevini al”** butonu.
  - Buton her tıklamada kullanıcıya ekran dışı bir makine mühendisliği araştırma görevi verir.
- Ana sayfada makine temalı silüetler (çark, motor, araba).
- İçerikler internetten RSS ile çekilir.
- Veriler **8 saatte bir** yenilenir.
- Her kategoride en fazla **50 bağlantı** tutulur.
- Staj ve seminer kategorilerinde eski bağlantılar tarih bazlı filtrelenir.

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
