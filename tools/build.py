#!/usr/bin/env python3
"""Builds the Nexus site pages from tools/pages/*.html.

Each page body lives in tools/pages/. This script wraps it with the shared
<head>, header, mobile menu, call-to-action band and footer, then writes the
finished HTML to the site root (index.html, about/index.html, ...).

Run from the repo root:  python3 tools/build.py
"""
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ver(rel):
    """Short content hash so browsers fetch a fresh copy whenever the file changes."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


CSS_V = ver("assets/css/styles.css")
JS_V = ver("assets/js/main.js")
V2_V = ver("assets/css/v2.css")
PAGES_DIR = ROOT / "tools" / "pages"
PARTIALS_DIR = ROOT / "tools" / "partials"
POSTS_DIR = ROOT / "tools" / "posts"
SITE = "https://nexusrg.co.uk"

NAV = [
    ("about", "/about/", "About"),
    ("sectors", "/sectors/", "Sectors"),
    ("candidates", "/candidates/", 'Candidates<span class="nav__live" title="Recruiting now" aria-label="(recruiting now)"></span>'),
    ("blog", "/blog/", "Blog"),
    ("contact", "/contact/", "Contact"),
]

# key, output file, url path, <title>, meta description, show CTA band, extra body class
PAGES = [
    ("home", "index.html", "/",
     "Nexus Resourcing Group | Connecting talent. Powering projects.",
     "Skilled, vetted people for commercial, domestic, marine and defence projects across the UK and worldwide. Talk directly to Nick Souness.",
     False, "page-home"),
    ("about", "about/index.html", "/about/",
     "About | Nexus Resourcing Group",
     "Built on more than twenty years of marine and defence experience. A proactive take on supplying skilled people to complex projects.",
     True, ""),
    ("sectors", "sectors/index.html", "/sectors/",
     "Sectors | Nexus Resourcing Group",
     "Skilled people for marine, commercial, domestic and defence projects. See the roles we supply and the projects we support.",
     True, ""),
    ("candidates", "candidates/index.html", "/candidates/",
     "Candidates | Nexus Resourcing Group",
     "Tradespeople, engineers and supervisors: register with Nexus and get matched to marine, commercial, domestic and defence work.",
     False, ""),
    ("contact", "contact/index.html", "/contact/",
     "Contact | Nexus Resourcing Group",
     "Book a call with Nick Souness, send an enquiry, or call 07963 398473.",
     False, ""),
    ("privacy", "privacy/index.html", "/privacy/",
     "Privacy & Cookie Policy | Nexus Resourcing Group",
     "How Nexus Resourcing Group collects, uses and protects your personal information.",
     False, "page-plain"),
    ("404", "404.html", "/404.html",
     "Page not found | Nexus Resourcing Group",
     "The page you were looking for could not be found.",
     False, "page-plain"),
]

FONTS = "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500&display=swap"


SCHEMA = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "EmploymentAgency",
    "name": "Nexus Resourcing Group",
    "legalName": "Nexus Resourcing Group Limited",
    "url": "https://nexusrg.co.uk/",
    "logo": "https://nexusrg.co.uk/assets/img/og-image.jpg",
    "image": "https://nexusrg.co.uk/assets/img/og-image.jpg",
    "slogan": "Connecting talent. Powering projects.",
    "description": "Skilled, vetted people for commercial, domestic, marine and defence projects across the UK and worldwide.",
    "telephone": "+447963398473",
    "email": "nick@nexusrg.co.uk",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "51 Burnham Park Road",
      "addressLocality": "Plymouth",
      "postalCode": "PL3 5QB",
      "addressCountry": "GB"
    },
    "areaServed": ["GB", "Worldwide"],
    "founder": { "@type": "Person", "name": "Nick Souness", "jobTitle": "Managing Director", "image": "https://nexusrg.co.uk/assets/img/nick-souness-600.webp?v=2" },
    "knowsAbout": ["Marine resourcing", "Commercial resourcing", "Domestic resourcing", "Defence resourcing"]
  }
  </script>
"""


