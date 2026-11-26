
import sys
import pandas as pd

METRICS = ["lajkovi", "komentari", "saves", "doseg"]


def load_metrics(path):
    df = pd.read_csv(path)
    required = ["datum", "tip_objave"] + METRICS

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Nedostaju stupci: {missing}")

    for col in METRICS:
        df[col] = pd.to_numeric(df[col], errors="raise")

    return df


def summarize(df):
    result = df[METRICS].mean()
    result["engagement_rate"] = (
        (df["lajkovi"] + df["komentari"] + df["saves"])
        / df["doseg"].replace(0, float("nan"))
        * 100
    ).mean()

    return result


def compare(old, new):
    old_stats = summarize(old)
    new_stats = summarize(new)

    print("\nDIDA BOŽA – USPOREDBA REZULTATA")
    print("=" * 55)

    for metric in old_stats.index:
        before = old_stats[metric]
        after = new_stats[metric]
        difference = after - before

        if before != 0:
            change = difference / abs(before) * 100
            change_text = f"{change:+.2f}%"
        else:
            change_text = "N/A"

        print(f"\n{metric}")
        print(f"  Prethodno: {before:.2f}")
        print(f"  Novo:      {after:.2f}")
        print(f"  Promjena:  {difference:+.2f} ({change_text})")


def main():
    if len(sys.argv) != 3:
        print("Upotreba: python compare_metrics.py stari.csv novi.csv")
        return

    try:
        old = load_metrics(sys.argv[1])
        new = load_metrics(sys.argv[2])
        compare(old, new)
    except Exception as error:
        print(f"Greška: {error}")


if __name__ == "__main__":
    main()
