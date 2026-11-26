
"""
DIDA BOŽA — NAPREDNA INSTAGRAM ANALITIKA

Značajke:
- Učitavanje i validacija CSV datoteka
- Normalizacija numeričkih vrijednosti
- Analiza kvalitete podataka
- Prosječni i ponderirani engagement rate
- Analiza prema tipu objave i danu u tjednu
- Analiza hashtagova
- Prepoznavanje najboljih rezultata
- Automatske preporuke
- Izvoz izvještaja u TXT datoteku

Ne koristi API niti zahtijeva plaćene servise.
"""

import argparse
import csv
import re
import sys

from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime


# ============================================================
# POSTAVKE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

DEFAULT_METRICS_FILE = BASE_DIR / "metrics_demo_new.csv"

REQUIRED_COLUMNS = {
    "datum",
    "tip_objave",
    "lajkovi",
    "komentari",
    "saves",
    "doseg",
    "hashtagovi",
}

NUMERIC_COLUMNS = (
    "lajkovi",
    "komentari",
    "saves",
    "doseg",
)

MIN_SAMPLE_SIZE = 5


# ============================================================
# POMOĆNE FUNKCIJE
# ============================================================

def parse_number(value):
    """Pretvara broj ili tekst u cijeli broj."""

    if value is None:
        return None

    text = str(value).strip().replace(" ", "")

    if not text:
        return None

    if text.lower() in {
        "nan", "none", "null", "n/a", "na", "-"
    }:
        return None

    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", text):
        text = text.replace(".", "").replace(",", "")
    else:
        text = text.replace(",", ".")

    try:
        number = float(text)

        if not number.is_integer():
            return None

        return int(number)

    except (ValueError, TypeError):
        return None


def parse_date(value):
    """Pretvara podržane formate datuma u datetime."""

    if not value:
        return None

    value = str(value).strip()

    formats = (
        "%d.%m.%Y.",
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
    )

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue

    return None


def average(values):
    """Izračun prosjeka bez nedostajućih vrijednosti."""

    valid = [
        value for value in values
        if value is not None
    ]

    if not valid:
        return None

    return sum(valid) / len(valid)


def format_average(value, decimals=0):
    """Formatiranje broja s decimalnom točkom."""

    if value is None:
        return "N/A"

    return f"{value:.{decimals}f}"


def safe_percentage(numerator, denominator):
    """Sigurno izračunavanje postotka."""

    if denominator is None or denominator <= 0:
        return None

    return numerator / denominator * 100


def normalize_text(value):
    """Normalizacija teksta."""

    return str(value or "").strip().lower()


# ============================================================
# UČITAVANJE CSV PODATAKA
# ============================================================

def load_metrics(path):
    """Učitava i validira CSV datoteku."""

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Datoteka ne postoji: {path}"
        )

    rows = []

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError(
                    "CSV datoteka nema zaglavlje."
                )

            headers = {
                str(header).strip().lower()
                for header in reader.fieldnames
                if header
            }

            missing = REQUIRED_COLUMNS - headers

            if missing:
                raise ValueError(
                    "Nedostaju obavezni stupci: "
                    + ", ".join(sorted(missing))
                )

            for row_number, raw_row in enumerate(
                reader,
                start=2
            ):

                row = {
                    str(key).strip().lower(): (
                        value.strip()
                        if isinstance(value, str)
                        else value
                    )
                    for key, value in raw_row.items()
                    if key
                }

                for column in NUMERIC_COLUMNS:
                    row[column] = parse_number(
                        row.get(column)
                    )

                row["datum_parsed"] = parse_date(
                    row.get("datum")
                )

                row["tip_objave"] = str(
                    row.get("tip_objave") or ""
                ).strip()

                row["hashtagovi"] = str(
                    row.get("hashtagovi") or ""
                ).strip()

                row["_row_number"] = row_number

                rows.append(row)

    except UnicodeDecodeError as exc:
        raise ValueError(
            "CSV nije moguće pročitati kao UTF-8 datoteku."
        ) from exc

    except csv.Error as exc:
        raise ValueError(
            f"Greška pri čitanju CSV datoteke: {exc}"
        ) from exc

    if not rows:
        raise ValueError(
            "CSV datoteka ne sadrži podatke."
        )

    return rows


# ============================================================
# KVALITETA PODATAKA
# ============================================================

