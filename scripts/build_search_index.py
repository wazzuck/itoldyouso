#!/usr/bin/env python3
"""
FILE: scripts/build_search_index.py

Purpose:
    Generates two "document tower" files, one per search on this site:

    1. assets/search-index.js, the service search on index.html at the
       repository root (41 service cards).
    2. migena/search-index.js, the documentation search on the seven
       official Migena client document pages (one record per section,
       so a result can jump straight to the matching heading).

    The "query tower" halves live in the browser: assets/service-search.js
    for the home page and migena/doc-search.js for the client portal.

    The pair work like a two-tower retrieval model: each tower maps text
    into the same fixed-length vector space, and relevance is the cosine
    similarity between a query vector and a document vector. Here the
    towers are deterministic (hashed word, concept and character-trigram
    features, weighted by Inverse Document Frequency (IDF)) rather than
    neural, so the whole system is static files that GitHub Pages can
    serve with no server, no API call and no tracking.

Deliberately NOT for:
    Hand-editing either generated index (change this file, then
    regenerate), or fetching anything over the network.

Invariants relied upon:
    1. The featurizer below (normalise, stem, hash, features) MUST match
       the one in assets/service-search.js AND the one in
       migena/doc-search.js step for step. If one changes, change the
       others and regenerate. Mismatched towers silently give poor
       results. The concept lexicon, stopwords, weights and dimension
       travel inside each index, so each query tower only has to share
       the maths, not the tables.
    2. Every service card in index.html has an href and an <h3> title.
    3. The seven pages listed in MIGENA_PAGES exist, and any section
       that should be jumpable to carries an id attribute.

Usage:
    python3 scripts/build_search_index.py          # regenerate both
    python3 scripts/build_search_index.py --check  # exit 1 if stale
"""

import html
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = REPO_ROOT / "index.html"
OUTPUT_JS = REPO_ROOT / "assets" / "search-index.js"

# Second corpus and second output: the Migena client portal. Its index
# is written beside the pages it searches so the portal loads it with
# a relative path, and so a copy of the portal folder stays complete.
MIGENA_DIR = REPO_ROOT / "migena"
MIGENA_OUTPUT = MIGENA_DIR / "search-index.js"

# The seven official document pages, in portal order, with the name
# shown beside every search result from that page. Consumed by
# read_migena_docs(). The hidden documents (questionnaire, handbook,
# cheat sheet) were removed at the client's request and are absent
# here on purpose.
MIGENA_PAGES = [
    ("contract.html", "Service Contract"),
    ("pricing.html", "Pricing & Terms"),
    ("admin.html", "Admin Guide"),
    ("management.html", "Management Guide"),
    ("till.html", "Till Procedures & Features"),
    ("till-procedures.html", "Till Procedures"),
    ("till-features.html", "Till Feature Reference"),
]

# How many characters of a section are kept as the visible snippet
# under a search result. Value: 140 characters, about two lines on a
# phone. Consumed by read_migena_docs() and shown by doc-search.js.
SNIPPET_LEN = 140

# Length of the hashed feature space. Value: 2048 buckets. Consumed by:
# both towers (bucket = hash % DIM). Larger means fewer collisions.
DIM = 2048

# Feature weights. Value: word=1.0, concept=2.0, trigram=0.3. Consumed by:
# both towers. Concepts count most because they carry meaning across
# different wording; trigrams count least and mainly absorb typos.
WEIGHT_WORD = 1.0
WEIGHT_CONCEPT = 2.0
WEIGHT_TRIGRAM = 0.3

# How many times a document title is repeated when building document
# text, so title words outweigh body words. Value: 3. Consumed by
# build_payload() for both corpora (service cards and doc sections).
TITLE_REPEAT = 3

# Common words carrying no meaning for matching. Consumed by tokenise().
STOPWORDS = set(
    "a an and are as at be but by can do for from get has have how i in "
    "is it its me my of on or our so that the their to up we with you "
    "your need want help please across london".split()
)

