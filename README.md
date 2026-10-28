# 🍯 AI Recept: Dida Boža — Generator Instagram Sadržaja

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![Status](https://img.shields.io/badge/Status-Završeno-success)

Ovaj repozitorij sadrži izvršivi AI recept (Python skriptu) korišten za izradu tri gotove Instagram objave za hrvatski brend **Dida Boža**. 

Cilj projekta je demonstrirati kako se korištenjem AI alata (LLM i generativna slika) može ubrzati i unaprijediti proces stvaranja sadržaja za društvene mreže, uz zadržavanje autentičnog vizualnog identiteta brenda.

## 📦 Isporučeni materijali (Deliverables)
Svi ključni dokumenti i datoteke dostupni su izravno u repozitoriju:
*   📄 [Osvrt i upute (PDF)](./Osvrt_i_Upute.pdf) - Dokumentacija, analiza i osvrt.
*   📝 [Tekstovi objava (TXT)](./Tekstovi_objava.txt) - Konačni copy za sve tri objave.
*   ⚙️ [Recept i promptovi (TXT)](./Recept_i_Promptovi.txt) - Paket promptova za ručno korištenje.
*   🐍 [Python skripta](./generate_content.py) - Automatizirani generator sadržaja.

## 🎨 Vizualni rezultati (Tri gotove objave)

*Ove slike su generirane pomoću opisanih AI promptova, a zatim finalizirane u Canvi (dodavanje tipografije).*

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
Skripta koristi OpenAI API (model **GPT-4o**) kako bi generirala specifične vizualne promptove, tekstove i hashtagove za tri formata (Karusel, Slika, Reel). Rezultat automatski sprema u mapu `output/`.

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
AI generirane slike ne mogu se koristiti kao vjerodostojan prikaz stvarnog pakiranja bez intervencije čovjeka. Za najbolje rezultate, obavezna je integracija stvarnog proizvoda (ljudska dorada). Fokus je stavljen na statične objave jer AI video alati još uvijek imaju problema s konzistentnošću tekstura hrane u pokretu.

