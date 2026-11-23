#!/usr/bin/env python3
"""
==============================================================================
FILE: scripts/verify_site.py
==============================================================================

PURPOSE:
Automated quality, discoverability, Search Engine Optimisation (SEO),
Generative Engine Optimisation (GEO), and policy verification script for the
IToldYouSo Computing website (itoldyouso.tech).

WHAT THIS FILE IS NOT FOR:
- Does not modify or format source files in place.
- Does not require external third-party Python packages outside the standard
  library.

INVARIANTS:
1. Exits with status code 0 only when all structural, search engine,
   Artificial Intelligence (AI) crawler, service-page, and 80-column
   documentation checks pass.
2. Exits with status code 1 and prints a diagnostic report if any check fails.
==============================================================================
"""

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Dict, List, Set, Tuple
import xml.etree.ElementTree as ET

# Maximum line width allowed for Markdown documentation and code comments per
# AGENTS.md Section 4, Policy 6.
# Value: 80 characters. Consumed by: check_line_lengths().
MAX_DOC_COLUMNS = 80

# Minimum number of alternative terms every service must list in the llms
# files. Value: 5. Consumed by: check_synonym_coverage().
MIN_SYNONYMS = 5

# Root directory of the repository checkout.
# Consumed by: main() and all verification helper routines.
REPO_ROOT = Path(__file__).resolve().parent.parent

# Canonical base Uniform Resource Locator (URL) for production hosting.
BASE_URL = "https://itoldyouso.tech"

# Total number of public service detail pages expected in services/.
# Consumed by: check_required_files(), check_sitemap_urls(), main().
EXPECTED_SERVICE_COUNT = 41


class IdCollector(HTMLParser):
    """Collect every element id of a page, in document order.

    Used to prove that a page holds no duplicate id. Two sections with
    the same id would make an in-page link jump to the wrong place.

    Attributes:
        ids: the id attribute of every element, in reading order.
    """

    def __init__(self, ids: List[str]) -> None:
        """Prepare the collector.

        Args:
            ids: the list to fill. It is cleared first, so a caller can
                reuse one list.
        """
        super().__init__(convert_charrefs=True)
        self.ids = ids
        self.ids.clear()

    def handle_starttag(self, tag: str,
                        attrs: List[Tuple[str, str]]) -> None:
        """Record an element's id attribute, if it has one.

        Args:
            tag: the element's tag name.
            attrs: its attribute pairs.
        """
        for name, value in attrs:
            if name == "id" and value:
                self.ids.append(value)


class SiteHTMLValidator(HTMLParser):
    """
    Lightweight HTML parser that records element identifiers, metadata tags,
    links, and title/header snippets for verification.

    Attributes:
        element_ids (Set[str]): Set of all id="..." values encountered.
        meta_tags (List[dict]): List of attribute dictionaries for meta tags.
        canonical_href (str | None): Target href of canonical link tag.
        sitemap_href (str | None): Target href of XML sitemap link tag.
        alternate_hrefs (List[str]): Target hrefs of alternate link tags.
    """

    def __init__(self) -> None:
        """Initialise the HTML validator state."""
        super().__init__()
        self.element_ids: Set[str] = set()
        self.meta_tags: List[Dict[str, str]] = []
        self.canonical_href: str | None = None
        self.sitemap_href: str | None = None
        self.alternate_hrefs: List[str] = []

    def handle_starttag(
        self, tag: str, attrs: List[Tuple[str, str | None]]
    ) -> None:
        """
        Inspect opening HTML tag and record identifiers, links, and metadata.

        Args:
            tag: Lowercase HTML tag name.
            attrs: List of (attribute_name, attribute_value) tuples.
        """
        attr_map = {k.lower(): v for k, v in attrs if v is not None}
        el_id = attr_map.get("id")
        if el_id:
            self.element_ids.add(el_id)

        if tag.lower() == "link":
            rel_val = attr_map.get("rel", "")
            if rel_val == "canonical":
                self.canonical_href = attr_map.get("href")
            elif rel_val == "sitemap":
                self.sitemap_href = attr_map.get("href")
            elif rel_val == "alternate" and attr_map.get("href"):
                self.alternate_hrefs.append(attr_map["href"])

        if tag.lower() == "meta":
            self.meta_tags.append(attr_map)


