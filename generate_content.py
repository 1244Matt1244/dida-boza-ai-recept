import os
from openai import OpenAI

# Preporuka: Koristite .env datoteku za API ključ, nemojte ga hardkodirati!
# os.environ["OPENAI_API_KEY"] = "vasi_kljuc_ovdje" 

client = OpenAI()

def generate_instagram_content():
    print("🚀 Pokrećem AI Recept za Dida Boža...\n")
    
    prompt = """
    Ti si stručnjak za društvene mreže i vizualni identitet brenda Dida Boža.
    Tvoj zadatak je generirati sadržaj za 3 Instagram objave.
    
    Brend: Dida Boža (ekološki džemovi, Dalmacija, tradicija, topao i nostalgičan ton).
    Ciljna publika: Foodie scena, ljubitelji prirodnih proizvoda, Slow Living.
    
    Molim te vrati odgovor u sljedećem formatu:
    1. Vizualni prompt na engleskom za DALL-E 3 (mediteranski ambijent, smokve, kruh, sir, toplo svjetlo).
    2. Tekst objave na hrvatskom (1. potiče interakciju, 2. potiče spremanje, 3. emocionalna povezanost).
    3. Hashtagove.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Ti si vrhunski AI stručnjak za marketing."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        print("✅ USPJEŠNO GENERIRANO:\n")
        print(response.choices[0].message.content)
        
        print("\n--- SLJEDEĆI KORAK: LJUDSKA DORADA ---")
        print("1. Kopirajte vizualni prompt u ChatGPT/DALL-E.")
        print("2. Generirajte sliku.")
        print("3. U Canvi izrežite stvarnu staklenku Dida Boža i ubacite je u kadar.")
        print("4. Zalijepite dobivene tekstove ispod slika.")
        
    except Exception as e:
        print(f"❌ Došlo je do pogreške: {e}")
        print("Provjerite je li vaš OPENAI_API_KEY ispravno postavljen.")

if __name__ == "__main__":
    generate_instagram_content()