# The semantic lexicon: each concept is a meaning, listing words people
# use to express it. A query word and a service word that share a concept
# become similar even when they share no letters ("telly" ~ "television").
# Consumed by both towers; shipped to the browser inside the index.
CONCEPTS: Dict[str, List[str]] = {
    "payments": "pay payment card reader terminal contactless chip sumup "
    "square worldpay barclaycard stripe takings checkout acquirer pdq "
    "chip pin cash merchant zettle s700 s710 wisepos wisepad revolut "
    "teya sdk webhook",
    "till": "till tills epos pos register cashier retail shop cafe "
    "restaurant takeaway hospitality kitchen venue drawer menu salon "
    "clinic stall counter ecr kds pub bar bespoke custom integration",
    "printer": "print printer printing printers ink toner label receipt "
    "scanner airprint paper",
    "wifi": "wifi wi-fi wireless internet broadband router network "
    "networks signal ethernet cabling cable mesh connection online "
    "offline dropout slow buffering booster extender zone dead lan "
    "broadband",
    "security": "security secure cyber hack hacked hacker virus malware "
    "phishing ransomware scam breach penetration audit gdpr safe protect",
    "cctv": "cctv camera cameras alarm sensor sensors lock locks "
    "doorbell burglar surveillance ring intruder",
    "smart": "smart automation automate alexa google assistant lighting "
    "thermostat heating bulbs hue speaker speakers voice",
    "tv": "tv telly television soundbar surround streaming netflix cinema "
    "audio sound speakers entertainment",
    "repair": "repair fix fixing broken failing crash crashed slow "
    "sluggish freezing frozen laptop desktop pc mac windows virus "
    "screen battery boot",
    "data": "data recovery recover lost deleted corrupted files folder "
    "drive disk disc usb ssd photos undelete",
    "backup": "backup backups archive archiving restore copy copies "
    "protect nas storage server cloud sync",
    "migration": "migrate migration transfer move moving upgrade new "
    "machine switch replace setup old",
    "cloud": "cloud azure aws amazon google hosting saas microsoft365",
    "office": "office microsoft365 word excel outlook email mail xero "
    "quickbooks sage accounts accounting tax mtd bookkeeping workspace",
    "software": "software program application app install installation "
    "licence license autocad solidworks matlab sage custom bespoke "
    "develop developer development code coding script automation "
    "programmer database",
    "web": "website web site webpage ecommerce shop online seo domain "
    "hosting wordpress",
    "ai": "ai chatgpt claude copilot gemini chatbot chatbots artificial "
    "intelligence machine learning prompt automate",
    "car": "car cars van vans vehicle vehicles motor motors motorbike "
    "motorbikes motorcycle motorcycles lorry lorries truck trucks fleet "
    "garage garages workshop workshops mechanic mechanics automotive "
    "diagnostic diagnostics mot autodata haynes bosch",
    "training": "training train lecture lectures lesson learn teach "
    "tutor seminar course education workshop class",
    "advice": "advice advise consultancy consultant guidance recommend "
    "recommendation buy buying purchase opinion quote",
    "phone": "phone phones mobile iphone android ios ipad tablet "
    "smartphone",
    "meeting": "meeting meetings zoom teams conferencing conference "
    "webcam microphone projector presentation display boardroom video",
    "photos": "photo photos photograph photographs picture pictures "
    "album memories faces index organise organisation library",
    "accounts": "password passwords locked lockout locksmith account "
    "accounts login access recover reset hacked",
    "spam": "spam advert adverts ads popup popups pop-up junk unwanted "
    "wellbeing calm clean inbox",
    "server": "server servers domain controller vpn nas administration "
    "admin monitoring",
    "chromebook": "chromebook chromeos flex old ageing slow laptop "
    "revive refurbish",
    "telephony": "telephony telephone landline landlines voip pbx sip "
    "pstn isdn switchover 020 0800 0330 number numbers porting extension "
    "extensions handset handsets dect deskphone softphone ivr voicemail call "
    "calls caller routing ringcentral 3cx vonage bonline yealink poly cisco "
    "grandstream gigaset ata",
    "mainframe": "archaic ancient mainframe mainframes minicomputer cobol "
    "fortran vax vms pdp as400 iseries system360 system370 ebcdic punch "
    "punched floppy msdos cpm os2 retro vintage heritage 1970s 1980s 1960s "
    "emulator emulation hercules simh vt100 3270 5250 jcl cics vsam rpg",
    "seo": "seo geo schema jsonld ldjson sitemap sitemaps robots indexnow "
    "canonical screaming frog sitebulb lighthouse pagespeed vitals ahrefs "
    "semrush moz ga4 gtm analytics searchconsole webmaster serp backlink "
    "backlinks ranking rankings llmstxt",
    "audio_prod": "daw logic ableton protools cubase reaper studio midi "
    "podcast voiceover vst kontakt focusrite rme universal apollo latency "
    "asio coreaudio pipewire mastering",
    "video_prod": "davinci resolve premiere finalcut fcp aftereffects avid "
    "nle 4k 6k 8k colour color grading transcode transcoding ffmpeg atem "
    "obs livestreaming proxy filmmaking",
    "iot": "iot embedded raspberry esp32 esp8266 arduino stm32 rp2040 "
    "microcontroller microcontrollers firmware micropython freertos zephyr "
    "esphome mqtt lorawan lora zigbee matter modbus canbus rs485 i2c spi "
    "uart telemetry grafana influxdb",
    # Live event technology: ticket scanning plus everything else that has
    # to work at a festival, conference, or venue door. Members are stemmed
    # by concept_stems(), so both "scanner" and "scanning" are listed to
    # cover the two stems ("scanner" and "scan") that tokenise() produces.
    # "office" is deliberately absent: it would fire this concept on the
    # office software, migration, and printer cards, which then outrank the
    # event card for queries such as "box office".
    "events": "event events festival festivals conference conferences "
    "congress exhibition exhibitions ticket tickets ticketing barcode qr "
    "scanner scanning wristband wristbands nfc rfid cashless turnstile gate "
    "gates accreditation badge lanyard box guest crowd ushers marquee stage "
    "streaming",
}

