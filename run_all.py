
"""
DIDA BOŽA — END-TO-END PIPELINE

Besplatni workflow:
1. Priprema prompta za ChatGPT
2. Izrada vizuala / carousel u lokalnoj skripti
3. Priprema uputa za Canvu
4. Analiza Instagram metrika
5. Usporedba rezultata
6. Izrada tjednog izvještaja
7. Izrada dashboarda

Nema automatskih API poziva.
"""

import argparse
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def run_script(script_name, *args):
    """Pokreće Python skriptu iz glavne mape projekta."""
    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"GREŠKA: Ne postoji datoteka {script_name}")
        return False

    command = [sys.executable, str(script_path)]
    command.extend(str(arg) for arg in args)

    result = subprocess.run(command, cwd=BASE_DIR)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description="Dida Boža — besplatni AI content i analytics pipeline"
    )
    parser.add_argument(
        "--save-content",
        action="store_true",
        help="Ručno spremanje sadržaja generiranog u ChatGPT-u"
    )
    parser.add_argument(
        "--skip-analytics",
        action="store_true",
        help="Preskače analizu i izvještaje"
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    print("\n" + "=" * 55)
    print("DIDA BOŽA — AUTOMATIZIRANI PIPELINE")
    print("Besplatni način rada — bez API poziva")
    print("=" * 55)

    # 1. Priprema prompta ili ručno spremanje sadržaja
    print("\n[1/7] PRIPREMA AI SADRŽAJA")

    if args.save_content:
        success = run_script("generate_content.py", "--save-content")
    else:
        success = run_script("generate_content.py")

    if not success:
        print("Greška u pripremi sadržaja. Pipeline je zaustavljen.")
        sys.exit(1)

    if args.save_content:
        print("\nSadržaj je spremljen.")
        print("Sljedeće možeš pokrenuti pipeline bez --save-content.")
        return

    # 2. Izrada carousela
    print("\n[2/7] IZRADA CAROUSELA")

    if not run_script("make_carousel.py"):
        print("Upozorenje: carousel nije izrađen.")

    # 3. Upute za Canvu
    print("\n[3/7] PRIPREMA UPUTA ZA CANVU")

    canva_text = """DIDA BOŽA — UPUTE ZA CANVA VIZUALE

1. Koristiti vizualni identitet brenda.
2. Koristiti čitljivu tipografiju.
3. Istaknuti glavni proizvod ili temu objave.
4. Ostaviti dovoljno praznog prostora.
5. Prilagoditi format Instagram objavi (1080 x 1080).
6. Provjeriti pravopis i čitljivost teksta.

Napomena:
Ovo su upute za ručnu doradu u Canvi.
"""

    canva_path = OUTPUT_DIR / "canva_upute.txt"
    canva_path.write_text(canva_text, encoding="utf-8")
    print(f"Upute spremljene: {canva_path}")

    if args.skip_analytics:
        print("\nAnalitika je preskočena.")
        print("\nPIPELINE ZAVRŠEN.")
        return

    # 4. Analiza metrika
    print("\n[4/7] ANALIZA INSTAGRAM METRIKA")

    if not run_script("analyze_metrics.py", BASE_DIR / "metrics_demo_new.csv"):
        print("Upozorenje: analiza metrika nije uspjela.")

    # 5. Usporedba razdoblja
    print("\n[5/7] USPOREDBA REZULTATA")

    old_csv = BASE_DIR / "metrics_demo_old.csv"
    new_csv = BASE_DIR / "metrics_demo_new.csv"

    if old_csv.exists() and new_csv.exists():
        if not run_script(
            "compare_metrics.py",
            old_csv,
            new_csv
        ):
            print("Upozorenje: usporedba nije uspjela.")
    else:
        print("Nedostaju CSV datoteke za usporedbu.")

    # 6. Tjedni izvještaj
    print("\n[6/7] IZRADA TJEDNOG IZVJEŠTAJA")

    if old_csv.exists() and new_csv.exists():
        if not run_script(
            "weekly_report.py",
            old_csv,
            new_csv
        ):
            print("Upozorenje: tjedni izvještaj nije izrađen.")
    else:
        print("Nedostaju CSV datoteke za tjedni izvještaj.")

    # 7. Dashboard
    print("\n[7/7] IZRADA DASHBOARDA")

    if old_csv.exists() and new_csv.exists():
        if not run_script(
            "create_dashboard.py",
            old_csv,
            new_csv
        ):
            print("Upozorenje: dashboard nije izrađen.")
    else:
        print("Nedostaju CSV datoteke za dashboard.")

    print("\n" + "=" * 55)
    print("PIPELINE ZAVRŠEN")
    print("Provjeri mapu output/ za rezultate.")
    print("Napomena: demo metrike su simulirani podaci.")
    print("Nema plaćenih API poziva.")
    print("=" * 55)


if __name__ == "__main__":
    main()
