#!/usr/bin/env python3
"""Static site generator for the psychologist's site. Run: python3 tools/build.py
Content lives in tools/content.py, fonts CSS in tools/fonts.css, images are made by tools/images.py."""
import datetime, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from content import PAGES  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ---- settings -------------------------------------------------------------
SITE = "https://alinabuba.github.io"
GA_ID = "G-PJW885J5PS"
DEMO = False  # True: noindex + yellow banner. Set False for the real launch.
HOURS = {"ua": "пн–сб, 9:00–21:00", "en": "Mon–Sat, 9:00–21:00"}
NAME = {"ua": "Аліна Буба", "en": "Alina Buba"}
TODAY = datetime.date.today().isoformat()

LANGS = ("ua", "en")
ORDER = ["home", "about", "specializations", "services", "faq", "contacts", "privacy"]
SLUG = {"home": "", "about": "about/", "specializations": "specializations/", "services": "services/",
        "faq": "faq/", "contacts": "contacts/", "privacy": "privacy/"}
NAV = ["about", "specializations", "services", "faq", "contacts"]
LABEL = {
    "home": ("Головна", "Home"), "about": ("Про мене", "About"), "specializations": ("Спеціалізації", "Specialisations"),
    "services": ("Послуги", "Services"), "faq": ("FAQ", "FAQ"), "contacts": ("Контакти", "Contacts"),
    "privacy": ("Конфіденційність", "Privacy"),
}


def parse_contacts():
    """contacts.md: URLs are classified by host, 'Key: value' lines by key. Nothing is invented."""
    out = {}
    p = ROOT / "contacts.md"
    if not p.exists():
        return out
    hosts = {"instagram.com": "instagram", "t.me": "telegram", "telegram.me": "telegram", "facebook.com": "facebook",
             "linkedin.com": "linkedin", "viber.com": "viber"}
    keys = {"telegram": "telegram", "viber": "viber", "instagram": "instagram", "facebook": "facebook", "linkedin": "linkedin",
            "пошта": "email", "email": "email", "e-mail": "email", "телефон": "phone", "phone": "phone"}
    for line in p.read_text().splitlines():
        for url in re.findall(r"https?://[^\s)>\]]+", line):
            for host, key in hosts.items():
                if host in url:
                    out[key] = url
        m = re.match(r"\s*[-*]?\s*([^:]+):\s*(\S.*)$", line)
        if m and m.group(1).strip().lower() in keys and not m.group(2).startswith("//"):
            out.setdefault(keys[m.group(1).strip().lower()], m.group(2).strip())
    return out


CONTACTS = parse_contacts()

# ---- theme tokens ---------------------------------------------------------
LIGHT = dict(bg="#F3EFE8", surface="#FBF9F5", alt="#EAE5DA", fg="#2B3A33", muted="#58675F", accent="#4F7360",
             line="#DDD7CB", onacc="#FFFFFF")
DARK = dict(bg="#1B211E", surface="#232B27", alt="#202824", fg="#E8EDE7", muted="#A3B0A8", accent="#9DBFA9",
            line="#33403A", onacc="#1B211E")


def tokens(d):
    return "".join(f"--{k}:{v};" for k, v in d.items())