def analyze_data_quality(rows):
    """Provjerava kvalitetu podataka."""

    result = {
        "total_rows": len(rows),
        "invalid_dates": 0,
        "missing_types": 0,
        "missing_metrics": 0,
        "negative_values": 0,
        "zero_reach": 0,
        "missing_reach": 0,
        "quality_issues": 0,
    }

    for row in rows:

        date = row.get("datum_parsed")

        if date is None:
            date = parse_date(row.get("datum"))

        if date is None:
            result["invalid_dates"] += 1

        if not row.get("tip_objave"):
            result["missing_types"] += 1

        for column in NUMERIC_COLUMNS:

            value = parse_number(row.get(column))

            if value is None:
                result["missing_metrics"] += 1

                if column == "doseg":
                    result["missing_reach"] += 1

            elif value < 0:
                result["negative_values"] += 1

        reach = parse_number(row.get("doseg"))

        if reach == 0:
            result["zero_reach"] += 1

    result["quality_issues"] = (
        result["invalid_dates"]
        + result["missing_types"]
        + result["missing_metrics"]
        + result["negative_values"]
    )

    return result


# ============================================================
# ENGAGEMENT RATE
# ============================================================

def calculate_engagement(row):
    """Izračun engagement ratea jedne objave."""

    likes = parse_number(row.get("lajkovi"))
    comments = parse_number(row.get("komentari"))
    saves = parse_number(row.get("saves"))
    reach = parse_number(row.get("doseg"))

    if reach is None or reach <= 0:
        return None

    values = (likes, comments, saves)

    if any(
        value is not None and value < 0
        for value in values
    ):
        return None

    likes = likes or 0
    comments = comments or 0
    saves = saves or 0

    return safe_percentage(
        likes + comments + saves,
        reach
    )


# ============================================================
# GRUPIRANJE
# ============================================================

def group_average(groups, metric=None):
    """Izračun prosjeka po grupama."""

    result = {}

    for key, values in groups.items():

        if metric is not None:
            if not isinstance(values, dict):
                continue

            values = values.get(metric, [])

        elif isinstance(values, dict):
            values = values.get("engagement", [])

        result[key] = average(values)

    return result


def best_group(groups, metric=None):
    """Pronalazi grupu s najboljim prosjekom."""

    averages = group_average(groups, metric)

    valid = {
        key: value
        for key, value in averages.items()
        if value is not None
    }

    if not valid:
        return None, None

    best = max(
        valid,
        key=valid.get
    )

    return best, valid[best]


# ============================================================
# GLAVNA ANALIZA
# ============================================================

def analyze(rows):
    """Analizira objave i vraća strukturirane rezultate."""

    if not rows:
        raise ValueError(
            "Nema podataka za analizu."
        )

    rows = [dict(row) for row in rows]

    for row in rows:

        for column in NUMERIC_COLUMNS:
            row[column] = parse_number(
                row.get(column)
            )

        if row.get("datum_parsed") is None:
            row["datum_parsed"] = parse_date(
                row.get("datum")
            )

    by_type = defaultdict(list)
    by_weekday = defaultdict(list)
    hashtags = Counter()

    engagement_rates = []
    invalid_dates = 0
    zero_reach = 0

    total_engagement = 0
    total_reach = 0

    # Osnovne numeričke metrike.
    metric_values = {
        column: [
            row.get(column)
            for row in rows
        ]
        for column in NUMERIC_COLUMNS
    }

    averages = {
        column: average(values)
        for column, values in metric_values.items()
    }

    # Analiza pojedinačnih objava.
    for row in rows:

        engagement = calculate_engagement(row)

        row["engagement_rate"] = engagement

        if engagement is not None:

            engagement_rates.append(engagement)

            total_engagement += (
                (row.get("lajkovi") or 0)
                + (row.get("komentari") or 0)
                + (row.get("saves") or 0)
            )

            total_reach += row["doseg"]

        # Datum i dan u tjednu.
        date = row.get("datum_parsed")

        if date is None:
            invalid_dates += 1
        else:
            weekday = date.strftime("%A")
            by_weekday[weekday].append(engagement)

        # Objave bez dosega.
        if row.get("doseg") == 0:
            zero_reach += 1

        # Tip objave.
        post_type = normalize_text(
            row.get("tip_objave")
        )

        if post_type and engagement is not None:
            by_type[post_type].append(engagement)

        # Hashtagovi.
        found_hashtags = re.findall(
            r"#[\wčćžšđČĆŽŠĐ]+",
            row.get("hashtagovi", ""),
            flags=re.UNICODE
        )

        for hashtag in found_hashtags:
            hashtags[hashtag.lower()] += 1

    average_er = average(engagement_rates)

    weighted_er = safe_percentage(
        total_engagement,
        total_reach
    )

    data_quality = analyze_data_quality(rows)

    # Strukturirani rezultati prema tipu objave.
    # Ovaj format omogućuje best_group(po_tipu, "engagement").
    po_tipu = {
        name: {
            "engagement": values
        }
        for name, values in by_type.items()
    }

    result = {
        # Izvorni engleski ključevi.
        "total_posts": len(rows),
        "averages": averages,
        "engagement_rates": engagement_rates,
        "average_engagement_rate": average_er,
        "weighted_engagement_rate": weighted_er,
        "total_engagement": total_engagement,
        "total_reach": total_reach,
        "by_type": dict(by_type),
        "by_weekday": dict(by_weekday),
        "hashtags": hashtags,
        "invalid_dates": invalid_dates,
        "zero_reach": zero_reach,
        "data_quality": data_quality,

        # Kompatibilnost s hrvatskim ključevima.
        "ukupno_objava": len(rows),
        "lajkovi": metric_values["lajkovi"],
        "komentari": metric_values["komentari"],
        "saves": metric_values["saves"],
        "doseg": metric_values["doseg"],
        "interakcije": engagement_rates,
        "po_tipu": po_tipu,
        "hashtagovi": hashtags,
        "neispravni_datumi": invalid_dates,
        "objave_bez_dosega": zero_reach,
    }

    return result