def _plain_text(markup: str) -> str:
    """
    Reduce HTML or JavaScript Object Notation (JSON) text to comparable plain
    text by stripping tags, decoding entities, and normalising whitespace.

    Args:
        markup: Raw text that may contain HTML entities and markup tags.

    Returns:
        Text with tags removed, entities decoded, and whitespace collapsed.
    """
    # 1. Strip script and style elements before removing tags.
    no_blocks = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1>",
        " ",
        markup,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # 2. Strip all remaining markup tags.
    no_tags = re.sub(r"<[^>]+>", " ", no_blocks)
    # 3. Decode entities and collapse multiple whitespace runs.
    return re.sub(r"\s+", " ", html.unescape(no_tags)).strip()


def _validate_page_metadata_and_jsonld(
    raw_html: str,
    label: str,
    expected_canonical: str,
    required_graph_types: Tuple[str, ...],
    min_faq_count: int = 0,
) -> Tuple[List[str], SiteHTMLValidator]:
    """
    Shared validator checking canonical link, meta description, Open Graph
    (OG), Twitter Card metadata, and JavaScript Object Notation for Linked
    Data (JSON-LD) graphs for any HTML page on the site.

    Args:
        raw_html: Full HTML document text.
        label: Short human-readable filename label for diagnostic errors.
        expected_canonical: Exact expected canonical URL string.
        required_graph_types: Schema.org @type names required in @graph.
        min_faq_count: Minimum Frequently Asked Questions (FAQ) items expected.

    Returns:
        Tuple of (list of diagnostic error strings, populated validator).
    """
    errors: List[str] = []
    page_text = _plain_text(raw_html)

    # 1. Parse HTML head and attribute metadata.
    validator = SiteHTMLValidator()
    validator.feed(raw_html)

    # 2. Verify canonical link target.
    if validator.canonical_href != expected_canonical:
        errors.append(
            f"{label} canonical link invalid: '{validator.canonical_href}' "
            f"(expected '{expected_canonical}')"
        )

    expected_sitemap_href = f"{BASE_URL}/sitemap.xml"
    if validator.sitemap_href != expected_sitemap_href:
        errors.append(
            f"{label} sitemap link invalid: '{validator.sitemap_href}' "
            f"(expected '{expected_sitemap_href}')"
        )

    for required_alt in (f"{BASE_URL}/llms.txt", f"{BASE_URL}/llms-full.txt"):
        if required_alt not in validator.alternate_hrefs:
            errors.append(
                f"{label} missing alternate LLM link: '{required_alt}'"
            )

    # 3. Verify meta description, robots, Open Graph, and Twitter Card tags.
    meta_props = {
        m.get("property"): m.get("content") for m in validator.meta_tags
    }
    meta_names = {
        m.get("name"): m.get("content") for m in validator.meta_tags
    }

    if not meta_names.get("description"):
        errors.append(f"{label} missing non-empty <meta name='description'>")

    robots_content = (meta_names.get("robots") or "").lower()
    if "index" not in robots_content or "follow" not in robots_content:
        errors.append(
            f"{label} <meta name='robots'> must allow 'index, follow'"
        )

    required_og = (
        "og:title",
        "og:description",
        "og:url",
        "og:type",
        "og:image",
    )
    for og_prop in required_og:
        if not meta_props.get(og_prop):
            errors.append(f"{label} missing Open Graph tag: '{og_prop}'")

    required_tw = (
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
    )
    for tw_name in required_tw:
        if not meta_names.get(tw_name):
            errors.append(f"{label} missing Twitter Card tag: '{tw_name}'")

    # 4. Verify <title> contains no embedded HTML tags such as <i>.
    title_match = re.search(
        r"<title>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL
    )
    if not title_match or not title_match.group(1).strip():
        errors.append(f"{label} missing non-empty <title> element")
    elif "<" in title_match.group(1) or ">" in title_match.group(1):
        errors.append(f"{label} <title> contains raw HTML tags")

    # 5. Verify first-party Google Analytics 4 (GA4) gtag.js tag presence.
    ga_src = "https://www.googletagmanager.com/gtag/js?id=G-XP0QRKTWKZ"
    if "G-XP0QRKTWKZ" not in raw_html or ga_src not in raw_html:
        errors.append(f"{label} missing GA4 G-XP0QRKTWKZ Google tag")

    # 6. Parse and validate JSON-LD structured data block.
    jsonld_blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', raw_html, re.S
    )
    if len(jsonld_blocks) != 1:
        return (
            errors
            + [
                f"Expected 1 JSON-LD block in {label}, "
                f"found {len(jsonld_blocks)}"
            ],
            validator,
        )

    try:
        data = json.loads(jsonld_blocks[0])
    except json.JSONDecodeError as exc:
        return (
            errors + [f"JSON-LD in {label} is invalid JSON: {exc}"],
            validator,
        )

    graph = data.get("@graph", [])
    if not graph:
        errors.append(f"JSON-LD in {label} is missing '@graph' list")

    types_present: Set[str] = set()
    faq_entity_count = 0

    # 7. Inspect Schema.org graph entities and check FAQ verbatim text match.
    for node in graph:
        node_type = node.get("@type")
        if isinstance(node_type, list):
            types_present.update(node_type)
        elif isinstance(node_type, str):
            types_present.add(node_type)

        if node.get("@type") == "FAQPage":
            faq_items = node.get("mainEntity", [])
            faq_entity_count = len(faq_items)
            for item in faq_items:
                q_name = item.get("name", "")
                ans_text = item.get("acceptedAnswer", {}).get("text", "")
                if not q_name or not ans_text:
                    errors.append(
                        f"{label} FAQPage Question missing 'name' or "
                        f"'acceptedAnswer.text'"
                    )
                if q_name not in page_text:
                    errors.append(
                        f"{label} FAQ Question not visible verbatim in HTML: "
                        f"'{q_name[:40]}...'"
                    )
                if ans_text not in page_text:
                    errors.append(
                        f"{label} FAQ Answer not visible verbatim in HTML: "
                        f"'{ans_text[:40]}...'"
                    )

    for req_type in required_graph_types:
        if req_type not in types_present:
            errors.append(
                f"{label} JSON-LD missing required '@type': '{req_type}'"
            )

    if min_faq_count > 0 and faq_entity_count < min_faq_count:
        errors.append(
            f"{label} expected at least {min_faq_count} FAQ entries, "
            f"found {faq_entity_count}"
        )

    return errors, validator


