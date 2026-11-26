
"""
Testovi za analyze_metrics.py.

Pokretanje:
    pytest tests/ -v
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from analyze_metrics import (
    parse_number,
    parse_date,
    average,
    format_average,
    load_metrics,
    analyze,
    best_group,
    generate_report,
)


def sample_rows():
    """Demo podaci za testiranje analitike."""
    return [
        {
            "datum": "2026-12-02",
            "tip_objave": "interakcija",
            "lajkovi": "150",
            "komentari": "25",
            "saves": "35",
            "doseg": "3800",
            "hashtagovi": "#DidaBoza #Smokva",
        },
        {
            "datum": "2026-12-04",
            "tip_objave": "edukacija",
            "lajkovi": "130",
            "komentari": "20",
            "saves": "65",
            "doseg": "3300",
            "hashtagovi": "#DidaBoza #Brunch",
        },
        {
            "datum": "2026-12-06",
            "tip_objave": "emocija",
            "lajkovi": "180",
            "komentari": "30",
            "saves": "40",
            "doseg": "4700",
            "hashtagovi": "#DidaBoza #Tradicija",
        },
    ]


def test_parse_number():
    assert parse_number("3200") == 3200
    assert parse_number("3.200") == 3200
    assert parse_number("3,200") == 3200
    assert parse_number("") is None
    assert parse_number("abc") is None


def test_parse_date():
    assert parse_date("2026-12-02") is not None
    assert parse_date("02.12.2026.") is not None
    assert parse_date("invalid-date") is None


def test_average():
    assert average([10, 20, 30]) == 20
    assert average([10, None, 30]) == 20
    assert average([None, None]) is None


def test_format_average():
    assert format_average(5.789, 2) == "5.79"
    assert format_average(None) == "N/A"


def test_analyze_counts_three_posts():
    metrics = analyze(sample_rows())

    assert metrics["ukupno_objava"] == 3


def test_analyze_calculates_average_metrics():
    metrics = analyze(sample_rows())

    assert round(average(metrics["lajkovi"]), 2) == 153.33
    assert average(metrics["komentari"]) == 25
    assert round(average(metrics["saves"]), 2) == 46.67
    assert round(average(metrics["doseg"]), 2) == 3933.33


def test_analyze_calculates_engagement_rate():
    metrics = analyze(sample_rows())

    assert round(average(metrics["interakcije"]), 2) == 5.79


def test_best_group_identifies_education():
    metrics = analyze(sample_rows())

    name, value = best_group(
        metrics["po_tipu"], "engagement"
    )

    assert name == "edukacija"
    assert round(value, 2) == 6.52


def test_analyze_counts_hashtags():
    metrics = analyze(sample_rows())

    assert metrics["hashtagovi"]["#didaboza"] == 3
    assert metrics["hashtagovi"]["#smokva"] == 1


def test_analyze_handles_invalid_date():
    rows = sample_rows()
    rows[0]["datum"] = "neispravan datum"

    metrics = analyze(rows)

    assert metrics["neispravni_datumi"] == 1


def test_analyze_handles_zero_reach():
    rows = sample_rows()
    rows[0]["doseg"] = "0"

    metrics = analyze(rows)

    assert metrics["objave_bez_dosega"] == 1


def test_generate_report_contains_results():
    metrics = analyze(sample_rows())
    report = generate_report(metrics)

    assert "Ukupno analiziranih objava: 3" in report
    assert "EDUKACIJA" in report
    assert "6.52%" in report


def test_load_metrics_reads_csv(tmp_path):
    csv_file = tmp_path / "test_metrics.csv"

    csv_file.write_text(
        "datum,tip_objave,lajkovi,komentari,saves,doseg,hashtagovi\n"
        "2026-12-02,edukacija,100,20,30,2000,#DidaBoza\n",
        encoding="utf-8",
    )

    rows = load_metrics(csv_file)

    assert len(rows) == 1
    assert rows[0]["tip_objave"] == "edukacija"
