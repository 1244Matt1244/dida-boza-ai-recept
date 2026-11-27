
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import streamlit as st

from generate_content import load_brand_voice, build_prompt
from analyze_metrics import (
    load_metrics,
    analyze,
    generate_report,
)


# ==================================================
# PUTANJE I POSTAVKE
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

EXAMPLES_FILE = BASE_DIR / "brand_voice_examples.txt"
CAROUSEL_DIR = BASE_DIR / "images" / "karusel"
CAROUSEL_SCRIPT = BASE_DIR / "make_carousel.py"

OLD_CSV = BASE_DIR / "metrics_demo_old.csv"
NEW_CSV = BASE_DIR / "metrics_demo_new.csv"

WEEKLY_REPORT = OUTPUT_DIR / "weekly_report.txt"
DASHBOARD_FILE = OUTPUT_DIR / "metrics_dashboard.png"


st.set_page_config(
    page_title="Dida Boža – AI Content Studio",
    page_icon="🍯",
    layout="wide",
)


# ==================================================
# INICIJALIZACIJA SESIJE
# ==================================================

DEFAULTS = {
    "generated_prompt": "",
    "generated_content": "",
    "content_input": "",
    "analytics_result": None,
    "analytics_report": "",
    "analytics_filename": "",
    "comparison_output": "",
    "weekly_output": "",
    "dashboard_generated": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# POMOĆNE FUNKCIJE
# ==================================================

def validate_content(content):
    """Provjerava sadrži li tekst tri označene objave."""

    normalized = content.upper()

    found_posts = set(
        re.findall(
            r"(?m)^\s*(?:OBJAVA|POST)\s*([1-3])\b",
            normalized,
        )
    )

    return [
        number
        for number in ("1", "2", "3")
        if number not in found_posts
    ]


def clear_generated_content():
    """Briše uneseni i spremljeni sadržaj."""

    st.session_state.content_input = ""
    st.session_state.generated_content = ""


def get_carousel_slides():
    """Vraća pravilno imenovane PNG slajdove."""

    if not CAROUSEL_DIR.exists():
        return []

    slides = [
        slide
        for slide in CAROUSEL_DIR.glob("slajd_*.png")
        if slide.stem.split("_", 1)[1].isdigit()
    ]

    return sorted(
        slides,
        key=lambda slide: int(
            slide.stem.split("_", 1)[1]
        ),
    )


def run_local_script(script_name, *args):
    """Pokreće lokalnu Python skriptu i vraća rezultat."""

    script_path = BASE_DIR / script_name

    if not script_path.exists():
        return False, f"Nedostaje datoteka: {script_name}"

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                *[str(arg) for arg in args],
            ],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            timeout=180,
        )

        output = result.stdout or ""

        if result.stderr:
            output += "\n" + result.stderr

        return result.returncode == 0, output

    except subprocess.TimeoutExpired:
        return False, "Izvršavanje je prekoračilo vremensko ograničenje."

    except OSError as error:
        return False, str(error)


def load_uploaded_metrics(uploaded_file):
    """Učitava korisnički CSV preko postojeće analytics funkcije."""

    suffix = Path(uploaded_file.name).suffix or ".csv"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / f"uploaded_metrics{suffix}"

        temp_path.write_bytes(uploaded_file.getvalue())

        rows = load_metrics(temp_path)

    return rows


