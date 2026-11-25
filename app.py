import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from generate_content import generate_with_api, get_mock_content

load_dotenv()

st.set_page_config(
    page_title="Dida Boža – Generator objava",
    page_icon="🍯",
    layout="wide",
)

st.title("🍯 Dida Boža – Generator Instagram objava")
st.markdown(
    "Unesite parametre u bočnoj traci i generirajte **tri Instagram objave** "
    "za brend Dida Boža. Aplikacija podržava **dry-run** (bez API ključa) i "
    "**stvarno generiranje** putem OpenAI API-ja."
)

with st.sidebar:
    st.header("⚙️ Parametri")

    proizvod = st.text_input(
        "Proizvod",
        "Ekološki džem od smokve 240 g",
        help="Naziv proizvoda koji se promovira u objavama.",
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
        help="Zadano pokriva sva tri formata iz recepta.",
    )

    ton = st.selectbox(
        "Ton komunikacije",
        ["Topao i nostalgičan", "Edukativan", "Emotivan", "Zaigran"],
    )

    st.divider()

    dry_run = st.checkbox(
        "Dry-run (bez API poziva)",
        value=True,
        help="Prikazuje primjer izlaza bez trošenja API kvote.",
    )

    api_key_input = ""
    if not dry_run:
        api_key_input = st.text_input(
            "OpenAI API ključ",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Ako je prazno, koristi se OPENAI_API_KEY iz .env datoteke.",
        )

    st.divider()
    st.caption("Model: `gpt-4o` · Temperatura: `0.7` · Jezik: hrvatski")


if st.button("🚀 Generiraj 3 objave", type="primary", use_container_width=True):
    if dry_run:
        content = get_mock_content()
        st.info("Dry-run: prikazujem primjer izlaza bez poziva API-ja.")
    else:
        key = api_key_input or os.getenv("OPENAI_API_KEY")
        if not key:
            st.error(
                "Nedostaje `OPENAI_API_KEY`. Postavite ga u `.env` datoteku "
                "ili upišite u bočnu traku."
            )
            st.stop()

        client = OpenAI(api_key=key)
        with st.spinner("Generiram tri objave…"):
            try:
                content = generate_with_api(
                    client,
                    proizvod=proizvod,
                    cilj=cilj,
                    ton=ton,
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
else:
    st.caption(
        "Klikni **Generiraj 3 objave** za početak. "
        "Dry-run je uključen prema zadanim postavkama."
    )