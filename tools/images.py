#!/usr/bin/env python3
"""Optimise photos from photos/ into img/ and render icons and og-image via headless Chrome."""
import base64, pathlib, shutil, subprocess, tempfile
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or "chromium"

SAGE, CREAM, INK = "#4F7360", "#F3EFE8", "#2B3A33"

# hero crop box on the 1280x1280 source: 4:5, centred on the face
HERO_BOX = (138, 0, 1162, 1280)
# about photo (853x1280 after EXIF rotation): 4:5 crop keeping the head and laptop
ABOUT_BOX = (0, 214, 853, 1280)

ICON_SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<style>.bg{{fill:{SAGE}}}.a{{stroke:{CREAM}}}@media (prefers-color-scheme:dark){{.bg{{fill:#9DBFA9}}.a{{stroke:#1B211E}}}}</style>
<rect class="bg" width="64" height="64" rx="16"/>
<path class="a" d="M19 47 32 17 45 47M24.5 37h15" fill="none" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/></svg>"""


def shot(html, out, w, h):
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d) / "p.html"
        f.write_text(html)
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={out}", f"--window-size={w},{h}", "--force-device-scale-factor=1",
                        "--allow-file-access-from-files", f.as_uri()],
                       check=True, capture_output=True)


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def font_css():
    css = ""
    for fam, name in (("Lora", "lora-cyrillic"), ("Lora", "lora-latin"), ("Onest", "onest-cyrillic"), ("Onest", "onest-latin")):
        css += f"@font-face{{font-family:'{fam}';font-weight:400 700;src:url({b64(ROOT / 'fonts' / (name + '.woff2'), 'font/woff2')})}}"
    return css


def photos():
    src = ROOT / "photos" / "IMG_3574.JPG"
    im = Image.open(src).convert("RGB").crop(HERO_BOX)
    for w in (640, 1024):
        h = round(w * 5 / 4)
        im.resize((w, h), Image.LANCZOS).save(ROOT / "img" / f"alina-portrait-{w}.webp", "WEBP", quality=80, method=6)
    im2 = ImageOps.exif_transpose(Image.open(ROOT / "photos" / "IMG_7619.jpeg")).convert("RGB").crop(ABOUT_BOX)
    for w in (640, 853):
        im2.resize((w, round(w * 5 / 4)), Image.LANCZOS).save(ROOT / "img" / f"alina-work-{w}.webp", "WEBP", quality=80, method=6)
    return src


def icons():
    (ROOT / "favicon.svg").write_text(ICON_SVG)
    svg = b64(ROOT / "favicon.svg", "image/svg+xml")
    page = lambda s: f"<body style='margin:0;background:transparent'><img src='{svg}' width='{s}' height='{s}' style='display:block'>"
    for name, s in (("favicon-32.png", 32), ("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
        shot(page(s), ROOT / name, s, s)


def og():
    portrait = b64(ROOT / "img" / "alina-portrait-1024.webp", "image/webp")
    html = f"""<style>{font_css()}
body{{margin:0;width:1200px;height:630px;background:{CREAM};font-family:Onest;color:{INK};display:flex;overflow:hidden}}
.t{{flex:1;padding:70px 20px 70px 80px;display:flex;flex-direction:column;justify-content:center}}
.k{{font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:{SAGE};font-weight:600}}
h1{{font-family:Lora;font-size:92px;line-height:1.05;margin:18px 0 22px}}
p{{font-size:34px;line-height:1.35;margin:0;color:#58675F}}
.p{{width:430px;margin:50px 80px 0 0;border-radius:999px 999px 18px 18px;overflow:hidden;height:640px;background:#EAE5DA}}
.p img{{width:100%;height:100%;object-fit:cover;object-position:50% 20%}}</style>
<div class="t"><div class="k">Психологиня · Psychologist</div><h1>Аліна Буба</h1><p>КПТ, нейропсихологія, психодіагностика.<br>Онлайн, українською й англійською.</p></div>
<div class="p"><img src="{portrait}"></div>"""
    shot(html, ROOT / "og-image.png", 1200, 630)


if __name__ == "__main__":
    (ROOT / "img").mkdir(exist_ok=True)
    photos(); icons(); og()
    for p in sorted((ROOT / "img").iterdir()):
        print(p.name, p.stat().st_size // 1024, "KB")
