
"""
DIDA BOŽA — INSTAGRAM CAROUSEL GENERATOR

Generira 4 Instagram slajda u formatu 1080 x 1350.
Koristi Pillow, bez API poziva i bez dodatnih troškova.

Izlaz:
images/karusel/slajd_1.png
images/karusel/slajd_2.png
images/karusel/slajd_3.png
images/karusel/slajd_4.png
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

# --------------------------------------------------
# POSTAVKE
# --------------------------------------------------

W, H = 1080, 1350

IMAGE_DIR = Path("images")
OUTPUT_DIR = IMAGE_DIR / "karusel"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# FONTOVI
# --------------------------------------------------

def get_font(size, bold=False):
    """Učitaj Windows font ili koristi rezervni font."""

    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold
        else r"C:\Windows\Fonts\segoeui.ttf",

        r"C:\Windows\Fonts\arialbd.ttf" if bold
        else r"C:\Windows\Fonts\arial.ttf",

        "arial.ttf",
    ]

    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue

    return ImageFont.load_default()


# --------------------------------------------------
# OBRADA SLIKA
# --------------------------------------------------

def cover_resize(img, width, height):
    """Popuni zadani format bez deformiranja fotografije."""

    src_w, src_h = img.size
    scale = max(width / src_w, height / src_h)

    new_w = int(src_w * scale)
    new_h = int(src_h * scale)

    img = img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - width) // 2
    top = (new_h - height) // 2

    return img.crop((left, top, left + width, top + height))


def add_overlay(img, alpha=120):
    """Dodaj tamni prozirni sloj radi čitljivosti."""

    overlay = Image.new("RGBA", img.size, (0, 0, 0, alpha))

    return Image.alpha_composite(
        img.convert("RGBA"),
        overlay
    )


def pick_bg(*candidates):
    """Pronađi prvu dostupnu pozadinsku fotografiju."""

    for candidate in candidates:
        path = Path(candidate)

        if path.exists():
            return path

    for path in IMAGE_DIR.iterdir():
        if path.suffix.lower() in (".jpg", ".jpeg", ".png"):
            if OUTPUT_DIR not in path.parents:
                return path

    raise FileNotFoundError(
        "Nema dostupne fotografije u mapi images/."
    )


# --------------------------------------------------
# TEKST
# --------------------------------------------------

def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def wrap_text(draw, text, font, max_width):
    """Automatski prelamaj tekst prema raspoloživoj širini."""

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = (
            word if not current_line
            else current_line + " " + word
        )

        if text_width(draw, test_line, font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_center(draw, text, y, font,
                fill=(255, 255, 255),
                shadow=True,
                max_width=920):
    """Centrirano ispisivanje teksta s automatskim prelamanjem."""

    lines = wrap_text(draw, text, font, max_width)

    total_height = 0

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        x = (W - width) // 2

        if shadow:
            draw.text(
                (x + 3, y + 3),
                line,
                font=font,
                fill=(0, 0, 0, 180),
            )

        draw.text(
            (x, y),
            line,
            font=font,
            fill=fill,
        )

        y += height + 8
        total_height += height + 8

    return total_height


# --------------------------------------------------
# SIGURNO SPREMANJE
# --------------------------------------------------

def safe_save(img, out_path):
    """Spremi PNG privremeno pa zamijeni konačnu datoteku."""

    out_path = Path(out_path)
    temp_path = out_path.with_name(out_path.stem + "_temp.png")

    try:
        img.convert("RGB").save(temp_path, format="PNG")
        os.replace(temp_path, out_path)

    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


# --------------------------------------------------
# GENERIRANJE SLAJDA
# --------------------------------------------------

def make_slide(
    bg_path,
    title,
    subtitle=None,
    bullets=None,
    cta=None,
    out_path="slide.png",
    overlay_alpha=120,
    bullet_spacing=22,
    start_y=380,
    title_size=84,
    body_size=42,
):
    """Generiraj jedan Instagram slajd."""

    if not Path(bg_path).exists():
        raise FileNotFoundError(
            f"Pozadinska slika ne postoji: {bg_path}"
        )

    img = Image.open(bg_path).convert("RGB")
    img = cover_resize(img, W, H)
    img = add_overlay(img, overlay_alpha)

    draw = ImageDraw.Draw(img)

    font_title = get_font(title_size, bold=True)
    font_sub = get_font(38)
    font_body = get_font(body_size)
    font_cta = get_font(46, bold=True)

    y = start_y

    # NASLOV
    if title:
        for line in title.split("\n"):
            height = draw_center(
                draw,
                line,
                y,
                font_title,
            )

            y += height + 22

        y += 30

    # PODNASLOV
    if subtitle:
        height = draw_center(
            draw,
            subtitle,
            y,
            font_sub,
            fill=(240, 230, 210),
        )

        y += height + 50

    # NATUKNICE
    if bullets:
        y += 20

        for bullet in bullets:
            height = draw_center(
                draw,
                bullet,
                y,
                font_body,
            )

            y += height + bullet_spacing

    # POZIV NA AKCIJU
    if cta:
        y += 30

        draw_center(
            draw,
            cta,
            y,
            font_cta,
            fill=(255, 220, 150),
        )

    safe_save(img, out_path)

    print(f"Slajd spremljen: {out_path}")


# --------------------------------------------------
# SLAJD 1 — HOOK
# --------------------------------------------------

make_slide(
    bg_path=pick_bg(
        "images/objava2.jpg",
        "images/objava3.jpg",
        "images/objava1.jpg",
    ),
    title="Smokva. Kruh.\nMalo Mediterana.",
    subtitle="Povuci za priču o smokvi",
    cta="Otkrij inspiraciju",
    out_path=OUTPUT_DIR / "slajd_1.png",
    overlay_alpha=120,
)


# --------------------------------------------------
# SLAJD 2 — PROIZVOD
# --------------------------------------------------

make_slide(
    bg_path=pick_bg(
        "images/staklenka.jpg",
        "images/objava1.jpg",
    ),
    title="Dida Boža",
    subtitle="Ekološki džem od smokve",
    bullets=[
        "BIO certifikat",
        "240 g",
        "Dalmacija",
    ],
    out_path=OUTPUT_DIR / "slajd_2.png",
    overlay_alpha=110,
)


# --------------------------------------------------
# SLAJD 3 — EDUKACIJA
# --------------------------------------------------

make_slide(
    bg_path=pick_bg(
        "images/objava1.jpg",
        "images/objava3.jpg",
    ),
    title="Zašto smokva?",
    bullets=[
        "Prirodni šećeri, bez konzervansa",
        "Spaja se sa sirom, orasima, vinom",
        "Dalmacija u svakoj žlici",
    ],
    out_path=OUTPUT_DIR / "slajd_3.png",
    overlay_alpha=130,
    bullet_spacing=65,
    start_y=520,
    title_size=78,
    body_size=38,
)


# --------------------------------------------------
# SLAJD 4 — POZIV NA AKCIJU
# --------------------------------------------------

make_slide(
    bg_path=pick_bg(
        "images/objava3.jpg",
        "images/objava1.jpg",
    ),
    title="Koji je tvoj\nomiljeni način\nposluživanja?",
    subtitle="",
    cta="Piši nam u komentarima",
    out_path=OUTPUT_DIR / "slajd_4.png",
    overlay_alpha=140,
    title_size=76,
)


# --------------------------------------------------
# ZAVRŠETAK
# --------------------------------------------------

print("\nKarusel uspješno generiran.")
print(f"Lokacija: {OUTPUT_DIR.resolve()}")
print("Broj slajdova: 4")