def display_analytics(result):
    """Prikazuje ključne Instagram metrike."""

    averages = result["averages"]

    st.subheader("Ključne metrike")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Objave",
        result["total_posts"],
    )

    col2.metric(
        "Prosječni lajkovi",
        f"{averages['lajkovi'] or 0:.1f}",
    )

    col3.metric(
        "Prosječni komentari",
        f"{averages['komentari'] or 0:.1f}",
    )

    col4.metric(
        "Prosječna spremanja",
        f"{averages['saves'] or 0:.1f}",
    )

    col5.metric(
        "Prosječni doseg",
        f"{averages['doseg'] or 0:.1f}",
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Prosječni engagement rate",
            (
                f"{result['average_engagement_rate']:.2f}%"
                if result["average_engagement_rate"] is not None
                else "N/A"
            ),
        )

    with col2:
        st.metric(
            "Ponderirani engagement rate",
            (
                f"{result['weighted_engagement_rate']:.2f}%"
                if result["weighted_engagement_rate"] is not None
                else "N/A"
            ),
        )

    st.caption(
        "ER = (lajkovi + komentari + spremanja) / doseg × 100."
    )

    st.divider()

    # Rezultati po tipu objave.
    st.subheader("Rezultati prema tipu objave")

    type_data = {}

    for post_type, values in result["by_type"].items():
        valid = [
            value
            for value in values
            if value is not None
        ]

        if valid:
            type_data[post_type.upper()] = sum(valid) / len(valid)

    if type_data:
        st.bar_chart(type_data)
    else:
        st.info("Nema dovoljno podataka za analizu tipova objava.")

    # Rezultati po danu.
    st.subheader("Rezultati prema danu u tjednu")

    weekday_data = {}

    for weekday, values in result["by_weekday"].items():
        valid = [
            value
            for value in values
            if value is not None
        ]

        if valid:
            weekday_data[weekday] = sum(valid) / len(valid)

    if weekday_data:
        st.bar_chart(weekday_data)
    else:
        st.info("Nema dovoljno podataka za analizu dana.")

    # Hashtagovi.
    st.subheader("Najčešći hashtagovi")

    if result["hashtags"]:
        hashtag_rows = [
            {
                "Hashtag": hashtag,
                "Broj korištenja": count,
            }
            for hashtag, count in result["hashtags"].most_common(10)
        ]

        st.dataframe(
            hashtag_rows,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("U podacima nisu pronađeni hashtagovi.")

    # Kvaliteta podataka.
    st.divider()
    st.subheader("Kvaliteta podataka")

    quality = result["data_quality"]

    q1, q2, q3 = st.columns(3)

    q1.metric(
        "Neispravni datumi",
        quality["invalid_dates"],
    )

    q2.metric(
        "Nedostajući tipovi",
        quality["missing_types"],
    )

    q3.metric(
        "Nedostajuće numeričke vrijednosti",
        quality["missing_metrics"],
    )

    q4, q5, q6 = st.columns(3)

    q4.metric(
        "Negativne vrijednosti",
        quality["negative_values"],
    )

    q5.metric(
        "Nedostajući doseg",
        quality["missing_reach"],
    )

    q6.metric(
        "Objave s dosegom 0",
        quality["zero_reach"],
    )

    if quality["quality_issues"] == 0:
        st.success("Nisu pronađene greške u kvaliteti podataka.")
    else:
        st.warning(
            f"Pronađeno je {quality['quality_issues']} problema "
            "u kvaliteti podataka. Provjeri CSV prije donošenja zaključaka."
        )


# ==================================================
# NASLOV
# ==================================================

st.title("🍯 Dida Boža – AI Content Studio")

st.caption(
    "Priprema sadržaja, generiranje karusela, "
    "Instagram analitika i izvještavanje."
)

st.info(
    "Aplikacija priprema prompt za ChatGPT. "
    "Tekst objava generiraš u ChatGPT-u, "
    "a zatim ga vraćaš u aplikaciju. "
    "Analitika se izvršava unutar aplikacije."
)


# ==================================================
# SIDEBAR – BRIEFING
# ==================================================

with st.sidebar:
    st.header("⚙️ Briefing")

    proizvod = st.text_input(
        "Proizvod",
        "Ekološki džem od smokve 240 g",
    )

    publika = st.text_input(
        "Ciljna publika",
        "Ljubitelji prirodnih proizvoda i mediteranske kuhinje",
    )

    cilj = st.selectbox(
        "Cilj objava",
        [
            "Interakcija, edukacija i emocionalna povezanost",
            "Interakcija",
            "Edukacija",
            "Emocionalna povezanost",
            "Prodaja",
        ],
    )

    ton = st.selectbox(
        "Ton komunikacije",
        [
            "Topao i nostalgičan",
            "Edukativan",
            "Emotivan",
            "Zaigran",
        ],
    )

    tema = st.text_input(
        "Tema objava",
        "Mediteranski proizvodi i način života",
    )

    st.divider()

    st.caption(
        "Generiranje teksta odvija se ručno u ChatGPT-u."
    )

    st.caption(
        "Aplikacija ne šalje OpenAI API zahtjeve."
    )


# ==================================================
# KARTICE
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📝 1. Prompt",
        "💬 2. Sadržaj",
        "🖼️ 3. Karusel",
        "📊 4. Analitika",
        "📑 5. Izvještaji",
    ]
)


# ==================================================
# 1. PRIPREMA PROMPTA
# ==================================================