def head(title, desc, path, key):
    # the homepage shares with the same short title and line as the original holding page
    og_title = "Nexus Resourcing Group" if key == "home" else title
    og_desc = ("Connecting talent. Powering projects. Skilled people for commercial, domestic, marine and defence projects."
               if key == "home" else desc)
    preload = '\n  <link rel="preload" as="image" href="/assets/img/hero-ship.webp" imagesrcset="/assets/img/hero-ship-1200.webp 1200w, /assets/img/hero-ship.webp 2480w" imagesizes="100vw">' if key == "home" else ""
    canonical = f"{SITE}{path}" if key != "404" else SITE + "/"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#0D0907">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Nexus Resourcing Group">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.jpg?v=2">
  <meta property="og:image:secure_url" content="{SITE}/assets/img/og-image.jpg?v=2">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Nexus Resourcing Group logo">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/img/og-image.jpg?v=2">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="icon" type="image/png" sizes="512x512" href="/assets/img/favicon.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">{preload}
  <link rel="stylesheet" href="/assets/css/styles.css?v={CSS_V}">
  <link rel="stylesheet" href="/assets/css/v2.css?v={V2_V}">
{SCHEMA if key == "home" else ""}
  <script>
    // Hide animated elements before first paint, only when motion is welcome.
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {{
      document.documentElement.classList.add('js-anim');
      // If the animation library is blocked (e.g. a locked-down work network), show everything straight away
      document.addEventListener('DOMContentLoaded', function () {{ if (!window.gsap) document.documentElement.classList.remove('js-anim'); }});
      setTimeout(function () {{ if (!window.gsap) document.documentElement.classList.remove('js-anim'); }}, 4000);
    }}
  </script>
</head>"""


def header(key):
    links = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if k == key else ""}>{label}</a>'
        for k, href, label in NAV)
    menu_links = "\n".join(
        f'        <li><a href="{href}"{" aria-current=\"page\"" if k == key else ""}>{label}</a></li>'
        for k, href, label in [("home", "/", "Home")] + NAV)
    return f"""  <a class="skip" href="#main">Skip to content</a>

  <header class="nav" id="nav">
    <a class="nav__brand" href="/" aria-label="Nexus Resourcing Group, home">
      <img src="/assets/img/logo-h-goldwhite.webp" alt="Nexus" width="600" height="167">
    </a>
    <nav class="nav__links" aria-label="Main">
{links}
    </nav>
    <a class="btn btn--gold btn--sm nav__cta" href="/contact/">Book a chat</a>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu">
      <span class="sr-only">Menu</span><span class="nav__bars" aria-hidden="true"></span>
    </button>
  </header>

  <div class="menu" id="menu" hidden>
    <img class="menu__mark" src="/assets/img/icon-gold.webp" alt="" aria-hidden="true">
    <nav class="menu__inner" aria-label="Menu">
      <ul class="menu__links">
{menu_links}
      </ul>
      <div class="menu__foot">
        <a class="btn btn--gold" href="/contact/">Book a chat with Nick</a>
        <p><a href="tel:+447963398473">07963 398473</a><br><a href="mailto:nick@nexusrg.co.uk">nick@nexusrg.co.uk</a><br><a href="https://wa.me/447963398473?text=Hi%20Nick%2C%20I%20found%20Nexus%20Resourcing%20Group%20online%20and%20would%20like%20to%20talk." target="_blank" rel="noopener">Message Nick on WhatsApp</a></p>
      </div>
    </nav>
  </div>
"""


CTA = """
  <section class="cta-band" aria-labelledby="cta-title">
    <img class="cta-band__mark" src="/assets/img/icon-gold.webp" alt="" aria-hidden="true">
    <div class="wrap cta-band__inner">
      <h2 class="display display--light" id="cta-title">There when you need us most.</h2>
      <p>Short notice or long programme, talk to Nick directly about the people your project needs.</p>
      <div class="cta-band__actions">
        <a class="btn btn--gold" href="/contact/">Book a chat with Nick</a>
        <a class="btn btn--ghost" href="tel:+447963398473">Call 07963 398473</a>
      </div>
    </div>
  </section>
