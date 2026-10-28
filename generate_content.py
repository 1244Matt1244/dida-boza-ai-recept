import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Učitava varijable iz .env datoteke
load_dotenv()

def generate_with_api(client):
    prompt = """
    Ti si vrhunski stručnjak za društvene mreže i vizualni identitet brenda Dida Boža.
    Tvoj zadatak je generirati sadržaj za 3 Instagram objave.
    
    Brend: Dida Boža (ekološki džemovi, Dalmacija, tradicija, topao i nostalgičan ton).
    Publika: Foodie scena, ljubitelji prirodnih proizvoda, Slow Living.
    
    Vrati odgovor točno u ovom formatu:
    
    --- OBJAVA 1: STATIČNA SLIKA (Interakcija) ---
    Vizualni prompt: [Vizualni prompt na engleskom za DALL-E 3]
    Tekst objave: [Tekst na hrvatskom s pitanjem publici]
    Hashtagovi: [5-8 hashtagova]
    
    --- OBJAVA 2: STATIČNA SLIKA (Edukacija i prikaz proizvoda) ---
    Vizualni prompt: [Vizualni prompt na engleskom]
    Ljudska dorada: [Uputa kako u Canvi ubaciti stvarnu staklenku Dida Boža]
    Tekst objave: [Tekst na hrvatskom]
    Hashtagovi: [5-8 hashtagova]
    
    --- OBJAVA 3: STATIČNA SLIKA (Emocionalna povezanost) ---
    Vizualni prompt: [Vizualni prompt na engleskom]
    Tekst objave: [Tekst na hrvatskom]
    Hashtagovi: [5-8 hashtagova]
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
    return """--- OBJAVA 1: STATIČNA SLIKA (Interakcija) ---
Vizualni prompt: "Close-up macro shot of ripe, dark purple figs on a branch, golden hour light, bokeh stone wall, no text, no people. --ar 4:5"
Tekst objave: Slatko susreće slano. 🧀🍯 Jeste li ikada probali smokvu uz sir? Ta mala promjena donosi potpuno novo iskustvo za stolom. Dida Boža džem od smokve savršeno se slaže s kremastim sirom na kriški domaćeg kruha. Ako ste ljubitelj ovakvih kombinacija, napišite nam u komentarima - koji je vaš omiljeni sir uz smokvu? 👇
Hashtagovi: #DidaBoza #Smokva #SlatkoSlano #Dalmacija #Gourmet #FoodieCroatia

--- OBJAVA 2: STATIČNA SLIKA (Edukacija i prikaz proizvoda) ---
Vizualni prompt: "Golden-hour Mediterranean terrace scene with crusty sourdough topped with creamy cheese and glossy fig compote, fresh figs, jam bowl, olive branches, blurred stone village and sea. --ar 4:5"
Ljudska dorada: U Canvi izrežite stvarnu staklenku Dida Boža, uklonite pozadinu, ubacite u kadar i dodajte meku sjenu.
Tekst objave: Mali mediteranski ritual. 🌿🌊 Smokva. Kruh. Malo Mediterana. Ponekad je za savršen užitak potrebno samo nekoliko pravih sastojaka i trenutak vremena za sebe. Spremite ovu objavu za svoj sljedeći brunch i uživajte u okusu Dalmacije. 📌
Hashtagovi: #DidaBoza #MediteranskiUgođaj #Brunch #SlowLiving #EkoDzem #HrvatskaHrana

--- OBJAVA 3: STATIČNA SLIKA (Emocionalna povezanost) ---
Vizualni prompt: "Rustic wooden table setting in a Mediterranean courtyard, bowl of fig jam, fresh figs, walnuts, warm natural light, editorial food photography. --ar 4:5"
Tekst objave: Okus koji usporava dan. ⏳✨ Mali ritual. Veliki užitak. Pronađite svoj omiljeni način posluživanja našeg ekološkog džema od smokve. Bilo da ga mažete na tost, dodajete u jogurt ili poslužujete uz sir – svaki zalogaj je podsjetnik na sunce i more. Označite osobu s kojom biste podijelili ovaj trenutak. 👇
Hashtagovi: #DidaBoza #Smokva #Tradicija #Uživanje #BreakfastIdeas #CroatianFood"""

def save_content(content):
    os.makedirs("output", exist_ok=True)
    with open("output/generirani_sadrzaj.txt", "w", encoding="utf-8") as f:
        f.write(content)
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