def check_required_files() -> List[str]:
    """
    Verify that all core root files, Large Language Model (LLM) context files,
    and all 41 service pages exist and are non-empty.

    Returns:
        List of error diagnostic messages (empty if all files exist).
    """
    errors: List[str] = []

    # 1. Verify primary root, status, workflow, and AI discovery files.
    core_files = [
        "index.html",
        "404.html",
        "favicon.ico",
        "assets/apple-touch-icon.png",
        "assets/social-card.png",
        "header.css",
        "header.js",
        "header-loader.js",
        "header-template.html",
        "CNAME",
        "README.md",
        "AGENTS.md",
        "STATUS.md",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
        "llms-full.txt",
        "scripts/submit_indexnow.py",
        "scripts/build_search_index.py",
        "scripts/split_portal.py",
        "scripts/build_offline_doc.py",
        "scripts/install_hooks.sh",
        ".githooks/pre-commit",
        ".github/workflows/search-index.yml",
        "assets/search-index.js",
        "assets/service-search.js",
        "migena/doc-search.css",
        "migena/doc-search.js",
        "migena/search-index.js",
        "migena/offline.html",
        "migena/documentation.html",
        "migena/sumup_password.txt",
        ".github/workflows/indexnow.yml",
    ]

    for rel_path in core_files:
        full_path = REPO_ROOT / rel_path
        if not full_path.is_file():
            errors.append(f"Missing required file: {rel_path}")
        elif full_path.stat().st_size == 0:
            errors.append(f"Required file is empty: {rel_path}")

    # 2. Verify a valid 32-character IndexNow verification key file exists.
    key_files = [
        p
        for p in sorted(REPO_ROOT.glob("*.txt"))
        if re.match(r"^[0-9a-f]{32}$", p.stem)
    ]
    if len(key_files) != 1:
        errors.append(
            f"Expected 1 IndexNow hex key file at repo root, "
            f"found {len(key_files)}"
        )
    elif key_files[0].read_text(encoding="utf-8").strip() != key_files[0].stem:
        errors.append(
            f"IndexNow key file {key_files[0].name} contents do not match "
            f"filename stem"
        )

    # 3. Verify the expected number of service HTML pages exist cleanly.
    services_dir = REPO_ROOT / "services"
    if not services_dir.is_dir():
        errors.append("Services directory missing: services/")
    else:
        service_htmls = list(services_dir.glob("*.html"))
        if len(service_htmls) != EXPECTED_SERVICE_COUNT:
            errors.append(
                f"Expected exactly {EXPECTED_SERVICE_COUNT} service HTML files, "
                f"found {len(service_htmls)}"
            )
        for sfile in service_htmls:
            if sfile.stat().st_size == 0:
                errors.append(f"Service file is empty: {sfile.name}")

    return errors