CSS = (
    ":root{" + tokens(LIGHT) + "--r:18px;color-scheme:light}"
    "@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){" + tokens(DARK) + "color-scheme:dark}}"
    ":root[data-theme=\"dark\"]{" + tokens(DARK) + "color-scheme:dark}"
    r"""
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--bg);color:var(--fg);font:400 clamp(1rem,.96rem + .2vw,1.0625rem)/1.65 Onest,system-ui,sans-serif}
h1,h2,h3{font-family:Lora,Georgia,serif;line-height:1.2;font-weight:600;margin:0 0 .5em;text-wrap:balance}
h1{font-size:clamp(2rem,1.4rem + 2.6vw,3.2rem)}h2{font-size:clamp(1.5rem,1.2rem + 1.4vw,2.1rem)}h3{font-size:1.2rem}
p{margin:0 0 1em}a{color:var(--accent);text-underline-offset:3px}img{max-width:100%}
.mt{margin-top:1.6em}.muted{color:var(--muted)}code{background:var(--alt);padding:0 .3em;border-radius:4px}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left));padding-right:max(20px,env(safe-area-inset-right))}
.narrow{max-width:760px}
section{padding:clamp(40px,6vw,76px) 0}.alt{background:var(--alt)}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--surface);padding:8px 14px;border-radius:8px;z-index:100}.skip:focus{left:8px}
.demo{background:#FFE98A;color:#2B2B2B;text-align:center;padding:6px 12px;font-size:.9rem}
mark.ph{background:#FFE98A;color:#2B2B2B;padding:0 .25em;border-radius:4px}
header.top{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;gap:14px;min-height:64px;flex-wrap:wrap;padding-top:6px;padding-bottom:6px}
.logo{font:600 1.35rem Lora,Georgia,serif;color:var(--fg);text-decoration:none;margin-right:auto}
.logo small{font:400 .8rem Onest,sans-serif;color:var(--muted);margin-left:8px}
nav.nav{display:flex;gap:4px 18px;flex-wrap:wrap}nav.nav a{color:var(--fg);text-decoration:none;padding:6px 2px;border-bottom:2px solid transparent}
nav.nav a:hover,nav.nav a[aria-current]{border-color:var(--accent)}
.tools{display:flex;gap:8px;align-items:center}
.pill,.burger{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;padding:6px 14px;font:inherit;font-size:.9rem;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;min-height:36px}
.burger{display:none}
#theme svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2}
@media (max-width:760px){
.js .burger{display:inline-flex}.js nav.nav{display:none;width:100%;flex-direction:column;order:5;padding-bottom:10px}.js nav.nav.open{display:flex}
.logo small{display:none}}
.btn{display:inline-block;background:var(--accent);color:var(--onacc);padding:12px 22px;border-radius:999px;text-decoration:none;font-weight:600;border:2px solid var(--accent);cursor:pointer;font-family:inherit;font-size:1rem}
.btn:hover{filter:brightness(1.07)}.btn.ghost{background:transparent;color:var(--accent)}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin:1.4em 0}
.eyebrow{color:var(--accent);font-weight:600;letter-spacing:.08em;text-transform:uppercase;font-size:.85rem}
.lead{font-size:clamp(1.08rem,1rem + .4vw,1.25rem);color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}
.chips li{border:1px solid var(--line);background:var(--surface);padding:4px 14px;border-radius:999px;font-size:.9rem}
.hero{display:grid;gap:36px;align-items:center}
@media (min-width:860px){.hero{grid-template-columns:1.25fr .75fr}}
.hero-sec{padding-top:clamp(28px,5vw,64px)}
.photo{margin:0;border-radius:999px 999px var(--r) var(--r);overflow:hidden;background:var(--alt);border:1px solid var(--line);aspect-ratio:4/5;width:100%;max-width:440px;justify-self:center}
.photo img{width:100%;height:100%;object-fit:cover;display:block}
.photo.empty{display:grid;place-items:center;text-align:center;padding:24px}
.about-teaser{display:grid;gap:32px;align-items:center}
@media (min-width:760px){.about-teaser{grid-template-columns:.7fr 1.3fr}}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:22px}
.card h3{margin-bottom:.4em}.card p:last-child{margin-bottom:0}
.link-card{text-decoration:none;color:var(--fg);transition:transform .15s,border-color .15s}.link-card:hover{transform:translateY(-2px);border-color:var(--accent)}
.price{font:600 1.7rem Lora,Georgia,serif;margin:0}
.ticks{list-style:none;padding:0;margin:0 0 1.2em}.ticks li{padding-left:28px;position:relative;margin-bottom:.6em}
.ticks li::before{content:"";position:absolute;left:4px;top:.55em;width:10px;height:10px;border-radius:50%;background:var(--accent)}
.ticks.plain li{padding-left:0}.ticks.plain li::before{display:none}
.steps{counter-reset:s;list-style:none;padding:0;margin:0 0 1em;display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr))}
.steps li{counter-increment:s;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:22px}
.steps li::before{content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--accent);color:var(--onacc);font-weight:600;margin-bottom:10px}
.alt .steps li{background:var(--surface)}
.timeline{list-style:none;padding:0;margin:0 0 1em}.timeline li{display:grid;gap:2px 18px;padding:14px 0;border-top:1px solid var(--line)}
.timeline .when{color:var(--accent);font-weight:600}
@media (min-width:640px){.timeline li{grid-template-columns:120px 1fr}}
.band{background:var(--accent);color:var(--onacc);text-align:center}
.band .btn{background:var(--onacc);color:var(--accent);border-color:var(--onacc)}
.page-head{padding-bottom:0}
.notice{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);padding:10px 16px;border-radius:8px}
details{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);margin-bottom:12px;padding:0 20px}
summary{cursor:pointer;font-weight:600;padding:16px 0;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}summary::after{content:"+";color:var(--accent);font-size:1.4rem;line-height:1}details[open] summary::after{content:"–"}
.ans{padding-bottom:6px}
footer.foot{border-top:1px solid var(--line);padding:32px 0 40px;color:var(--muted);font-size:.92rem}
.foot .wrap{display:grid;gap:12px}.foot nav{display:flex;gap:6px 18px;flex-wrap:wrap}
.foot a,.foot button{color:var(--muted)}.foot button{background:none;border:0;font:inherit;text-decoration:underline;cursor:pointer;padding:0;text-underline-offset:3px}
#consent{position:fixed;left:max(12px,env(safe-area-inset-left));right:max(12px,env(safe-area-inset-right));bottom:12px;z-index:50;max-width:620px;margin:0 auto;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;box-shadow:0 8px 30px rgba(0,0,0,.18)}
#consent[hidden]{display:none}#consent p{margin:0 0 12px;font-size:.93rem}#consent .row{display:flex;gap:10px;flex-wrap:wrap}
#consent .btn{padding:8px 18px;font-size:.95rem}
.nf{text-align:center;padding:12vh 0}
"""
)

