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
- **Modern responsive layout (`049e2bd`)**: Reworked `index.html`,
  `header.css`, and `services/styles.css` with a slate-and-amber visual
  system, split hero with flagship POS panel, filterable 32-service catalogue
  collapsing to single-column cards on phones, split FAQ section, and wrapped
  mobile breadcrumbs and call buttons.

---

## Next (Outside-Git Search & Authority To-Do List)

Note: ChatGPT Search, DeepSeek, Claude, Perplexity, and Grok do not offer
direct business directory forms. They rely on web crawlers, search-engine
indexes, business profiles, and external consensus across the web.

### 1. Search Console & Indexing Submissions (Immediate)

- [ ] **Google Search Console (`search.google.com/search-console`)**: Verify
  ownership of `itoldyouso.tech`, submit `https://itoldyouso.tech/sitemap.xml`,
  and run **Request Indexing** on `/`, `/services/pos-payment.html`,
  `/services/pos-payments.html`, and
  `/services/restaurant-order-management.html`.
- [ ] **Bing Webmaster Tools (`bing.com/webmastertools`)**: Verify site
  ownership (or import from Google Search Console) and submit
  `https://itoldyouso.tech/sitemap.xml`. Feeds Microsoft Copilot, Yahoo,
  DuckDuckGo, and secondary search pipelines.

### 2. Business Profiles & Map Entities (High Impact)

- [ ] **Google Business Profile (GBP)**: Confirm business name
  (`IToldYouSo Computing`), Hampstead base (`Corringham Court, Corringham Road,
  London NW11 7BY`), phone (`020 4520 9114`), Greater London service area,
  POS / EPOS installation categories, and product/service cards linking to
  `/services/pos-payment.html`.
- [ ] **Bing Places for Business**: Claim/update listing with identical Name,
  Address, and Phone (NAP) details and Greater London service coverage.
- [ ] **Apple Business Connect (`businessconnect.apple.com`)**: Register or
  update listing for Apple Maps, Siri, and Spotlight recommendations across
  London.

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