with tab1:

    st.subheader("1. Priprema prompta")

    st.write(
        "Pripremi upute za ChatGPT na temelju "
        "proizvoda, ciljne publike i komunikacijskog stila brenda."
    )

    st.markdown(
        """
        **Kako koristiti ovu karticu:**

        1. Provjeri podatke u lijevom izborniku.
        2. Klikni na gumb za pripremu prompta.
        3. Kopiraj ili preuzmi pripremljeni prompt.
        4. Zalijepi ga u ChatGPT i pošalji.
        5. Kopiraj ChatGPT odgovor u drugu karticu.
        """
    )

    if st.button(
        "✨ Pripremi prompt",
        type="primary",
        key="prepare_prompt",
    ):

        if not all(
            value.strip()
            for value in [proizvod, publika, tema]
        ):
            st.warning(
                "Popuni proizvod, ciljnu publiku i temu."
            )

        elif not EXAMPLES_FILE.exists():
            st.error(
                "Nedostaje datoteka brand_voice_examples.txt."
            )

        else:
            try:
                brand_voice = load_brand_voice(EXAMPLES_FILE)

                if not brand_voice:
                    st.error(
                        "Primjeri komunikacije brenda su prazni."
                    )
                else:
                    prompt = build_prompt(
                        brand_voice=brand_voice,
                        topic=(
                            f"Proizvod: {proizvod}\n"
                            f"Ciljna publika: {publika}\n"
                            f"Cilj: {cilj}\n"
                            f"Ton: {ton}\n"
                            f"Tema: {tema}"
                        ),
                    )

                    st.session_state.generated_prompt = prompt

                    st.success(
                        "Prompt je uspješno pripremljen."
                    )

            except Exception as error:
                st.error(
                    f"Greška pri pripremi prompta: {error}"
                )

    if st.session_state.generated_prompt:

        st.divider()
        st.subheader("Pripremljeni prompt")

        st.text_area(
            "Kopiraj cijeli tekst i pošalji ga u ChatGPT:",
            value=st.session_state.generated_prompt,
            height=350,
            key="prompt_preview",
        )

        st.download_button(
            "📥 Preuzmi prompt za ChatGPT (.txt)",
            data=st.session_state.generated_prompt,
            file_name="prompt_za_chatgpt.txt",
            mime="text/plain",
            key="download_prompt",
        )

        st.success(
            "Ova datoteka sadrži upute za ChatGPT, "
            "a ne gotove Instagram objave."
        )


# ==================================================
# 2. GENERIRANI SADRŽAJ
# ==================================================

with tab2:

    st.subheader("2. Spremanje generiranog sadržaja")

    st.write(
        "Ovdje zalijepi odgovor koji je ChatGPT generirao "
        "nakon slanja prompta iz prve kartice."
    )

    st.markdown(
        """
        **Očekivani sadržaj:**
        - OBJAVA 1
        - OBJAVA 2
        - OBJAVA 3

        Svaka objava treba sadržavati tekst, vizualni prompt,
        CTA i hashtagove.
        """
    )

    content = st.text_area(
        "Zalijepi generirane Instagram objave:",
        height=400,
        placeholder=(
            "OBJAVA 1\n"
            "Naslov:\n"
            "Tekst objave:\n"
            "Vizualni prompt:\n"
            "CTA:\n"
            "Hashtagovi:\n\n"
            "OBJAVA 2\n"
            "...\n\n"
            "OBJAVA 3\n"
            "..."
        ),
        key="content_input",
    )

    col1, col2 = st.columns(2)

    with col1:
        save_clicked = st.button(
            "💾 Spremi generirani sadržaj",
            type="primary",
            key="save_content",
            use_container_width=True,
        )

    with col2:
        st.button(
            "🗑️ Očisti sadržaj",
            key="clear_content",
            on_click=clear_generated_content,
            use_container_width=True,
        )

    if save_clicked:

        if not content.strip():
            st.warning(
                "Najprije zalijepi generirani sadržaj."
            )

        else:
            missing = validate_content(content)

            st.session_state.generated_content = content

            if missing:
                st.warning(
                    "Sadržaj je spremljen, ali nisu "
                    "prepoznate sve tri objave. "
                    "Provjeri oznake OBJAVA 1, OBJAVA 2 i OBJAVA 3."
                )
            else:
                st.success(
                    "Sve tri objave su prepoznate i spremljene."
                )

    saved_content = st.session_state.generated_content

    if saved_content.strip():

        st.divider()
        st.subheader("Rezultat")

        missing_saved = validate_content(saved_content)

        if missing_saved:
            st.warning(
                "Spremljeni tekst nema sve tri prepoznatljive "
                "oznake objava."
            )
        else:
            st.success(
                "Spremljeni sadržaj sadrži sve tri objave."
            )

        if content != saved_content:
            st.warning(
                "U tekstnom polju postoje nespremljene izmjene. "
                "Klikni Spremi prije preuzimanja."
            )
        else:
            st.success(
                "Spremljena verzija odgovara tekstu u polju."
            )

        st.download_button(
            "📥 Preuzmi generirane objave (.txt)",
            data=saved_content,
            file_name="dida_boza_objave.txt",
            mime="text/plain",
            key="download_generated_content",
            disabled=(content != saved_content),
        )

        st.caption(
            "Sadržaj se čuva u aktivnoj Streamlit sesiji. "
            "Nije trajno pohranjen na poslužitelju."
        )

    else:
        st.info(
            "Nakon spremanja generiranih objava "
            "ovdje će se pojaviti opcija za preuzimanje."
        )


