#!/usr/bin/env python3
"""Build taumorrow.com from src/index.src.html.

Outputs one static page per language (crawlable without JavaScript), the shared
assets (favicons, Open Graph image, manifest), robots.txt and a sitemap with
hreflang alternates. Run from the repository root:  python3 tools/build.py
"""
import html, json, os, random, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "index.src.html")
SITE = "https://taumorrow.com"

LANGS = [  # folder, html lang, hreflang, og:locale, label
    ("", "en", "en", "en_US", "EN"),
    ("de", "de", "de", "de_DE", "DE"),
    ("es", "es", "es", "es_ES", "ES"),
    ("zh", "zh-Hans", "zh-Hans", "zh_CN", "中文"),
    ("ru", "ru", "ru", "ru_RU", "RU"),
    ("fr", "fr", "fr", "fr_FR", "FR"),
    # ("th", "th", "th", "th_TH", "ไทย"),   # Thai switched off for now; translations stay in src, uncomment to re-enable
]
META = {
    "en": ("Taumorrow Chess, games whose every round you can recompute, a playable Nomic",
           "Chess engine on the Tau language that cannot bluff (9 : 1 vs Claude Sonnet 5.5), multiplayer games whose every round anyone can recompute, a playable Nomic. Papers with DOIs, in the open since 2024."),
    "de": ("Taumorrow Chess, Spiele, deren jede Runde man nachrechnen kann, ein spielbares Nomic",
           "Schach-Engine auf der Tau-Sprache, die nicht bluffen kann (9 : 1 gegen Claude Sonnet 5.5), Mehrspieler-Spiele, deren Runden jeder nachrechnen kann, ein spielbares Nomic. Schriften mit DOI, offen seit 2024."),
    "es": ("Taumorrow Chess, juegos en los que cada ronda se puede recalcular, Nomic jugable",
           "Motor de ajedrez sobre el lenguaje Tau que no puede farolear (9 : 1 contra Claude Sonnet 5.5), juegos multijugador en los que cualquiera puede recalcular cada ronda y un Nomic jugable. Artículos con DOI, en abierto desde 2024."),
    "zh": ("Taumorrow Chess、每一轮都可复算的游戏、可玩的 Nomic",
           "基于 Tau 语言的国际象棋引擎，不会虚张声势（对 Claude Sonnet 5.5 取得 9 : 1），每一轮都可由任何人复算的多人游戏，以及可玩的 Nomic。论文均有 DOI，自 2024 年起公开。"),
    "ru": ("Taumorrow Chess, игры, каждый раунд которых можно пересчитать, играбельный Nomic",
           "Шахматный движок на языке Tau, который не может блефовать (9 : 1 против Claude Sonnet 5.5), многопользовательские игры, каждый раунд которых может пересчитать любой, и играбельный Nomic. Статьи с DOI, открыто с 2024 года."),
    "fr": ("Taumorrow Chess, jeux dont chaque tour peut être recalculé, Nomic jouable",
           "Moteur d’échecs sur le langage Tau qui ne peut pas bluffer (9 : 1 contre Claude Sonnet 5.5), des jeux multijoueurs dont chaque tour peut être recalculé par n’importe qui, un Nomic jouable. Articles avec DOI, en accès ouvert depuis 2024."),
    "th": ("Taumorrow Chess เกมที่ทุกรอบคำนวณซ้ำได้ และ Nomic ที่เล่นได้",
           "เอนจินหมากรุกบนภาษา Tau ที่หลอกไม่ได้ (ชนะ Claude Sonnet 5.5 9 : 1) เกมหลายผู้เล่นที่ใครก็คำนวณซ้ำได้ทุกรอบ และ Nomic ที่เล่นได้ บทความมี DOI เปิดเผยตั้งแต่ปี 2024"),
}
PAPERS = [
    ("2026-08-21", "10.5281/zenodo.22038825", "A Playable Nomic with a Provably Entrenched Core: Two-level self-amendment on a decidable substrate"),
    ("2026-10-07", "10.5281/zenodo.23208762", "The Round as a Formula: Fair, transparent, real-time multiplayer games with the Tau language"),
    ("2026-10-07", "10.5281/zenodo.23165449", "The Admitted Shortcut: Tree search over sub-specifications of a decidable logic, with Taumorrow Chess as the worked example"),
    ("2026-10-07", "10.5281/zenodo.23208550", "Learning under a Decided Gate: Changing a table that an admitted shortcut reads"),
]
STR = r'"((?:[^"\\]|\\.)*)"'


def parse_i18n(src):
    """Return {lang: {key: value}} from the JavaScript dictionary in the source."""
    a = src.index("const I18N = {")
    b = src.index("\n}};", a)
    blk = src[a:b]
    out = {}
    for m in re.finditer(r"\n(\w+):\{", blk):
        lang = m.group(1)
        start = m.end()
        nxt = re.search(r"\n\w+:\{", blk[start:])
        body = blk[start:start + nxt.start()] if nxt else blk[start:]
        d = {}
        for km in re.finditer(STR + r"\s*:\s*" + STR, body):
            d[json.loads('"' + km.group(1) + '"')] = json.loads('"' + km.group(2) + '"')
        out[lang] = d
    return out


