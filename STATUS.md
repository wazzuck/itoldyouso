# Project Status & Off-Site Action Checklist

Repository state and outside-Git actions required to maximise rankings for
`itoldyouso.tech` (`IToldYouSo Computing`) in UK Artificial Intelligence (AI)
search assistants, especially for Greater London Point of Sale (POS) and till
installation.

---

## Done (In-Repository)

- **Crawler & AI context files (`f356f8f`, `e210ccf`)**: Updated
  `robots.txt` to allow AI search and retrieval crawlers (`OAI-SearchBot`,
  `ChatGPT-User`, `Claude-SearchBot`, `PerplexityBot`, `DeepSeekBot`,
  `DeepSeek-User`, `GrokBot`, `MistralAI-User`, `DuckAssistBot`, `QwenBot`,
  `Bingbot`, `Applebot`, and `Google-Extended`). Rewrote `llms.txt` and added
  `llms-full.txt` prioritising London POS / Electronic Point of Sale (EPOS)
  services and our Hampstead base serving Greater London. Updated
  `sitemap.xml` priorities across all 33 public pages.
- **Home page & flagship POS pages (`981e1a1`)**: Positioned POS, till, and
  card payment installation first on `index.html`; rewrote
  `services/pos-payment.html`, `services/pos-payments.html`, and
  `services/restaurant-order-management.html` with London-wide coverage,
  Hampstead base details, platform comparisons, static headers, and verbatim
  JavaScript Object Notation for Linked Data (JSON-LD) Frequently Asked
  Questions (FAQ) schema.
- **Full 32-page service consistency (`72decaa`)**: Standardised all 32
  `services/*.html` pages with canonical links, Open Graph (OG) and Twitter
  tags, `Service` + `BreadcrumbList` JSON-LD, static crawler-visible headers,
  unified `IToldYouSo Computing` branding, and British English copy.
- **Automated verification (`9f67114`)**: Extended `scripts/verify_site.py`
  to check all 32 service pages, `llms-full.txt`, and major AI crawler
  rules.
- **IndexNow instant push notifications**: Added key file
  `4cd63bf4d0be4b3ca44d92ba5c1e37ad.txt`, submission script
  `scripts/submit_indexnow.py`, and `.github/workflows/indexnow.yml` so
  Microsoft Bing and IndexNow-participating AI search engines are notified
  whenever GitHub Pages deploys `main`.
- **Modern responsive layout (`049e2bd`, `69a8c8f`)**: Reworked `index.html`,
  `header.css`, and `services/styles.css` with a slate-and-amber visual
  system, streamlined full-width hero welcoming all IT and POS work,
  filterable 32-service catalogue keeping POS cards first above the fold and
  collapsing to single-column cards on phones, split FAQ section, and wrapped
  mobile breadcrumbs and call buttons.
- **Header logo & ChromeOS Flex harmonisation (`ef6af71`, `7e3046e`)**:
  Compressed `assets/glasses.png` from 574 kilobytes to a 7-kilobyte
  256x256 circular Portable Network Graphics (PNG) badge and harmonised
  `services/chromeos-flex.html` onto the shared Cascading Style Sheets (CSS)
  design system and FAQ schema.
- **Process section, cross-links & Search Engine Optimisation (`403c35f`)**:
  Added the three-step `#how-it-works` process section (initial consultation,
  written statement of work with fixed no-obligation up-front price, and zero
  sales chasing) across `index.html`, `llms.txt`, and `llms-full.txt`. Added
  `favicon.ico`, Apple touch icon, `1200x630` `assets/social-card.png`,
  custom `404.html`, 32-page `FAQPage` structured data, and three-card
  sibling service cross-links across every `services/*.html` page, enforced
  by `scripts/verify_site.py`.
- **Call & consultation dialogue (`e08f543`, `33ab7ff`)**: Updated the FAQ
  `Speak With an Engineer` action on `index.html` to open an accessible
  `#call-dialog` on desktop and Chromebook browsers (showing `020 4520 9114`,
  one-click copy, direct call link, and email option) while keeping native
  one-tap `tel:` dialling on mobile phones.
- **Property address correction (`a927e32`)**: Set the house number to
  `25 Corringham Court` across the home page JSON-LD and footer, the flagship
  POS page, `llms.txt`, and `llms-full.txt`, matching the Google Business
  Profile listing for Name, Address, Phone (NAP) consistency. Client document
  pages were left untouched (see Blocked below).

