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

## 18:27
- Locked-down networks: if a company network blocks the animation library (common on defence and corporate sites), pages now show all content immediately instead of waiting up to four seconds.
- Phones held sideways: the homepage hero shrinks to fit, so the logo, tagline and both buttons sit on one screen.

## 18:43
- Sector links (footer and sector index): landing on a sector now leaves clear space under the sticky header and sector pills on phones and desktop.

## 18:59 (final)
- Full regression on all seven pages at phone size: no overflow, no undersized tap targets, no missing images, no script errors. Registration flow, enquiry deep links, mobile menu and sector panels all pass.

## 19:30 to 19:47: three new features
- Recruiting now: live vacancy pills (Mechanical Fitter, Devonport; Welders, Bahamas) with a pulsing "Recruiting now" indicator. Tap to expand the role, apply (pre-fills the registration form with the role) or WhatsApp Nick about it. Shown on the homepage and as "Active vacancies" at the top of Candidates; a green dot on the Candidates menu link signals live roles.
- Where we work: dotted world map on the homepage with gold pins (Plymouth HQ, Romania, Nashville, The Bahamas, Brazil) and dashed connection arcs from Plymouth. Pins drop in on scroll; hover or tap to highlight. On phones the map zooms into the Americas and Europe with a tap-to-reveal location list.
- WhatsApp: message Nick directly from the mobile quick bar, mobile menu, footer, contact details and each vacancy, with a pre-written opening message.

## 19:48
- Map labels: Plymouth's label now sits above its pin so it never collides with the Nashville and Bahamas labels; labels go compact (name only) below 1100px. Checked clean at 1440, 1024, 768 and 390.

## 20:05
- Sectors page: Marine and Commercial now show a live "1 role recruiting now" badge linking straight to the vacancies, so live roles surface wherever people are browsing.

## 20:21
- Map and vacancies linked: Plymouth and The Bahamas pins carry a pulsing green dot, and the Bahamas label reads "Recruiting now", matching the live roles.

## 20:37
- Checked the new features at 360px: quick bar (Call, WhatsApp, Book) fits, vacancy cards stack their buttons full width, and closed vacancy links are hidden from keyboard focus.
- README updated with how to add or close vacancies, change map pins and update the WhatsApp number.
