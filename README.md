# Dida Boža — AI-Assisted Content & Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.10--3.12%20tested-blue)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-yellow)
![Tests](https://img.shields.io/badge/Tests-21%20passed-brightgreen)
[![CI](https://github.com/1244Matt1244/dida-boza-ai-recept/actions/workflows/tests.yml/badge.svg)](https://github.com/1244Matt1244/dida-boza-ai-recept/actions/workflows/tests.yml)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://dida-boza-ai-recept-hcp9mzhdpg2sauln56z57m.streamlit.app/)
![API Cost](https://img.shields.io/badge/API%20Cost-€0%20for%20core%20workflow-brightgreen)

Python projekt koji demonstrira pripremu AI-potpomognutog Instagram sadržaja, izradu vizualnih materijala, analizu društvenih metrika i automatizirano izvještavanje za hrvatski brend **Dida Boža**.

Projekt povezuje Python automatizaciju, prompt engineering, obradu slika, CSV podatke, analitičke izračune, Streamlit korisničko sučelje, automatizirano testiranje i GitHub Actions CI.

**Ključne kompetencije:** Python, automatizacija procesa, obrada i analiza podataka, prompt engineering, Streamlit, testiranje i Git/GitHub.

## 🚀 Live Demo

**[Otvori Dida Boža AI Content Studio](https://dida-boza-ai-recept-hcp9mzhdpg2sauln56z57m.streamlit.app/)**

Aplikacija je dostupna putem Streamlit Clouda. Za osnovni workflow nije potreban OpenAI API ključ.

## 1. Cilj projekta

Cilj je demonstrirati kako se AI alati i Python mogu koristiti za podršku digitalnom marketingu:

- priprema strukturiranih promptova za generiranje sadržaja;
- korištenje primjera komunikacijskog stila brenda;
- izrada Instagram carousel vizuala;
- priprema uputa za grafičku doradu;
- analiza Instagram metrika iz CSV datoteka;
- izračun engagement ratea;
- usporedba rezultata između dva razdoblja;
- generiranje tekstualnih izvještaja;
- izrada grafičkog dashboarda.

Projekt je osmišljen tako da se osnovni workflow može izvršavati bez plaćenih API poziva.

## 2. Tehnologije

| Tehnologija | Primjena |
|---|---|
| Python | Automatizacija i obrada podataka |
| ChatGPT | Ručno generiranje sadržaja na temelju promptova |
| Prompt Engineering | Strukturiranje zadataka i konteksta brenda |
| Pillow | Izrada i obrada vizualnih materijala |
| Matplotlib | Vizualizacija analitičkih rezultata |
| CSV | Ulazni podaci za analitiku |
| Streamlit | Interaktivno korisničko sučelje |
| pytest | Automatizirano testiranje |
| GitHub Actions | Kontinuirana integracija (CI) |

## 3. Streamlit aplikacija

Aplikacija sadrži pet funkcionalnih kartica:

### 1. Prompt

- unos proizvoda, ciljne publike i marketinškog cilja;
- učitavanje primjera tona komunikacije brenda;
- priprema strukturiranog prompta;
- pregled i preuzimanje prompta za ChatGPT.

### 2. Sadržaj

- ručno unošenje teksta generiranog u ChatGPT-u;
- provjera oznaka za tri Instagram objave;
- spremanje sadržaja u aktivnoj sesiji;
- preuzimanje tekstualne datoteke.

### 3. Karusel

- pokretanje Python skripte iz aplikacije;
- izrada Instagram carousel slajdova pomoću Pillow biblioteke;
- pregled generiranih PNG datoteka;
- pojedinačno preuzimanje slajdova.

Kod lokalnog pokretanja obrada se izvršava u lokalnom Python okruženju. U objavljenoj verziji aplikacije obrada se izvršava na Streamlit Cloud poslužitelju.

### 4. Analitika

- učitavanje vlastite CSV datoteke;
- korištenje demonstracijskih podataka;
- izračun prosječnih metrika;
- izračun prosječnog i ponderiranog engagement ratea;
- analiza rezultata prema tipu objave;
- analiza rezultata prema danu objavljivanja;
- pregled najčešćih hashtagova;
- provjera kvalitete podataka;
- generiranje i preuzimanje tekstualnog izvještaja.

Učitana CSV datoteka koristi se za analizu u aplikaciji. Analitički modul obrađuje podatke u okruženju u kojem je aplikacija pokrenuta, lokalno ili na Streamlit Cloud poslužitelju.

### 5. Izvještaji

- usporedba rezultata između dva razdoblja;
- generiranje tjednog izvještaja;
- izrada grafičkog dashboarda;
- pregled i preuzimanje generiranih datoteka.

**Napomena:** Trenutačna funkcija generiranja usporedbe, tjednog izvještaja i dashboarda koristi demonstracijske CSV datoteke projekta. Analiza vlastitog CSV-a dostupna je u četvrtoj kartici.

## 4. Struktura projekta

```text
dida-boza-ai-recept/
│
├── app.py                       # Streamlit aplikacija
├── generate_content.py          # Priprema prompta i sadržaja
├── make_carousel.py             # Generator karusela (Pillow)
├── analyze_metrics.py           # Analiza Instagram metrika
├── compare_metrics.py           # Usporedba razdoblja
├── weekly_report.py             # Tjedni izvještaj
├── create_dashboard.py          # Grafički dashboard
├── run_all.py                   # End-to-end pipeline
│
├── brand_voice_examples.txt
├── requirements.txt
│
├── metrics_template.csv
├── metrics_demo.csv
├── metrics_demo_old.csv
├── metrics_demo_new.csv
│
├── images/
│   └── karusel/
│       ├── slajd_1.png
│       ├── slajd_2.png
│       ├── slajd_3.png
│       └── slajd_4.png
│
├── output/
│   ├── prompt_za_chatgpt.txt
│   ├── canva_upute.txt
│   ├── instagram_report_*.txt
│   ├── weekly_report.txt
│   └── metrics_dashboard.png
│
├── tests/
│   ├── test_generate.py
│   └── test_analytics.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── PORTFOLIO.md
├── Osvrt_i_Upute.pdf
└── README.md
```

Generirane datoteke u direktoriju `output/` služe kao rezultati izvršavanja projekta i ne moraju biti dio Git repozitorija.

## 5. Instalacija

Potrebni su Python i Git.

Kloniranje repozitorija:

```bash
git clone https://github.com/1244Matt1244/dida-boza-ai-recept.git
cd dida-boza-ai-recept
```

Preporučeno je korištenje virtualnog okruženja:

```bash
python -m venv .venv
```

Aktivacija na Windowsu:

```bash
.venv\Scripts\activate
```

Instalacija ovisnosti:

```bash
python -m pip install -r requirements.txt
```

Provjera instalacije:

```bash
python -m pip check
```

## 6. Pokretanje Streamlit aplikacije

```bash
python -m streamlit run app.py
```

Aplikacija će se otvoriti u pregledniku, u pravilu na adresi:

```text
http://localhost:8501
```

## 7. Generiranje AI sadržaja

### Korak 1 — priprema prompta

```bash
python generate_content.py
```

Skripta učitava primjere komunikacijskog stila iz datoteke `brand_voice_examples.txt` i priprema prompt za ChatGPT.

Rezultat se sprema u:

```text
output/prompt_za_chatgpt.txt
```

Kopiraj sadržaj datoteke u ChatGPT i generiraj Instagram objave.

**Transparentnost:** Python skripta priprema prompt i upravlja datotekama. Generiranje teksta obavlja se ručno u ChatGPT-u, bez OpenAI API poziva.

### Korak 2 — izrada Instagram karusela

```bash
python make_carousel.py
```

Skripta izrađuje četiri PNG slajda u direktoriju:

```text
images/karusel/
```

Vizuali se izrađuju pomoću Pythona i Pillow biblioteke. Kod lokalnog pokretanja obrada se izvršava lokalno, a u objavljenoj Streamlit aplikaciji na poslužitelju.

### Korak 3 — priprema Canva uputa

Upute za grafičku doradu i pripremu vizuala generiraju se kroz glavni pipeline:

```text
output/canva_upute.txt
```

## 8. Automatizirani pipeline

Glavna skripta povezuje sedam koraka u jedinstveni proces:

```bash
python run_all.py
```

Pipeline obuhvaća:

1. Pripremu AI prompta.
2. Izradu carousel vizuala.
3. Pripremu Canva uputa.
4. Analizu Instagram metrika.
5. Usporedbu dvaju razdoblja.
6. Generiranje tjednog izvještaja.
7. Izradu grafičkog dashboarda.

Skripta prati uspješnost pojedinih koraka i prikazuje završni status izvršavanja.

## 9. Instagram Analytics

Analitički modul `analyze_metrics.py` obrađuje CSV datoteke bez potrebe za Instagram API integracijom.

Pokretanje analize:

```bash
python analyze_metrics.py --file metrics_demo_new.csv
```

Analiza obuhvaća:

- prosječan broj lajkova;
- prosječan broj komentara;
- broj spremanja;
- doseg;
- prosječni engagement rate;
- ponderirani engagement rate;
- rezultate prema tipu objave;
- rezultate prema danu objavljivanja;
- učestalost hashtagova;
- kvalitetu ulaznih podataka;
- preporuke za sljedeći ciklus sadržaja.

### CSV format

Ulazna datoteka treba sadržavati sljedeće stupce:

| Stupac | Opis |
|---|---|
| `datum` | Datum objave |
| `tip_objave` | Tip sadržaja |
| `lajkovi` | Broj lajkova |
| `komentari` | Broj komentara |
| `saves` | Broj spremanja |
| `doseg` | Doseg objave |
| `hashtagovi` | Korišteni hashtagovi |

### Engagement rate

Osnovni izračun:

```text
ER = (lajkovi + komentari + saves) / doseg × 100
```

Modul dodatno računa ponderirani engagement rate na temelju ukupnih interakcija i ukupnog dosega.

### Usporedba rezultata

```bash
python compare_metrics.py metrics_demo_old.csv metrics_demo_new.csv
```

### Tjedni izvještaj

```bash
python weekly_report.py
```

### Grafički dashboard

```bash
python create_dashboard.py
```

Dashboard se sprema u:

```text
output/metrics_dashboard.png
```

## 10. Demonstracijski rezultati

Za provjeru analitičkog modula korišteni su demonstracijski podaci s tri objave u svakom razdoblju.

| Metrika | Prethodno razdoblje | Novo razdoblje | Promjena |
|---|---:|---:|---:|
| Lajkovi | 121,67 | 153,33 | +26,03% |
| Komentari | 17,33 | 25,00 | +44,23% |
| Spremanja | 34,33 | 46,67 | +35,92% |
| Doseg | 3.366,67 | 3.933,33 | +16,83% |
| Engagement rate | 5,19% | 5,79% | +0,60 postotnih bodova |

Najuspješniji format u novom demonstracijskom uzorku bio je edukativni sadržaj s engagement rateom od 6,52%.

**Važno:** Podaci su simulirani i služe za demonstraciju funkcionalnosti analitičkog sustava. Nisu stvarni rezultati Instagram profila Dida Boža. Uzorak je premalen za pouzdane poslovne zaključke.

## 11. Automatizirano testiranje

Projekt sadrži 21 pytest test.

Pokretanje testova:

```bash
python -m pytest tests/ -v
```

**Rezultat posljednjeg lokalnog testiranja:**

```text
21 passed
```

Testovi provjeravaju:

- izradu i strukturu promptova;
- podršku za prilagođene teme;
- učitavanje primjera tona brenda;
- parsiranje brojeva i datuma;
- izračun analitičkih metrika;
- engagement rate;
- obradu neispravnih datuma i dosega;
- učitavanje CSV podataka;
- postojanje ključnih skripti.

GitHub Actions automatski pokreće testove na Python 3.10, 3.11 i 3.12.

## 12. Konfiguracija i troškovi

Osnovni workflow ne zahtijeva OpenAI API ključ.

- Promptove priprema Python.
- Tekstove generira korisnik ručno u ChatGPT-u.
- Karusel se izrađuje pomoću Pillow biblioteke.
- Analitika se izvršava nad CSV podacima.
- Demonstracijske metrike nisu stvarni Instagram podaci.
- Nema automatskih plaćenih API poziva u opisanom workflowu.

## 13. Ograničenja i transparentnost

Projekt razlikuje automatizirane funkcije od ručnih AI koraka.

- Generiranje teksta nije automatizirano putem OpenAI API-ja.
- Analitika se temelji na CSV podacima.
- Demonstracijski rezultati nisu stvarni poslovni podaci.
- Nije implementirano automatsko preuzimanje Instagram Insights podataka.
- Usporedba, tjedni izvještaj i dashboard u Streamlit kartici Izvještaji koriste demonstracijske datoteke.
- Projekt nije potpuno autonoman sustav za upravljanje društvenim mrežama.

## 14. Moguća buduća unapređenja

- Integracija sa stvarnim Instagram Insights podacima.
- Automatizirano preuzimanje metrika putem podržanog API-ja.
- Integracija baze podataka za povijesne rezultate.
- A/B testiranje promptova i sadržajnih formata.
- Proširenje dashboarda dodatnim analitičkim pokazateljima.
- Usporedba proizvoljno učitanih razdoblja kroz Streamlit sučelje.

---

**Autor:** Matej Martinović

**Projekt:** Dida Boža — AI-Assisted Content & Analytics Pipeline

**Tehnologije:** Python, AI Prompt Engineering, Pillow, Matplotlib, CSV, Streamlit, pytest, GitHub Actions

**GitHub:** https://github.com/1244Matt1244/dida-boza-ai-recept

**Live demo:** https://dida-boza-ai-recept-hcp9mzhdpg2sauln56z57m.streamlit.app/