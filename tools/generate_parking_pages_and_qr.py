import csv
import html
import math
import os
import sys

sys.path.insert(0, r"C:\Users\rquevedo\AppData\Local\Temp\codex_qr_deps")

import qrcode
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = r"C:\Users\rquevedo\Music\parking mapa"
OUT_DIR = os.path.join(BASE_DIR, "qr_casillas_amarillas")
PAGES_DIR = os.path.join(BASE_DIR, "casillas")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
SITE_BASE_URL = "https://zamorafter.github.io/parking-puesto"

CODES = [
    "C-01",
    "D-01",
    "E-01",
    "F-01",
    "G-01",
    "L-01",
    "C-02",
    "E-02",
    "F-02",
    "L-02",
    "B-03",
    "C-03",
    "E-03",
    "L-03",
    "M-03",
    "B-04",
    "C-04",
    "D-04",
    "E-04",
    "F-04",
    "G-04",
    "H-04",
    "J-04",
    "L-04",
    "M-04",
    "G-05",
    "H-06",
    "I-07",
]


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Ubicación de Estacionamiento {code}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --navy-deep: #0a192f;
            --navy-card: rgba(17, 34, 64, 0.85);
            --navy-light: #172a45;
            --yellow-primary: #f5c518;
            --yellow-glow: rgba(245, 197, 24, 0.15);
            --text-light: #f8f9fa;
            --text-muted: #8892b0;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        body, html {{
            width: 100%;
            height: 100%;
            height: 100dvh;
            overflow: hidden;
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--navy-deep);
            background-image: radial-gradient(circle at center, var(--navy-light) 0%, var(--navy-deep) 100%);
            color: var(--text-light);
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .bg-glow-1 {{
            position: absolute;
            top: -10%;
            left: -10%;
            width: 60%;
            height: 60%;
            background: radial-gradient(circle, rgba(245, 197, 24, 0.08) 0%, rgba(10, 25, 47, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
        }}

        .bg-glow-2 {{
            position: absolute;
            bottom: -10%;
            right: -10%;
            width: 70%;
            height: 70%;
            background: radial-gradient(circle, rgba(23, 42, 69, 0.6) 0%, rgba(10, 25, 47, 0) 80%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
        }}

        .app-container {{
            width: 100%;
            max-width: 480px;
            height: 100%;
            height: 100dvh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 2rem 1.5rem;
            position: relative;
            z-index: 2;
        }}

        header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: fadeInDown 0.8s ease-out;
        }}

        .logo-badge {{
            background-image: url('../../vinil.jpg');
            background-size: cover;
            background-position: center;
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(245, 197, 24, 0.3);
            flex: 0 0 auto;
        }}

        .brand-name {{
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: var(--text-light);
        }}

        .brand-tagline {{
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .card {{
            background: var(--navy-card);
            border: 1px solid rgba(245, 197, 24, 0.15);
            border-radius: 24px;
            padding: 2.5rem 2rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 30px var(--yellow-glow);
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: zoomIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(to right, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.03) 50%, rgba(255, 255, 255, 0) 100%);
            transform: skewX(-25deg);
            transition: 0.75s;
        }}

        .card:hover::before {{
            left: 150%;
            transition: 0.75s;
        }}

        .info-text {{
            font-size: 1.35rem;
            line-height: 1.6;
            color: var(--text-light);
            margin-bottom: 0;
            font-weight: 600;
        }}

        .highlight-text {{
            color: var(--yellow-primary);
            font-weight: 800;
            display: inline-block;
            text-shadow: 0 0 10px rgba(245, 197, 24, 0.3);
        }}

        .zone {{
            font-size: 1.8rem;
            margin: 0.25rem 0;
        }}

        .spot {{
            font-size: 2.2rem;
        }}

        .logo-container {{
            margin-top: 2.5rem;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .logo-clean {{
            max-width: 170px;
            height: auto;
            animation: logoFloat 4s ease-in-out infinite;
        }}

        footer {{
            text-align: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            animation: fadeInUp 0.8s ease-out;
        }}

        @keyframes logoFloat {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-6px); }}
            100% {{ transform: translateY(0); }}
        }}

        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes zoomIn {{
            from {{ opacity: 0; transform: scale(0.9); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
    </style>
</head>
<body>
    <div class="bg-glow-1"></div>
    <div class="bg-glow-2"></div>

    <div class="app-container">
        <header>
            <div class="logo-badge" aria-hidden="true"></div>
            <div>
                <div class="brand-name">Parking Tolón</div>
                <div class="brand-tagline">Ubicación de estacionamiento</div>
            </div>
        </header>

        <main class="card">
            <p class="info-text">
                Usted está estacionado en el <br>
                <span class="highlight-text zone">Sótano 1, Lado Norte</span> <br>
                Columna <span class="highlight-text spot">{code}</span>
            </p>

            <div class="logo-container">
                <img src="../../logo.png" alt="Parking Tolón" class="logo-clean">
            </div>
        </main>

        <footer>
            <p>&copy; 2026 SmartPark. Todos los derechos reservados.</p>
        </footer>
    </div>
</body>
</html>
"""


def load_font(size):
    for path in [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def crop_black_margins(img):
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    min_x, min_y, max_x, max_y = width, height, 0, 0
    found = False

    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            if alpha > 10 and (red > 20 or green > 20 or blue > 20):
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                found = True

    if not found:
        return rgba

    pad = 18
    return rgba.crop(
        (
            max(min_x - pad, 0),
            max(min_y - pad, 0),
            min(max_x + pad + 1, width),
            min(max_y + pad + 1, height),
        )
    )


def contain(img, max_width, max_height):
    contained = img.copy()
    contained.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return contained


def write_pages():
    os.makedirs(PAGES_DIR, exist_ok=True)
    for code in CODES:
        page_dir = os.path.join(PAGES_DIR, code)
        os.makedirs(page_dir, exist_ok=True)
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8", newline="\n") as file:
            file.write(PAGE_TEMPLATE.format(code=html.escape(code)))


def write_qr_images():
    os.makedirs(OUT_DIR, exist_ok=True)
    label_font = load_font(54)
    small_font = load_font(28)
    title_font = load_font(44)
    logo_src = crop_black_margins(Image.open(LOGO_PATH))
    manifest_rows = []

    for code in CODES:
        url = f"{SITE_BASE_URL}/casillas/{code}/"
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=18,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_img = qr_img.resize((720, 720), Image.Resampling.NEAREST).convert("RGBA")

        badge_width, badge_height = 240, 136
        badge = Image.new("RGBA", (badge_width, badge_height), (0, 0, 0, 255))
        mask = Image.new("L", (badge_width, badge_height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, badge_width - 1, badge_height - 1), radius=18, fill=255)
        rounded_badge = Image.new("RGBA", (badge_width, badge_height), (0, 0, 0, 0))
        rounded_badge.paste(badge, (0, 0), mask)

        logo = contain(logo_src, 215, 110)
        rounded_badge.alpha_composite(
            logo,
            ((badge_width - logo.width) // 2, (badge_height - logo.height) // 2),
        )
        qr_img.alpha_composite(
            rounded_badge,
            ((720 - badge_width) // 2, (720 - badge_height) // 2),
        )

        canvas = Image.new("RGB", (820, 960), "white")
        canvas.paste(qr_img.convert("RGB"), (50, 40))
        draw = ImageDraw.Draw(canvas)
        bbox = draw.textbbox((0, 0), code, font=label_font)
        draw.text(((820 - (bbox[2] - bbox[0])) // 2, 790), code, fill="black", font=label_font)
        short_url = f"/casillas/{code}/"
        bbox2 = draw.textbbox((0, 0), short_url, font=small_font)
        draw.text(
            ((820 - (bbox2[2] - bbox2[0])) // 2, 855),
            short_url,
            fill=(80, 80, 80),
            font=small_font,
        )
        canvas.save(os.path.join(OUT_DIR, f"{code}.png"), "PNG")
        manifest_rows.append([code, f"{code}.png", url])

    with open(os.path.join(OUT_DIR, "lista_qr.csv"), "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["codigo", "archivo", "url"])
        writer.writerows(manifest_rows)

    thumb_width, thumb_height = 246, 292
    columns = 4
    rows = math.ceil(len(CODES) / columns)
    sheet = Image.new("RGB", (columns * thumb_width, rows * thumb_height + 70), "white")
    draw = ImageDraw.Draw(sheet)
    title = f"QR casillas amarillas con logo ({len(CODES)})"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((sheet.width - (bbox[2] - bbox[0])) // 2, 14), title, fill="black", font=title_font)

    for index, code in enumerate(CODES):
        image = Image.open(os.path.join(OUT_DIR, f"{code}.png")).convert("RGB")
        image.thumbnail((210, 250), Image.Resampling.LANCZOS)
        x = (index % columns) * thumb_width + (thumb_width - image.width) // 2
        y = 70 + (index // columns) * thumb_height
        sheet.paste(image, (x, y))

    sheet.save(os.path.join(OUT_DIR, "indice_qr_casillas_amarillas.png"), "PNG")


def main():
    write_pages()
    write_qr_images()
    print(f"Generated {len(CODES)} pages and QR images")
    print(f"First URL: {SITE_BASE_URL}/casillas/{CODES[0]}/")
    print(f"Last URL: {SITE_BASE_URL}/casillas/{CODES[-1]}/")


if __name__ == "__main__":
    main()
