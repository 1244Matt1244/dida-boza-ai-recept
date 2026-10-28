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
```

---

### 3. `README.md` (S popisom svih datoteka)
*Kritika je tražila jasan popis datoteka i potvrdu statusa. Zalijepi ovo:*

```markdown
# 🍯 AI Recept: Dida Boža — Generator Instagram Sadržaja

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![Status](https://img.shields.io/badge/Status-Završeno-success)

Ovaj repozitorij sadrži izvršivi AI recept (Python skriptu) korišten za izradu tri gotove Instagram objave za hrvatski brend **Dida Boža**. Projekt demonstrira kako se korištenjem AI alata može ubrzati proces stvaranja sadržaja uz zadržavanje autentičnog vizualnog identiteta brenda.

## 📦 Isporučeni materijali (Deliverables)
Svi ključni dokumenti dostupni su izravno u repozitoriju:
*   📄 [Osvrt i upute (PDF)](./Osvrt_i_Upute.pdf) - Dokumentacija, analiza i osvrt.
*   📝 [Tekstovi objava (TXT)](./Tekstovi_objava.txt) - Konačni copy za sve tri objave.
*   ⚙️ [Recept i promptovi (TXT)](./Recept_i_Promptovi.txt) - Paket promptova za ručno korištenje.
*   🐍 [Python skripta](./generate_content.py) - Automatizirani generator sadržaja.

## 🎨 Vizualni rezultati (Tri gotove objave)

*Slike su generirane pomoću opisanih AI promptova, a zatim finalizirane u Canvi (dodavanje tipografije i integracija proizvoda).*

| Objava 1 | Objava 2 (s proizvodom) | Objava 3 |
| :---: | :---: | :---: |
| ![Objava 1](images/objava1.jpg) | ![Staklenka](images/staklenka.jpg) | ![Objava 3](images/objava3.jpg) |
| *Cilj: Poticanje interakcije* | *Cilj: Prikaz proizvoda i edukacija* | *Cilj: Emocionalna povezanost* |

### 🔍 Dokaz ljudske dorade
Kako bi se izbjeglo da AI "izmisli" etiketu, korištena je stvarna staklenka Dida Boža s njihove službene stranice, koja je naknadno ubačena u AI-generirani ambijent (prikazano na slici za Objavu 2).

---

## 🚀 Kako pokrenuti Python skriptu

### 1. Preduvjeti
Potreban vam je [Python 3.8+](https://www.python.org/downloads/) i aktivan [OpenAI API ključ](https://platform.openai.com/).

### 2. Instalacija
```bash
git clone https://github.com/1244Matt1244/dida-boza-ai-recept.git
cd dida-boza-ai-recept
pip install -r requirements.txt
```

### 3. Konfiguracija (.env)
Kopirajte primjer konfiguracijske datoteke i dodajte svoj API ključ:
```bash
cp config.example.env .env
```
Zatim otvorite `.env` i zamijenite vrijednost: `OPENAI_API_KEY=sk-proj-vas_tajni_kljuc_ovdje`. 
*(Napomena: `.env` je zaštićena `.gitignore` pravilima).*

### 4. Pokretanje
```bash
python generate_content.py
```

---

## ⚙️ Što skripta radi i primjer izlaza?
Skripta koristi OpenAI API (model **GPT-4o**) kako bi generirala specifične vizualne promptove, tekstove i hashtagove za sve tri forme (Karusel, Slika, Reel). Rezultat se **automatski sprema** u mapu `output/generirani_sadrzaj.txt`.

**Primjer generiranog izlaza:**
```text
--- OBJAVA 2: POJEDINAČNA SLIKA ---
Cilj: Poticanje interakcije
Vizualni prompt: "A rustic Mediterranean table setting featuring crusty sourdough..."
Ljudska dorada: "U Canvi izrežite stvarnu staklenku Dida Boža i postavite je..."
Tekst objave: "Slatko susreće slano. 🧀🍯 Jeste li ikada probali..."
Hashtagovi: #DidaBoza #Smokva #SlatkoSlano
```

---

## 📁 Struktura repozitorija
```text
├── generate_content.py      # Glavna skripta (Recept)
├── requirements.txt         # Python ovisnosti
├── config.example.env       # Primjer konfiguracije bez ključa
├── .gitignore               # Ignorira .env i output/
├── README.md                # Dokumentacija
├── Osvrt_i_Upute.pdf        # Završni PDF dokument
├── Tekstovi_objava.txt      # Konačni tekstovi
├── Recept_i_Promptovi.txt   # Paket promptova
└── images/                  # Finalni vizuali
```

## ⚠️ Ograničenja
AI generirane slike ne mogu se koristiti kao vjerodostojan prikaz stvarnog pakiranja bez intervencije čovjeka. Fokus je stavljen na statične objave jer AI video alati još uvijek imaju problema s konzistentnošću tekstura hrane u pokretu.
