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
- **London-based & Hampstead base hero copy (`2e18d64`)**: Sharpened the
  opening hero statement in `index.html` so London-based coverage and the
  Hampstead base appear explicitly in the first sentence.
- **Telephony & Archaic Mainframes (`cbf3338`, `a9e1e2f`)**: Expanded the
  catalogue from 34 to 36 service cards and dedicated pages:
  - `services/telephony.html`: Virtual `020` London, `0800`, and `0330`
    landlines, number porting, United Kingdom (UK) Public Switched Telephone
    Network (PSTN) and Integrated Services Digital Network (ISDN) switchover
    migrations, Voice over Internet Protocol (VoIP), Cloud Private Branch
    Exchange (PBX), Session Initiation Protocol (SIP) trunks, Interactive
    Voice Response (IVR) menus, AI receptionists, Customer Relationship
    Management (CRM) and POS caller-ID integration, Internet Protocol (IP)
    and Digital Enhanced Cordless Telecommunications (DECT) handsets,
    Analogue Telephone Adapters (ATAs), Power over Ethernet (PoE), and Voice
    Virtual Local Area Network (VLAN) Quality of Service (QoS).
  - `services/legacy-mainframes.html`: Archaic 1960s–1990s mainframes
    (International Business Machines (IBM) System/360, System/370, and
    Application System/400 (AS/400); International Computers Limited (ICL)),
    Digital Equipment Corporation (DEC) Programmed Data Processor (PDP-11)
    and Virtual Address Extension (VAX / OpenVMS), Common Business-Oriented
    Language (COBOL), Formula Translation (FORTRAN), Report Program
    Generator (RPG), Job Control Language (JCL), Customer Information
    Control System (CICS), Virtual Storage Access Method (VSAM), Control
    Program for Microcomputers (CP/M), Microsoft Disk Operating System
    (MS-DOS), Operating System/2 (OS/2), Extended Binary Coded Decimal
    Interchange Code (EBCDIC) tape and floppy extraction, Hercules and SIMH
    emulation, and Application Programming Interface (API) bridging.
  - Updated `index.html`, `404.html`, `services/*.html`, `sitemap.xml`,
    `robots.txt` (`95a4c9b`), `llms.txt`, `llms-full.txt`,
    `scripts/build_search_index.py`, `assets/search-index.js`, and
    `scripts/verify_site.py`.
- **SEO & AI Search Optimisation (`019e445`)**: Added
  `services/seo-optimisation.html` and expanded the catalogue from 36 to 37
  services, covering Technical Search Engine Optimisation (SEO), Generative
  Engine Optimisation (GEO), Google Search Console (GSC), Bing Webmaster
  Tools, IndexNow, Google Analytics 4 (GA4), Google Tag Manager (GTM),
  Screaming Frog, Sitebulb, Lighthouse, Core Web Vitals, Ahrefs, Semrush, Moz
  Pro, Schema.org JSON-LD, `llms.txt`, Google Business Profile (GBP), Bing
  Places, Apple Business Connect, and CI SEO gates; updated `index.html`,
  `404.html`, `services/*.html`, `sitemap.xml`, `robots.txt`, `llms.txt`,
  `llms-full.txt`, `scripts/build_search_index.py`, `assets/search-index.js`,
  and `scripts/verify_site.py`.
- **Home hero headline (`fedf514`)**: Updated the main `<h1>` in `index.html`
  to `"Technology, Hardware, Software and Networks Consultancy Across London"`.
- **Digital Audio & Video Production (`c19e2e4`)**: Added
  `services/audio-production.html` and `services/video-production.html`,
  expanding the catalogue from 37 to 39 services (Digital Audio Workstations
  (DAWs), audio interfaces, Musical Instrument Digital Interface (MIDI),
  low-latency Deferred Procedure Call (DPC) tuning, podcast studios, DaVinci
  Resolve, Premiere Pro, Final Cut Pro, 10-Gigabit Ethernet (10GbE) Network
  Attached Storage (NAS) shared editing pools, colour calibration, and
  Blackmagic ATEM / OBS live streaming); updated `index.html`, `404.html`,
  `services/*.html`, `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`,
  `scripts/build_search_index.py`, `assets/search-index.js`, and
  `scripts/verify_site.py`.
- **IoT & Embedded Devices (`4fd9ffe`)**: Added `services/iot-embedded.html`
  and expanded the catalogue from 39 to 40 services (Raspberry Pi, ESP32,
  Arduino, STM32, C/C++ and MicroPython firmware, Embedded Linux, FreeRTOS,
  Zephyr, Message Queuing Telemetry Transport (MQTT), Long Range Wide Area
  Network (LoRaWAN), Zigbee, Matter, Modbus, Controller Area Network (CAN bus),
  cold-chain temperature logging, InfluxDB/Grafana, and segregated IoT VLANs);
  updated `index.html`, `404.html`, `services/*.html`, `sitemap.xml`,
  `robots.txt`, `llms.txt`, `llms-full.txt`, `scripts/build_search_index.py`,
  `assets/search-index.js`, and `scripts/verify_site.py`.