# ============================================================
# AUTOMATSKE PREPORUKE
# ============================================================

def generate_recommendations(result):
    """Generira preporuke na temelju analize."""

    recommendations = []

    if result["total_posts"] < MIN_SAMPLE_SIZE:

        recommendations.append(
            f"Uzorak je malen. Prikupite najmanje "
            f"{MIN_SAMPLE_SIZE} objava prije donošenja "
            "čvrstih zaključaka."
        )

    average_er = result["average_engagement_rate"]
    weighted_er = result["weighted_engagement_rate"]

    if average_er is not None and weighted_er is not None:

        if weighted_er > average_er:

            recommendations.append(
                "Ponderirani ER veći je od prosječnog ER-a "
                "po objavi. Objave s većim dosegom relativno "
                "dobro doprinose ukupnom angažmanu."
            )

        elif weighted_er < average_er:

            recommendations.append(
                "Ponderirani ER niži je od prosječnog ER-a "
                "po objavi. Provjerite rezultate objava "
                "s najvećim dosegom."
            )

    best_type, best_type_value = best_group(
        result["by_type"]
    )

    if best_type is not None:

        recommendations.append(
            f"Najbolji tip objave u ovom uzorku je "
            f"'{best_type}' s prosječnim ER-om "
            f"{best_type_value:.2f}%."
        )

    best_day, best_day_value = best_group(
        result["by_weekday"]
    )

    if best_day is not None:

        recommendations.append(
            f"Najbolji dan u analiziranom uzorku je "
            f"{best_day} ({best_day_value:.2f}% ER)."
        )

    if result["data_quality"]["quality_issues"] > 0:

        recommendations.append(
            "Prije donošenja zaključaka provjerite kvalitetu "
            "podataka i ispravite nedostajuće ili neispravne vrijednosti."
        )

    if not recommendations:

        recommendations.append(
            "Nema dovoljno podataka za specifične preporuke."
        )

    return recommendations


# ============================================================
# IZVJEŠTAJ
# ============================================================

