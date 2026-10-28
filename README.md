# 🍯 AI Recept: Dida Boža — Generator Instagram Sadržaja

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)
![Status](https://img.shields.io/badge/Status-Završeno-success)

Ovaj repozitorij sadrži izvršivi AI recept (Python skriptu) korišten za izradu tri gotove Instagram objave za hrvatski brend **Dida Boža**. Projekt demonstrira kako se korištenjem AI alata može ubrzati proces stvaranja sadržaja uz zadržavanje autentičnog vizualnog identiteta brenda.

## 📦 Isporučeni materijali (Deliverables)
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
Kako bi se izbjeglo da AI "izmisli" etikete, korištena je stvarna staklenka Dida Boža s njihove službene stranice, koja je naknadno ubačena u AI-generirani ambijent (prikazano na slici za Objavu 2).

---

## 📝 Konačni tekstovi objava (Copy)

**Objava 1 (Slatko susreće slano)**
> Slatko susreće slano. 🧀🍯
> Jeste li ikada probali smokvu uz sir? Ta mala promjena donosi potpuno novo iskustvo za stolom. Dida Boža džem od smokve savršeno se slaže s kremastim sirom na kriški domaćeg kruha. 
> Ako ste ljubitelj ovakvih kombinacija, napišite nam u komentarima - koji je vaš omiljeni sir uz smokvu? 👇
> #DidaBoza #Smokva #SlatkoSlano #Dalmacija #Gourmet #FoodieCroatia

**Objava 2 (Smokva. Kruh. Malo Mediterana.)**
> Mali mediteranski ritual. 🌿🌊
> Smokva. Kruh. Malo Mediterana. Ponekad je za savršen užitak potrebno samo nekoliko pravih sastojaka i trenutak vremena za sebe. 
> Spremite ovu objavu za svoj sljedeći brunch i uživajte u okusu Dalmacije. 📌
> #DidaBoza #MediteranskiUgođaj #Brunch #SlowLiving #EkoDzem #HrvatskaHrana

**Objava 3 (Mali ritual. Veliki užitak.)**
> Okus koji usporava dan. ⏳✨
> Mali ritual. Veliki užitak. Pronađite svoj omiljeni način posluživanja našeg ekološkog džema od smokve. Bilo da ga mažete na tost, dodajete u jogurt ili poslužujete uz sir – svaki zalogaj je podsjetnik na sunce i more.
> Označite osobu s kojom biste podijelili ovaj trenutak. 👇
> #DidaBoza #Smokva #Tradicija #Uživanje #BreakfastIdeas #CroatianFood

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

**Opcija A — s API ključem (stvarno generiranje):**
```bash
python generate_content.py
```

**Opcija B — bez API ključa (dry-run za testiranje):**
```bash
python generate_content.py --dry-run
```

---

## ⚙️ Što skripta radi i primjer izlaza?
Skripta koristi OpenAI API (model **GPT-4o**) kako bi generirala specifične vizualne promptove, tekstove i hashtagove za sve tri forme (Karusel, Slika, Reel). Rezultat se **automatski sprema** u mapu `output/`.

**Primjer izlaza nakon pokretanja (dry-run):**
```text
🚀 Pokrećem AI Recept za Dida Boža...
ℹ️  Dry-run način: koristim primjer izlaza (bez API poziva).
✅ Sadržaj spremljen u mapu 'output/'.
```

Struktura generirane mape:
```text
output/
├── generirani_sadrzaj.txt
├── objava_1.txt
├── objava_2.txt
└── objava_3.txt
```

---

## 📁 Struktura repozitorija
```text
├── generate_content.py      # Glavna skripta
├── requirements.txt         # Python ovisnosti
├── config.example.env       # Primjer konfiguracije bez ključa
├── .gitignore               # Ignorira .env i output/
├── README.md                # Dokumentacija
├── Osvrt_i_Upute.pdf        # Završni PDF dokument
├── Tekstovi_objava.txt      # Konačni tekstovi
├── Recept_i_Promptovi.txt   # Paket promptova
└── images/                  # Finalni vizuali
```

## ⚠️ Ograničenja i napomene
1. AI generirane slike ne mogu se koristiti kao vjerodostojan prikaz stvarnog pakiranja bez intervencije čovjeka (integracija staklenke).
2. Fokus je stavljen na statične objave. Iako skripta generira i promptove za Reel, konačni video nije priložen jer je zadatak dopuštao odabir formata (odabrane su tri statične slike).
3. **Napomena o PDF-u:** Ako se PDF datoteka ne prikazuje ispravno u GitHubovom pregledniku, istu možete preuzeti klikom na gumb "Download" i otvoriti lokalno.
4. **Napomena o testiranju:** Skripta je testirana u `--dry-run` načinu rada. Stvarno generiranje putem API-ja zahtijeva vlastiti OpenAI ključ.