# ==================================================
# 3. INSTAGRAM KARUSEL
# ==================================================

with tab3:

    st.subheader("3. Instagram karusel")

    st.write(
        "Izradi vizualne slajdove unutar aplikacije pomoću Pillow biblioteke."
    )

    st.caption(
        "Format: 1080 × 1350 px (Instagram 4:5). "
        "Izrada ne zahtijeva plaćeni API."
    )

    if st.button(
        "🎨 Generiraj karusel",
        type="primary",
        key="generate_carousel",
    ):

        if not CAROUSEL_SCRIPT.exists():
            st.error(
                "Nedostaje datoteka make_carousel.py."
            )

        else:
            try:
                with st.spinner(
                    "Izrađujem Instagram karusel..."
                ):
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(CAROUSEL_SCRIPT),
                        ],
                        cwd=str(BASE_DIR),
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )

                if result.returncode != 0:
                    st.error(
                        "Došlo je do greške pri izradi karusela."
                    )
                    st.code(
                        result.stderr or result.stdout
                    )
                else:
                    st.success(
                        "Karusel je uspješno izrađen."
                    )

                    if result.stdout:
                        st.code(result.stdout)

            except subprocess.TimeoutExpired:
                st.error(
                    "Izrada karusela trajala je predugo."
                )

            except Exception as error:
                st.error(
                    f"Greška pri izradi karusela: {error}"
                )

    slides = get_carousel_slides()

    if slides:

        st.divider()
        st.subheader(
            f"Pregled slajdova ({len(slides)})"
        )

        columns = st.columns(2)

        for index, slide in enumerate(slides):

            with columns[index % 2]:

                st.image(
                    str(slide),
                    caption=f"Slajd {index + 1}",
                    width="stretch",
                )

                st.download_button(
                    f"📥 Preuzmi slajd {index + 1}",
                    data=slide.read_bytes(),
                    file_name=slide.name,
                    mime="image/png",
                    key=f"download_{slide.name}",
                    use_container_width=True,
                )

    else:
        st.info(
            "Karusel još nije izrađen. "
            "Klikni na gumb za generiranje."
        )

    st.caption(
        "Napomena: karusel se izrađuje prema predlošku "
        "u make_carousel.py. Nije automatski povezan "
        "s tekstom objava iz druge kartice."
    )


# ==================================================
# 4. INSTAGRAM ANALITIKA
# ==================================================

with tab4:

    st.subheader("4. Instagram analitika")

    st.write(
        "Učitaj vlastitu CSV datoteku s Instagram metrikama "
        "ili upotrijebi demo podatke projekta."
    )

    st.caption(
        "CSV mora sadržavati stupce: datum, tip_objave, "
        "lajkovi, komentari, saves, doseg i hashtagovi."
    )

    uploaded_file = st.file_uploader(
        "Učitaj Instagram CSV",
        type=["csv"],
        key="analytics_upload",
    )

    use_demo = st.checkbox(
        "Koristi demo podatke projekta",
        value=False,
        key="use_demo_metrics",
    )

    if st.button(
        "📊 Analiziraj podatke",
        type="primary",
        key="run_analytics",
    ):

        try:
            if uploaded_file is not None:

                rows = load_uploaded_metrics(uploaded_file)

                filename = uploaded_file.name

            elif use_demo:

                if not NEW_CSV.exists():
                    raise FileNotFoundError(
                        "Nedostaje metrics_demo_new.csv."
                    )

                rows = load_metrics(NEW_CSV)
                filename = NEW_CSV.name

            else:
                raise ValueError(
                    "Učitaj CSV datoteku ili odaberi demo podatke."
                )

            result = analyze(rows)
            report = generate_report(result)

            st.session_state.analytics_result = result
            st.session_state.analytics_report = report
            st.session_state.analytics_filename = filename

            st.success(
                f"Analiza datoteke {filename} uspješno je završena."
            )

        except Exception as error:
            st.error(
                f"Analiza nije uspjela: {error}"
            )

    result = st.session_state.analytics_result

    if result is not None:

        st.divider()

        st.caption(
            f"Analizirana datoteka: "
            f"{st.session_state.analytics_filename}"
        )

        display_analytics(result)

        st.divider()
        st.subheader("Tekstualni izvještaj")

        st.download_button(
            "📥 Preuzmi Instagram izvještaj (.txt)",
            data=st.session_state.analytics_report,
            file_name="instagram_analytics_report.txt",
            mime="text/plain",
            key="download_analytics_report",
        )

        with st.expander("Prikaži cijeli izvještaj"):
            st.text(st.session_state.analytics_report)

    else:
        st.info(
            "Učitaj CSV datoteku i pokreni analizu "
            "kako bi se prikazali rezultati."
        )