def check_sitemap_urls() -> List[str]:
    """
    Validate sitemap.xml format and ensure it indexes the home page and all
    41 service pages.

    Returns:
        List of error diagnostic messages (empty if sitemap is valid).
    """
    errors: List[str] = []
    sitemap_path = REPO_ROOT / "sitemap.xml"
    if not sitemap_path.is_file():
        return ["sitemap.xml not found"]

    # 1. Parse Extensible Markup Language (XML) tree.
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
    except ET.ParseError as exc:
        return [f"sitemap.xml is invalid XML: {exc}"]

    # 2. Extract all location URLs with XML namespace handling.
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {
        loc.text.strip()
        for loc in root.findall("sm:url/sm:loc", ns)
        if loc.text
    }

    # 3. Check home page presence.
    expected_home = f"{BASE_URL}/"
    if expected_home not in urls:
        errors.append(f"sitemap.xml missing home page: {expected_home}")

    # 4. Check all 41 service pages presence.
    services_dir = REPO_ROOT / "services"
    if services_dir.is_dir():
        for sfile in services_dir.glob("*.html"):
            expected_url = f"{BASE_URL}/services/{sfile.name}"
            if expected_url not in urls:
                errors.append(
                    f"sitemap.xml missing service page: {expected_url}"
                )

    # 5. Verify total URL count (home + services).
    expected_total = 1 + EXPECTED_SERVICE_COUNT
    if len(urls) != expected_total:
        errors.append(
            f"sitemap.xml expected {expected_total} URLs (home + services), "
            f"found {len(urls)}"
        )

    return errors


def check_robots_txt() -> List[str]:
    """
    Verify robots.txt permits search engines and AI assistants to crawl the
    domain and references sitemap.xml.

    Returns:
        List of error diagnostic messages (empty if valid).
    """
    errors: List[str] = []
    robots_path = REPO_ROOT / "robots.txt"
    if not robots_path.is_file():
        return ["robots.txt not found"]

    content = robots_path.read_text(encoding="utf-8")

    # 1. Verify sitemap directive.
    expected_sitemap = f"Sitemap: {BASE_URL}/sitemap.xml"
    if expected_sitemap not in content:
        errors.append(
            f"robots.txt missing sitemap reference: '{expected_sitemap}'"
        )

    # 2. Verify site is not universally blocked.
    if re.search(r"(?im)^\s*Disallow:\s*/\s*$", content):
        errors.append("robots.txt must not disallow the root path '/'")

    # 3. Verify wildcard and major AI search bot user-agents are permitted.
    required_agents = (
        "User-agent: *",
        "User-agent: OAI-SearchBot",
        "User-agent: Claude-SearchBot",
        "User-agent: PerplexityBot",
        "User-agent: DeepSeekBot",
        "User-agent: GrokBot",
    )
    for agent in required_agents:
        if agent not in content:
            errors.append(f"robots.txt missing '{agent}' directive")

    # 4. Verify telephony, mainframes, and LLM context references are present.
    for keyword in ("telephony", "mainframes", "llms.txt", "llms-full.txt"):
        if keyword not in content.lower():
            errors.append(
                f"robots.txt missing expected crawler keyword: '{keyword}'"
            )

    return errors


