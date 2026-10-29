#!/usr/bin/env python3
"""Sanity checks on the built site: internal links, hreflang reciprocity, JSON-LD, horizontal scroll."""
import json, pathlib, re, sys
from shots import ROOT, serve, chrome

errors = []
pages = sorted(p for p in ROOT.rglob("*.html") if not any(x in p.parts for x in ("photos", "shots", ".git", ".idea")))


def to_file(href):
    path = href.split("#")[0].split("?")[0]
    f = ROOT / path.lstrip("/")
    return f / "index.html" if f.is_dir() or path.endswith("/") else f


for p in pages:
    h = p.read_text()
    rel = p.relative_to(ROOT)
    for m in re.findall(r'(?:href|src)="(/[^"]*)"', h):
        if not to_file(m).exists():
            errors.append(f"{rel}: broken link {m}")
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(raw)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    if rel.name != "404.html":
        for alt in re.findall(r'hreflang="(?:uk|en)" href="https://[^/]+(/[^"]*)"', h):
            back = to_file(alt).read_text()
            if f'rel="canonical" href="' not in back or alt not in back:
                errors.append(f"{rel}: hreflang target {alt} lacks reciprocal tags")
    if "Psychologist\"" in h and '"@type": "Psychologist"' in h:
        errors.append(f"{rel}: invalid schema type Psychologist")

# horizontal scroll at phone width: load each page in a same-origin iframe and measure
probe = ("<body><script>var out=[];var list=%s;var n=0;list.forEach(function(u){var f=document.createElement('iframe');f.style.cssText='width:390px;height:800px;border:0';"
         "f.src=u;f.onload=function(){var d=f.contentDocument.documentElement;if(d.scrollWidth>390)out.push(u+' '+d.scrollWidth);if(++n==list.length)document.body.setAttribute('data-r',JSON.stringify(out))};document.body.appendChild(f)})</script>")
urls = ["/" + str(p.relative_to(ROOT).parent).replace(".", "") + "/" for p in pages if p.name == "index.html"]
urls = [re.sub("//+", "/", u) for u in urls]
srv, base = serve({"/__probe__.html": probe % json.dumps(urls)})
dom = chrome("--virtual-time-budget=8000", "--dump-dom", f"{base}/__probe__.html").stdout
srv.shutdown()
m = re.search(r"data-r='?\"?(\[.*?\])", dom.replace("&quot;", '"'))
if not m:
    errors.append("scroll probe returned nothing")
elif json.loads(m.group(1)):
    errors += [f"horizontal scroll: {x}" for x in json.loads(m.group(1))]

print("\n".join(errors) or f"OK: {len(pages)} html files, links, hreflang, JSON-LD, no horizontal scroll")
sys.exit(1 if errors else 0)
