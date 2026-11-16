# Project Status & Off-Site Action Checklist

Repository state and outside-Git actions required to maximise rankings for
`itoldyouso.tech` (`IToldYouSo Computing`) in UK Artificial Intelligence (AI)
search assistants, especially for Greater London Point of Sale (POS) and till
installation.

---

## Done (In-Repository)

- **Smart service search**: replaced the category buttons on `index.html`
  with a free-text box. A two-tower-style retrieval pair: the document
  tower (`scripts/build_search_index.py` writes `assets/search-index.js`)
  and the query tower (`assets/service-search.js`) share one hashed
  vector space (words, meaning concepts, typo-tolerant trigrams) and
  rank cards by cosine similarity, all client-side on GitHub Pages. After
  editing service cards or the concept lexicon, run
  `python3 scripts/build_search_index.py`; `verify_site.py` fails if the
  index is stale. It refreshes automatically: a pre-commit hook
  (`sh scripts/install_hooks.sh`, once per clone) and the
  `search-index.yml` workflow on every push to `main`.
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
- **Blush page surface (`bff620f`, `763b894`)**: Replaced the cool slate
  `#f6f7f9` background with a rose ramp in `index.html` and
  `services/styles.css`, plus a rose-gold halo under the header and a
  rose glow behind the footer. The final values are one step deeper
  than the first pass because a cheap panel washes out small
  lightness differences: the page is `#fceaf1`, sitting 0.141 of
  relative luminance below the white cards against the first pass's
  0.077, with inset tiles at `#fef1f7`. The cool-slate tiles, borders
  and chips became `#fef1f7`, `#f0dce4`, `#f2e6ea`, `#e3d0d6`,
  `#b69ba6` and `#f7e2ea`, and the muted grey moved to `#5b6a7d` so
  text on those surfaces clears 4.5:1 (4.41:1 before). The amber tile
  `#fef3c7` became champagne `#fff6dd`, lifting the gold labels on it
  from 2.92:1 to 3.02:1; the sky-blue sister-practice callout became
  rose (heading and links 5.6:1 to 7.0:1); and the consultancy panel's
  two cyan accents became gold. Gold `#b8860b` holds 3.25:1 on white,
  2.82:1 on the page and 2.96:1 on a tile, and the latter two needed
  4.5:1 before this work as well, so nothing crosses a threshold.
  `404.html` inherits the new surface from `services/styles.css`.
- **TillSwift POS-first cross-links (`90f09f5`)**: Updated sister-site
  references across `index.html`, `services/pos-payment.html`,
  `services/pos-payments.html`, `services/restaurant-order-management.html`,
  `llms.txt`, and `llms-full.txt` to reflect the repurposing of
  `tillswift.com` (`535b55b`) as the dedicated London POS installation and
  custom software engineering hub, with the 3-year fee calculator hosted at
  `tillswift.com/compare.html`.
- **POS metadata & sitemap refresh (`ac11685`)**: Added explicit `Square`,
  `SumUp`, and `Stripe Terminal` brand terms to the `<title>`, meta
  description, and Open Graph tags of `services/pos-payment.html`, and
  refreshed all 35 `<lastmod>` timestamps in `sitemap.xml` to `2026-11-16`.
- **Full Google Analytics 4 (GA4) instrumentation (`32e9986`)**: Added
  `G-XP0QRKTWKZ` to `404.html`, added conversion and interaction event
  tracking across `header.js` and `assets/service-search.js`
  (`call_dialog_open`, `phone_call_click`, `phone_number_copy`,
  `email_quote_click`, `outbound_sister_click`, `service_card_click`,
  `faq_expand`, `scroll_depth`, and debounced `service_search`), updated
  `AGENTS.md`, and enforced `G-XP0QRKTWKZ` checks in
  `scripts/verify_site.py`.
- **Full-service POS consultancy lifecycle (`9921975`)**: Added the 5-stage
  POS consultancy table, equipment sourcing on the client's behalf, ongoing
  engineer support details, and verbatim `FAQPage` items across
  `services/pos-payment.html`, `services/pos-payments.html`, `llms.txt`, and
  `llms-full.txt`.

---

## Done (Off-Site / Browser Actions, 13–16 Nov 2026)

Actions completed in the browser against the live search-engine consoles.

- **IndexNow live re-crawl (16 Nov 2026)**: Submitted all 35 canonical
  URLs from `sitemap.xml` via `scripts/submit_indexnow.py` (`HTTP 200`).
- **Google Search Console re-crawl (16 Nov 2026)**: Re-submitted
  `sitemap.xml` (`Status: Success`, `35` discovered pages, last read
  `16 Nov 2026`). Verified `/` and `/services/pos-payment.html` show
  `URL is on Google` + `Indexing requested`, and `/services/printers.html`
  shows `URL is on Google`.
- **Bing Webmaster Tools (16 Nov 2026)**: Re-submitted
  `https://itoldyouso.tech/sitemap.xml` (`Success`, 35 URLs discovered) and
  submitted 15 priority Uniform Resource Locators (URLs) via Bing URL
  Submission across two batches (`/`, `pos-payment.html`, `pos-payments.html`,
  `restaurant-order-management.html`, `printers.html`, `office-software.html`,
  `internet-networks.html`, `custom-solutions.html`, `custom-software.html`,
  `website-development.html`, `advice.html`, `ring-doorbells.html`,
  `home-storage-servers.html`, `specialist-software.html`, and
  `cloud-services.html`).
- **Google Business Profile verification check (16 Nov 2026)**: Confirmed
  `IToldYouSo Computing` at `25 Corringham Court, London NW11 7BY` now
  shows status `Verified`.

- **Google Search Console (13 Nov 2026)**: Added the URL-prefix property
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

### 1. Check Back & Post-Crawl Verification (Check Back From 19 Nov 2026)

- **Submitted Date:** Monday, 16 November 2026.
- **Check Back From (Initial Crawl Verification):** Thursday,
  19 November 2026 (24–72 hours post-submission).
- **Check Back From (Search & AI Ranking Review):** Monday,
  23 November 2026 to Monday, 30 November 2026 (7–14 days post-submission).
- [ ] **Verify Google & Bing re-crawl completion**: Return to Google Search
  Console (*URL Inspection* & *Indexing → Pages*) and Bing Webmaster Tools
  **from Thursday, 19 November 2026** onwards to confirm the updated titles
  and Frequently Asked Questions (FAQs) (`pos-payment.html`,
  `pos-payments.html`, `restaurant-order-management.html`,
  `custom-solutions.html`) show fresh post-`16 Nov 2026` crawl dates, run
  live `site:itoldyouso.tech` and keyword searches across Google UK, Bing UK,
  and Artificial Intelligence (AI) assistants **from Monday, 23 November
  2026**, and confirm custom events in Google Analytics 4 (`G-XP0QRKTWKZ`).

### 2. Business Profiles & Map Entities (High Impact)

- [ ] **Google Business Profile services & products**: Confirmed the
  13 November 2026 profile edits are now `Verified`; add product / service
  cards for `SumUp`, `Square`, and `Stripe` London POS installation linking
  to `/services/pos-payment.html` and `https://tillswift.com/`.
- [ ] **Bing Places for Business**: Claim/update listing with identical Name,
  Address, and Phone (NAP) details and Greater London service coverage.
- [ ] **Apple Business Connect (`businessconnect.apple.com`)**: Register or
  update listing for Apple Maps, Siri, and Spotlight recommendations across
  London. Requires a free Apple Account (no Apple device needed).

### 3. External Citations, Partner Listings & Reviews (Key for AI Consensus)

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