def check_llms_txt() -> List[str]:
    """
    Verify that llms.txt and llms-full.txt provide high-signal Markdown context
    including Hampstead base, London-wide coverage, telephone, email, sister
    practices, Point of Sale (POS) priority, and all 41 service links.

    Returns:
        List of error diagnostic messages (empty if valid).
    """
    errors: List[str] = []
    llms_path = REPO_ROOT / "llms.txt"
    llms_full_path = REPO_ROOT / "llms-full.txt"

    if not llms_path.is_file():
        return ["llms.txt not found"]

    content = llms_path.read_text(encoding="utf-8")

    # 1. Verify mandatory entity, contact, and location phrases in llms.txt.
    required_phrases = [
        "IToldYouSo Computing",
        "020 4520 9114",
        "contactus@itoldyouso.tech",
        "Hampstead",
        "Greater London",
        "Highgate",
        "Golders Green",
        "Belsize Park",
        "TillSwift",
        "Heath & City Technology",
        "https://heathandcity.com/",
        "llms-full.txt",
    ]
    for phrase in required_phrases:
        if phrase not in content:
            errors.append(f"llms.txt missing required phrase: '{phrase}'")

    # 2. Verify all 41 service HTML pages are linked in llms.txt.
    services_dir = REPO_ROOT / "services"
    if services_dir.is_dir():
        for sfile in services_dir.glob("*.html"):
            expected_link = f"{BASE_URL}/services/{sfile.name}"
            if expected_link not in content:
                errors.append(
                    f"llms.txt missing link to service page: {expected_link}"
                )

    # 3. Verify llms-full.txt contains extended London POS knowledge base.
    if not llms_full_path.is_file():
        errors.append("llms-full.txt not found")
    else:
        full_text = llms_full_path.read_text(encoding="utf-8")
        full_required = [
            "IToldYouSo Computing",
            "020 4520 9114",
            "contactus@itoldyouso.tech",
            "Hampstead",
            "Greater London",
            "Point of Sale",
            "TillSwift",
            "Heath & City Technology",
            "pos-payment.html",
            "pos-payments.html",
        ]
        for phrase in full_required:
            if phrase not in full_text:
                errors.append(
                    f"llms-full.txt missing required phrase: '{phrase}'"
                )

    return errors


def check_synonym_coverage() -> List[str]:
    """Check every service page keeps rich alternative wording everywhere.

    Enforces the findability rule: each services/*.html page must have
    (1) a link in llms.txt followed by an "Also searched as:" line with at
    least MIN_SYNONYMS comma-separated terms, (2) an entry in the
    llms-full.txt synonym section with at least MIN_SYNONYMS terms, and
    (3) a vector in the generated search index (so the site search can
    find it). The general "Also Known As" glossary must also exist.

    Returns:
        List of error diagnostic messages (empty if all covered).
    """
    errors: List[str] = []
    llms = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")
    full = (REPO_ROOT / "llms-full.txt").read_text(encoding="utf-8")
    index_js = (REPO_ROOT / "assets/search-index.js").read_text(
        encoding="utf-8"
    )
    for heading in ("## Also Known As", "## General Terminology"):
        source = llms if "Also" in heading else full
        if heading not in source:
            errors.append(f"missing glossary heading: {heading}")

    for sfile in sorted((REPO_ROOT / "services").glob("*.html")):
        slug = sfile.name
        # Step 1: llms.txt link line followed by synonym continuation.
        match = re.search(
            re.escape(f"{BASE_URL}/services/{slug})")
            + r"\s*\n\s+Also searched as:(.*?)(?:\n\n|\n- |\n#|\Z)",
            llms,
            re.S,
        )
        if not match or match.group(1).count(",") + 1 < MIN_SYNONYMS:
            errors.append(f"llms.txt: {slug} lacks synonym line")
        # Step 2: llms-full.txt synonym entry.
        match = re.search(
            r"- services/" + re.escape(slug) + r"\s*\n(.*?)(?:\n- |\n\n)",
            full,
            re.S,
        )
        if not match or match.group(1).count(",") + 1 < MIN_SYNONYMS:
            errors.append(f"llms-full.txt: {slug} lacks synonym entry")
        # Step 3: search index vector (cards only exist for these).
        if f'"h":"services/{slug}"' not in index_js:
            errors.append(f"search index: no vector for {slug}")
    return errors