# Extra concepts for the Migena documentation corpus only. The public
# home page never meets words such as "z report", "allergy" or "PIN",
# but the till guides are full of them, so without these the doc
# search would rank poorly on the client's own vocabulary. Merged on
# top of CONCEPTS by build_migena(); the public payload keeps CONCEPTS
# untouched, and each index ships its own concept list, so the query
# tower always uses the set its index was built with.
MIGENA_CONCEPTS: Dict[str, List[str]] = {
    "till_ops": "refund refunds void voided discount discounts pin pins "
    "staff staffmember employee employees login logins permission "
    "permissions role roles closing close closed closeout zreport "
    "zreports z report takings cash cashing up float tillout "
    "reconcile reconciliation reconcile payout payouts opening open "
    "opened course courses allergy allergies dietary modifier modifiers "
    "split splitbill splitting bill bills table tables order orders "
    "waitress waiting server tab barcode loyalty gift voucher vouchers "
    "receipt reprint reprinting training roster shift shifts drawer "
    "cashfloat centrepayment gratuity tip tips service charge",
    "cafe_docs": "cafe coffee barista brunch lunch menu menus dish "
    "dishes plate plates kitchen food fpoh front counter service "
    "station stations tillroll tillroll paper",
    "accounts_docs": "invoice invoices vat quarterly bookkeeper "
    "accountant margin gross net profit loss sheet sheets turnover "
    "bank statement statements reconciliation nominal year end",
}


def normalise(text: str) -> str:
    """Lower-case text and reduce it to space-separated ASCII words.

    Args:
        text: any string (HTML entities allowed; they are decoded).

    Returns:
        A string of lower-case a-z and 0-9 words.
    """
    # Step 1: decode entities such as &amp; so they do not leak in.
    text = html.unescape(text).lower()
    # Step 2: fold "wi-fi" into "wifi" so both spellings are one word.
    text = text.replace("wi-fi", "wifi")
    # Step 3: keep letters and digits; everything else (hyphens too) is
    # a word gap, so "dead-zone" becomes "dead zone".
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def stem(word: str) -> str:
    """Strip common English suffixes so related forms share a stem.

    Args:
        word: one normalised word.

    Returns:
        The word without a plural "s" or an "ing"/"ed" ending, when long
        enough to do so safely.
    """
    # Step 1: "ing" and "ed" endings only on words of 6+ letters.
    if len(word) >= 6 and word.endswith("ing"):
        return word[:-3]
    if len(word) >= 6 and word.endswith("ed"):
        return word[:-2]
    # Step 2: plural "s", but never "ss" (e.g. "access").
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokenise(text: str) -> List[str]:
    """Split text into stemmed, stop-word-free tokens."""
    words = normalise(text).split()
    return [stem(w) for w in words if w and w not in STOPWORDS]


def fnv1a(text: str) -> int:
    """32-bit Fowler-Noll-Vo (FNV-1a) hash of an ASCII string.

    The browser reimplements this exactly, so a given feature name lands
    in the same bucket in both towers.
    """
    value = 2166136261
    for byte in text.encode("ascii"):
        value ^= byte
        value = (value * 16777619) & 0xFFFFFFFF
    return value


