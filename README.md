# Nexus Resourcing Group website

Static site deployed by Netlify from this repo.

- `main` is live on nexusrg.co.uk (currently the holding page in `placeholder/`).
- `staging` is the full site in progress, at staging--nexusshowcase.netlify.app.

## Editing pages
Page content lives in `tools/pages/*.html`, and shared pieces (contact card) in `tools/partials/`.
The header, menu, footer and call-to-action band are in `tools/build.py`.

After any change, rebuild the HTML from the repo root:

```
python3 tools/build.py
```

This writes `index.html`, `about/`, `sectors/`, `candidates/`, `contact/`, `privacy/` and `404.html`. Commit the built files too.

- Styles: `assets/css/styles.css`
- Interactions: `assets/js/main.js` (GSAP, ScrollTrigger and Lenis load from CDNs)
- Images: `assets/img/`

## Vacancies, map and WhatsApp
- **Vacancies:** edit `tools/partials/vacancies.html` (one `<li class="vac">` per role), then rebuild. The same list appears on the homepage and Candidates. Update the "recruiting now" badges in `tools/pages/sectors.html` and the green dot on the Candidates menu link (`NAV` in `tools/build.py`) to match.
- **Map pins:** edit `LOCATIONS` and `LIVE` in `tools/make_map.py`, run it with the Natural Earth `ne_110m_land.geojson` file, then rebuild.
- **WhatsApp:** links use `https://wa.me/447963398473` with a pre-written message. Change the number in `tools/build.py`, `tools/partials/vacancies.html` and the contact pages if it changes.

## Placeholders
Anything with `class="ph"` is placeholder content shown with a dashed gold outline: client logos, case studies, testimonials, Nick's photo and the privacy policy retention periods. Replace it and remove the `ph` class before launch.

## Before going live
- Set Nick's real booking link in `CAL_URL` at the top of `assets/js/main.js`.
- Netlify Forms: two forms, `enquiry` and `candidate-registration` (with CV upload). Turn on form detection and add email notifications in Netlify.
- Remove the `X-Robots-Tag: noindex` header in `netlify.toml` and the holding-page redirect on `main`.
- Have Nexus review the privacy policy.