def generate_report(result):
    """Generira tekstualni izvještaj."""

    lines = []

    lines.append("=" * 65)
    lines.append("DIDA BOŽA — INSTAGRAM ANALYTICS REPORT")
    lines.append("=" * 65)

    lines.append(
        f"\nUkupno analiziranih objava: {result['total_posts']}"
    )

    # Osnovne metrike.
    lines.append("\n1. PROSJEČNE METRIKE")
    lines.append("-" * 45)

    labels = {
        "lajkovi": "Prosječno lajkova",
        "komentari": "Prosječno komentara",
        "saves": "Prosječno spremanja",
        "doseg": "Prosječni doseg",
    }

    for key, label in labels.items():

        value = result["averages"].get(key)

        lines.append(
            f"{label}: {format_average(value, 2)}"
        )

    # Engagement.
    lines.append("\n2. ENGAGEMENT RATE")
    lines.append("-" * 45)

    lines.append(
        "Prosječni ER po objavi: "
        + format_average(
            result["average_engagement_rate"], 2
        )
        + "%"
    )

    lines.append(
        "Ponderirani ER: "
        + format_average(
            result["weighted_engagement_rate"], 2
        )
        + "%"
    )

    lines.append(
        f"Ukupni angažman: {result['total_engagement']}"
    )

    lines.append(
        f"Ukupni doseg: {result['total_reach']}"
    )

    # Tip objave.
    lines.append("\n3. REZULTATI PREMA TIPU OBJAVE")
    lines.append("-" * 45)

    type_averages = group_average(
        result["by_type"]
    )

    if type_averages:

        for name, value in sorted(
            type_averages.items(),
            key=lambda item: (
                item[1] is not None,
                item[1] if item[1] is not None else -1
            ),
            reverse=True
        ):

            lines.append(
                f"{name.upper()}: {format_average(value, 2)}%"
            )

    else:
        lines.append("Nema dostupnih podataka.")

    best_type, best_type_value = best_group(
        result["by_type"]
    )

    if best_type is not None:

        lines.append(
            f"\nNajuspješniji tip objave: "
            f"{best_type.upper()} ({best_type_value:.2f}%)"
        )

    # Dan u tjednu.
    lines.append("\n4. REZULTATI PREMA DANU")
    lines.append("-" * 45)

    weekday_averages = group_average(
        result["by_weekday"]
    )

    if weekday_averages:

        for name, value in sorted(
            weekday_averages.items(),
            key=lambda item: (
                item[1] is not None,
                item[1] if item[1] is not None else -1
            ),
            reverse=True
        ):

            lines.append(
                f"{name}: {format_average(value, 2)}%"
            )

    else:
        lines.append("Nema dostupnih podataka.")

    # Hashtagovi.
    lines.append("\n5. HASHTAGOVI")
    lines.append("-" * 45)

    if result["hashtags"]:

        for hashtag, count in result["hashtags"].most_common(10):
            lines.append(
                f"{hashtag}: {count}"
            )

    else:
        lines.append("Nema pronađenih hashtagova.")

    # Kvaliteta podataka.
    quality = result["data_quality"]

    lines.append("\n6. KVALITETA PODATAKA")
    lines.append("-" * 45)

    lines.append(
        f"Neispravni datumi: {quality['invalid_dates']}"
    )

    lines.append(
        f"Nedostajući tipovi objava: {quality['missing_types']}"
    )

    lines.append(
        f"Nedostajuće numeričke vrijednosti: "
        f"{quality['missing_metrics']}"
    )

    lines.append(
        f"Negativne vrijednosti: {quality['negative_values']}"
    )

    lines.append(
        f"Nedostajući doseg: {quality['missing_reach']}"
    )

    lines.append(
        f"Objave s dosegom 0: {quality['zero_reach']}"
    )

    # Preporuke.
    lines.append("\n7. PREPORUKE")
    lines.append("-" * 45)

    recommendations = generate_recommendations(
        result
    )

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        lines.append(
            f"{index}. {recommendation}"
        )

    lines.append("\n" + "=" * 65)

    lines.append(
        "Napomena: Engagement rate izračunat je kao "
        "(lajkovi + komentari + spremanja) / doseg × 100."
    )

    lines.append(
        "Rezultati opisuju isključivo podatke iz učitane CSV datoteke."
    )

    lines.append("=" * 65)

    return "\n".join(lines)


# ============================================================
# SPREMANJE IZVJEŠTAJA
# ============================================================

def save_report(report, path=None):
    """Sprema izvještaj u TXT datoteku."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if path is None:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        path = OUTPUT_DIR / (
            f"instagram_report_{timestamp}.txt"
        )

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        report,
        encoding="utf-8"
    )

    return path


# ============================================================
# CLI
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Dida Boža — napredna Instagram analiza"
    )

    parser.add_argument(
        "--file",
        default=str(DEFAULT_METRICS_FILE),
        help="Putanja do CSV datoteke"
    )

    parser.add_argument(
        "--output",
        help="Putanja za spremanje izvještaja"
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Prikaži izvještaj bez spremanja"
    )

    args = parser.parse_args()

    try:

        rows = load_metrics(args.file)

        result = analyze(rows)

        report = generate_report(result)

        print(report)

        if not args.no_save:

            path = save_report(
                report,
                args.output
            )

            print(
                f"\nIzvještaj spremljen: {path}"
            )

    except (FileNotFoundError, ValueError) as exc:

        print(
            f"\nGREŠKA: {exc}",
            file=sys.stderr
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