- **Migena portal documentation (`0b047d7`)**: Published the three
  requested guides in the password-protected client portal
  (`migena/index.html`): Operations Flash Cards (17 tap-to-flip cards
  for daily tasks such as opening and closing, and for stressful ones
  such as refunds), an Admin Guide (adding, changing and removing
  staff PINs — Personal Identification Numbers), and a Management
  Guide (accounts, records, and daily, weekly and monthly routines).
  Navigation items 3 to 5 now link to them, the article anchor offset
  was raised to clear the sticky navigation bar, and the document was
  bumped to version 1.1.
- **Event Management Technology (`5efeaf4`)**: Added
  `services/event-management.html` and expanded the catalogue from 40 to
  41 services (1D/2D barcode and QR Code ticket readers, offline-capable
  check-in and box office software, Radio-Frequency Identification (RFID)
  and Near Field Communication (NFC) wristbands, cashless top-ups,
  turnstiles, badge printers, high-density venue Wi-Fi with failover,
  roaming card readers, people counting, Closed-Circuit Television (CCTV),
  digital mobile radio, and OBS Studio / Blackmagic ATEM streaming);
  added an `events` search concept so queries such as "barcode ticket
  scanner" rank the new page first; updated `index.html`, `404.html`,
  `services/*.html`, `sitemap.xml`, `robots.txt`, `llms.txt`,
  `llms-full.txt`, `scripts/build_search_index.py`,
  `assets/search-index.js`, and `scripts/verify_site.py`. Legal and
  patent check found no risk: descriptive first-party copy with
  nominative vendor names only.
- **Migena portal owner tasks and download link (`ee400f1`)**: The
  main page (`migena/index.html`) is a landing page with three
  buttons. The Documentation page (`migena/documentation.html`) has a
  prominent offline-copy download banner at the top, then four owner
  task cards: verify identity, update software, turn on cash payments,
  and buy a handheld strap or lanyard so staff can carry the devices
  hands-free. A separate section lists the tasks owned by Neville, not the
  owner. The five guides are embedded on the page below those sections,
  so there are no guide buttons. The guide pages keep their own search.
- **Migena portal: grouped navigation, documentation search and
  offline copy**: Grouped the Admin Guide, Management Guide and Till
  Procedures & Features under a `3. Documentation` button on the
  landing page (`migena/index.html`), which opens the Documentation
  page (`migena/documentation.html`). Removed the three hidden documents
  entirely at the client's request (Technical Intake Questionnaire,
  Cafe Client Handbook, Countertop Cheat Sheet): their articles,
  navigation items, stylesheet rules, the dead questionnaire script,
  the three generated pages, and their entries in
  `scripts/split_portal.py`. Added a two-tower search to all seven
  official document pages: `scripts/build_search_index.py` now also
  emits `migena/search-index.js` (59 section records, each carrying
  an anchor id so a result jumps to the exact heading),
  `migena/doc-search.js` is the query tower, `migena/doc-search.css`
  styles the box, and `scripts/build_offline_doc.py` writes
  `migena/offline.html`, one self-contained file holding every guide,
  the search inlined and the User Passwords page, laid out for a
  390-pixel phone and for a desktop window alike. The pre-commit
  hook, `search-index.yml` and `scripts/verify_site.py` regenerate
  and check all of it. Legal and patent check found no risk:
  first-party HTML, CSS and JavaScript only, no third-party
  libraries, and the hashed vector retrieval is a standard
  technique implemented from scratch.
- **GitHub Pages deploys unblocked: AGENTS.md pointer (`6d3dda2`)**:
  Every Pages build had failed with "Page build failed" since
  `8396e8c` (21 Nov 2026), when `AGENTS.md` became a symlink to
  `../vunderland/settings/AGENTS.md`. GitHub's build machines do not
  hold that path, so the dangling link aborted every build and froze
  the live site at the 21 Nov 05:17 version. The failure boundary was
  exact: `51cdb79`, the commit before the symlink, built. `AGENTS.md`
  is now a regular pointer file naming the golden master, which still
  holds every common rule, so one edit reaches all repositories with
  no copy to drift. `AGENTS.local.md` records the local rule that
  common changes go to the golden master; `_config.yml` keeps its
  exclude so Jekyll never publishes the pointer, and `.nojekyll` was
  removed as a misdiagnosis. First green build after two days:
  `6d3dda2`, 23 Nov 2026 17:38 GMT. Companion changes: `vunderland`
  `d7eca05` rewrote the golden source for the pointer scheme, and
  `datavault` `8563efa`, `kay` `24e3767`, `tillswift` `8886843`
  converted the same way. Still symlinked: `heathandcity`, whose
  local branch is ahead 138 / behind 175 and needs an operator
  decision before anything is committed there.
