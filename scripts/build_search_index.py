#!/usr/bin/env python3
"""
FILE: scripts/build_search_index.py

Purpose:
    Generates assets/search-index.js, the "document tower" half of the
    service search on index.html. The "query tower" half lives in
    assets/service-search.js and runs in the visitor's browser.

    The pair work like a two-tower retrieval model: each tower maps text
    into the same fixed-length vector space, and relevance is the cosine
    similarity between a query vector and a service vector. Here the
    towers are deterministic (hashed word, concept and character-trigram
    features, weighted by Inverse Document Frequency (IDF)) rather than
    neural, so the whole system is static files that GitHub Pages can
    serve with no server, no API call and no tracking.

Deliberately NOT for:
    Hand-editing assets/search-index.js (it is generated: change this
    file, then regenerate), or fetching anything over the network.

Invariants relied upon:
    1. The featurizer below (normalise, stem, hash, features) MUST match
       the one in assets/service-search.js step for step. If one changes,
       change the other and regenerate. Mismatched towers silently give
       poor results.
    2. Every service card in index.html has an href and an <h3> title.

Usage:
    python3 scripts/build_search_index.py          # regenerate
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

# Length of the hashed feature space. Value: 2048 buckets. Consumed by:
# both towers (bucket = hash % DIM). Larger means fewer collisions.
DIM = 2048

# Feature weights. Value: word=1.0, concept=2.0, trigram=0.3. Consumed by:
# both towers. Concepts count most because they carry meaning across
# different wording; trigrams count least and mainly absorb typos.
WEIGHT_WORD = 1.0
WEIGHT_CONCEPT = 2.0
WEIGHT_TRIGRAM = 0.3

# How many times a service title is repeated when building document text,
# so title words outweigh description words. Value: 3.
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
    "chip pin cash merchant zettle",
    "till": "till tills epos pos register cashier retail shop cafe "
    "restaurant takeaway hospitality kitchen venue drawer menu salon "
    "clinic stall counter ecr kds pub bar",
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


def concept_stems() -> Dict[str, set]:
    """Return each concept's member words, stemmed like real tokens."""
    return {
        name: {stem(w) for w in words.split()}
        for name, words in CONCEPTS.items()
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


def build() -> str:
    """Build the full text of assets/search-index.js.

    Returns:
        JavaScript source assigning window.SERVICE_SEARCH_INDEX.
    """
    cards = read_cards()
    concepts = concept_stems()

    # Step 1: encode each card's text into raw bucket weights.
    raw: List[Dict[int, float]] = []
    texts: List[str] = []
    for card in cards:
        text = " ".join(
            [card["title"]] * TITLE_REPEAT + [card["desc"], card["tag"]]
        )
        texts.append(normalise(text))
        raw.append(bucketise(featurise(text, concepts)))

    # Step 2: IDF per bucket, so rare features count more than common.
    n = len(cards)
    df = [0] * DIM
    for vec in raw:
        for b in vec:
            df[b] += 1
    idf = [round(math.log((n + 1) / (d + 1)) + 1, 3) for d in df]

    # Step 3: apply log-tf and IDF, then L2-normalise each document.
    docs = []
    for card, text, vec in zip(cards, texts, raw):
        weighted = {
            b: (1 + math.log(w)) * idf[b] if w > 0 else 0.0
            for b, w in vec.items()
        }
        norm = math.sqrt(sum(v * v for v in weighted.values())) or 1.0
        sparse = sorted(
            (b, round(v / norm, 4)) for b, v in weighted.items()
        )
        docs.append({
            "h": card["href"],
            "t": normalise(card["title"]),
            "x": text,
            "v": [[b, v] for b, v in sparse],
        })

    # Step 4: emit one JSON-ish line per record to keep diffs readable.
    payload = {
        "dim": DIM,
        "idf": idf,
        "concepts": {k: sorted(v) for k, v in concepts.items()},
        "weights": [WEIGHT_WORD, WEIGHT_CONCEPT, WEIGHT_TRIGRAM],
        "stopwords": sorted(STOPWORDS),
        "docs": docs,
    }
    lines = ["/* GENERATED by scripts/build_search_index.py. Do not edit. */",
             "window.SERVICE_SEARCH_INDEX = {"]
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


def main(argv: List[str]) -> int:
    """Entry point: regenerate, or with --check compare to disk."""
    content = build()
    if "--check" in argv:
        current = (OUTPUT_JS.read_text(encoding="utf-8")
                   if OUTPUT_JS.is_file() else "")
        if current != content:
            print("assets/search-index.js is stale; rerun the builder.")
            return 1
        return 0
    OUTPUT_JS.write_text(content, encoding="utf-8")
    print("Wrote %s (%d bytes)" % (OUTPUT_JS, len(content)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