EARLY = """<script>(function(){try{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}document.documentElement.classList.add('js')})()</script>"""

JS = r"""
(function(){
var GA='__GA__',L=document.documentElement.lang==='en'?'en':'ua';
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}window.gtag=gtag;
gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});
var KEY='cookie-consent',box=document.getElementById('consent');
function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
function set(v){try{localStorage.setItem(KEY,v)}catch(e){}}
var loaded=false;
function loadGA(){if(loaded)return;loaded=true;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA;document.head.appendChild(s);
gtag('js',new Date());gtag('config',GA,{allow_google_signals:false,allow_ad_personalization_signals:false})}
function clearCookies(){var names=document.cookie.split(';').map(function(c){return c.split('=')[0].trim()}).filter(function(n){return n==='_ga'||n.indexOf('_ga_')===0});
var parts=location.hostname.split('.'),doms=[''];for(var i=0;i<parts.length-1;i++)doms.push(';domain=.'+parts.slice(i).join('.'));
names.forEach(function(n){doms.forEach(function(d){document.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'+d})})}
function apply(v){if(v==='granted'){gtag('consent','update',{analytics_storage:'granted'});loadGA()}else{gtag('consent','update',{analytics_storage:'denied'});clearCookies()}}
function choose(v){set(v);box.hidden=true;apply(v)}
var saved=get();if(saved)apply(saved);else box.hidden=false;
document.getElementById('c-yes').onclick=function(){choose('granted')};
document.getElementById('c-no').onclick=function(){choose('denied')};
document.querySelectorAll('[data-cookie-settings]').forEach(function(b){b.onclick=function(){box.hidden=false;document.getElementById('c-yes').focus()}});
function track(n,p){if(get()==='granted'&&loaded)gtag('event',n,p||{})}
document.addEventListener('click',function(e){var a=e.target.closest('[data-track]');if(a)track(a.dataset.track,{label:a.dataset.label})});
document.querySelectorAll('details').forEach(function(d){d.addEventListener('toggle',function(){if(d.open)track('faq_open',{label:d.querySelector('summary').textContent})})});
if(location.hash){var t=document.querySelector('details'+location.hash);if(t)t.open=true}
var seen={};window.addEventListener('scroll',function(){var h=document.documentElement,p=(h.scrollTop+innerHeight)/h.scrollHeight*100;[50,90].forEach(function(x){if(p>=x&&!seen[x]){seen[x]=1;track('scroll_depth',{label:x+'%'})}})},{passive:true});
var th=document.getElementById('theme');th.onclick=function(){var r=document.documentElement,cur=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'),n=cur==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}track('theme_change',{label:n})};
var bg=document.getElementById('burger'),nv=document.getElementById('nav');bg.onclick=function(){var o=nv.classList.toggle('open');bg.setAttribute('aria-expanded',o)};
})();
"""

