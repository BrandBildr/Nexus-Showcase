# Nexus Resourcing Group: homepage concept

A single-page showcase of what the Nexus Resourcing Group website could be. Static HTML, CSS and JS, deployed to Netlify from `main`.

- `index.html` page markup
- `assets/css/styles.css` styles (brand palette and Montserrat)
- `assets/js/main.js` interactions (GSAP, ScrollTrigger and Lenis load from CDNs)
- `assets/img/` logos, wordmark letters and photography

## Before going live
- Set Nick's real booking link in `CAL_URL` at the top of `assets/js/main.js`.
- Enquiries use Netlify Forms (form name `enquiry`). Turn on form detection in Netlify under Forms, then add an email notification.
- The site is set to `noindex` (meta tag, `netlify.toml` header and `robots.txt`). Remove all three at launch.