def strip_i18n_script(src):
    a = src.index("const I18N = {")
    s = src.rindex("<script>", 0, a)
    e = src.index("</script>", a) + len("</script>")
    return src[:s] + src[e:]


def translate(doc, d, lang):
    """Replace the text of every data-i18n element and drop the attributes."""
    n = [0]

    def rep_text(m):
        tag, pre, key, post, inner = m.groups()
        n[0] += 1
        if lang != "en" and key in d:
            inner = html.escape(d[key], quote=False)
        return "<%s%s%s>%s</%s>" % (tag, pre, post, inner, tag)

    def rep_html(m):
        tag, pre, key, post, inner = m.groups()
        n[0] += 1
        if lang != "en" and key in d:
            inner = d[key]
        return "<%s%s%s>%s</%s>" % (tag, pre, post, inner, tag)

    doc = re.sub(r'<(\w+)([^>]*?)\sdata-i18n-html="([^"]+)"([^>]*)>(.*?)</\1>', rep_html, doc, flags=re.S)
    doc = re.sub(r'<(\w+)([^>]*?)\sdata-i18n="([^"]+)"([^>]*)>(.*?)</\1>', rep_text, doc, flags=re.S)
    assert "data-i18n" not in doc, "unreplaced data-i18n left"
    return doc, n[0]


def lang_links(active):
    parts = []
    for folder, hl, hreflang, _, label in LANGS:
        href = "/" if not folder else "/%s/" % folder
        cur = ' aria-current="page"' if hl == active else ""
        parts.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (href, hreflang, hl, cur, label))
    return '<div class="lang" role="group" aria-label="Language">' + "".join(parts) + "</div>"


def head_block(folder, hl, hreflang, locale, title, desc):
    url = SITE + ("/" if not folder else "/%s/" % folder)
    alts = "".join('\n<link rel="alternate" hreflang="%s" href="%s">' % (h, SITE + ("/" if not f else "/%s/" % f)) for f, _, h, _, _ in LANGS)
    alts += '\n<link rel="alternate" hreflang="x-default" href="%s/">' % SITE
    graph = [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Taumorrow", "url": SITE + "/",
         "logo": SITE + "/icon-512.png", "email": "hallo@taumorrow.com",
         "sameAs": ["https://x.com/tau_l0g1x", "https://github.com/taumorrow"]},
        {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Taumorrow",
         "publisher": {"@id": SITE + "/#org"}, "inLanguage": [h for _, _, h, _, _ in LANGS]},
        {"@type": "WebPage", "url": url, "name": title, "description": desc, "inLanguage": hreflang,
         "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#org"}},
    ]
    for date, doi, name in PAPERS:
        graph.append({"@type": "ScholarlyArticle", "name": name, "identifier": "https://doi.org/" + doi,
                      "url": "https://doi.org/" + doi, "datePublished": date,
                      "publisher": {"@type": "Organization", "name": "Zenodo"}})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    t = html.escape(title, quote=True)
    dsc = html.escape(desc, quote=True)
    return ('<title>%s</title>\n<meta name="description" content="%s">\n'
            '<link rel="canonical" href="%s">%s\n'
            '<meta name="color-scheme" content="light dark">\n'
            '<meta name="theme-color" media="(prefers-color-scheme: light)" content="#f1f3f6">\n'
            '<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0d1117">\n'
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Taumorrow">\n'
            '<meta property="og:url" content="%s">\n<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n<meta property="og:image" content="%s/og.png">\n'
            '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta property="og:image:alt" content="Taumorrow — Decided, not guessed.">\n<meta property="og:locale" content="%s">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:site" content="@tau_l0g1x">\n'
            '<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
            '<meta name="twitter:image" content="%s/og.png">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/manifest.webmanifest">\n'
            '<script type="application/ld+json">%s</script>'
            % (t, dsc, url, alts, url, t, dsc, SITE, locale, t, dsc, SITE, ld))


ROOT_REDIRECT = ('<script>try{var L=["de","es","zh","ru","fr"],l=localStorage.getItem("taumorrow.lang");'
                 'if(!l)l=((navigator.language||"en").toLowerCase().slice(0,2));'
                 'if(L.indexOf(l)>=0&&location.pathname==="/")location.replace("/"+l+"/"+location.hash);}catch(_){}</script>')
LANG_STORE = ('<script>document.querySelectorAll(".lang a").forEach(function(a){a.addEventListener("click",function(){'
              'try{localStorage.setItem("taumorrow.lang",a.getAttribute("lang").slice(0,2));}catch(_){}});});</script>')