"""

QUICKBAR = """
  <div class="quickbar" aria-label="Quick contact">
    <a class="quickbar__call" href="tel:+447963398473">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>
      Call Nick
    </a>
    <a class="quickbar__wa" href="https://wa.me/447963398473?text=Hi%20Nick%2C%20I%20found%20Nexus%20Resourcing%20Group%20online%20and%20would%20like%20to%20talk." target="_blank" rel="noopener" aria-label="Message Nick on WhatsApp">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 19.1z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5"/></svg>
    </a>
    <a class="btn btn--gold btn--sm" href="{href}">{label}</a>
  </div>
"""

FOOTER = """
  <footer class="foot">
    <div class="wrap foot__grid">
      <div class="foot__brand">
        <img class="foot__logo" src="/assets/img/logo-white.webp" alt="Nexus Resourcing Group" width="700" height="457" loading="lazy">
        <p class="foot__tag"><span>Connecting talent.</span> <span>Powering projects.</span></p>
      </div>
      <nav class="foot__col" aria-label="Footer">
        <h2>Explore</h2>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/sectors/">Sectors</a></li>
          <li><a href="/candidates/">Candidates</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </nav>
      <div class="foot__col">
        <h2>Sectors</h2>
        <ul>
          <li><a href="/sectors/#marine">Marine</a></li>
          <li><a href="/sectors/#commercial">Commercial</a></li>
          <li><a href="/sectors/#domestic">Domestic</a></li>
          <li><a href="/sectors/#defence">Defence</a></li>
        </ul>
      </div>
      <div class="foot__col">
        <h2>Talk to Nick</h2>
        <ul>
          <li><a href="tel:+447963398473">07963 398473</a></li>
          <li><a href="mailto:nick@nexusrg.co.uk">nick@nexusrg.co.uk</a></li>
          <li><a href="https://wa.me/447963398473?text=Hi%20Nick%2C%20I%20found%20Nexus%20Resourcing%20Group%20online%20and%20would%20like%20to%20talk." target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="/contact/">Book a call</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap foot__base">
      <p>&copy; <span data-year>2026</span> Nexus Resourcing Group Limited. Registered in England and Wales, company no. 17426336.</p>
      <p><a href="/privacy/">Privacy &amp; cookies</a></p>
    </div>
    <div class="wrap foot__credit">
      <a href="https://brandbildr.com" target="_blank" rel="noopener">
        <span class="foot__credit-text">Website and brand developed by</span>
        <img src="/assets/img/brandbildr-mark.png" alt="" width="57" height="48" loading="lazy" decoding="async">
        <span class="foot__credit-name">BrandBildr<sup>™</sup></span>
      </a>
    </div>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
  <script src="/assets/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""


def vac_updated():
    """Date the vacancies were last changed: last commit to the partial, else today."""
    import subprocess, datetime
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", "tools/partials/vacancies.html"],
                             capture_output=True, text=True, cwd=ROOT).stdout.strip()
        d = datetime.date.fromisoformat(out) if out else datetime.date.today()
    except Exception:
        d = datetime.date.today()
    return f"{d.day} {d.strftime('%B %Y')}"


# ---------------------------------------------------------------------------
# Blog: one Markdown file per post in tools/posts/<slug>.md
#
#   ---
#   title: Mobilising 100 trades to Grand Bahama
#   date: 2026-11-12
#   summary: One or two sentences for the blog list and search results.
#   image: /assets/img/case-cruise-liner.webp
#   category: Marine
#   ---
#   Body in plain Markdown: paragraphs, ## headings, - lists, **bold**,
#   [links](https://...), ![alt text](/assets/img/photo.webp) and > quotes.
#
# Files starting with "_" are drafts and are skipped.
# ---------------------------------------------------------------------------
import datetime, html as _html


