"""
run_all.py — end-to-end pipeline za Dida Boža AI recept.

Pokreće:
1. Generiranje tri Instagram objave (GPT-4o ili dry-run)
2. Generiranje karusela (4 slajda, Pillow)
3. Spremanje uputa za ljudsku doradu u Canvi

Korištenje:
    python run_all.py                 # dry-run (bez API ključa)
    python run_all.py --api           # stvarno generiranje (treba OPENAI_API_KEY)
"""

import os
import sys
import subprocess

os.makedirs("output", exist_ok=True)

print("=" * 60)
print("🚀 DIDA BOŽA — END-TO-END PIPELINE")
print("=" * 60)


# --- KORAK 1: Generiranje tekstova ---
print("\n[1/3] Generiranje tri Instagram objave...")

if "--api" in sys.argv:
    from openai import OpenAI
    from dotenv import load_dotenv
    from generate_content import generate_with_api

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY nije pronađen. Pokreni bez --api za dry-run.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    content = generate_with_api(client)
    print("   ✅ Generirano putem GPT-4o")
else:
    from generate_content import get_mock_content
    content = get_mock_content()
    print("   ✅ Dry-run (bez API poziva)")

with open("output/objave.txt", "w", encoding="utf-8") as f:
    f.write(content)
print("   💾 Spremljeno: output/objave.txt")


# --- KORAK 2: Generiranje karusela ---
print("\n[2/3] Generiranje karusela (4 slajda, Pillow)...")

# Postavi UTF-8 za subprocess (rješava Windows cp1250 problem s emoji)
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

try:
    result = subprocess.run(
        [sys.executable, "make_carousel.py"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=True,
    )
    print("   ✅ Karusel generiran")
    print("   💾 Spremljeno: images/karusel/slajd_1..4.png")
except subprocess.CalledProcessError as e:
    print("   ⚠️  Karusel nije generiran.")
    if e.stderr:
        print("   --- STDERR (prvih 1500 znakova) ---")
        print(e.stderr[:1500])
    if e.stdout:
        print("   --- STDOUT (prvih 500 znakova) ---")
        print(e.stdout[:500])
except Exception as e:
    print(f"   ⚠️  Neočekivana greška: {e}")


# --- KORAK 3: Upute za Canvu ---
print("\n[3/3] Priprema uputa za ljudsku doradu u Canvi...")

upute = """UPUTE ZA LJUDSKU DORADU U CANVI
================================

Cilj: od AI-generirane pozadine i stvarne staklenke napraviti tri finalne objave.

1. OTVORI CANVU
   - https://www.canva.com
   - Create a design → Instagram Post (1080 × 1350 px)

2. UVEZI POZADINU
   - Uploads → uploadaj AI-generiranu pozadinu (iz output/ ili images/)
   - Povuci na platno, rastegni da pokrije cijelu površinu

3. INTEGRIRAJ STVARNU STAKLENKU
   - Uploads → uploadaj images/staklenka.jpg (stvarna fotografija Dida Boža)
   - Klikni na sliku → "Background Remover" (uklanja pozadinu)
   - Postavi staklenku u prvi plan, prilagodi veličinu i perspektivu
   - Dodaj meku sjenu ispod staklenke (Effects → Shadows → Soft)

4. DODAJ TIPOGRAFIJU
   - Text → dodaj naslov i kratku poruku za svaku objavu:
     * Objava 1: "Slatko susreće slano / Jeste li probali smokvu uz sir?"
     * Objava 2: "Smokva. Kruh. Malo Mediterana. / Jednostavan zalogaj, veliki užitak."
     * Objava 3: "Mali ritual. Veliki užitak. / Pronađite svoj omiljeni način posluživanja smokve."
   - Font: Playfair Display (serif) za naslov, Inter za podnaslov
   - Boja: krem #FAF7F0 s laganom sjenom

5. DODAJ BRENDING
   - Mali banner "DIDA BOŽA • KREATIVNI KONCEPT" na dno slike
   - Boja: #8B4513 (zemljana smeđa)

6. IZVEZI
   - Share → Download → PNG
   - Spremi u images/objava1.jpg, images/staklenka.jpg, images/objava3.jpg

NAPOMENA:
Koraci 3–5 su ljudska dorada — AI ne smije izmišljati etikete ni ambalažu.
Stvarna staklenka se uvijek integrira ručno.
"""

with open("output/upute_za_canvu.txt", "w", encoding="utf-8") as f:
    f.write(upute)
print("   💾 Spremljeno: output/upute_za_canvu.txt")


# --- SAŽETAK ---
print("\n" + "=" * 60)
print("🎉 PIPELINE ZAVRŠEN")
print("=" * 60)
print("\nRezultat u output/:")
print("  - objave.txt              (tri Instagram objave)")
print("  - upute_za_canvu.txt      (koraci za ljudsku doradu)")
print("  - karusel/                (ako je make_carousel.py uspio)")
print("\nSljedeći korak: otvori Canvu i prati upute_za_canvu.txt")