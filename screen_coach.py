#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from random import choice
from typing import Any

DATA_FILE = Path("data/screen_time_log.json")


@dataclass
class Evaluation:
    level: str
    message: str
    action: str


def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {"entries": {}}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_today_key() -> str:
    return date.today().isoformat()


def add_minutes(minutes: int) -> int:
    data = load_data()
    key = get_today_key()
    today_minutes = int(data["entries"].get(key, 0)) + minutes
    data["entries"][key] = today_minutes
    save_data(data)
    return today_minutes


def get_minutes(day_key: str | None = None) -> int:
    data = load_data()
    key = day_key or get_today_key()
    return int(data["entries"].get(key, 0))


def evaluate(minutes: int) -> Evaluation:
    hours = minutes / 60
    if hours <= 2:
        return Evaluation(
            level="İYİ",
            message=f"Bugünkü ekran süren {hours:.2f} saat. Kontrol sende!",
            action="Aynı tempoda devam et. 25-30 dakikada bir kısa göz molası ver.",
        )
    if 2 < hours <= 5:
        return Evaluation(
            level="ORTA",
            message=(
                f"Bugünkü ekran süren {hours:.2f} saat. 2 saati aştın; denge zamanı."
            ),
            action=mechanical_task(),
        )
    return Evaluation(
        level="KÖTÜ",
        message=(
            f"Bugünkü ekran süren {hours:.2f} saat. 5 saatin üstü odak ve sağlık için riskli."
        ),
        action=mechanical_task(deep=True),
    )


def mechanical_task(deep: bool = False) -> str:
    standard_tasks = [
        "10 dakika boyunca bir makine elemanını (rulman, dişli, mil) kâğıda çizip çalışma prensibini not et.",
        "Ekrandan uzak 15 dakikada bir termo/akış konusu seç ve günlük hayattan 3 örnek yaz.",
        "Evdeki bir mekanizmayı (kapı menteşesi, pompa, bisiklet fren sistemi) inceleyip serbest cisim diyagramını çıkar.",
        "Bir üretim yöntemini (CNC, döküm, kaynak) seç; avantaj/dezavantajlarını 8 maddede karşılaştır.",
    ]
    deep_tasks = [
        "20 dakikalık ‘mini tasarım görevi’: 500 ml su şişesi taşıyan hafif bir tutucu tasarla; malzeme ve kesit kararını yaz.",
        "Bir ısı değiştirici tipini seç (plakalı/borulu) ve hangi endüstride neden uygun olduğunu 1 sayfa özetle.",
        "Basit bir mekanik sistem için (yay-kütle-sönümleyici) parametre değişiminin davranışa etkisini kağıt üstünde analiz et.",
        "Bir enerji verimliliği problemi tanımla (oda ısıtma, pompa seçimi vb.) ve 3 çözüm önerisini kıyasla.",
    ]
    return choice(deep_tasks if deep else standard_tasks)


def print_status(minutes: int) -> None:
    result = evaluate(minutes)
    print("=" * 56)
    print(f"Seviye : {result.level}")
    print(result.message)
    print(f"Öneri  : {result.action}")
    print("=" * 56)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Günlük ekran süresi takipçisi ve makine mühendisliği odak görevi üreticisi"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    log_cmd = sub.add_parser("log", help="Bugüne ekran süresi ekle (dakika)")
    log_cmd.add_argument("minutes", type=int, help="Eklenecek dakika")

    sub.add_parser("status", help="Bugünkü durumu göster")

    suggest_cmd = sub.add_parser("suggest", help="Sadece görev önerisi ver")
    suggest_cmd.add_argument(
        "--deep",
        action="store_true",
        help="Daha kapsamlı görev üret",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "log":
        if args.minutes <= 0:
            raise SystemExit("Dakika pozitif olmalı.")
        total = add_minutes(args.minutes)
        print(f"Bugünkü toplam süre: {total} dakika ({total / 60:.2f} saat)")
        print_status(total)
        return

    if args.command == "status":
        total = get_minutes()
        print(f"Bugünkü toplam süre: {total} dakika ({total / 60:.2f} saat)")
        print_status(total)
        return

    if args.command == "suggest":
        print(mechanical_task(deep=args.deep))
        return


if __name__ == "__main__":
    main()