def _inline(t):
    t = _html.escape(t, quote=False)
    t = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1" loading="lazy" decoding="async">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: f'<a href="{m.group(2)}"' + (' target="_blank" rel="noopener"' if m.group(2).startswith("http") else "") + f">{m.group(1)}</a>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def markdown(md):
    out, para, items, quote = [], [], [], []
    def flush():
        if para: out.append("<p>" + _inline(" ".join(para)) + "</p>"); para.clear()
        if items: out.append("<ul>" + "".join(f"<li>{_inline(i)}</li>" for i in items) + "</ul>"); items.clear()
        if quote: out.append("<blockquote><p>" + _inline(" ".join(quote)) + "</p></blockquote>"); quote.clear()
    for line in md.splitlines():
        l = line.strip()
        if not l: flush(); continue
        m = re.match(r"(#{2,4})\s+(.*)", l)
        if m:
            flush(); n = len(m.group(1)); out.append(f"<h{n}>{_inline(m.group(2))}</h{n}>"); continue
        if re.match(r"[-*]\s+", l):
            if para or quote: flush()
            items.append(re.sub(r"^[-*]\s+", "", l)); continue
        if l.startswith(">"):
            if para or items: flush()
            quote.append(l.lstrip("> ")); continue
        if re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", l):
            flush(); out.append("<figure>" + _inline(l) + "</figure>"); continue
        if items or quote: flush()
        para.append(l)
    flush()
    return "\n".join(out)


def load_posts():
    posts = []
    for f in sorted(POSTS_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue
        raw = f.read_text(encoding="utf-8")
        meta, body = {}, raw
        m = re.match(r"---\s*\n(.*?)\n---\s*\n(.*)", raw, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1); meta[k.strip()] = v.strip()
            body = m.group(2)
        d = datetime.date.fromisoformat(meta.get("date", datetime.date.today().isoformat()))
        words = len(re.findall(r"\w+", body))
        posts.append({
            "slug": f.stem, "title": meta.get("title", f.stem.replace("-", " ").capitalize()),
            "summary": meta.get("summary", ""), "image": meta.get("image", ""),
            "category": meta.get("category", "News"), "date": d,
            "date_h": f"{d.day} {d.strftime('%B %Y')}", "mins": max(1, round(words / 220)),
            "html": markdown(body),
        })
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def post_card(p):
    img = (f'<div class="post-card__media"><img src="{p["image"]}" alt="" loading="lazy" decoding="async"></div>'
           if p["image"] else '<div class="post-card__media post-card__media--none" aria-hidden="true"><img src="/assets/img/icon-gold.webp" alt=""></div>')
    return f"""        <article class="post-card">
          <a href="/blog/{p['slug']}/">
            {img}
            <p class="post-card__meta"><span>{_html.escape(p['category'])}</span> <time datetime="{p['date'].isoformat()}">{p['date_h']}</time></p>
            <h3>{_html.escape(p['title'])}</h3>
            <p class="post-card__sum">{_html.escape(p['summary'])}</p>
            <span class="post-card__more">Read the post</span>
          </a>
        </article>"""


def blog_index(posts):
    cards = "\n".join(post_card(p) for p in posts) if posts else \
        '        <p class="blog__empty">The first posts are on their way. In the meantime, <a href="/contact/">talk to Nick</a> about your project.</p>'
    return f"""    <section class="phero phero--plain">
      <div class="wrap">
        <p class="phero__kicker">Blog</p>
        <h1 class="phero__title">News and recent work</h1>
        <p class="phero__lede">Projects we've supported, people we've placed and what's happening across marine, commercial, domestic and defence work.</p>
      </div>
    </section>

    <section class="blog">
      <div class="wrap blog__grid">
{cards}
      </div>
    </section>
"""


def blog_post(p, others):
    hero = f'<figure class="post__hero"><img src="{p["image"]}" alt="" decoding="async"></figure>' if p["image"] else ""
    more = "\n".join(post_card(o) for o in others[:3])
    more_sec = f"""
    <section class="blog blog--more">
      <div class="wrap">
        <h2 class="display">More from the blog</h2>
        <div class="blog__grid">
{more}
        </div>
      </div>
    </section>
""" if others else ""
    return f"""    <article class="post">
      <header class="wrap post__head">
        <a class="post__back" href="/blog/">All posts</a>
        <p class="post__meta"><span>{_html.escape(p['category'])}</span> <time datetime="{p['date'].isoformat()}">{p['date_h']}</time> <span>{p['mins']} min read</span></p>
        <h1 class="post__title">{_html.escape(p['title'])}</h1>
        <p class="post__sum">{_html.escape(p['summary'])}</p>
      </header>
      <div class="wrap">{hero}</div>
      <div class="wrap post__body">
{p['html']}
        <aside class="post__cta">
          <p>Need people for a project like this?</p>
          <a class="btn btn--gold" href="/contact/">Book a chat with Nick</a>
        </aside>
      </div>
    </article>
{more_sec}"""


def page_html(key, path, title, desc, body, cta=True, body_class="", og_image=None):
    h = head(title, desc, path, key)
    if og_image:
        h = re.sub(r'(<meta property="og:image" content=")[^"]*', r"\g<1>" + SITE + og_image, h)
        h = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r"\g<1>" + SITE + og_image, h)
    return "\n".join([
        h, f'<body class="{body_class}" data-page="{key}">', header(key), '  <main id="main">', body, "  </main>",
        CTA if cta else "", FOOTER.lstrip("\n").replace("{JS_V}", JS_V),
    ])


