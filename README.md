Evo točno onoga što trebaš kopirati i zalijepiti na GitHub. Tri datoteke, čisto i spremno za predaju.

### 1. `generate_content.py`
*(Otvori datoteku na GitHubu, klikni olovčicu, obriši sve i zalijepi ovo)*

```python
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
        
        # Automatsko stvaranje mape i spremanje datoteke
        os.makedirs("output", exist_ok=True)
        filename = "output/generirani_sadrzaj.txt"
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
            
        print(f"✅ USPJEŠNO GENERIRANO I SPREMLJENO u: {filename}\n")
        print("--- PREGLED SADRŽAJA (prvih 500 znakova) ---")
        print(content[:500] + "\n\n[...] (Ostatak pogledajte u generiranoj datoteci)")
        
        print("\n--- SLJEDEĆI KORAK: LJUDSKA DORADA ---")
        print("1. Generirajte vizuale prema promptovima u DALL-E 3.")
        print("2. U Canvi izrežite stvarnu staklenku Dida Boža i ubacite je u kadar.")
        print("3. Zalijepite dobivene tekstove ispod slika.")
        
    except Exception as e:
        print(f"❌ Došlo je do pogreške: {e}")
        print("Provjerite je li vaš API ključ valjan i imate li internetsku vezu.")

if __name__ == "__main__":
    generate_and_save_content()
```

---

### 2. `.gitignore`
*(Otvori datoteku na GitHubu, klikni olovčicu, obriši sve i zalijepi ovo)*

```text
.env
__pycache__/
*.pyc
output/
```

---

### 3. `README.md`
*(Otvori datoteku na GitHubu, klikni olovčicu, obriši sve i zalijepi ovo - status je sada "Završeno")*

```markdown
# 🍯 AI Recept: Dida Boža — Generator Instagram Sadržaja

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![Status](https://img.shields.io/badge/Status-Završeno-success)

Ovaj repozitorij sadrži izvršivi AI recept (Python skriptu) korišten za izradu tri gotove Instagram objave za hrvatski brend **Dida Boža**. 

Cilj projekta je demonstrirati kako se korištenjem AI alata (LLM i generativna slika) može ubrzati i unaprijediti proces stvaranja sadržaja za društvene mreže, uz zadržavanje autentičnog vizualnog identiteta brenda.

## 🎨 Vizualni rezultati (Finalne objave)

*Ove slike su generirane pomoću opisanih promptova, a zatim finalizirane u Canvi (integracija stvarnog proizvoda i tipografija).*

| Objava 1 | Objava 2 | Objava 3 |
| :---: | :---: | :---: |
| ![Objava 1](images/objava1.jpg) | ![Objava 2](images/objava2.jpg) | ![Objava 3](images/objava3.jpg) |
| *Cilj: Poticanje interakcije* | *Cilj: Edukacija i spremanje* | *Cilj: Emocionalna povezanost* |

### 🔍 Dokaz ljudske dorade (Integracija stvarnog brenda)
Kako bi se izbjeglo da AI "izmisli" etiketu, korištena je stvarna staklenka Dida Boža s njihove službene stranice, koja je naknadno ubačena u AI-generirani ambijent:

![Staklenka Dida Boža](images/staklenka.jpg)

---

## 🚀 Kako pokrenuti

### 1. Preduvjeti
Potreban vam je [Python 3.8+](https://www.python.org/downloads/) i aktivan [OpenAI API ključ](https://platform.openai.com/).

### 2. Instalacija
Klonirajte repozitorij i instalirajte potrebne ovisnosti:
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
Zatim otvorite `.env` datoteku i zamijenite vrijednost:
```text
OPENAI_API_KEY=sk-proj-vas_tajni_kljuc_ovdje
```
*(Napomena: `.env` datoteka je zaštićena `.gitignore` pravilima i nikada se neće poslati na GitHub).*

### 4. Pokretanje
```bash
python generate_content.py
```

---

## ⚙️ Što skripta radi?
Skripta koristi OpenAI API (model **GPT-4o**) kako bi generirala:
1. **Specifične vizualne promptove** za svaku od 3 objave (Karusel, Pojedinačna slika, Reel).
2. **Copy (tekstove)** i hashtagove prilagođene hrvatskom tržištu.
3. **Upute za ljudsku doradu** (kako spojiti AI pozadinu sa stvarnim proizvodom u Canvi).
4. Automatski sprema rezultate u `output/generirani_sadrzaj.txt`.

*Napomena: Skripta ne generira same slike kako bi se izbjeglo trošenje API kredita, već vraća točne promptove i tekstove koje možete zalijepiti u ChatGPT ili DALL-E.*

---

## 📁 Struktura repozitorija
```text
├── generate_content.py      # Glavna skripta (Recept)
├── requirements.txt         # Python ovisnosti
├── config.example.env       # Primjer konfiguracije bez ključa
├── .gitignore               # Ignorira .env i cache
├── README.md                # Dokumentacija
├── Osvrt_i_Upute.pdf        # Završni PDF dokument s osvrtom
├── Tekstovi_objava.txt      # Konačni tekstovi za sve tri objave
├── Recept_i_Promptovi.txt   # Paket promptova za ručno korištenje
└── images/                  # Finalni vizuali (dokaz rada)
```

## ⚠️ Ograničenja
AI generirane slike ne mogu se koristiti kao vjerodostojan prikaz stvarnog pakiranja bez intervencije čovjeka. Za najbolje rezultate, obavezna je integracija stvarnog proizvoda (ljudska dorada). Također, AI video alati još uvijek imaju problema s konzistentnošću tekstura hrane u pokretu, stoga je fokus stavljen na statične objave.

## 📄 Licenca
Ovaj projekt je otvorenog koda i dostupan pod [MIT licencom](https://choosealicense.com/licenses/mit/).
```

Kada sve tri datoteke ažuriraš na GitHubu, repozitorij je zaključan i spreman. Slobodno pošalji ZIP na e-mail i link na GitHub. Sretno!
