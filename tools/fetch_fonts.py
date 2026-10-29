#!/usr/bin/env python3
"""Download latin + cyrillic woff2 subsets of Lora and Onest, write tools/fonts.css."""
import re, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
URL = "https://fonts.googleapis.com/css2?family=Lora:wght@400..700&family=Onest:wght@400..700&display=swap"

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read()

css = get(URL).decode()
out = []
for subset, family, body in re.findall(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S) and \
        [(m[0], re.search(r"font-family: '(\w+)'", m[1]).group(1), m[1])
         for m in re.findall(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S)]:
    if subset not in ("latin", "cyrillic"):
        continue
    src = re.search(r"url\((https:[^)]+)\)", body).group(1)
    name = f"{family.lower()}-{subset}.woff2"
    (ROOT / "fonts" / name).write_bytes(get(src))
    rng = re.search(r"unicode-range: ([^;]+);", body).group(1)
    out.append(
        f"@font-face{{font-family:'{family}';font-style:normal;font-weight:400 700;font-display:swap;"
        f"src:url(/fonts/{name}) format('woff2');unicode-range:{rng}}}"
    )
(ROOT / "tools" / "fonts.css").write_text("\n".join(out) + "\n")
print(*out, sep="\n")
