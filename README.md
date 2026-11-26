# Dida Boža — AI-Assisted Content & Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-yellow)
![Tests](https://img.shields.io/badge/Tests-21%20passed-brightgreen)
![API Cost](https://img.shields.io/badge/API%20Cost-€0%20in%20local%20workflow-brightgreen)

Python projekt koji demonstrira pripremu AI-generiranog Instagram sadržaja, lokalnu automatizaciju vizualnih materijala i analizu društvenih metrika za hrvatski brend **Dida Boža**.

Projekt povezuje Python automatizaciju, prompt engineering, obradu slika, CSV podatke i analitičko izvještavanje u jedinstveni workflow.

## 1. Cilj projekta

Cilj je demonstrirati kako se AI alati i Python mogu koristiti za podršku digitalnom marketingu:

- priprema strukturiranih promptova za generiranje sadržaja;
- korištenje primjera komunikacijskog stila brenda;
- izrada Instagram carousel vizuala;
- priprema uputa za grafičku doradu;
- analiza demonstracijskih Instagram metrika;
- usporedba rezultata između dva razdoblja;
- generiranje izvještaja i grafičkog dashboarda.

Projekt je osmišljen tako da se osnovni workflow može izvršavati bez plaćenih API poziva.

## 2. Tehnologije

| Tehnologija | Primjena |
|---|---|
| Python | Automatizacija i obrada podataka |
| ChatGPT | Ručno generiranje sadržaja na temelju pripremljenih promptova |
| AI Prompt Engineering | Strukturiranje zadataka i konteksta brenda |
| Pillow | Izrada i obrada vizualnih materijala |
| Pandas | Analiza i obrada CSV podataka |
| Matplotlib | Vizualizacija analitičkih rezultata |
| CSV | Pohrana demonstracijskih i analitičkih podataka |
| Streamlit | Sučelje aplikacije |
| pytest | Automatizirano testiranje |

## 3. Struktura projekta

```text
dida-boza-ai-recept/
│
├── app.py
├── generate_content.py
├── make_carousel.py
├── analyze_metrics.py
├── compare_metrics.py
├── weekly_report.py
├── create_dashboard.py
├── run_all.py
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
│   ├── analiza_rezultata.txt
│   └── ...
│
└── tests/
    ├── test_generate.py
    └── test_analytics.py
```

Generirane datoteke u direktoriju `output/` ne moraju biti dio Git repozitorija.

## 4. Instalacija

Potrebni su Python 3.8 ili noviji i Git.

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
source .venv/Scripts/activate
```

Instalacija ovisnosti:

```bash
python -m pip install -r requirements.txt
```

Provjera instalacije:

```bash
python -m pip check
```

## 5. Generiranje AI sadržaja

### Korak 1 — priprema prompta

```bash
python generate_content.py
```

Skripta učitava primjere komunikacijskog stila brenda iz datoteke `brand_voice_examples.txt` i priprema prompt za ChatGPT.

Prompt se sprema u:

```text
output/prompt_za_chatgpt.txt
```

Kopiraj sadržaj datoteke u ChatGPT i generiraj tri Instagram objave.

**Napomena:** Python skripta priprema prompt i upravlja datotekama. Generiranje teksta obavlja se ručno u ChatGPT-u, bez OpenAI API poziva.

### Dodatne opcije generatora

Prilagođavanje teme:

```bash
python generate_content.py --topic "Mediteranski doručak"
```

Prikaz prompta bez spremanja:

```bash
python generate_content.py --dry-run
```

Odabir datoteke s primjerima tona brenda:

```bash
python generate_content.py --examples-file brand_voice_examples.txt
```

Ručno spremanje sadržaja generiranog u ChatGPT-u:

```bash
python generate_content.py --save-content
```

Nakon pokretanja postupka slijedi upute u terminalu za unos i spremanje generiranog sadržaja.

### Korak 2 — izrada Instagram karusela

```bash
python make_carousel.py
```

Skripta izrađuje četiri PNG slajda u direktoriju:

```text
images/karusel/
```

Vizuali se izrađuju lokalno pomoću Pythona i Pillow biblioteke.

### Korak 3 — priprema Canva uputa

Upute za grafičku doradu i pripremu vizuala generiraju se kroz glavni pipeline:

```text
output/canva_upute.txt
```

## 6. Automatizirani pipeline

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

Dodatne opcije:

**Preskakanje analitičkih koraka:**

```bash
python run_all.py --skip-analytics
```

Pokreće pripremu prompta, izradu karusela i Canva upute, bez analize, usporedbe, izvještaja i dashboarda.

**Ručno spremanje AI sadržaja:**

```bash
python run_all.py --save-content
```

Pokreće samo postupak ručnog spremanja sadržaja generiranog u ChatGPT-u, a zatim završava.

Nakon spremanja sadržaja, za pokretanje cijelog pipelinea koristi:

```bash
python run_all.py
```

## 7. Instagram Analytics

Projekt sadrži zaseban modul za analizu Instagram metrika.

Pokretanje:

```bash
python analyze_metrics.py metrics_demo_new.csv
```

Analiza obuhvaća:

- prosječan broj lajkova;
- prosječan broj komentara;
- broj spremanja;
- doseg;
- engagement rate;
- usporedbu tipova objava;
- analizu dana objavljivanja;
- učestalost hashtagova;
- preporuke za sljedeći ciklus.

### Usporedba rezultata

Za usporedbu prethodnog i novog razdoblja:

```bash
python compare_metrics.py metrics_demo_old.csv metrics_demo_new.csv
```

Modul omogućuje usporedbu ključnih metrika i promjena između dva razdoblja.

### Tjedni izvještaj

```bash
python weekly_report.py
```

Skripta generira izvještaj s pregledom analitičkih rezultata.

### Grafički dashboard

```bash
python create_dashboard.py
```

Rezultat se sprema u:

```text
output/metrics_dashboard.png
```

## 8. Demonstracijski rezultati

Za provjeru analitičkog modula korišteni su demonstracijski podaci s tri objave u svakom razdoblju.

| Metrika | Prethodno razdoblje | Novo razdoblje | Promjena |
|---|---:|---:|---:|
| Lajkovi | 121,67 | 153,33 | +26,03% |
| Komentari | 17,33 | 25,00 | +44,23% |
| Spremanja | 34,33 | 46,67 | +35,92% |
| Doseg | 3.366,67 | 3.933,33 | +16,83% |
| Engagement rate | 5,19% | 5,79% | +0,60 postotnih bodova |

Najuspješniji format u novom demonstracijskom uzorku bio je edukativni sadržaj s engagement rateom od 6,52%.

**Važno:** navedeni podaci su simulirani i služe za demonstraciju funkcionalnosti analitičkog sustava. Nisu stvarni rezultati Instagram profila Dida Boža. Uzorak je premalen za pouzdane poslovne zaključke.

## 9. Automatizirano testiranje

Projekt sadrži 21 pytest test.

Pokretanje testova:

```bash
python -m pytest tests/ -v
```

**Rezultat zadnjeg testiranja:**

```text
21 passed
```

Testovi provjeravaju:

- izradu i strukturu promptova;
- podršku za prilagođene teme;
- učitavanje primjera tona brenda;
- spremanje sadržaja;
- parsiranje brojeva i datuma;
- izračun analitičkih metrika;
- usporedbu rezultata.

Provjera sintakse Python datoteka:

```bash
python -m compileall -q .
```

## 10. Konfiguracija i troškovi

Osnovni workflow ne zahtijeva OpenAI API ključ.

- Promptove priprema Python.
- Tekstove generira korisnik ručno u ChatGPT-u.
- Karusel se izrađuje lokalno pomoću Pythona i Pillow biblioteke.
- Analitika se izvršava lokalno nad CSV podacima.
- Demonstracijske metrike nisu stvarni Instagram podaci.
- U aktualnom workflowu nema plaćenih API poziva.

Za lokalno pokretanje osnovnog pipelinea nije potrebno konfigurirati `OPENAI_API_KEY`.

## 11. Ograničenja i transparentnost

Projekt razlikuje automatizirane funkcije od ručnih AI koraka.

- Generiranje teksta nije automatizirano putem API-ja.
- Analitika se temelji na CSV podacima.
- Demonstracijski rezultati nisu stvarni poslovni podaci.
- Nije implementirano automatsko preuzimanje Instagram Insights podataka.
- Projekt ne predstavlja potpuno autonomni sustav za upravljanje društvenim mrežama.

Time se izbjegava predstavljanje demonstracijskih rezultata kao stvarnih poslovnih podataka ili ručnog AI procesa kao potpuno autonomnog sustava.

## 12. Moguća buduća unapređenja

- Povezivanje sa stvarnim Instagram Insights podacima.
- Automatizirano preuzimanje metrika putem podržanog API-ja.
- Integracija baze podataka za povijesne rezultate.
- A/B testiranje promptova i sadržajnih formata.
- Proširenje dashboarda dodatnim analitičkim pokazateljima.
- Daljnje proširenje Streamlit sučelja.

---

**Autor:** Matej Martinović

**Projekt:** Dida Boža — AI-Assisted Content & Analytics Pipeline

**Tehnologije:** Python, AI Prompt Engineering, Pillow, Pandas, Matplotlib, CSV, Streamlit, pytest

**GitHub:** https://github.com/1244Matt1244/dida-boza-ai-recept