def check_html_and_jsonld() -> List[str]:
    """
    Verify index.html canonical link, metadata, FAQ section, JSON-LD graph,
    and outbound links to all 41 service pages.

    Returns:
        List of error diagnostic messages (empty if valid).
    """
    errors: List[str] = []
    index_path = REPO_ROOT / "index.html"
    if not index_path.is_file():
        return ["index.html not found"]

    raw_html = index_path.read_text(encoding="utf-8")

    # 1. Run shared metadata, Open Graph, Twitter Card, and FAQ checks.
    page_errors, validator = _validate_page_metadata_and_jsonld(
        raw_html=raw_html,
        label="index.html",
        expected_canonical=f"{BASE_URL}/",
        required_graph_types=("FAQPage",),
        min_faq_count=4,
    )
    errors.extend(page_errors)

    # 2. Check presence of #faq section element id.
    if "faq" not in validator.element_ids:
        errors.append(
            "index.html missing required FAQ section element id='faq'"
        )

    # 3. Verify ITService or LocalBusiness entity exists in JSON-LD @graph.
    jsonld_match = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', raw_html, re.S
    )
    if jsonld_match:
        try:
            data = json.loads(jsonld_match.group(1))
            types_present: Set[str] = set()
            for node in data.get("@graph", []):
                nt = node.get("@type")
                if isinstance(nt, list):
                    types_present.update(nt)
                elif isinstance(nt, str):
                    types_present.add(nt)
            if not (
                "ITService" in types_present or "LocalBusiness" in types_present
            ):
                errors.append(
                    "index.html JSON-LD missing 'ITService' or 'LocalBusiness'"
                )
        except json.JSONDecodeError:
            pass

    # 4. Verify index.html links to all 41 service pages (zero orphan pages).
    services_dir = REPO_ROOT / "services"
    if services_dir.is_dir():
        for sfile in sorted(services_dir.glob("*.html")):
            rel_link = f"services/{sfile.name}"
            if rel_link not in raw_html:
                errors.append(
                    f"index.html does not link to service page: {rel_link}"
                )

    # 5. Verify custom 404.html carries the first-party GA4 gtag.js snippet.
    err404_path = REPO_ROOT / "404.html"
    if err404_path.is_file():
        err404_html = err404_path.read_text(encoding="utf-8")
        ga_src = "https://www.googletagmanager.com/gtag/js?id=G-XP0QRKTWKZ"
        if "G-XP0QRKTWKZ" not in err404_html or ga_src not in err404_html:
            errors.append("404.html missing GA4 G-XP0QRKTWKZ Google tag")

    return errors


def check_service_pages() -> List[str]:
    """
    Validate all 41 pages under services/ for SEO metadata, static crawler-
    visible headers, JSON-LD Service + BreadcrumbList + FAQPage accuracy, and
    clean brand unification.

    Returns:
        List of error diagnostic messages (empty if all 41 pages pass).
    """
    errors: List[str] = []
    services_dir = REPO_ROOT / "services"
    if not services_dir.is_dir():
        return ["services/ directory not found"]

    for sfile in sorted(services_dir.glob("*.html")):
        raw_html = sfile.read_text(encoding="utf-8")
        label = f"services/{sfile.name}"

        # 1. Verify SEO metadata, Open Graph, Twitter Card, JSON-LD, and FAQs.
        page_errors, _ = _validate_page_metadata_and_jsonld(
            raw_html=raw_html,
            label=label,
            expected_canonical=f"{BASE_URL}/services/{sfile.name}",
            required_graph_types=("Service", "BreadcrumbList", "FAQPage"),
            min_faq_count=3,
        )
        errors.extend(page_errors)

        # 2. Verify static header markup for non-JavaScript AI bots.
        header_match = re.search(
            r"<header>(.*?)</header>", raw_html, re.IGNORECASE | re.DOTALL
        )
        if not header_match or not header_match.group(1).strip():
            errors.append(f"{label} has an empty <header></header> block")
        else:
            header_body = header_match.group(1)
            if "020 4520 9114" not in header_body:
                errors.append(f"{label} static <header> missing phone number")

        # 3. Verify stale Personal/Legacy branding has been removed.
        if re.search(r"\bNeville\b", raw_html):
            errors.append(f"{label} still contains stale 'Neville' branding")

        # 4. Verify at least three sibling cross-link cards are present.
        if len(re.findall(r'class="related-card"', raw_html)) < 3:
            errors.append(
                f"{label} missing 3 sibling cross-link cards (.related-card)"
            )

    return errors


