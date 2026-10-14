# Staging review log (14 Oct 2026)

## 16:45
- Tablet (701–980px): page heroes stay two-column instead of stacking a huge image.
- Mobile: bigger tap areas on text links, contact details, footer and legal links; logo link padded.
- Sectors (mobile): the sticky sector pills move up to the top when the header hides on scroll.
- Dropped an unused font weight (300) to lighten page loads.

## 17:02
- Search: added business details for Google (EmploymentAgency schema with address, phone and founder) on the homepage.
- Search: build now generates sitemap.xml; robots.txt points to it (staging stays hidden via the noindex header).
- Small phones (360px): registration steps show only the current step's label so they don't wrap.

## 17:19
- Mobile speed: phones now load a 65KB hero image instead of the 220KB desktop one (srcset + matching preload).
- Less jumping while pages load: width and height added to every page image, with a global `height: auto` so nothing stretches.

## 17:36
- Mobile: a quick-contact bar ("Call Nick" + "Book a chat") slides up once you're past the page header, and tucks away wherever the page already shows contact options (hero, contact card, registration form, closing banner, footer). On Candidates it says "Register now" instead.