def concept_stems(lexicon: Dict[str, List[str]] = CONCEPTS) -> Dict[str, set]:
    """Return each concept's member words, stemmed like real tokens.

    Args:
        lexicon: concept name to space-separated member words. Defaults
            to the public CONCEPTS lexicon; build_migena() passes the
            merged documentation lexicon instead.

    Returns:
        Mapping of concept name to the set of stemmed member words.
    """
    return {
        name: {stem(w) for w in words.split()}
        for name, words in lexicon.items()
    }


def featurise(text: str, concepts: Dict[str, set]) -> Dict[str, float]:
    """Turn text into weighted named features (the shared featurizer).

    Args:
        text: raw text to encode.
        concepts: output of concept_stems().

    Returns:
        Mapping of feature name to summed weight (before IDF).
    """
    feats: Dict[str, float] = {}
    tokens = tokenise(text)
    seen = set(tokens)
    for tok in tokens:
        # Step 1: the whole-word feature.
        feats["w:" + tok] = feats.get("w:" + tok, 0.0) + WEIGHT_WORD
        # Step 2: character trigrams over the padded word (typo-proof).
        padded = "^" + tok + "$"
        for i in range(len(padded) - 2):
            key = "g:" + padded[i:i + 3]
            feats[key] = feats.get(key, 0.0) + WEIGHT_TRIGRAM
    # Step 3: one concept feature per meaning present in the text.
    for name, members in concepts.items():
        if members & seen:
            feats["c:" + name] = WEIGHT_CONCEPT
    return feats


def bucketise(feats: Dict[str, float]) -> Dict[int, float]:
    """Fold named features into DIM hashed buckets (the hashing trick)."""
    out: Dict[int, float] = {}
    for name, weight in feats.items():
        b = fnv1a(name) % DIM
        out[b] = out.get(b, 0.0) + weight
    return out


def read_cards() -> List[Dict[str, str]]:
    """Read every service card (href, title, description) from index.html.

    Returns:
        One dict per card, in page order.
    """
    page = INDEX_HTML.read_text(encoding="utf-8")
    pattern = re.compile(
        r'<a href="(services/[^"]+)" class="service-card[^"]*"'
        r'[^>]*>(.*?)</a>',
        re.S,
    )
    cards = []
    for href, body in pattern.findall(page):
        title = re.search(r"<h3>(.*?)</h3>", body, re.S)
        desc = re.search(r"<p>(.*?)</p>", body, re.S)
        tag = re.search(r'service-tag">(.*?)<', body, re.S)
        cards.append({
            "href": href,
            "title": html.unescape(title.group(1)).strip(),
            "desc": html.unescape(desc.group(1)).strip() if desc else "",
            "tag": html.unescape(tag.group(1)).strip() if tag else "",
        })
    return cards


def strip_tags(fragment: str) -> str:
    """Reduce an HTML fragment to its plain words.

    Args:
        fragment: any HTML text, entities allowed.

    Returns:
        The text with every tag removed, HTML entities decoded, and
        whitespace collapsed to single spaces.
    """
    text = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def portal_main(page_html: str) -> str:
    """Return the article area of a portal page.

    Args:
        page_html: full source of one of the five portal pages.

    Returns:
        The inside of <main class="doc-main">, which holds the single
        document article and nothing else.

    Raises:
        ValueError: if the page has no main area, which would mean the
            page is not a portal page and the corpus list is wrong.
    """
    match = re.search(r'<main class="doc-main">(.*?)</main>',
                      page_html, re.S)
    if not match:
        raise ValueError("page has no <main class=\"doc-main\"> area")
    return match.group(1)


def sheet_body(page_html: str) -> str:
    """Return the instructional content of a printable A4 sheet.

    Args:
        page_html: full source of till-procedures.html or
            till-features.html.

    Returns:
        The body with the cover header, the print note, the footer,
        the search bar and the scripts removed, leaving only the
        numbered sections that are worth searching.
    """
    match = re.search(r"<body>(.*?)</body>", page_html, re.S)
    if not match:
        raise ValueError("sheet has no <body> element")
    text = match.group(1)
    for pattern in (
        r'<header class="cover">.*?</header>',
        r'<div class="box">.*?</div>',
        r'<div class="doc-search-bar">.*?</div>',
        r"<footer.*?</footer>",
        r"<script.*?</script>",
    ):
        text = re.sub(pattern, "", text, flags=re.S)
    return text


