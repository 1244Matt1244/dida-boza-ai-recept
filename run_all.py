
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
    """Pokreće Python skriptu i vraća informaciju o uspjehu."""
    script_path = BASE_DIR / script_name

    if not script_path.exists():
        print(f"GREŠKA: Ne postoji datoteka {script_name}")
        return False

    command = [sys.executable, str(script_path)]
    command.extend(str(arg) for arg in args)

    try:
        result = subprocess.run(command, cwd=BASE_DIR)
        return result.returncode == 0
    except OSError as error:
        print(f"GREŠKA pri pokretanju {script_name}: {error}")
        return False


def print_summary(statuses):
    """Prikazuje završni pregled svih koraka."""
    print("\n" + "=" * 55)
    print("ZAVRŠNI PREGLED PIPELINEA")
    print("=" * 55)

    for step, status in statuses:
        print(f"{step:<38} {status}")

    failed = sum(status == "NEUSPJEŠNO" for _, status in statuses)
    skipped = sum(status == "PRESKOČENO" for _, status in statuses)
    successful = sum(status == "USPJEŠNO" for _, status in statuses)

    print("-" * 55)
    print(f"Uspješno:    {successful}")
    print(f"Neuspješno:  {failed}")
    print(f"Preskočeno:  {skipped}")
    print("=" * 55)

    if failed:
        print("\nPIPELINE ZAVRŠEN S GREŠKAMA.")
        print("Provjeri poruke iznad i popravi neuspješne korake.")
        return False

    print("\nPIPELINE USPJEŠNO ZAVRŠEN.")
    print("Provjeri mapu output/ za rezultate.")
    return True


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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    statuses = []

    print("\n" + "=" * 55)
    print("DIDA BOŽA — AUTOMATIZIRANI PIPELINE")
    print("Besplatni način rada — bez API poziva")
    print("=" * 55)

    # 1. Priprema prompta ili ručno spremanje sadržaja
    print("\n[1/7] PRIPREMA AI SADRŽAJA")

    if args.save_content:
        success = run_script(
            "generate_content.py",
            "--save-content"
        )
    else:
        success = run_script("generate_content.py")

    statuses.append((
        "1. Priprema AI sadržaja",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

    if not success:
        print("\nPriprema sadržaja nije uspjela.")
        print_summary(statuses)
        sys.exit(1)

    if args.save_content:
        print("\nSadržaj je spremljen.")
        print("Sljedeće pokreni pipeline bez --save-content.")
        print_summary(statuses)
        return

    # 2. Izrada carousela
    print("\n[2/7] IZRADA CAROUSELA")

    success = run_script("make_carousel.py")

    statuses.append((
        "2. Izrada carousela",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

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

    try:
        canva_path = OUTPUT_DIR / "canva_upute.txt"
        canva_path.write_text(canva_text, encoding="utf-8")
        print(f"Upute spremljene: {canva_path}")
        success = True
    except OSError as error:
        print(f"GREŠKA pri spremanju Canva uputa: {error}")
        success = False

    statuses.append((
        "3. Upute za Canvu",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

    # Analitika se može preskočiti
    if args.skip_analytics:
        print("\nAnalitika je preskočena.")

        for step in [
            "4. Analiza Instagram metrika",
            "5. Usporedba rezultata",
            "6. Tjedni izvještaj",
            "7. Dashboard",
        ]:
            statuses.append((step, "PRESKOČENO"))

        pipeline_success = print_summary(statuses)

        if not pipeline_success:
            sys.exit(1)

        return

    # CSV datoteke
    old_csv = BASE_DIR / "metrics_demo_old.csv"
    new_csv = BASE_DIR / "metrics_demo_new.csv"

    # 4. Analiza metrika
    print("\n[4/7] ANALIZA INSTAGRAM METRIKA")

    if new_csv.exists():
        success = run_script(
            "analyze_metrics.py",
            "--file",
            new_csv
        )
    else:
        print(f"GREŠKA: Nedostaje datoteka {new_csv}")
        success = False

    statuses.append((
        "4. Analiza Instagram metrika",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

    # 5. Usporedba rezultata
    print("\n[5/7] USPOREDBA REZULTATA")

    if old_csv.exists() and new_csv.exists():
        success = run_script(
            "compare_metrics.py",
            old_csv,
            new_csv
        )
    else:
        print("GREŠKA: Nedostaju CSV datoteke za usporedbu.")
        success = False

    statuses.append((
        "5. Usporedba rezultata",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

    # 6. Tjedni izvještaj
    print("\n[6/7] IZRADA TJEDNOG IZVJEŠTAJA")

    if old_csv.exists() and new_csv.exists():
        success = run_script(
            "weekly_report.py",
            old_csv,
            new_csv
        )
    else:
        print("GREŠKA: Nedostaju CSV datoteke za tjedni izvještaj.")
        success = False

    statuses.append((
        "6. Tjedni izvještaj",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

    # 7. Dashboard
    print("\n[7/7] IZRADA DASHBOARDA")

    if old_csv.exists() and new_csv.exists():
        success = run_script(
            "create_dashboard.py",
            old_csv,
            new_csv
        )
    else:
        print("GREŠKA: Nedostaju CSV datoteke za dashboard.")
        success = False

    statuses.append((
        "7. Dashboard",
        "USPJEŠNO" if success else "NEUSPJEŠNO"
    ))

    # Završni pregled
    pipeline_success = print_summary(statuses)

    print("\nDodatne informacije:")
    print("- Rezultati se spremaju u mapu output/.")
    print("- Demo metrike su simulirani podaci.")
    print("- Nema plaćenih API poziva.")

    if not pipeline_success:
        sys.exit(1)


if __name__ == "__main__":
    main()
