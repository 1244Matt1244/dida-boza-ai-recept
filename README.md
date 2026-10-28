# AI Recept: Dida Boža (Instagram Content Generator)

Ovaj repozitorij sadrži izvršivi AI recept (skriptu) korišten za izradu tri gotove Instagram objave za brend Dida Boža. 

## Kako pokrenuti
1. Klonirajte repozitorij: `git clone <link>`
2. Instalirajte ovisnosti: `pip install -r requirements.txt`
3. Postavite svoj OpenAI API ključ kao environment varijablu: `export OPENAI_API_KEY="vasi_kljuc"`
4. Pokrenite skriptu: `python generate_content.py`

## Što skripta radi?
Skripta koristi OpenAI API (GPT-4) kako bi generirala:
1. Detaljne vizualne promptove za DALL-E 3 (za pozadinu).
2. Copy (tekstove) za tri različite objave (interakcija, edukacija, emocionalna povezanost).
3. Ispisuje upute za ljudsku doradu (integracija stvarne staklenke u Canvi).

*Napomena: Skripta ne generira same slike (kako bi se izbjeglo trošenje API kredita), već vraća točne promptove i tekstove koje možete zalijepiti u ChatGPT ili DALL-E.*