def split_sections(content: str) -> List[Tuple[str, str]]:
    """Split a document body into (anchor, fragment) pieces.

    The first piece is everything before the first <section> (the
    document's own header and lead); each later piece is one top-level
    <section> element together with its id attribute, or "" when the
    section carries no id. The scan counts nesting depth, so a section
    nested inside another still closes where it should.

    Args:
        content: the article or sheet body, tags intact.

    Returns:
        Pieces in document order, with empty or tag-only pieces
        dropped.
    """
    pieces: List[Tuple[str, str]] = []
    depth = 0
    cursor = 0
    anchor = ""
    for match in re.finditer(r"<section\b([^>]*)>|</section>", content):
        if match.group(0).startswith("<section"):
            if depth == 0:
                pieces.append((anchor, content[cursor:match.start()]))
                id_match = re.search(r'id="([^"]+)"', match.group(1))
                anchor = id_match.group(1) if id_match else ""
                cursor = match.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                pieces.append((anchor, content[cursor:match.end()]))
                cursor = match.end()
                anchor = ""
    if cursor < len(content):
        pieces.append((anchor, content[cursor:]))
    return [(a, f) for a, f in pieces if strip_tags(f)]


def read_migena_docs() -> List[Dict[str, object]]:
    """Read the seven official document pages into search records.

    One record is produced per section (or per document when a page
    has no sections), so a search result can link straight to the
    heading the visitor wants rather than to the top of a long page.

    Returns:
        Records in portal order. Each carries href (page plus anchor),
        title (the section heading, or the document title for the
        leading piece), page (the display name shown beside a result),
        snippet (the first SNIPPET_LEN characters of plain text) and
        parts (the text pieces featurised after the repeated title).

    Raises:
        FileNotFoundError: if any listed page has not been generated.
    """
    records: List[Dict[str, object]] = []
    for filename, display in MIGENA_PAGES:
        page_html = (MIGENA_DIR / filename).read_text(encoding="utf-8")
        if '<main class="doc-main">' in page_html:
            content = portal_main(page_html)
        else:
            content = sheet_body(page_html)
        # The leading piece anchors to the article id on portal pages;
        # the sheets have no article, so their lead links to the page.
        article = re.search(r'<article id="([^"]+)"', content)
        doc_anchor = article.group(1) if article else ""
        for position, (anchor, fragment) in enumerate(split_sections(content)):
            heading_match = re.search(r"<h[23][^>]*>(.*?)</h[23]>",
                                      fragment, re.S)
            heading = (strip_tags(heading_match.group(1))
                       if heading_match else "")
            body = strip_tags(fragment)
            if len(body) < 10:
                continue
            if not heading:
                heading = display
            piece_anchor = anchor or (doc_anchor if position == 0 else "")
            href = f"{filename}#{piece_anchor}" if piece_anchor else filename
            records.append({
                "href": href,
                "title": heading,
                "page": display,
                "snippet": body[:SNIPPET_LEN]
                + ("..." if len(body) > SNIPPET_LEN else ""),
                "parts": [body],
            })
    return records


