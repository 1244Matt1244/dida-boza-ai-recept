
from pathlib import Path
import streamlit as st

from generate_content import (
    load_brand_voice,
    build_prompt,
    save_file,
    CONTENT_FILE,
    OUTPUT_DIR,
)

BASE_DIR = Path(__file__).resolve().parent
EXAMPLES_FILE = BASE_DIR / "brand_voice_examples.txt"
CAROUSEL_DIR = BASE_DIR / "images" / "karusel"

st.set_page_config(
    page_title="Dida Boža – AI Content Studio",
    page_icon="🍯",
    layout="wide",
)

st.title("🍯 Dida Boža – AI Content Studio")
st.caption(
    "Besplatna priprema AI sadržaja, spremanje tekstova "
    "i lokalna izrada Instagram karusela."
)

if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""

if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""

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

    st.caption("Generiranje teksta odvija se ručno u ChatGPT-u.")
    st.caption("Aplikacija ne šalje API zahtjeve.")

st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Priprema prompta",
        "💬 Generirani sadržaj",
        "🖼️ Instagram karusel",
    ]
)

with tab1:
    st.subheader("1. Priprema AI prompta")

    st.write(
        "Aplikacija koristi primjere komunikacije brenda "
        "kako bi pripremila prompt za ChatGPT."
    )

    if st.button("Pripremi prompt", type="primary"):
        brand_voice = load_brand_voice(EXAMPLES_FILE)

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

        prompt_path = OUTPUT_DIR / "prompt_za_chatgpt.txt"
        save_file(prompt_path, prompt)

        st.success("Prompt je uspješno pripremljen.")

    if st.session_state.generated_prompt:
        st.text_area(
            "Prompt za ChatGPT",
            value=st.session_state.generated_prompt,
            height=350,
        )

        st.download_button(
            "Preuzmi prompt (.txt)",
            data=st.session_state.generated_prompt,
            file_name="prompt_za_chatgpt.txt",
            mime="text/plain",
        )

        st.info(
            "Kopiraj prompt, zalijepi ga u ChatGPT i "
            "generirani rezultat prenesi u sljedeću karticu."
        )

with tab2:
    st.subheader("2. Spremanje generiranog sadržaja")

    st.write(
        "Ovdje zalijepi tekst koji si prethodno generirao "
        "u ChatGPT-u."
    )

    content = st.text_area(
        "Generirani sadržaj",
        value=st.session_state.generated_content,
        height=350,
        placeholder="Zalijepi tri generirane Instagram objave...",
    )

    if st.button("Spremi sadržaj"):
        if not content.strip():
            st.warning("Najprije unesi generirani sadržaj.")
        else:
            st.session_state.generated_content = content

            save_file(CONTENT_FILE, content)

            st.success("Sadržaj je spremljen.")

    if CONTENT_FILE.exists():
        saved_content = CONTENT_FILE.read_text(encoding="utf-8")

        st.download_button(
            "Preuzmi spremljeni sadržaj (.txt)",
            data=saved_content,
            file_name="dida_boza_objave.txt",
            mime="text/plain",
        )

with tab3:
    st.subheader("3. Lokalna izrada Instagram karusela")

    st.write(
        "Karusel se izrađuje lokalno pomoću Pillow biblioteke. "
        "Nema API poziva ni dodatnih troškova."
    )

    st.caption("Format: 1080 × 1350 px (Instagram 4:5).")

    if st.button("Generiraj karusel", type="primary"):
        try:
            import subprocess
            import sys

            result = subprocess.run(
                [
                    sys.executable,
                    str(BASE_DIR / "make_carousel.py"),
                ],
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode != 0:
                st.error("Greška pri izradi karusela.")
                st.code(result.stderr or result.stdout)
            else:
                st.success("Karusel je uspješno izrađen.")
                if result.stdout:
                    st.code(result.stdout)

        except Exception as error:
            st.error(f"Greška: {error}")

    if CAROUSEL_DIR.exists():
        slides = sorted(CAROUSEL_DIR.glob("slajd_*.png"))

        if slides:
            st.divider()
            st.subheader("Pregled slajdova")

            columns = st.columns(2)

            for index, slide in enumerate(slides):
                with columns[index % 2]:
                    st.image(
                        str(slide),
                        caption=f"Slajd {index + 1}",
                        width="stretch",
                    )

                    st.download_button(
                        f"Preuzmi slajd {index + 1}",
                        data=slide.read_bytes(),
                        file_name=slide.name,
                        mime="image/png",
                        key=f"download_{slide.name}",
                    )
        else:
            st.info(
                "Karusel još nije izrađen. "
                "Klikni na gumb iznad."
            )

st.divider()

st.caption(
    "Dida Boža AI Content Studio | "
    "Lokalni Python pipeline | Bez plaćenih API poziva"
)
