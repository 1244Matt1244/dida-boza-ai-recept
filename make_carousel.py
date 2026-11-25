"""
Generira 4 slajda za Instagram karusel od postojećih slika.
Koristi Pillow (PIL) — bez ikakvih API poziva ili trošenja.
Izlaz: images/karusel/slajd_1.png ... slajd_4.png
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("images/karusel", exist_ok=True)

W, H = 1080, 1350  # Instagram 4:5 format


def get_font(size, bold=False):
    """Probaj nekoliko fontova; fallback na default."""
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        "arial.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def cover_resize(img, W, H):
    """Resize image to cover WxH, crop overflow (Instagram format)."""
    src_w, src_h = img.size
    scale = max(W / src_w, H / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    return img.crop((left, top, left + W, top + H))


def add_overlay(img, alpha=120):
    """Dodaj poluprozimu crnu podlogu za čitljivost teksta."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def draw_center(draw, text, y, font, fill=(255, 255, 255), shadow=True):
    """Centrirani tekst s mekom sjenom."""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2
    if shadow:
        draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def make_slide(bg_path, title, subtitle=None, bullets=None, cta=None,
               out_path="slide.png", overlay_alpha=120):
    if not os.path.exists(bg_path):
        raise FileNotFoundError(f"Slika ne postoji: {bg_path}")

    img = Image.open(bg_path).convert("RGB")
    img = cover_resize(img, W, H)
    img = add_overlay(img, overlay_alpha)
    draw = ImageDraw.Draw(img)

    font_title = get_font(84, bold=True)
    font_sub = get_font(38)
    font_body = get_font(42)
    font_cta = get_font(46, bold=True)

    y = 380

    if title:
        for line in title.split("\n"):
            h = draw_center(draw, line, y, font_title)
            y += h + 22
        y += 30

    if subtitle:
        h = draw_center(draw, subtitle, y, font_sub, fill=(240, 230, 210))
        y += h + 50

    if bullets:
        y += 20
        for b in bullets:
            h = draw_center(draw, b, y, font_body)
            y += h + 22

    if cta:
        y += 50
        draw_center(draw, cta, y, font_cta, fill=(255, 220, 150))

    img.convert("RGB").save(out_path, "PNG")
    print(f"✅ {out_path}")


# --- Provjeri koje slike postoje; fallback na bilo koju dostupnu ---
def pick_bg(*candidates):
    for c in candidates:
        if os.path.exists(c):
            return c
    # Fallback: prva .jpg u images/
    for f in os.listdir("images"):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            return os.path.join("images", f)
    raise FileNotFoundError("Nema nijedne slike u images/ za karusel.")


# --- Slajd 1: Hook (povuci za priču) ---
make_slide(
    bg_path=pick_bg("images/objava2.jpg", "images/objava3.jpg", "images/objava1.jpg"),
    title="Smokva. Kruh.\nMalo Mediterana.",
    subtitle="→ Povuci za priču o smokvi",
    out_path="images/karusel/slajd_1.png",
    overlay_alpha=110,
)

# --- Slajd 2: Prikaz proizvoda ---
make_slide(
    bg_path=pick_bg("images/staklenka.jpg", "images/objava1.jpg"),
    title="Dida Boža",
    subtitle="Ekološki džem od smokve",
    bullets=["BIO certifikat", "240 g", "Dalmacija"],
    out_path="images/karusel/slajd_2.png",
    overlay_alpha=110,
)

# --- Slajd 3: Edukacija ---
make_slide(
    bg_path=pick_bg("images/objava1.jpg", "images/objava3.jpg"),
    title="Zašto smokva?",
    bullets=[
        "Prirodni šećeri, bez konzervansa",
        "Spaja se sa sirom, orasima, vinom",
        "Dalmacija u svakoj žlici",
    ],
    out_path="images/karusel/slajd_3.png",
    overlay_alpha=130,
)

# --- Slajd 4: CTA (poziv na akciju) ---
make_slide(
    bg_path=pick_bg("images/objava3.jpg", "images/objava1.jpg"),
    title="Koji je tvoj\nomiljeni način\nposluživanja?",
    subtitle="👇",
    cta="Piši nam u komentarima",
    out_path="images/karusel/slajd_4.png",
    overlay_alpha=140,
)

print("\n🎉 Karusel spreman u images/karusel/")
print("Za pregled: otvori 4 PNG-a u folderu.")