UI = {
    "menu": ("Меню", "Menu"), "skip": ("До змісту", "Skip to content"), "theme": ("Змінити тему", "Toggle theme"),
    "demo": ("Демо-версія: сайт ще не опублікований, жовтим виділено дані, яких бракує.", "Demo version: the site is not published yet, missing data is highlighted in yellow."),
    "role": ("Психологиня", "Psychologist"),
    "privacy": ("Конфіденційність", "Privacy"), "cookies": ("Налаштування cookie", "Cookie settings"),
    "urgent": ("Це не екстрена служба. У разі небезпеки телефонуйте 112 або Lifeline Ukraine 7333.", "This is not an emergency service. In danger, call 112 or Lifeline Ukraine 7333."),
    "cc": ("Ми використовуємо cookie Google Analytics лише за вашої згоди, щоб бачити, які сторінки читають.", "We use Google Analytics cookies only with your consent, to see which pages are read."),
    "yes": ("Дозволити", "Allow"), "no": ("Відхилити", "Decline"), "lang": ("EN", "UA"),
}

SUN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5 19 19M5 19l1.5-1.5M17.5 6.5 19 5"/></svg>'


class Ctx:
    def __init__(self, lang):
        self.l = lang
        self.contacts = CONTACTS
        self.hours = HOURS[lang]
        self.today = TODAY

    def t(self, ua, en):
        return ua if self.l == "ua" else en

    def u(self, key):
        return url_path(key, self.l)

    def ph(self, text):
        return f'<mark class="ph">{html.escape(text) if "<" not in text else text}</mark>'

    def photo(self, role, hero=False):
        alt = self.t("Аліна, психологиня, усміхається, сидячи в кріслі", "Alina, psychologist, smiling while seated in an armchair")
        if role == "portrait":
            return (f'<figure class="photo"><img src="/img/alina-portrait-1024.webp" srcset="/img/alina-portrait-640.webp 640w, /img/alina-portrait-1024.webp 1024w" '
                    f'sizes="(max-width:760px) 90vw, 440px" width="1024" height="1280" alt="{alt}" fetchpriority="high"></figure>')
        alt2 = self.t("Аліна за ноутбуком у кріслі: онлайн-консультація", "Alina with a laptop in an armchair: an online session")
        return (f'<figure class="photo"><img src="/img/alina-work-853.webp" srcset="/img/alina-work-640.webp 640w, /img/alina-work-853.webp 853w" '
                f'sizes="(max-width:760px) 90vw, 360px" width="853" height="1066" alt="{alt2}" loading="lazy"></figure>')