- **Owner task: straps and lanyards for the hand-held devices**: The
  fourth owner task on `migena/documentation.html` holds a purchase
  shortlist of straps, lanyards and holsters, so staff can carry the
  devices hands-free on a belt, round the neck or over the shoulder.
  It opens with a note from Neville: the handheld devices are top
  heavy with the built-in printers and can be easily dropped and
  smashed, and whilst they are relatively cheap to replace they take
  a long time to set up, so they are best kept in good working order
  if you can. Prices were checked on
  Amazon on 23 November 2026: the DURA belt-loop holster made for the
  SumUp Terminal at £21.00, which is the only listing that names this
  Terminal; the MOBILIS shockproof case at £19.99 with its O-rings at
  £6.99 and breakaway shoulder strap at £19.49, about £46 in all; the
  universal sling pouch at £36.12; and a trial chest harness or
  three-way buckle holster at £7.33 to £7.58. The card warns that
  lanyard holders made only for the SumUp Air, Solo or 3G will not
  hold this Terminal, and tells the owner to ring Neville if a listing
  does not name the SumUp Terminal. It is not gated behind tasks 1 to
  3, because buying a strap changes nothing on the till.
  `scripts/split_portal.py` builds the card, `scripts/verify_site.py`
  now expects four owner cards rather than three, and
  `migena/documentation.html` was regenerated. Legal and patent check
  found no risk: first-party copy with nominative vendor names, plain
  product links and no affiliate tag.
- **Offline copy: search box centred on desktop**: In the download
  (`migena/offline.html`) the search box sat hard against the left
  edge of the window on a desktop, because `.doc-search-bar` is a
  plain block and the `flex: 1 1 auto` on the box inside it did
  nothing. `migena/doc-search.css` now centres the box with
  `margin: 0 auto`, so it sits on the same axis as the centred
  content column. A phone is unchanged: the bar there is narrower
  than the 640-pixel cap, so the box still fills the row at 16px
  type. The two printable sheets are unchanged as well, for the same
  reason. `migena/offline.html` was regenerated from the stylesheet.

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

## Next (Migena installation)

- [ ] **Neville's six Migena tasks**: listed under "Tasks owned by
  Neville" on `migena/documentation.html`. They are the printer routing
  check, the Wi-Fi check, a written guide to printing the bill before
  payment, modifiers printed under their items on tickets, staff names on
  order tickets, and a payout method for withdrawing cash from SumUp. The
  payout method needs the owner's decision.

## Blocked / Open Decisions

- [ ] **Private client document privacy**: Existing client pages
  (`amazon-till-docs.html`, `square-till-docs.html`, `george/index.html`,
  `illyrian/index.html`, and `migena/index.html`) were left untouched. Decide
  whether to add `<meta name="robots" content="noindex, nofollow">` and
  `robots.txt` `Disallow:` rules so client installation notes do not appear
  in public AI search snippets.
- [ ] **Till documents say cash is not taken**: `migena/TILL_PROCEDURES.md`
  section 8.4 and `migena/TILL_FEATURES.md` still say cash is not taken on
  the payment screen. Update them, and the closing-up routine, once the
  owner has done task 3 (turn on cash payments). Needs the operator's go-ahead.
- [ ] **Migena portal script error (pre-existing)**: Unlocking the
  portal with `?pwd=migenalika` or a stored unlock state throws
  `Cannot access 'TERMS_DAY_STORAGE_KEY' before initialization` and
  aborts the portal script before it defines the terms-acceptance and
  questionnaire handlers. The fix is to move the
  `TERMS_DAY_STORAGE_KEY` constant declaration up to the configuration
  block at the top of the same script. Confirmed present before the
  documentation work in `0b047d7` and left unfixed there to keep that
  change limited to documentation.
- [x] **Client credentials location — operator override recorded 23
  November 2026**: the earlier rule that the SumUp username and
  password are "never stored in this public repository" is
  superseded for the Migena job by the operator's explicit decision,
  taken after the risk was stated in full. The credentials now live
  in `migena/sumup_password.txt` and are embedded in the generated
  `migena/offline.html`, both committed here. The portal's password
  gate is client-side only, so anyone with the repository URL can
  read them; the operator accepted that risk. The password was also
  shared over chat on 18 November 2026, so it should be rotated by
  the client. The private repository `wazzuck/itoldyouso_client`
  still holds `ACCESS.md`.
- [x] **Staff passwords in the offline copy — operator acknowledgement
  recorded 23 November 2026**: the operator has acknowledged the risk of
  the staff passwords in `migena/sumup_password.txt` appearing on the
  User Passwords page of `migena/offline.html`. This extends the override
  above to those staff rows, and supersedes the rule in the Migena
  checklist (`INSTALLATION_CHECKLIST.md`, section 5.7, item 1) for them.
  The operator's stated reason is that a sign-in from a new device needs
  a two-factor authentication (2FA) code sent to the owner's phone. That
  covers new devices. It does not cover a device that is already signed
  in to the account.