def build_pages(src):
    i18n = parse_i18n(src)
    base = strip_i18n_script(src)
    base = base.replace('.lang button{', '.lang button,.lang a{text-decoration:none;')
    base = base.replace('.lang button[aria-pressed="true"]{', '.lang button[aria-pressed="true"],.lang a[aria-current="page"]{')
    base = base.replace('.lang button{padding:7px 7px', '.lang button,.lang a{padding:7px 7px')
    base = re.sub(r'<div class="lang" role="group" aria-label="Language">.*?</div>', "@@LANG@@", base, count=1, flags=re.S)
    head_old = re.search(r'<title>Taumorrow</title>\n<meta name="description" content="[^"]*">', base).group(0)
    base = base.replace(head_old, "@@HEAD@@")
    base = base.replace("</body>", LANG_STORE + "\n</body>")
    counts = {}
    for folder, hl, hreflang, locale, label in LANGS:
        short = hl[:2]
        title, desc = META[short]
        doc, n = translate(base, i18n.get(short, {}), short)
        doc = doc.replace('<html lang="en">', '<html lang="%s">' % hl, 1)
        doc = doc.replace("@@LANG@@", lang_links(hl))
        doc = doc.replace("@@HEAD@@", head_block(folder, hl, hreflang, locale, title, desc))
        if not folder:
            doc = doc.replace("</script>\n<link rel=\"stylesheet\" href=\"/fonts/fonts.css\">", "</script>\n" + ROOT_REDIRECT + "\n<link rel=\"stylesheet\" href=\"/fonts/fonts.css\">", 1)
            assert ROOT_REDIRECT in doc
        out_dir = os.path.join(ROOT, folder) if folder else ROOT
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w") as f:
            f.write(doc)
        counts[hl] = n
    return counts


def build_assets():
    from PIL import Image, ImageDraw, ImageFont
    bold = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
    # Open Graph image
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#0d1117")
    dr = ImageDraw.Draw(im)
    rnd = random.Random(20261020)
    pts = [(rnd.randint(40, W - 40), rnd.randint(40, H - 40)) for _ in range(70)]
    for i, p in enumerate(pts):
        near = sorted(pts, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)[1:3]
        for q in near:
            dr.line([p, q], fill="#1b2434", width=2)
    for p in pts:
        dr.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill="#273447")
    for p in rnd.sample(pts, 9):
        dr.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill="#6f8dff")
    dr.text((168, 74), "TAUMORROW", font=ImageFont.truetype(bold, 30), fill="#6f8dff")
    dr.text((80, 150), "Decided,", font=ImageFont.truetype(bold, 112), fill="#e9edf3")
    dr.text((80, 270), "not guessed.", font=ImageFont.truetype(bold, 112), fill="#e9edf3")
    dr.text((80, 420), "Taumorrow Chess · games you can recompute · a playable Nomic", font=ImageFont.truetype(reg, 34), fill="#c3cad6")
    dr.text((80, 468), "built on the Tau language · 9 : 1 vs Claude Sonnet 5.5 · every move a record", font=ImageFont.truetype(reg, 28), fill="#8a93a6")
    dr.text((80, 556), "taumorrow.com", font=ImageFont.truetype(bold, 30), fill="#6f8dff")
    og = im
    # Icons: the Taumorrow mark (the gate) — same geometry as brand/taumorrow-mark.svg
    import math
    def arc(cx, cy, r, a0, a1, n=32):
        return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    POLY = [(13, 15), (51, 15), (51, 24), (36.5, 24), (36.5, 36)] + arc(41, 36, 4.5, 180, 90)[1:] + [(47, 40.5), (47, 49.5), (41, 49.5)] + arc(41, 36, 13.5, 90, 180)[1:] + [(27.5, 24), (13, 24)]
    def icon(size, bg=(36, 72, 200), fg=(255, 255, 255), ss=8):
        s = size * ss
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        k = s / 64
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(14 * k), fill=bg)
        d.polygon([(x * k, y * k) for x, y in POLY], fill=fg)
        return im.resize((size, size), Image.LANCZOS)
    icon(32).save(os.path.join(ROOT, "favicon-32.png"), optimize=True)
    icon(180).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"), optimize=True)
    icon(192).save(os.path.join(ROOT, "icon-192.png"), optimize=True)
    icon(512).save(os.path.join(ROOT, "icon-512.png"), optimize=True)
    with open(os.path.join(ROOT, "brand", "taumorrow-mark.svg")) as f, open(os.path.join(ROOT, "favicon.svg"), "w") as g:
        g.write(f.read())
    m = icon(72, bg=(111, 141, 255), fg=(13, 17, 23))
    og.paste(m, (80, 56), m)
    og.save(os.path.join(ROOT, "og.png"), optimize=True)
    with open(os.path.join(ROOT, "manifest.webmanifest"), "w") as f:
        json.dump({"name": "Taumorrow", "short_name": "Taumorrow", "start_url": "/", "display": "browser",
                   "background_color": "#0d1117", "theme_color": "#2448c8",
                   "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                             {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, f, indent=1)
        f.write("\n")


def build_sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for folder, hl, hreflang, _, _ in LANGS:
        loc = SITE + ("/" if not folder else "/%s/" % folder)
        alts = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (h, SITE + ("/" if not f else "/%s/" % f)) for f, _, h, _, _ in LANGS)
        alts += '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s/"/>' % SITE
        urls.append("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>%s\n  </url>" % (loc, today, alts))
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)


if __name__ == "__main__":
    src = open(SRC).read()
    counts = build_pages(src)
    build_assets()
    build_sitemap()
    print("pages:", counts)
