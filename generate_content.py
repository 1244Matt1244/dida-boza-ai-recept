import os
from openai import OpenAI
from dotenv import load_dotenv

# Učitava varijable iz .env datoteke
load_dotenv()

# Provjera je li API ključ postavljen
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY nije pronađen. Molimo kopirajte config.example.env u .env i upišite svoj ključ.")

client = OpenAI(api_key=api_key)

def generate_and_save_content():
    print("🚀 Pokrećem AI Recept za Dida Boža...\n")
    
    prompt = """
    Ti si vrhunski stručnjak za društvene mreže i vizualni identitet brenda Dida Boža.
    Tvoj zadatak je generirati sadržaj za 3 Instagram objave (Karusel, Pojedinačna slika, Reel).
    
    Brend: Dida Boža (ekološki džemovi, Dalmacija, tradicija, topao i nostalgičan ton).
    Publika: Foodie scena, ljubitelji prirodnih proizvoda, Slow Living.
    
    Molim te vrati odgovor točno u ovom formatu (bez dodatnih uvoda):
    
    --- OBJAVA 1: KARUSEL (3 slajda) ---
    Cilj: [npr. Edukacija i poticanje spremanja]
    Slajd 1 prompt: [Vizualni prompt na engleskom za DALL-E 3, fokus na sirovinu]
    Slajd 2 prompt: [Vizualni prompt na engleskom, fokus na pripremu]
    Slajd 3 prompt: [Vizualni prompt na engleskom, fokus na finalni proizvod]
    Tekst objave: [Tekst na hrvatskom]
    Hashtagovi: [5-8 hashtagova]
    
    --- OBJAVA 2: POJEDINAČNA SLIKA ---
    Cilj: [npr. Poticanje interakcije]
    Vizualni prompt: [Vizualni prompt na engleskom za prekrasan mediteranski ambijent]
    Ljudska dorada: [Uputa kako u Canvi ubaciti stvarnu staklenku Dida Boža]
    Tekst objave: [Tekst na hrvatskom s pitanjem publici]
    Hashtagovi: [5-8 hashtagova]
    
    --- OBJAVA 3: REEL (3 kadra) ---
    Cilj: [npr. Emocionalna povezanost]
    Kadar 1 prompt: [Vizualni prompt na engleskom]
    Kadar 2 prompt: [Vizualni prompt na engleskom]
    Kadar 3 uputa: [Uputa za spajanje u CapCut/Canva]
    Tekst objave: [Tekst na hrvatskom]
    Hashtagovi: [5-8 hashtagova]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ti si vrhunski AI stručnjak za marketing i vizualni identitet."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Automatsko stvaranje mape i spremanje datoteke (rješava kritiku B)
        os.makedirs("output", exist_ok=True)
        filename = "output/generirani_sadrzaj.txt"
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
            
        print(f"✅ USPJEŠNO GENERIRANO I SPREMLJENO u: {filename}\n")
        print("--- PREGLED SADRŽAJA (prvih 500 znakova) ---")
        print(content[:500] + "\n\n[...] (Ostatak pogledajte u generiranoj datoteci)")
        
    except Exception as e:
        print(f"❌ Došlo je do pogreške: {e}")
        print("Provjerite je li vaš API ključ valjan i imate li internetsku vezu.")

if __name__ == "__main__":
    generate_and_save_content()
