"""
analyze_metrics.py — analiza Instagram metrika iz CSV datoteke.

Čita metrics.csv (ili metrics_template.csv) i računa:
- Prosječne lajkove, komentare, saves, doseg
- Stopu interakcije po objavi
- Najbolji dan i tip objave
- Najčešće hashtagove

Korištenje:
    python analyze_metrics.py                    # koristi metrics.csv
    python analyze_metrics.py metrics_template.csv  # ili drugi CSV
"""

import csv
import os
import sys
from collections import Counter
from datetime import datetime


def load_metrics(path):
    """Učitava CSV i vraća listu rječnika."""
    if not os.path.exists(path):
        print(f"❌ Datoteka ne postoji: {path}")
        print("   Napravi metrics.csv prema predlošku iz metrics_template.csv")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_number(value):
    """Pretvori string u broj (podržava '3.200' i '3200')."""
    try:
        return int(str(value).replace(".", "").replace(",", ""))
    except (ValueError, AttributeError):
        return 0


def analyze(rows):
    """Analizira metrike i vraća rječnik s rezultatima."""
    if not rows:
        return None

    metrics = {
        "ukupno_objava": len(rows),
        "lajkovi": [],
        "komentari": [],
        "saves": [],
        "doseg": [],
        "interakcije": [],
        "hashtagovi": Counter(),
        "po_tipu": {},
    }

    for row in rows:
        lajkovi = parse_number(row.get("lajkovi", 0))
        komentari = parse_number(row.get("komentari", 0))
        saves = parse_number(row.get("saves", 0))
        doseg = parse_number(row.get("doseg", 0))

        metrics["lajkovi"].append(lajkovi)
        metrics["komentari"].append(komentari)
        metrics["saves"].append(saves)
        metrics["doseg"].append(doseg)

        # Stopa interakcije = (lajkovi + komentari + saves) / doseg
        if doseg > 0:
            interakcija = (lajkovi + komentari + saves) / doseg * 100
        else:
            interakcija = 0
        metrics["interakcije"].append(interakcija)

        # Hashtagovi
        hashtags = row.get("hashtagovi", "")
        for tag in hashtags.split():
            if tag.startswith("#"):
                metrics["hashtagovi"][tag] += 1

        # Po tipu objave
        tip = row.get("tip_objave", "nepoznato")
        if tip not in metrics["po_tipu"]:
            metrics["po_tipu"][tip] = {
                "lajkovi": [],
                "komentari": [],
                "saves": [],
                "doseg": [],
            }
        metrics["po_tipu"][tip]["lajkovi"].append(lajkovi)
        metrics["po_tipu"][tip]["komentari"].append(komentari)
        metrics["po_tipu"][tip]["saves"].append(saves)
        metrics["po_tipu"][tip]["doseg"].append(doseg)

    return metrics


def print_report(metrics):
    """Ispisuje formatirani izvještaj."""
    if not metrics:
        print("Nema podataka za analizu.")
        return

    print("=" * 60)
    print("📊 ANALIZA INSTAGRAM METRIKA")
    print("=" * 60)
    print(f"\nUkupno objava: {metrics['ukupno_objava']}")

    # Prosjeci
    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    print("\n── PROSJEČNE VRIJEDNOSTI PO OBJAVI ──")
    print(f"  Lajkovi:      {avg(metrics['lajkovi']):.0f}")
    print(f"  Komentari:    {avg(metrics['komentari']):.0f}")
    print(f"  Saves:        {avg(metrics['saves']):.0f}")
    print(f"  Doseg:        {avg(metrics['doseg']):.0f}")
    print(f"  Interakcija:  {avg(metrics['interakcije']):.2f}%")

    # Po tipu
    print("\n── PO TIPU OBJAVE ──")
    for tip, data in metrics["po_tipu"].items():
        print(f"\n  {tip.upper()}:")
        print(f"    Lajkovi:      {avg(data['lajkovi']):.0f}")
        print(f"    Komentari:    {avg(data['komentari']):.0f}")
        print(f"    Saves:        {avg(data['saves']):.0f}")
        print(f"    Doseg:        {avg(data['doseg']):.0f}")

    # Hashtagovi
    print("\n── NAJČEŠĆI HASHTAGOVI ──")
    for tag, count in metrics["hashtagovi"].most_common(10):
        print(f"  {tag}: {count}×")

    # Preporuke
    print("\n── PREPORUKE ZA SLJEDEĆI CIKLUS ──")

    saves_avg = avg(metrics["saves"])
    komentari_avg = avg(metrics["komentari"])
    interakcija_avg = avg(metrics["interakcije"])

    if saves_avg > 40:
        print("  ✅ Saves su iznad prosjeka — nastavi s edukativnim sadržajem.")
    elif saves_avg > 20:
        print("  ⚠️  Saves su osrednji — probaj s konkretnijim savjetima (recepti, upute).")
    else:
        print("  ❌ Saves su niski — povećaj edukativni element u objavama.")

    if komentari_avg > 15:
        print("  ✅ Komentari su iznad prosjeka — pitanja publici dobro rade.")
    else:
        print("  ⚠️  Komentari su niski — postavi izravnije pitanje na kraju objave.")

    if interakcija_avg > 5:
        print("  ✅ Stopa interakcije je iznad 5% — cilj ispunjen.")
    elif interakcija_avg > 3:
        print("  ⚠️  Stopa interakcije je 3-5% — blizu cilja, nastavi pratiti.")
    else:
        print("  ❌ Stopa interakcije je ispod 3% — razmisli o jačem hooku.")

    print("\n" + "=" * 60)
    print("💡 Za detaljniju analizu, popuni više objava u CSV.")
    print("=" * 60)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "metrics.csv"

    if not os.path.exists(path):
        # Ako metrics.csv ne postoji, probaj template
        if os.path.exists("metrics_template.csv"):
            print(f"⚠️  {path} ne postoji. Koristim metrics_template.csv kao primjer.\n")
            path = "metrics_template.csv"
        else:
            print(f"❌ Ni {path} ni metrics_template.csv ne postoje.")
            sys.exit(1)

    rows = load_metrics(path)
    metrics = analyze(rows)
    print_report(metrics)


if __name__ == "__main__":
    main()