def url_path(key, lang):
    return ("/" if lang == "ua" else "/en/") + SLUG[key]


def esc(s):
    return html.escape(s, quote=True)


def jsonld(items):
    return "".join(f'<script type="application/ld+json">{json.dumps(i, ensure_ascii=False).replace("</", "<\\/")}</script>' for i in items)


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def head(c, key, page, path_ua, path_en, noindex):
    lang = c.l
    full = SITE + (path_ua if lang == "ua" else path_en)
    locale, alt_locale = ("uk_UA", "en_US") if lang == "ua" else ("en_US", "uk_UA")
    title = page["title"]
    robots = "noindex,nofollow" if noindex else "index,follow"
    og_alt = c.t("Аліна Буба, психологиня онлайн", "Alina Buba, online psychologist")
    preload = "cyrillic" if lang == "ua" else "latin"
    fonts = "".join(f'<link rel="preload" href="/fonts/{f}-{preload}.woff2" as="font" type="font/woff2" crossorigin>' for f in ("lora", "onest"))
    return f"""<!doctype html>
<html lang="{'uk' if lang == 'ua' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(page['desc'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{full}">
<link rel="alternate" hreflang="uk" href="{SITE + path_ua}">
<link rel="alternate" hreflang="en" href="{SITE + path_en}">
<link rel="alternate" hreflang="x-default" href="{SITE + path_ua}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{esc(NAME[lang])}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(page['desc'])}">
<meta property="og:url" content="{full}"><meta property="og:locale" content="{locale}"><meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:image" content="{SITE}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(page['desc'])}"><meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="{LIGHT['bg']}"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="{DARK['bg']}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
{fonts}
{EARLY}
<style>{FONTS_CSS}{CSS}</style>
"""


def shell(c, key, page, noindex, extra_ld, nf=False):
    lang = c.l
    path_ua, path_en = url_path(key, "ua"), url_path(key, "en")
    other = "en" if lang == "ua" else "ua"
    nav = "".join(
        f'<a href="{url_path(k, lang)}"{" aria-current=page" if k == key else ""}>{LABEL[k][0 if lang == "ua" else 1]}</a>' for k in NAV
    )
    i = 0 if lang == "ua" else 1
    demo = f'<div class="demo">{UI["demo"][i]}</div>' if DEMO else ""
    switch = "" if nf else f'<a class="pill" href="{url_path(key, other)}" hreflang="{"en" if other == "en" else "uk"}" lang="{"en" if other == "en" else "uk"}" data-track="lang_switch" data-label="{other}">{UI["lang"][i]}</a>'
    foot_nav = f'<a href="{url_path("privacy", lang)}">{UI["privacy"][i]}</a><button type="button" data-cookie-settings>{UI["cookies"][i]}</button>'
    out = head(c, key, page, path_ua, path_en, noindex) + jsonld(extra_ld) + "\n</head>\n<body>\n"
    out += f'<a class="skip" href="#main">{UI["skip"][i]}</a>{demo}\n'
    out += f"""<header class="top"><div class="wrap bar">
<a class="logo" href="{url_path('home', lang)}">{NAME[lang]}<small>{UI['role'][i]}</small></a>
<div class="tools">{switch}<button class="pill" id="theme" type="button" aria-label="{UI['theme'][i]}">{SUN}</button>
<button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="nav">{UI['menu'][i]}</button></div>
<nav class="nav" id="nav" aria-label="{'Основна навігація' if lang == 'ua' else 'Main navigation'}">{nav}</nav>
</div></header>
<main id="main">{page['body']}</main>
<footer class="foot"><div class="wrap"><nav>{foot_nav}</nav><p>© {datetime.date.today().year} {NAME[lang]}. {UI['urgent'][i]}</p></div></footer>
<div id="consent" role="dialog" aria-label="Cookie" hidden><p>{UI['cc'][i]} <a href="{url_path('privacy', lang)}">{UI['privacy'][i]}</a></p>
<div class="row"><button class="btn" id="c-yes" type="button">{UI['yes'][i]}</button><button class="btn ghost" id="c-no" type="button">{UI['no'][i]}</button></div></div>
<script>{JS.replace('__GA__', GA_ID)}</script>
</body></html>
"""
    return out


