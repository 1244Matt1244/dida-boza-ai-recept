
"""
DIDA BOŽA — INSTAGRAM ANALYTICS DASHBOARD

Usporedba prethodnog i novog razdoblja.
Pet odvojenih grafikona, KPI pokazatelji i postotne promjene.

Pokretanje:
python create_dashboard.py metrics_demo_old.csv metrics_demo_new.csv
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


METRICS = ["lajkovi", "komentari", "saves", "doseg"]

LABELS = {
    "lajkovi": "Lajkovi",
    "komentari": "Komentari",
    "saves": "Spremanja",
    "doseg": "Doseg",
    "engagement": "Engagement rate"
}


def load_data(path):
    df = pd.read_csv(path)

    required = METRICS

    for column in required:
        if column not in df.columns:
            raise ValueError(f"Nedostaje stupac: {column}")

        df[column] = pd.to_numeric(
            df[column], errors="raise"
        )

        if df[column].isna().any():
            raise ValueError(
                f"Stupac {column} sadrži prazne vrijednosti."
            )

        if (df[column] < 0).any():
            raise ValueError(
                f"Stupac {column} sadrži negativne vrijednosti."
            )

    return df


def calculate_engagement(df):
    rates = []

    for _, row in df.iterrows():
        reach = row["doseg"]

        if reach <= 0:
            rates.append(float("nan"))
            continue

        interactions = (
            row["lajkovi"]
            + row["komentari"]
            + row["saves"]
        )

        rates.append(interactions / reach * 100)

    return pd.Series(rates, index=df.index)


def calculate_metrics(df):
    values = {
        metric: df[metric].mean()
        for metric in METRICS
    }

    engagement = calculate_engagement(df)

    values["engagement"] = engagement.mean()

    return values


def format_value(metric, value):
    if pd.isna(value):
        return "N/A"

    if metric == "engagement":
        return f"{value:.2f}%"

    return f"{value:,.0f}".replace(",", " ")


def percentage_change(old, new):
    if pd.isna(old) or pd.isna(new):
        return None

    if old == 0:
        if new == 0:
            return 0.0
        return None

    return (new - old) / abs(old) * 100


def create_dashboard(old_df, new_df):
    old = calculate_metrics(old_df)
    new = calculate_metrics(new_df)

    metrics = METRICS + ["engagement"]

    # Vizualni identitet
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
    })

    fig = plt.figure(figsize=(15, 12))

    fig.suptitle(
        "DIDA BOŽA | INSTAGRAM PERFORMANCE",
        fontsize=21,
        fontweight="bold",
        y=0.98
    )

    fig.text(
        0.5, 0.945,
        "PRETHODNO RAZDOBLJE  vs.  NOVO RAZDOBLJE",
        ha="center",
        fontsize=11,
        color="dimgray"
    )

    # KPI pokazatelji
    kpi_metrics = [
        "lajkovi",
        "komentari",
        "saves",
        "doseg",
        "engagement"
    ]

    for index, metric in enumerate(kpi_metrics):
        change = percentage_change(
            old[metric], new[metric]
        )

        if change is None:
            change_text = "N/A"
        else:
            sign = "+" if change > 0 else ""
            change_text = f"{sign}{change:.1f}%"

        ax = fig.add_axes([
            0.055 + index * 0.185,
            0.815,
            0.165,
            0.09
        ])

        ax.set_facecolor("#F3F0E8")
        ax.set_xticks([])
        ax.set_yticks([])

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.text(
            0.5, 0.76,
            LABELS[metric],
            ha="center",
            fontsize=9,
            color="#555555"
        )

        ax.text(
            0.5, 0.28,
            change_text,
            ha="center",
            fontsize=17,
            fontweight="bold",
            color="#397A55" if change is not None and change >= 0
            else "#A94442"
        )

    # Pet odvojenih grafikona
    positions = [
        [0.08, 0.57, 0.38, 0.19],
        [0.55, 0.57, 0.38, 0.19],
        [0.08, 0.34, 0.38, 0.19],
        [0.55, 0.34, 0.38, 0.19],
        [0.30, 0.11, 0.40, 0.19],
    ]

    colors = ["#B7A58A", "#557A5C"]

    for metric, position in zip(metrics, positions):
        ax = fig.add_axes(position)

        old_value = old[metric]
        new_value = new[metric]

        bars = ax.bar(
            ["Prethodno", "Novo"],
            [old_value, new_value],
            color=colors,
            width=0.48
        )

        ax.set_title(LABELS[metric], pad=10)

        ax.yaxis.set_major_locator(MaxNLocator(5))
        ax.grid(
            axis="y",
            alpha=0.22,
            linestyle="--"
        )

        ax.set_axisbelow(True)

        for bar, value in zip(
            bars, [old_value, new_value]
        ):
            if pd.notna(value):
                label = format_value(metric, value)

                ax.annotate(
                    label,
                    (bar.get_x() + bar.get_width() / 2,
                     bar.get_height()),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center",
                    fontsize=9,
                    fontweight="bold"
                )

        maximum = max(
            old_value if pd.notna(old_value) else 0,
            new_value if pd.notna(new_value) else 0
        )

        ax.set_ylim(0, maximum * 1.25 if maximum > 0 else 1)

        if metric == "engagement":
            ax.set_ylabel("%")
        else:
            ax.set_ylabel("Prosjek po objavi")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.text(
        0.5,
        0.035,
        (
            f"Objave: {len(old_df)} prethodno | "
            f"{len(new_df)} novo razdoblje\n"
            "Demo / simulirani podaci – "
            "nije stvarna Instagram analitika."
        ),
        ha="center",
        fontsize=9,
        color="dimgray"
    )

    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "metrics_dashboard.png"

    fig.savefig(
        output_file,
        dpi=180,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)

    print(f"Dashboard spremljen: {output_file}")


def main():
    if len(sys.argv) != 3:
        print(
            "Upotreba: python create_dashboard.py "
            "prethodno.csv novo.csv"
        )
        sys.exit(1)

    try:
        old_df = load_data(sys.argv[1])
        new_df = load_data(sys.argv[2])

        create_dashboard(old_df, new_df)

    except Exception as error:
        print(f"Greška: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