def build_payload(records: List[Dict[str, object]],
                  concepts: Dict[str, set],
                  title_repeat: int) -> Dict[str, object]:
    """Featurise records and assemble an index payload.

    Args:
        records: dicts holding href, title and parts (the text pieces
            joined after the repeated title). Documentation records may
            also carry page and snippet, which are copied through.
        concepts: output of concept_stems().
        title_repeat: how often the title is repeated in the document
            text so title words outweigh body words. Value: 3, the
            same weighting for both corpora.

    Returns:
        The payload dict consumed by render().
    """
    # Step 1: encode each record's text into raw bucket weights.
    raw: List[Dict[int, float]] = []
    texts: List[str] = []
    for record in records:
        text = " ".join(
            [str(record["title"])] * title_repeat
            + [str(p) for p in record["parts"]]
        )
        texts.append(normalise(text))
        raw.append(bucketise(featurise(text, concepts)))

    # Step 2: IDF per bucket, so rare features count more than common.
    n = len(records)
    df = [0] * DIM
    for vec in raw:
        for b in vec:
            df[b] += 1
    idf = [round(math.log((n + 1) / (d + 1)) + 1, 3) for d in df]

    # Step 3: apply log-tf and IDF, then L2-normalise each document.
    docs = []
    for record, text, vec in zip(records, texts, raw):
        weighted = {
            b: (1 + math.log(w)) * idf[b] if w > 0 else 0.0
            for b, w in vec.items()
        }
        norm = math.sqrt(sum(v * v for v in weighted.values())) or 1.0
        sparse = sorted(
            (b, round(v / norm, 4)) for b, v in weighted.items()
        )
        doc = {
            "h": record["href"],
            "t": normalise(str(record["title"])),
            "x": text,
            "v": [[b, v] for b, v in sparse],
        }
        if "page" in record:
            # Documentation records only: "n" is the display title the
            # panel shows (t holds the normalised form used for
            # matching), "p" the document it belongs to, "s" the
            # snippet under it.
            doc["n"] = str(record["title"])
            doc["p"] = record["page"]
        if "snippet" in record:
            doc["s"] = record["snippet"]
        docs.append(doc)

    return {
        "dim": DIM,
        "idf": idf,
        "concepts": {k: sorted(v) for k, v in concepts.items()},
        "weights": [WEIGHT_WORD, WEIGHT_CONCEPT, WEIGHT_TRIGRAM],
        "stopwords": sorted(STOPWORDS),
        "docs": docs,
    }


def render(payload: Dict[str, object], global_name: str) -> str:
    """Render a payload as JavaScript source.

    Args:
        payload: output of build_payload().
        global_name: the window property to assign, for example
            SERVICE_SEARCH_INDEX or MIGENA_SEARCH_INDEX.

    Returns:
        JavaScript source assigning window.<global_name>, one JSON line
        per document so version-control diffs stay readable.
    """
    lines = ["/* GENERATED by scripts/build_search_index.py. Do not edit. */",
             "window.%s = {" % global_name]
    for key, value in payload.items():
        if key == "docs":
            lines.append('"docs": [')
            lines.append(",\n".join(
                json.dumps(d, separators=(",", ":")) for d in value))
            lines.append("]")
        else:
            lines.append(
                '"%s": %s,' % (key, json.dumps(value, separators=(",", ":")))
            )
    lines.append("};")
    return "\n".join(lines) + "\n"


def build() -> str:
    """Build the full text of assets/search-index.js.

    Returns:
        JavaScript source assigning window.SERVICE_SEARCH_INDEX.
    """
    cards = read_cards()
    records = [{
        "href": card["href"],
        "title": card["title"],
        "parts": [card["desc"], card["tag"]],
    } for card in cards]
    return render(
        build_payload(records, concept_stems(), TITLE_REPEAT),
        "SERVICE_SEARCH_INDEX",
    )


def documentation_lexicon() -> Dict[str, List[str]]:
    """Return the concept lexicon used for both documentation indexes.

    Returns:
        The public CONCEPTS lexicon with MIGENA_CONCEPTS layered on
        top. build_migena() and scripts/build_offline_doc.py both call
        this, so the online portal and the offline copy always search
        with the same meanings.
    """
    lexicon = dict(CONCEPTS)
    lexicon.update(MIGENA_CONCEPTS)
    return lexicon


def build_migena() -> str:
    """Build the full text of migena/search-index.js.

    Returns:
        JavaScript source assigning window.MIGENA_SEARCH_INDEX, built
        from the seven document pages with the public lexicon plus the
        documentation-only concepts.
    """
    return render(
        build_payload(read_migena_docs(),
                      concept_stems(documentation_lexicon()),
                      TITLE_REPEAT),
        "MIGENA_SEARCH_INDEX",
    )


def main(argv: List[str]) -> int:
    """Entry point: regenerate both indexes, or with --check compare.

    Args:
        argv: command-line arguments; "--check" switches from writing
            to comparing.

    Returns:
        0 on success or when nothing is stale, 1 when --check finds a
        stale output.
    """
    outputs = [
        (OUTPUT_JS, build(), "assets/search-index.js"),
        (MIGENA_OUTPUT, build_migena(), "migena/search-index.js"),
    ]
    if "--check" in argv:
        stale = [
            label for path, content, label in outputs
            if not path.is_file()
            or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            print("%s is stale; rerun the builder."
                  % ", ".join(stale))
            return 1
        return 0
    for path, content, _ in outputs:
        path.write_text(content, encoding="utf-8")
        print("Wrote %s (%d bytes)" % (path, len(content)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
