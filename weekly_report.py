
import sys
from pathlib import Path
import pandas as pd

METRICS = ["lajkovi", "komentari", "saves", "doseg"]


def load_data(path):
    df = pd.read_csv(path)

    required = ["datum", "tip_objave"] + METRICS
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Nedostaju stupci: {missing}")

    for col in METRICS:
        df[col] = pd.to_numeric(df[col], errors="raise")

    df["engagement_rate"] = (
        (df["lajkovi"] + df["komentari"] + df["saves"])
        / df["doseg"].replace(0, float("nan"))
        * 100
    )

    return df


def average_metrics(df):
    return {
        "Objave": len(df),
        "Prosječno lajkova": df["lajkovi"].mean(),
        "Prosječno komentara": df["komentari"].mean(),
        "Prosječno spremanja": df["saves"].mean(),
        "Prosječan doseg": df["doseg"].mean(),
        "Prosječan engagement rate": df["engagement_rate"].mean()
    }


def build_report(old_df, new_df):
    old = average_metrics(old_df)
    new = average_metrics(new_df)

    lines = [
        "DIDA BOŽA – TJEDNI IZVJEŠTAJ",
        "=" * 55,
        "",
        "NAPOMENA: Izvještaj koristi demo/simulirane podatke.",
        "",
        "1. REZULTATI NOVOG RAZDOBLJA",
        "-" * 55
    ]

    for metric, value in new.items():
        if metric == "Objave":
            lines.append(f"{metric}: {value}")
        else:
            lines.append(f"{metric}: {value:.2f}")

    lines += [
        "",
        "2. USPOREDBA S PRETHODNIM RAZDOBLJEM",
        "-" * 55
    ]

    for metric in old:
        before = old[metric]
        after = new[metric]
        difference = after - before

        if before != 0:
            percent = difference / abs(before) * 100
            change = f"{percent:+.2f}%"
        else:
            change = "N/A"

        lines.append(
            f"{metric}: {difference:+.2f} ({change})"
        )

    lines += [
        "",
        "3. REZULTATI PO TIPU OBJAVE",
        "-" * 55
    ]

    grouped = new_df.groupby("tip_objave")

    for post_type, group in grouped:
        rate = group["engagement_rate"].mean()
        lines.append(
            f"{post_type.upper()}: "
            f"{len(group)} objave | "
            f"Prosječan engagement rate: {rate:.2f}%"
        )

    best_type = (
        new_df.groupby("tip_objave")["engagement_rate"]
        .mean()
        .idxmax()
    )

    lines += [
        "",
        "4. AUTOMATSKI ZAKLJUČAK",
        "-" * 55,
        f"Najuspješniji tip objave prema engagement rateu: "
        f"{best_type.upper()}.",
        "",
        "Preporuka: nastaviti testirati uspješnije formate "
        "i pratiti rezultate kroz veći broj objava.",
        "",
        "Napomena: mali uzorak nije dovoljan za pouzdane "
        "dugoročne zaključke.",
        "",
        "Izvještaj je generiran lokalno pomoću Pythona.",
        "Dodatni AI API pozivi nisu korišteni."
    ]

    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print(
            "Upotreba: python weekly_report.py "
            "prethodno.csv novo.csv"
        )
        return

    try:
        old_df = load_data(sys.argv[1])
        new_df = load_data(sys.argv[2])

        report = build_report(old_df, new_df)

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "weekly_report.txt"
        output_file.write_text(report, encoding="utf-8")

        print(report)
        print(f"\nIzvještaj spremljen: {output_file}")

    except Exception as error:
        print(f"Greška: {error}")


if __name__ == "__main__":
    main()
