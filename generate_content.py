
"""
DIDA BOŽA — AI CONTENT GENERATOR

Besplatna verzija:
- Priprema prompt za ChatGPT
- Učitava primjere tona brenda
- Omogućuje ručno spremanje AI sadržaja
- Ne koristi API
"""

import argparse
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

EXAMPLES_FILE = BASE_DIR / "brand_voice_examples.txt"
PROMPT_FILE = OUTPUT_DIR / "prompt_za_chatgpt.txt"
CONTENT_FILE = OUTPUT_DIR / "generirani_sadrzaj.txt"

MAX_BRAND_VOICE_CHARS = 9000


def load_brand_voice(path=EXAMPLES_FILE):
    """Učitava primjere komunikacije brenda."""
    path = Path(path)

    if not path.exists():
        print("Nema datoteke s primjerima tona brenda.")
        return ""

    text = path.read_text(encoding="utf-8")
    return text[:MAX_BRAND_VOICE_CHARS]


def build_prompt(brand_voice="", topic=None):
    """Priprema prompt za ručno korištenje u ChatGPT-u."""

    topic_text = topic or "Mediteranski proizvodi i način života"

    prompt = f"""
TI SI: Iskusni stručnjak za Instagram marketing i copywriting.

BREND: Dida Boža

ZADATAK:
Izradi tri originalne Instagram objave za brend Dida Boža.

TEMA:
{topic_text}

TON KOMUNIKACIJE:
Topao, autentičan, mediteranski, prijateljski i prirodan.

PRIMJERI KOMUNIKACIJE BRENDA:
{brand_voice if brand_voice else "Nisu dostupni dodatni primjeri."}

ZA SVAKU OBJAVU NAVEDI:

1. Naslov objave
2. Tekst objave
3. Vizualni prompt
4. Poziv na akciju (CTA)
5. Hashtagove

VAŽNA PRAVILA:
- Napiši tri različite objave.
- Koristi prirodan hrvatski jezik.
- Nemoj kopirati postojeće objave.
- Ne izmišljaj sastav, certifikate ili zdravstvene učinke proizvoda.
- Vizualni prompt mora biti dovoljno detaljan za izradu slike.
- Prilagodi sadržaj Instagram publici.

FORMAT:

OBJAVA 1
Tekst objave:
Vizualni prompt:
CTA:
Hashtagovi:

OBJAVA 2
Tekst objave:
Vizualni prompt:
CTA:
Hashtagovi:

OBJAVA 3
Tekst objave:
Vizualni prompt:
CTA:
Hashtagovi:
"""

    return prompt.strip()


def save_file(path, content):
    """Sprema tekstualnu datoteku."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Datoteka spremljena: {path}")


def save_generated_content():
    """Omogućuje ručno spremanje sadržaja iz ChatGPT-a."""

    print("\nZalijepi generirani sadržaj.")
    print("Kada završiš, u novi red upiši GOTOVO.\n")

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().upper() == "GOTOVO":
            break

        lines.append(line)

    content = "\n".join(lines).strip()

    if not content:
        print("Nije unesen nikakav sadržaj.")
        return False

    save_file(CONTENT_FILE, content)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_file = OUTPUT_DIR / f"sadrzaj_{timestamp}.txt"
    save_file(archive_file, content)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Dida Boža — besplatna priprema AI sadržaja"
    )

    parser.add_argument(
        "--topic",
        help="Tema Instagram objava"
    )

    parser.add_argument(
        "--examples-file",
        default=str(EXAMPLES_FILE),
        help="Putanja do primjera tona brenda"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prikaži prompt bez spremanja"
    )

    parser.add_argument(
        "--save-content",
        action="store_true",
        help="Ručno spremanje sadržaja iz ChatGPT-a"
    )

    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.save_content:
        save_generated_content()
        return

    print("Pripremam prompt bez API poziva...")

    brand_voice = load_brand_voice(args.examples_file)
    prompt = build_prompt(brand_voice, args.topic)

    if args.dry_run:
        print("\n" + "=" * 60)
        print(prompt)
        print("=" * 60)
        return

    save_file(PROMPT_FILE, prompt)

    print("\nPrompt je spreman za ChatGPT.")
    print("Otvori output/prompt_za_chatgpt.txt i kopiraj sadržaj.")
    print("Nakon generiranja možeš spremiti rezultat naredbom:")
    print("python generate_content.py --save-content")


if __name__ == "__main__":
    main()
