
"""
analyze_metrics.py

Analiza Instagram metrika za projekt Dida Boža.

Analizira:
- Prosječne lajkove, komentare, saves i doseg
- Engagement rate (stopu interakcije)
- Najbolji dan objavljivanja
- Najuspješniji tip objave
- Najčešće hashtagove
- Preporuke za sljedeći ciklus objava

Korištenje:
    python analyze_metrics.py
    python analyze_metrics.py metrics_template.csv
    python analyze_metrics.py metrics.csv

CSV stupci:
    datum,tip_objave,lajkovi,komentari,saves,doseg,hashtagovi
"""

import csv
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime


# --------------------------------------------------
# POSTAVKE
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

DEFAULT_CSV = BASE_DIR / "metrics.csv"
TEMPLATE_CSV = BASE_DIR / "metrics_template.csv"
REPORT_FILE = OUTPUT_DIR / "analiza_rezultata.txt"

DAYS_HR = {
    0: "Ponedjeljak",
    1: "Utorak",
    2: "Srijeda",
    3: "Četvrtak",
    4: "Petak",
    5: "Subota",
    6: "Nedjelja",
}


# --------------------------------------------------
# POMOĆNE FUNKCIJE
# --------------------------------------------------

def parse_number(value):
    """
    Pretvara tekst u broj.
    Podržava formate poput 3200, 3.200 i 3,200.
    Prazne ili neispravne vrijednosti vraćaju None.
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    value = value.replace(" ", "")

    try:
        return int(value.replace(".", "").replace(",", ""))
    except ValueError:
        return None


def parse_date(value):
    """
    Podržava nekoliko uobičajenih formata datuma.
    """

    if not value:
        return None

    value = str(value).strip()

    formats = [
        "%d.%m.%Y.",
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
    ]

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return None


def average(values):
    """Računa prosjek samo dostupnih vrijednosti."""

    valid = [value for value in values if value is not None]

    if not valid:
        return None

    return sum(valid) / len(valid)


def format_average(value, decimals=0):
    """Formatira prosjek ili prikazuje N/A."""

    if value is None:
        return "N/A"

    return f"{value:.{decimals}f}"


# --------------------------------------------------
# UČITAVANJE CSV DATOTEKE
# --------------------------------------------------

def load_metrics(path):
    """Učitava CSV i vraća listu redaka."""

    if not path.exists():
        print(f"❌ Datoteka ne postoji: {path}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("❌ CSV datoteka nema zaglavlja.")
                sys.exit(1)

            required_columns = {
                "datum",
                "tip_objave",
                "lajkovi",
                "komentari",
                "saves",
                "doseg",
                "hashtagovi",
            }

            missing = required_columns - set(reader.fieldnames)

            if missing:
                print(
                    "❌ Nedostaju CSV stupci: "
                    + ", ".join(sorted(missing))
                )
                sys.exit(1)

            rows = list(reader)

    except OSError as error:
        print(f"❌ Greška pri čitanju CSV datoteke: {error}")
        sys.exit(1)

    if not rows:
        print("⚠️ CSV datoteka ne sadrži podatke.")
        return []

    return rows


# --------------------------------------------------
# ANALIZA PODATAKA
# --------------------------------------------------

def analyze(rows):
    """Analizira metrike i vraća rezultate."""

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
        "po_tipu": defaultdict(list),
        "po_danu": defaultdict(list),
        "neispravni_datumi": 0,
        "objave_bez_dosega": 0,
    }

    for row in rows:

        lajkovi = parse_number(row.get("lajkovi"))
        komentari = parse_number(row.get("komentari"))
        saves = parse_number(row.get("saves"))
        doseg = parse_number(row.get("doseg"))

        # Nedostajuće vrijednosti ne računamo kao nule.
        metrics["lajkovi"].append(lajkovi)
        metrics["komentari"].append(komentari)
        metrics["saves"].append(saves)
        metrics["doseg"].append(doseg)

        # Engagement rate.
        if doseg is not None and doseg > 0:
            interaction_values = [
                value for value in [lajkovi, komentari, saves]
                if value is not None
            ]

            if interaction_values:
                engagement = (
                    sum(interaction_values) / doseg * 100
                )
                metrics["interakcije"].append(engagement)
            else:
                engagement = None
        else:
            engagement = None
            metrics["objave_bez_dosega"] += 1

        # Tip objave.
        tip = (
            row.get("tip_objave") or "Nepoznato"
        ).strip()

        metrics["po_tipu"][tip].append({
            "lajkovi": lajkovi,
            "komentari": komentari,
            "saves": saves,
            "doseg": doseg,
            "engagement": engagement,
        })

        # Dan objavljivanja.
        datum = parse_date(row.get("datum"))

        if datum:
            dan = DAYS_HR[datum.weekday()]

            metrics["po_danu"][dan].append({
                "lajkovi": lajkovi,
                "komentari": komentari,
                "saves": saves,
                "doseg": doseg,
                "engagement": engagement,
            })
        else:
            metrics["neispravni_datumi"] += 1

        # Hashtagovi.
        hashtags = row.get("hashtagovi") or ""

        for tag in re.findall(r"#[\wčćžšđČĆŽŠĐ]+", hashtags):
            metrics["hashtagovi"][tag.lower()] += 1

    return metrics


# --------------------------------------------------
# ANALIZA PO GRUPAMA
# --------------------------------------------------

def group_average(data, field):
    """Računa prosjek određene metrike unutar grupe."""

    values = [item[field] for item in data]

    return average(values)


def best_group(groups, field):
    """Pronalazi grupu s najboljim prosjekom."""

    results = {}

    for name, data in groups.items():
        result = group_average(data, field)

        if result is not None:
            results[name] = result

    if not results:
        return None, None

    best_name = max(results, key=results.get)

    return best_name, results[best_name]


# --------------------------------------------------
# GENERIRANJE IZVJEŠTAJA
# --------------------------------------------------

def generate_report(metrics):
    """Generira tekstualni izvještaj."""

    if not metrics:
        return "Nema podataka za analizu."

    lines = []

    def add(text=""):
        lines.append(text)

    add("=" * 60)
    add("DIDA BOŽA – ANALIZA INSTAGRAM METRIKA")
    add("=" * 60)

    add(f"\nUkupno analiziranih objava: {metrics['ukupno_objava']}")

    # Prosjeci.
    add("\n--- PROSJEČNE VRIJEDNOSTI PO OBJAVI ---")

    for label, key in [
        ("Lajkovi", "lajkovi"),
        ("Komentari", "komentari"),
        ("Spremanja (saves)", "saves"),
        ("Doseg", "doseg"),
    ]:
        add(
            f"{label:25}: "
            f"{format_average(average(metrics[key]))}"
        )

    add(
        f"{'Engagement rate':25}: "
        f"{format_average(average(metrics['interakcije']), 2)}%"
        if metrics["interakcije"]
        else "Engagement rate: N/A (nema dovoljno podataka o dosegu)"
    )

    # Tip objave.
    add("\n--- REZULTATI PO TIPU OBJAVE ---")

    for tip, data in metrics["po_tipu"].items():

        add(f"\n{tip.upper()}")

        add(
            f"  Prosjek lajkova: "
            f"{format_average(group_average(data, 'lajkovi'))}"
        )

        add(
            f"  Prosjek komentara: "
            f"{format_average(group_average(data, 'komentari'))}"
        )

        add(
            f"  Prosjek spremanja: "
            f"{format_average(group_average(data, 'saves'))}"
        )

        add(
            f"  Prosjek dosega: "
            f"{format_average(group_average(data, 'doseg'))}"
        )

        engagement = group_average(data, "engagement")

        add(
            f"  Engagement rate: "
            f"{format_average(engagement, 2)}%"
            if engagement is not None
            else "  Engagement rate: N/A"
        )

    # Najuspješniji tip.
    best_type, best_type_value = best_group(
        metrics["po_tipu"], "engagement"
    )

    if best_type:
        add(
            f"\nNajbolji tip prema engagement rateu: "
            f"{best_type} ({best_type_value:.2f}%)"
        )
    else:
        add(
            "\nNajbolji tip prema engagement rateu: "
            "Nije moguće odrediti bez podataka o dosegu."
        )

    # Dan objavljivanja.
    add("\n--- REZULTATI PO DANU OBJAVLJIVANJA ---")

    for dan, data in metrics["po_danu"].items():

        engagement = group_average(data, "engagement")

        add(
            f"{dan}: "
            f"{len(data)} objava, "
            f"prosječni engagement: "
            f"{format_average(engagement, 2)}%"
        )

    best_day, best_day_value = best_group(
        metrics["po_danu"], "engagement"
    )

    if best_day:
        add(
            f"\nNajbolji dan prema engagement rateu: "
            f"{best_day} ({best_day_value:.2f}%)"
        )
    else:
        add(
            "\nNajbolji dan: Nije moguće odrediti "
            "bez podataka o dosegu."
        )

    # Hashtagovi.
    add("\n--- NAJČEŠĆI HASHTAGOVI ---")

    if metrics["hashtagovi"]:
        for tag, count in metrics["hashtagovi"].most_common(10):
            add(f"{tag}: {count} puta")
    else:
        add("Nema dostupnih hashtagova.")

    # Preporuke.
    add("\n--- PREPORUKE ZA SLJEDEĆI CIKLUS ---")

    if metrics["ukupno_objava"] < 5:
        add(
            "• Uzorak je malen. Prikupi više objava "
            "prije donošenja čvrstih zaključaka."
        )

    if best_type:
        add(
            f"• Dodatno testiraj format '{best_type}', "
            "koji je u ovom uzorku imao najbolji engagement rate."
        )

    if best_day:
        add(
            f"• Razmotri dodatno testiranje objava "
            f"na dan {best_day}."
        )

    if not metrics["interakcije"]:
        add(
            "• Unesi podatke o dosegu kako bi se mogao "
            "izračunati engagement rate."
        )

    if metrics["neispravni_datumi"]:
        add(
            f"• {metrics['neispravni_datumi']} datuma nije "
            "prepoznato. Provjeri format datuma u CSV-u."
        )

    if metrics["objave_bez_dosega"]:
        add(
            f"• {metrics['objave_bez_dosega']} objava nema "
            "valjan podatak o dosegu."
        )

    add(
        "\nNapomena: Rezultati opisuju samo unesene podatke. "
        "Ne predstavljaju univerzalne benchmarke."
    )

    add("\n" + "=" * 60)
    add("Kraj izvještaja")
    add("=" * 60)

    return "\n".join(lines)


# --------------------------------------------------
# ISPIS I SPREMANJE
# --------------------------------------------------

def save_report(report):
    """Sprema izvještaj u output mapu."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        REPORT_FILE.write_text(report, encoding="utf-8")
        print(f"\n✅ Izvještaj spremljen: {REPORT_FILE}")

    except OSError as error:
        print(f"\n❌ Greška pri spremanju izvještaja: {error}")


# --------------------------------------------------
# GLAVNA FUNKCIJA
# --------------------------------------------------

def main():

    if len(sys.argv) > 2:
        print("Korištenje: python analyze_metrics.py [datoteka.csv]")
        sys.exit(1)

    if len(sys.argv) == 2:
        path = Path(sys.argv[1])

        if not path.is_absolute():
            path = BASE_DIR / path
    else:
        path = DEFAULT_CSV

    # Ako glavna datoteka ne postoji, koristi predložak.
    if not path.exists() and TEMPLATE_CSV.exists():
        print(
            f"⚠️ {path.name} ne postoji. "
            "Koristim metrics_template.csv kao primjer.\n"
        )
        path = TEMPLATE_CSV

    print("\n🚀 Dida Boža – Instagram Analytics")
    print("=" * 45)

    rows = load_metrics(path)

    print(f"📂 Učitana datoteka: {path.name}")
    print(f"📊 Broj redaka: {len(rows)}")

    metrics = analyze(rows)

    report = generate_report(metrics)

    print("\n" + report)

    save_report(report)

    print("\n✅ Analiza završena.")


if __name__ == "__main__":
    main()
