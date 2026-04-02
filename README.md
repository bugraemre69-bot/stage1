# Screen Coach (Makine Mühendisliği Öğrencisi için)

Bu araç günlük ekran süreni dakika bazında tutar, durumunu değerlendirir ve ekran başından kalkman için **makine mühendisliği odaklı görevler** önerir.

## Kurallar
- **0–2 saat**: İyi
- **2–5 saat**: Orta (görev önerilir)
- **5+ saat**: Kötü (daha kapsamlı görev önerilir)

## Kullanım
Python 3 ile çalıştır:

```bash
python3 screen_coach.py log 60
python3 screen_coach.py status
python3 screen_coach.py suggest
python3 screen_coach.py suggest --deep
```

## Veri dosyası
Kayıtlar şu dosyada tutulur:

`data/screen_time_log.json`

Her gün için `YYYY-MM-DD` anahtarı altında toplam dakika saklanır.