---

## Done (Off-Site / Browser Actions, 13 Nov 2026)

Actions completed in the browser against the live search-engine consoles.

- **Google Search Console**: Added the URL-prefix property
  `https://itoldyouso.tech/`; ownership auto-verified through the existing
  Google Analytics (`gtag.js`) tag. Submitted `sitemap.xml`, then ran
  **Request Indexing** on the four priority URLs. `/` and
  `/services/restaurant-order-management.html` were already indexed and were
  re-queued for a fresh crawl; `/services/pos-payment.html` and
  `/services/pos-payments.html` were unknown to Google and are now queued.
  The sitemap row may briefly show "Couldn't fetch" until Google retries.
- **Bing Webmaster Tools**: Signed in and imported the site from Google
  Search Console (no manual verification needed). Sitemap registered with
  35 URLs discovered and 0 errors; reports may take up to 48 hours to fill.
- **Google Business Profile**: Completed the existing managed profile:
  - uploaded three photos (`assets/social-card.png`,
    `assets/glasses_square.png`, `assets/network.png` — `glasses.png` at
    7 kilobytes is below Google's ~10 kilobyte minimum),
  - changed the business name from `itoldyouso.tech` to
    `IToldYouSo Computing`,
  - set the primary category to `IT support and services` with additional
    `Computer repair service` (Google's UK list has no POS / till category),
  - replaced the description with POS / EPOS / London keyword copy
    (421 of 750 characters; URLs are rejected in this field),
  - set the service area to London (Google does not accept
    "Greater London" as a term), and
  - corrected the street address to `25 Corringham Court` (Google had
    canonicalised it to `7 Corringham Court`).
  Phone `020 4520 9114` and website verified correct. All edits show
  "pending", usually reviewed within 10 minutes. The £400 Google Ads credit
  and Google Workspace trial offers were declined, not the paid products.

---

## Next (Outside-Git Search & Authority To-Do List)

Note: ChatGPT Search, DeepSeek, Claude, Perplexity, and Grok do not offer
direct business directory forms. They rely on web crawlers, search-engine
indexes, business profiles, and external consensus across the web.

### 1. Business Profiles & Map Entities (High Impact)

- [ ] **Google Business Profile follow-up**: Confirm the pending edits
  (name, categories, description, service area, address) were approved after
  10 minutes, then add product / service cards linking to
  `/services/pos-payment.html`.
- [ ] **Bing Places for Business**: Claim/update listing with identical Name,
  Address, and Phone (NAP) details and Greater London service coverage.
- [ ] **Apple Business Connect (`businessconnect.apple.com`)**: Register or
  update listing for Apple Maps, Siri, and Spotlight recommendations across
  London. Requires a free Apple Account (no Apple device needed).

### 2. External Citations, Partner Listings & Reviews (Key for AI Consensus)

- [ ] **Consistent UK directory profiles**: Publish identical NAP details and
  backlinks to `https://itoldyouso.tech/services/pos-payment.html` on:
  - Trustpilot (`uk.trustpilot.com`)
  - Yell (`yell.com`)
  - FreeIndex (`freeindex.co.uk`)
  - Bark (`bark.com`)
  - LinkedIn Company Page
  - Companies House / official registrar alignment where applicable
- [ ] **POS hardware & software partner directories**: Register or link as a
  London installer where eligible (Square Specialist, Shopify Partner,
  Zettle, SumUp, Clover, Lightspeed). External links from vendor sites aid
  discovery in DeepSeek, Brave Search (used alongside Claude), and Google.
- [ ] **X (Twitter) account for Grok visibility**: Create/maintain an active
  business profile sharing short London POS, thermal printer, and hospitality
  till notes so xAI Grok sees live activity.
- [ ] **Collect keyword-rich UK customer reviews**: Ask recent hospitality and
  retail till clients for Google and Trustpilot reviews specifically
  mentioning `"London"`, `"till installation"`, and `"POS"` / `"EPOS"`.

---

## Blocked / Open Decisions

- [ ] **Private client document privacy**: Existing client pages
  (`amazon-till-docs.html`, `square-till-docs.html`, `george/index.html`,
  `illyrian/index.html`, and `migena/index.html`) were left untouched. Decide
  whether to add `<meta name="robots" content="noindex, nofollow">` and
  `robots.txt` `Disallow:` rules so client installation notes do not appear
  in public AI search snippets.