def schema(c, key, page):
    lang = c.l
    full = SITE + url_path(key, lang)
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": NAME[lang], "url": SITE + url_path("home", lang),
           "inLanguage": "uk" if lang == "ua" else "en"}]
    if key == "home":
        same = [CONTACTS[k] for k in ("instagram", "facebook", "linkedin", "telegram", "viber") if k in CONTACTS]
        person = {"@type": "Person", "name": NAME[lang], "jobTitle": c.t("Психологиня", "Psychologist"),
                  "knowsAbout": ["Cognitive behavioural therapy", "Neuropsychology", "Psychodiagnostics", "Anxiety", "Burnout", "Self-esteem", "ADHD"],
                  "knowsLanguage": ["uk", "en", "fr"],
                  "alumniOf": {"@type": "CollegeOrUniversity", "name": "Taras Shevchenko National University of Kyiv"}}
        svc = {"@type": "ProfessionalService", "name": c.t("Аліна Буба, психологиня онлайн", "Alina Buba, online psychologist"), "url": full,
               "image": SITE + "/og-image.png", "areaServed": "UA", "availableLanguage": ["uk", "en"],
               "openingHours": "Mo-Sa 09:00-21:00", "priceRange": "800 UAH", "founder": person}
        if same:
            person["sameAs"] = same
            svc["sameAs"] = same
        for k, f in (("email", "email"), ("phone", "telephone")):
            if k in CONTACTS:
                svc[f] = CONTACTS[k]
        ld += [dict(svc, **{"@context": "https://schema.org"}), dict(person, **{"@context": "https://schema.org"})]
    else:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": LABEL["home"][0 if lang == "ua" else 1], "item": SITE + url_path("home", lang)},
            {"@type": "ListItem", "position": 2, "name": LABEL[key][0 if lang == "ua" else 1], "item": full}]})
    if key == "faq":
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for _, q, a in page["faq"]]})
    return ld


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def main():
    global FONTS_CSS
    FONTS_CSS = (ROOT / "tools" / "fonts.css").read_text().replace("\n", "")
    count = 0
    for lang in LANGS:
        c = Ctx(lang)
        for key in ORDER:
            page = PAGES[key](c)
            write(url_path(key, lang).lstrip("/") + "index.html", shell(c, key, page, DEMO, schema(c, key, page)))
            count += 1
    # 404
    c = Ctx("ua")
    nf = dict(title="Сторінку не знайдено", desc="Такої сторінки немає.",
              body='<section class="nf"><div class="wrap"><h1>404</h1><p>Такої сторінки немає.</p><p><a class="btn" href="/">На головну</a></p></div></section>')
    write("404.html", shell(c, "home", nf, True, [], nf=True))
    # sitemap, robots, manifest
    urls = ""
    for key in ORDER:
        for lang in LANGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE + url_path(key, l)}"/>' for l, h in (("ua", "uk"), ("en", "en")))
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE + url_path(key, "ua")}"/>'
            urls += f"<url><loc>{SITE + url_path(key, lang)}</loc><lastmod>{TODAY}</lastmod>{alts}</url>\n"
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": "Аліна Буба, психологиня", "short_name": "Аліна Буба", "lang": "uk", "start_url": "/", "display": "standalone",
        "background_color": LIGHT["bg"], "theme_color": LIGHT["accent"],
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
        ensure_ascii=False, indent=2) + "\n")
    print(f"built {count} pages + 404.html (DEMO={DEMO})")


if __name__ == "__main__":
    main()
