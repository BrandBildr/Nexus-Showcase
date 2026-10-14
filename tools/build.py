#!/usr/bin/env python3
"""Builds the Nexus site pages from tools/pages/*.html.

Each page body lives in tools/pages/. This script wraps it with the shared
<head>, header, mobile menu, call-to-action band and footer, then writes the
finished HTML to the site root (index.html, about/index.html, ...).

Run from the repo root:  python3 tools/build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "tools" / "pages"
PARTIALS_DIR = ROOT / "tools" / "partials"
SITE = "https://nexusrg.co.uk"

NAV = [
    ("about", "/about/", "About"),
    ("sectors", "/sectors/", "Sectors"),
    ("candidates", "/candidates/", "Candidates"),
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
     "Built on more than twenty years of marine resourcing experience. A proactive take on supplying skilled people to complex projects.",
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
    "founder": { "@type": "Person", "name": "Nick Souness", "jobTitle": "Managing Director" },
    "knowsAbout": ["Marine resourcing", "Commercial resourcing", "Domestic resourcing", "Defence resourcing"]
  }
  </script>
"""


def head(title, desc, path, key):
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
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.jpg?v=1">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Nexus Resourcing Group logo">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="/assets/img/favicon.png">
  <link rel="apple-touch-icon" href="/assets/img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">{preload}
  <link rel="stylesheet" href="/assets/css/styles.css">
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
        <p><a href="tel:+447963398473">07963 398473</a><br><a href="mailto:nick@nexusrg.co.uk">nick@nexusrg.co.uk</a></p>
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
          <li><a href="/contact/">Book a call</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap foot__base">
      <p>&copy; <span data-year>2026</span> Nexus Resourcing Group Limited. Registered in England and Wales, company no. 17426336. Registered office: 51 Burnham Park Road, Plymouth, PL3 5QB.</p>
      <p><a href="/privacy/">Privacy &amp; cookies</a></p>
    </div>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def build():
    for key, out, path, title, desc, cta, body_class in PAGES:
        body = (PAGES_DIR / f"{key}.html").read_text(encoding="utf-8").strip("\n")
        # <!--include:name--> pulls in tools/partials/name.html
        body = re.sub(r"<!--include:([\w-]+)-->",
                      lambda m: (PARTIALS_DIR / f"{m.group(1)}.html").read_text(encoding="utf-8").rstrip("\n"),
                      body)
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
            FOOTER.lstrip("\n"),
        ])
        target = ROOT / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print("built", out)

    # sitemap for search engines (every page except the 404)
    urls = "\n".join(f"  <url><loc>{SITE}{path}</loc></url>" for key, out, path, *_ in PAGES if key != "404")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    print("built sitemap.xml")


if __name__ == "__main__":
    build()