def check_line_lengths() -> List[str]:
    """
    Verify that Markdown documentation files and code comments wrap at or
    below MAX_DOC_COLUMNS (80 characters), exempting lines containing URLs.

    Returns:
        List of error diagnostic messages (empty if all lines comply).
    """
    errors: List[str] = []

    # 1. Check Markdown, robots.txt, and plain-text LLM documentation files.
    md_files = [
        "README.md",
        "STATUS.md",
        "llms.txt",
        "llms-full.txt",
        "robots.txt",
    ]
    for rel_path in md_files:
        path = REPO_ROOT / rel_path
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            if len(line) > MAX_DOC_COLUMNS and "http" not in line:
                errors.append(
                    f"{rel_path}:{lineno} exceeds {MAX_DOC_COLUMNS} cols "
                    f"({len(line)} chars)"
                )

    # 2. Check code comments in Python scripts and workflow YAML.
    code_files = [
        "scripts/verify_site.py",
        "scripts/submit_indexnow.py",
        "scripts/build_search_index.py",
        "scripts/split_portal.py",
        "scripts/build_offline_doc.py",
        ".github/workflows/indexnow.yml",
    ]
    for rel_path in code_files:
        path = REPO_ROOT / rel_path
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()
            is_comment = stripped.startswith("#")
            if is_comment and len(line) > MAX_DOC_COLUMNS and "http" not in line:
                errors.append(
                    f"{rel_path}:{lineno} comment exceeds "
                    f"{MAX_DOC_COLUMNS} cols ({len(line)} chars)"
                )

    return errors


def check_search_index() -> List[str]:
    """Check the smart service search index is fresh and wired in.

    Returns:
        Error messages: stale generated index, or index.html missing the
        search input or script tags.
    """
    errors: List[str] = []
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/build_search_index.py"),
         "--check"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        errors.append("assets/search-index.js is stale (rerun builder).")
    page = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
    for needle in (
        'id="service-search-input"',
        'src="assets/search-index.js"',
        'src="assets/service-search.js"',
    ):
        if needle not in page:
            errors.append(f"index.html is missing {needle}")
    return errors