# ==================================================
# 5. IZVJEŠTAJI
# ==================================================

with tab5:

    st.subheader("5. Izvještaji i dashboard")

    st.write(
        "Ovdje možeš generirati usporedbu razdoblja, "
        "tjedni izvještaj i dashboard koristeći demo CSV datoteke."
    )

    st.warning(
        "Usporedba i tjedni izvještaj u ovoj verziji "
        "koriste demo CSV datoteke. Nemoj ih zamijeniti "
        "izvještajem iz vlastitih Instagram podataka."
    )

    if st.button(
        "📑 Generiraj izvještaje i dashboard",
        type="primary",
        key="generate_reports",
    ):

        if not OLD_CSV.exists() or not NEW_CSV.exists():

            st.error(
                "Nedostaje metrics_demo_old.csv ili metrics_demo_new.csv."
            )

        else:

            with st.spinner(
                "Generiram usporedbu, tjedni izvještaj i dashboard..."
            ):

                comparison_ok, comparison_output = run_local_script(
                    "compare_metrics.py",
                    OLD_CSV,
                    NEW_CSV,
                )

                weekly_ok, weekly_output = run_local_script(
                    "weekly_report.py",
                    OLD_CSV,
                    NEW_CSV,
                )

                dashboard_ok, dashboard_output = run_local_script(
                    "create_dashboard.py",
                    OLD_CSV,
                    NEW_CSV,
                )

            st.session_state.comparison_output = comparison_output
            st.session_state.weekly_output = weekly_output
            st.session_state.dashboard_generated = dashboard_ok

            if comparison_ok:
                st.success("Usporedba rezultata uspješno je generirana.")
            else:
                st.error("Generiranje usporedbe nije uspjelo.")
                st.code(comparison_output)

            if weekly_ok:
                st.success("Tjedni izvještaj uspješno je generiran.")
            else:
                st.error("Generiranje tjednog izvještaja nije uspjelo.")
                st.code(weekly_output)

            if dashboard_ok:
                st.success("Dashboard je uspješno generiran.")
            else:
                st.error("Generiranje dashboarda nije uspjelo.")
                st.code(dashboard_output)

    # Usporedba.
    if st.session_state.comparison_output:

        st.divider()
        st.subheader("Usporedba rezultata")

        st.text(st.session_state.comparison_output)

        st.download_button(
            "📥 Preuzmi usporedbu (.txt)",
            data=st.session_state.comparison_output,
            file_name="usporedba_rezultata.txt",
            mime="text/plain",
            key="download_comparison",
        )

    # Tjedni izvještaj.
    if WEEKLY_REPORT.exists():

        st.divider()
        st.subheader("Tjedni izvještaj")

        weekly_text = WEEKLY_REPORT.read_text(
            encoding="utf-8"
        )

        st.text(weekly_text)

        st.download_button(
            "📥 Preuzmi tjedni izvještaj (.txt)",
            data=weekly_text,
            file_name="weekly_report.txt",
            mime="text/plain",
            key="download_weekly_report",
        )

    elif st.session_state.weekly_output:

        st.text(st.session_state.weekly_output)

    # Dashboard.
    if DASHBOARD_FILE.exists():

        st.divider()
        st.subheader("Dashboard")

        st.image(
            str(DASHBOARD_FILE),
            caption="Dida Boža – Instagram metrics dashboard",
            width="stretch",
        )

        st.download_button(
            "📥 Preuzmi dashboard (.png)",
            data=DASHBOARD_FILE.read_bytes(),
            file_name="metrics_dashboard.png",
            mime="image/png",
            key="download_dashboard",
        )

    else:
        st.info(
            "Dashboard još nije generiran. "
            "Klikni na gumb iznad."
        )


# ==================================================
# PODNOŽJE
# ==================================================

st.divider()

st.caption(
    "Dida Boža AI Content Studio | "
    "Python | Streamlit | Pillow | "
    "Instagram Analytics | Bez plaćenih API poziva"
)