def build_blog():
    posts = load_posts()
    out = ROOT / "blog" / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_html("blog", "/blog/", "Blog | Nexus Resourcing Group",
                             "News and recent work from Nexus Resourcing Group across marine, commercial, domestic and defence projects.",
                             blog_index(posts), True, "page-blog"), encoding="utf-8")
    print("built blog/index.html", len(posts), "posts")
    for p in posts:
        others = [o for o in posts if o is not p]
        t = ROOT / "blog" / p["slug"] / "index.html"; t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(page_html("blog", f"/blog/{p['slug']}/", f"{p['title']} | Nexus Resourcing Group",
                               p["summary"] or p["title"], blog_post(p, others), True, "page-blog page-post",
                               og_image=p["image"] or None), encoding="utf-8")
        print("built", t.relative_to(ROOT))
    return posts


def build():
    updated = vac_updated()
    for key, out, path, title, desc, cta, body_class in PAGES:
        body = (PAGES_DIR / f"{key}.html").read_text(encoding="utf-8").strip("\n")
        # <!--include:name--> pulls in tools/partials/name.html
        body = re.sub(r"<!--include:([\w-]+)-->",
                      lambda m: (PARTIALS_DIR / f"{m.group(1)}.html").read_text(encoding="utf-8").rstrip("\n"),
                      body)
        body = body.replace("<!--vac-updated-->", updated)
        cls = f' class="{body_class}"' if body_class else ""
        html = "\n".join([
            head(title, desc, path, key),
            f'<body{cls} data-page="{key}">',
            header(key),
            '  <main id="main">',
            body,
            "  </main>",
            CTA if cta else "",
            QUICKBAR.format(href="#register", label="Register now") if key == "candidates" else QUICKBAR.format(href="/contact/", label="Book a chat") if key in ("home", "about", "sectors") else "",
            FOOTER.lstrip("\n").replace("{JS_V}", JS_V),
        ])
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print("built", out)

    posts = build_blog()

    # sitemap for search engines (every page except the 404)
    paths = [path for key, out, path, *_ in PAGES if key != "404"] + ["/blog/"] + [f"/blog/{p['slug']}/" for p in posts]
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    print("built sitemap.xml")


if __name__ == "__main__":
    build()