def check_migena_portal() -> List[str]:
    """Check the Migena portal pages, their search and the offline copy.

    Verifies that:
      1. the three generated portal pages are in step with
         scripts/split_portal.py;
      2. the offline copy is in step with scripts/build_offline_doc.py;
      3. all seven official document pages (and the offline copy)
         carry the search box, its stylesheet and both search scripts;
      4. index.html is a landing page with three buttons and no longer
         holds the three documents removed at the client's request;
      5. documentation.html shows the three owner task cards, the six
         cards owned by Neville and the five embedded guides, with no
         duplicate ids, and is password gated;
      6. the offline copy contains the User Passwords page.

    Returns:
        Error messages; empty when every artefact is in step.
    """
    errors: List[str] = []

    # 1. Staleness of the two generators this check owns; the search
    #    index itself is covered by check_search_index().
    for script in ("split_portal.py", "build_offline_doc.py"):
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / script),
             "--check"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors.append(
                result.stdout.strip() or f"{script} --check failed"
            )

    # 2. The search box on every official document page.
    pages = [
        "contract.html", "pricing.html", "admin.html",
        "management.html", "till.html",
        "till-procedures.html", "till-features.html",
    ]
    for name in pages:
        path = REPO_ROOT / "migena" / name
        if not path.is_file():
            errors.append(f"Missing migena/{name}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in (
            'id="doc-search-input"',
            'href="doc-search.css"',
            'src="doc-search.js"',
            'src="search-index.js"',
        ):
            if needle not in text:
                errors.append(f"migena/{name} is missing {needle}")

    # 3. The main page is a landing page with three buttons; the three
    #    documents removed at the client's request are gone.
    portal = (REPO_ROOT / "migena" / "index.html").read_text(
        encoding="utf-8")
    for link in ('href="contract.html"', 'href="pricing.html"',
                 'href="documentation.html"'):
        if link not in portal:
            errors.append(f"migena/index.html is missing {link}")
    if '<section class="portal-landing"' not in portal:
        errors.append("migena/index.html has no portal landing section")
    if '<section class="owner-tasks"' in portal:
        errors.append("migena/index.html should not show owner tasks "
                      "(they belong on documentation.html)")
    for gone in ('id="questionnaire"', 'id="handbook"',
                 'id="cheatsheet"', 'id="nav-doc-toggle"'):
        if gone in portal:
            errors.append(f"migena/index.html still contains removed "
                          f"{gone}")

    # 4. The Documentation page shows the three owner task cards, the six
    #    cards owned by Neville and the five embedded guides, each anchor
    #    once with no duplicates, and is password gated.
    hub = REPO_ROOT / "migena" / "documentation.html"
    if not hub.is_file():
        errors.append("Missing migena/documentation.html")
    else:
        hub_text = hub.read_text(encoding="utf-8")
        if hub_text.count('<section class="owner-task-card">') != 3:
            errors.append("migena/documentation.html must show the three "
                          "owner task cards")
        if hub_text.count('<section class="engineer-task-card">') != 6:
            errors.append("migena/documentation.html must show the six "
                          "task cards owned by Neville")
        if '<section class="engineer-tasks"' not in hub_text:
            errors.append("migena/documentation.html has no section "
                          "owned by Neville")
        if 'href="offline.html"' not in hub_text:
            errors.append("migena/documentation.html is missing the "
                          "offline copy link")
        # The five guides are embedded, so each anchor appears once and
        # the guide pages are no longer linked from the hub.
        for anchor in ('doc-admin', 'doc-management', 'doc-till',
                       'doc-till-procedures', 'doc-till-features'):
            if hub_text.count(f'id="{anchor}"') != 1:
                errors.append(
                    "migena/documentation.html must embed "
                    f"{anchor} exactly once")
        for gone in ('href="admin.html"', 'href="management.html"',
                     'href="till.html"', 'portal-buttons'):
            if gone in hub_text:
                errors.append(f"migena/documentation.html still contains "
                              f"the old guide link or button {gone}")
        ids: List[str] = []
        counter = IdCollector(ids)
        counter.feed(hub_text)
        repeated = sorted({i for i in ids if ids.count(i) > 1})
        if repeated:
            errors.append(
                "migena/documentation.html repeats these ids: "
                + ", ".join(repeated))
        if 'id="auth-gate"' not in hub_text:
            errors.append("migena/documentation.html has no password gate")

    # 5. The offline copy must be whole: passwords page plus search.
    offline = REPO_ROOT / "migena" / "offline.html"
    if offline.is_file():
        text = offline.read_text(encoding="utf-8")
        if 'id="puserpasswords"' not in text:
            errors.append("migena/offline.html has no User Passwords page")
        if 'id="doc-search-input"' not in text:
            errors.append("migena/offline.html has no search box")
    return errors


def main() -> int:
    """
    Execute all verification routines and return process exit status.

    Returns:
        0 if all verification checks pass cleanly, or 1 if any check fails.
    """
    all_errors: List[str] = []

    # Step 1: Check required file presence.
    all_errors.extend(check_required_files())

    # Step 2: Check sitemap URL indexing.
    all_errors.extend(check_sitemap_urls())

    # Step 3: Check robots.txt directives.
    all_errors.extend(check_robots_txt())

    # Step 4: Check llms.txt and llms-full.txt content and service links.
    all_errors.extend(check_llms_txt())

    # Step 5: Check home page HTML canonical, Open Graph, and JSON-LD FAQ data.
    all_errors.extend(check_html_and_jsonld())

    # Step 6: Check all 41 service pages for SEO, JSON-LD, and static headers.
    all_errors.extend(check_service_pages())

    # Step 7: Check 80-column line length restrictions.
    all_errors.extend(check_line_lengths())

    # Step 8: Check the smart service search index and wiring.
    all_errors.extend(check_search_index())

    # Step 9: Check synonym coverage for every service (findability rule).
    all_errors.extend(check_synonym_coverage())

    # Step 10: Check the Migena portal pages, search and offline copy.
    all_errors.extend(check_migena_portal())

    # Report results.
    if all_errors:
        print("VERIFICATION FAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print(
        "ALL VERIFICATION CHECKS PASSED (files, sitemap, robots, llms, "
        f"home HTML/JSON-LD, {EXPECTED_SERVICE_COUNT} service pages, 80-col)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
