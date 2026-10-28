# AI Recept: Dida Boža (Instagram Content Generator)

Ovaj repozitorij sadrži izvršivi AI recept (skriptu) korišten za izradu tri gotove Instagram objave za brend Dida Boža. 

## Kako pokrenuti
1. Klonirajte repozitorij: `git clone <link>`
2. Instalirajte ovisnosti: `pip install -r requirements.txt`
3. Stvorite `.env` datoteku u glavnom direktoriju i upišite svoj OpenAI API ključ:
OPENAI_API_KEY=vasi_kljuc_ovdje

4. Pokrenite skriptu: `python generate_content.py`

## Što skripta radi?
Skripta koristi OpenAI API (GPT-4o) kako bi generirala:
1. Detaljne vizualne promptove za DALL-E 3 (za pozadinu).
2. Copy (tekstove) za tri različite objave (interakcija, edukacija, emocionalna povezanost).
3. Ispisuje upute za ljudsku doradu (integracija stvarne staklenke u Canvi).

*Napomena: Skripta ne generira same slike (kako bi se izbjeglo trošenje API kredita), već vraća točne promptove i tekstove koje možete zalijepiti u ChatGPT ili DALL-E.*

## Primjer izlaza (skraćeno)
```text
✅ USPJEŠNO GENERIRANO:

1. Vizualni prompt: "A rustic Mediterranean table setting..."
2. Tekst objave: "Slatko susreće slano. 🧀🍯 Jeste li ikada probali..."
3. Hashtagovi: #DidaBoza #Smokva #SlatkoSlano

--- SLJEDEĆI KORAK: LJUDSKA DORADA ---
1. Kopirajte vizualni prompt u ChatGPT/DALL-E.
...

---

### 3. requirements.txt

```text
openai
python-dotenv
