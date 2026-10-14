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

## 17:53
- Accessibility: homepage sector panels now behave as expand buttons for screen readers (they were marked as tabs with no matching panels), keep arrow-key support, and show a clear focus ring.
- Contrast: inactive registration step labels and the sector index links darkened to pass readability guidelines.

## 18:10
- Phone keyboards: email fields open the email keyboard with no auto-capitals or autocorrect, phone fields open the number pad, names capitalise automatically, and the keyboard's return key reads "Next" while filling in forms.
- Re-tested the full registration flow, enquiry deep links and mobile menu: all working.
