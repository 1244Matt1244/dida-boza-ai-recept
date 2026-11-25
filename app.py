import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_carousel import carousel

from generate_content import (
    generate_with_api,
    get_mock_content,
    generate_image,
    generate_carousel_images,
)

load_dotenv()


def get_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY", "")


st.set_page_config(
    page_title="Dida Boža – Generator objava",
    page_icon="🍯",
    layout="wide",
)

st.title("🍯 Dida Boža – Generator Instagram objava")
st.markdown(
    "Unesite parametre u bočnoj traci i generirajte **tri Instagram objave** "
    "za brend Dida Boža. Aplikacija podržava **dry-run** (bez API ključa), "
    "**stvarno generiranje teksta** i **generiranje vizuala pomoću DALL-E 3** "
    "(dostupno uz API ključ)."
)

with st.sidebar:
    st.header("⚙️ Brifing")

    proizvod = st.text_input("Proizvod", "Ekološki džem od smokve 240 g")
    publika = st.text_input(
        "Ciljna publika",
        "Foodie scena, ljubitelji prirodnih proizvoda, Slow Living",
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
        ["Topao i nostalgičan", "Edukativan", "Emotivan", "Zaigran"],
    )

    st.divider()
    st.subheader("📎 Dodatne reference (opcionalno)")

    web_stranica = st.text_input(
        "Web stranica brenda", placeholder="https://www.didaboza.hr/"
    )
    inspiracija = st.text_input(
        "Inspiracija / uzor", placeholder="npr. @bonne_maman"
    )

    st.divider()
    st.subheader("🖼️ Format i vizuali")

    # DALL-E je dostupan samo ako postoji API ključ
    ima_kljuc = bool(get_api_key())

    if ima_kljuc:
        format_objave = st.radio(
            "Format objave",
            ["Statična slika", "Karusel (4 slajda)"],
            help="Karusel generira 4 povezane slike.",
        )
        generiraj_vizuale = st.checkbox(
            "Generiraj vizuale (DALL-E 3)",
            value=False,
            help="Troši OpenAI kredit (~$0.04 po slici).",
        )
    else:
        format_objave = "Statična slika"
        generiraj_vizuale = False
        st.caption(
            "🖼️ Generiranje vizuala (DALL-E 3) dostupno je samo uz "
            "OpenAI API ključ. Dry-run radi bez ključa."
        )

    st.divider()

    dry_run = st.checkbox("Dry-run (bez API poziva)", value=True)

    api_key_input = ""
    if not dry_run or generiraj_vizuale:
        api_key_input = st.text_input(
            "OpenAI API ključ",
            type="password",
            value=get_api_key(),
            help="Ako je prazno, koristi se OPENAI_API_KEY iz Secrets/.env.",
        )

    st.caption("Model: `gpt-4o` · DALL-E 3 · Temperatura: `0.7` · Jezik: hrvatski")


if st.button("🚀 Generiraj 3 objave", type="primary", use_container_width=True):
    if dry_run:
        content = get_mock_content()
        st.info("Dry-run: prikazujem primjer izlaza bez poziva API-ja.")
    else:
        key = api_key_input or get_api_key()
        if not key:
            st.error("Nedostaje `OPENAI_API_KEY`.")
            st.stop()

        client = OpenAI(api_key=key)
        with st.spinner("Generiram tri objave…"):
            try:
                content = generate_with_api(
                    client,
                    proizvod=proizvod,
                    cilj=cilj,
                    ton=ton,
                    publika=publika,
                    web_stranica=web_stranica,
                    inspiracija=inspiracija,
                )
            except Exception as e:
                st.error(f"Greška pri pozivu API-ja: {e}")
                st.stop()

        st.success("✅ Objave su generirane.")

    st.divider()
    st.text(content)

    st.download_button(
        "⬇️ Preuzmi kao .txt",
        data=content,
        file_name="dida_boza_objave.txt",
        mime="text/plain",
        use_container_width=True,
    )

    # --- Generiranje vizuala (samo ako je uključeno i ima ključa) ---
    if generiraj_vizuale:
        key = api_key_input or get_api_key()
        if not key:
            st.error("Za generiranje vizuala potreban je OpenAI API ključ.")
            st.stop()

        client = OpenAI(api_key=key)
        st.subheader("🖼️ Generirani vizuali")

        base_prompt = (
            "Editorial food photography for Dida Boža fig jam, Mediterranean "
            "terrace, golden hour, rustic ceramic, figs, cheese, warm tones, "
            "no text, no people"
        )

        if format_objave == "Statična slika":
            with st.spinner("Generiram sliku (DALL-E 3)…"):
                try:
                    img_url = generate_image(client, base_prompt)
                    st.image(
                        img_url,
                        caption="DALL-E 3 generirani vizual",
                        use_container_width=True,
                    )
                    st.markdown(f"[Otvori sliku u novom tabu]({img_url})")
                except Exception as e:
                    st.error(f"Greška pri generiranju slike: {e}")

        else:  # Karusel
            with st.spinner("Generiram 4 slike za karusel (DALL-E 3)…"):
                try:
                    urls = generate_carousel_images(
                        client, base_prompt, num_slides=4
                    )
                    items = [
                        {"title": f"Slajd {i + 1}", "text": "", "img": url}
                        for i, url in enumerate(urls)
                    ]
                    carousel(items=items)
                except Exception as e:
                    st.error(f"Greška pri generiranju karusela: {e}")

else:
    st.caption(
        "Klikni **Generiraj 3 objave** za početak. "
        "Dry-run je uključen prema zadanim postavkama."
    )