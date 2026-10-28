import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_with_api(client):
    prompt = """
    Ti si vrhunski stručnjak za društvene mreže i vizualni identitet brenda Dida Boža.
    Tvoj zadatak je generirati sadržaj za 3 Instagram objave (Karusel, Pojedinačna slika, Reel).
    
    Brend: Dida Boža (ekološki džemovi, Dalmacija, tradicija, topao i nostalgičan ton).
    Publika: Foodie scena, ljubitelji prirodnih proizvoda, Slow Living.
    
    Vrati odgovor točno u ovom formatu:
    
    --- OBJAVA 1: KARUSEL (3 slajda) ---
    Cilj: ...
    Slajd 1 prompt: ...
    Slajd 2 prompt: ...
    Slajd 3 prompt: ...
    Tekst objave: ...
    Hashtagovi: ...
    
    --- OBJAVA 2: POJEDINAČNA SLIKA ---
    Cilj: ...
    Vizualni prompt: ...
    Ljudska dorada: ...
    Tekst objave: ...
    Hashtagovi: ...
    
    --- OBJAVA 3: REEL (3 kadra) ---
    Cilj: ...
    Kadar 1 prompt: ...
    Kadar 2 prompt: ...
    Kadar 3 uputa: ...
    Tekst objave: ...
    Hashtagovi: ...
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ti si vrhunski AI stručnjak za marketing."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def get_mock_content():
    """Primjer izlaza za --dry-run (bez API poziva)."""
    return """--- OBJAVA 1: KARUSEL (3 slajda) ---
Cilj: Edukacija i poticanje spremanja
Slajd 1 prompt: "Close-up macro shot of ripe, dark purple figs on a branch, golden hour light, bokeh stone wall, no text, no people. --ar 4:5"
Slajd 2 prompt: "Rustic Mediterranean table with a ceramic bowl of glossy fig jam, fresh figs, walnuts, rosemary, warm natural light, editorial food photography. --ar 4:5"
Slajd 3 prompt: "Handmade ceramic plate with crusty sourdough, creamy cheese, glossy fig compote, thyme sprig, blurred stone village and sea in background. --ar 4:5"
Tekst objave: Od grane do stola. 🌿 Znate li koliko je strpljenja potrebno za jednu savršenu smokvu? Dida Boža zna. Povuci prstom lijevo i otkrij kako nastaje naš Ekološki džem od smokve. 👉 Spremi ovu objavu za svoj sljedeći brunch!
Hashtagovi: #DidaBoza #EkoSmokva #DalmatinskaTradicija #SlowFood #BrunchIdeje #HrvatskaHrana

--- OBJAVA 2: POJEDINAČNA SLIKA ---
Cilj: Poticanje interakcije
Vizualni prompt: "Golden-hour Mediterranean terrace scene with crusty sourdough topped with creamy cheese and glossy fig compote, fresh figs, jam bowl, olive branches, blurred stone village and sea. --ar 4:5"
Ljudska dorada: U Canvi izrežite stvarnu staklenku Dida Boža, uklonite pozadinu, ubacite u kadar i dodajte meku sjenu.
Tekst objave: Malo mora, kamen, maslina... i onaj savršeni spoj koji svi obožavaju. 🫒🌊 Znate li koji je najbolji način za uživati u Dida Boža namazu od smokve? Ako biste ovaj tanjur ponijeli sa sobom na jadransku obalu, napišite nam u komentarima - više volite slatki ili slani doručak? 👇
Hashtagovi: #DidaBoza #Smokva #DalmatinskaTradicija #DoručakNaMoru #HrvatskaHrana #FoodieCroatia

--- OBJAVA 3: REEL (3 kadra) ---
Cilj: Emocionalna povezanost
Kadar 1 prompt: "Sun rays piercing through olive branches, gentle sway, Mediterranean coast blurred in background, cinematic."
Kadar 2 prompt: "Slow motion close-up of a knife spreading glossy fig jam onto crusty sourdough bread, cinematic lighting."
Kadar 3 uputa: U CapCut/Canva spojite kadrove s laganim crossfade prijelazom i nježnom mediteranskom glazbom. Završite stvarnom staklenkom Dida Boža.
Tekst objave: Ponekad je najbolji začin – vrijeme. ⏳🌊 Mali podsjetnik da usporiš. Uzmi krišku dobrog kruha, malo sira i žlicu Dida Boža džema od smokve. Trenutak koji vrijedi.
Hashtagovi: #DidaBoza #MediteranskiUgođaj #SlowLiving #Dalmacija #ReelCroatia"""

def save_content(content):
    os.makedirs("output", exist_ok=True)
    
    # Spremi sve u jednu datoteku
    with open("output/generirani_sadrzaj.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Pokušaj razdvojiti po objavama
    sections = content.split("---")
    for i, section in enumerate(sections):
        if "OBJAVA" in section:
            filename = f"output/objava_{i}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(section.strip())
    
    print("✅ Sadržaj spremljen u mapu 'output/'.")

def main():
    use_dry_run = "--dry-run" in sys.argv
    
    print("🚀 Pokrećem AI Recept za Dida Boža...\n")
    
    if use_dry_run:
        print("ℹ️  Dry-run način: koristim primjer izlaza (bez API poziva).\n")
        content = get_mock_content()
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY nije pronađen. Postavite ga u .env datoteku ili pokrenite s --dry-run.")
        client = OpenAI(api_key=api_key)
        content = generate_with_api(client)
    
    save_content(content)
    
    print("\n--- PREGLED (prvih 300 znakova) ---")
    print(content[:300] + "\n[...]")

if __name__ == "__main__":
    main()
