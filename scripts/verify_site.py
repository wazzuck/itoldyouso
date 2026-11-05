#!/usr/bin/env python3
"""
==============================================================================
FILE: scripts/verify_site.py
==============================================================================

PURPOSE:
Automated quality, discoverability, search engine, and policy verification
script for the IToldYouSo Computing website (itoldyouso.tech).

WHAT THIS FILE IS NOT FOR:
- Does not modify or format source files in place.
- Does not require external third-party Python packages outside the standard
  library.

INVARIANTS:
1. Exits with status code 0 only when all structural, search engine, Artificial
   Intelligence (AI) crawler, and 80-column documentation checks pass.
2. Exits with status code 1 and prints a diagnostic report if any check fails.
==============================================================================
"""

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import List, Set, Tuple
import xml.etree.ElementTree as ET

# Maximum line width allowed for Markdown documentation and code comments per
# AGENTS.md Section 4, Policy 6.
# Value: 80 characters. Consumed by: check_line_lengths().
MAX_DOC_COLUMNS = 80

# Root directory of the repository checkout.
# Consumed by: main() and all verification helper routines.
REPO_ROOT = Path(__file__).resolve().parent.parent

# Canonical base Uniform Resource Locator (URL) for production hosting.
BASE_URL = "https://itoldyouso.tech"


class SiteHTMLValidator(HTMLParser):
    """
    Lightweight HTML parser that records element identifiers and meta tags in
    index.html.

    Attributes:
        element_ids (Set[str]): Set of all id="..." values encountered.
        meta_tags (List[dict]): List of attribute dictionaries for meta tags.
        canonical_href (str | None): Target href of canonical link tag.
    """

    def __init__(self) -> None:
        """Initialise the HTML validator state."""
        super().__init__()
        self.element_ids: Set[str] = set()
        self.meta_tags: List[dict] = []
        self.canonical_href: str | None = None

    def handle_starttag(
        self, tag: str, attrs: List[Tuple[str, str | None]]
    ) -> None:
        """
        Inspect opening HTML tag and record ids, links, and meta attributes.

        Args:
            tag: Lowercase HTML tag name.
            attrs: List of (attribute_name, attribute_value) tuples.
        """
        attr_map = {k.lower(): v for k, v in attrs if v is not None}
        el_id = attr_map.get("id")
        if el_id:
            self.element_ids.add(el_id)

        if tag.lower() == "link" and attr_map.get("rel") == "canonical":
            self.canonical_href = attr_map.get("href")

        if tag.lower() == "meta":
            self.meta_tags.append(attr_map)


def _plain_text(markup: str) -> str:
    """
    Reduce HTML or JSON text to comparable plain text by stripping tags,
    decoding entities, and normalising whitespace.

    Args:
        markup: Raw text that may contain HTML entities and markup tags.

    Returns:
        The text with tags removed, entities decoded, and whitespace sequences
        collapsed into single spaces.
    """
    # 1. Strip all markup tags.
    no_tags = re.sub(r"<[^>]+>", " ", markup)
    # 2. Decode HTML entities and collapse multiple whitespace runs.
    return re.sub(r"\s+", " ", html.unescape(no_tags)).strip()


def check_required_files() -> List[str]:
    """
    Verify that all required core files and all 32 service pages exist and are
    non-empty.

    Returns:
        List of error diagnostic messages (empty if all files exist).
    """
    errors: List[str] = []

    # 1. Verify primary root files.
    core_files = [
        "index.html",
        "header.css",
        "header.js",
        "header-loader.js",
        "header-template.html",
        "CNAME",
        "README.md",
        "AGENTS.md",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
    ]

    for rel_path in core_files:
        full_path = REPO_ROOT / rel_path
        if not full_path.is_file():
            errors.append(f"Missing required file: {rel_path}")
        elif full_path.stat().st_size == 0:
            errors.append(f"Required file is empty: {rel_path}")

    # 2. Verify all service HTML pages.
    services_dir = REPO_ROOT / "services"
    if not services_dir.is_dir():
        errors.append("Services directory missing: services/")
    else:
        service_htmls = list(services_dir.glob("*.html"))
        if len(service_htmls) != 32:
            errors.append(
                f"Expected exactly 32 service HTML files, "
                f"found {len(service_htmls)}"
            )
        for sfile in service_htmls:
            if sfile.stat().st_size == 0:
                errors.append(f"Service file is empty: {sfile.name}")

    return errors


def check_sitemap_urls() -> List[str]:
    """
    Validate sitemap.xml format and ensure it indexes the home page and all
    32 service pages.

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

    # 4. Check all 32 service pages presence.
    services_dir = REPO_ROOT / "services"
    if services_dir.is_dir():
        for sfile in services_dir.glob("*.html"):
            expected_url = f"{BASE_URL}/services/{sfile.name}"
            if expected_url not in urls:
                errors.append(
                    f"sitemap.xml missing service page: {expected_url}"
                )

    # 5. Confirm total indexed URL count matches 33 (1 home + 32 services).
    if len(urls) != 33:
        errors.append(
            f"sitemap.xml expected 33 URLs (home + 32 services), "
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

    # 3. Verify user-agent wildcard directive.
    if "User-agent: *" not in content:
        errors.append("robots.txt missing 'User-agent: *' directive")

    return errors


def check_llms_txt() -> List[str]:
    """
    Verify that llms.txt provides a high-signal Markdown summary including
    coverage areas, telephone, email, sister practice, and all service links.

    Returns:
        List of error diagnostic messages (empty if valid).
    """
    errors: List[str] = []
    llms_path = REPO_ROOT / "llms.txt"
    if not llms_path.is_file():
        return ["llms.txt not found"]

    content = llms_path.read_text(encoding="utf-8")

    # 1. Verify mandatory contact and location phrases.
    required_phrases = [
        "IToldYouSo Computing",
        "020 4520 9114",
        "contactus@itoldyouso.tech",
        "Hampstead",
        "Highgate",
        "Golders Green",
        "Belsize Park",
        "Heath & City Technology",
        "https://heathandcity.com/",
    ]
    for phrase in required_phrases:
        if phrase not in content:
            errors.append(f"llms.txt missing required phrase: '{phrase}'")

    # 2. Verify all 32 service HTML pages are linked in llms.txt.
    services_dir = REPO_ROOT / "services"
    if services_dir.is_dir():
        for sfile in services_dir.glob("*.html"):
            expected_link = f"{BASE_URL}/services/{sfile.name}"
            if expected_link not in content:
                errors.append(
                    f"llms.txt missing link to service page: {expected_link}"
                )

    return errors


def check_html_and_jsonld() -> List[str]:
    """
    Verify canonical links, Open Graph metadata, Twitter Card tags, and
    Schema.org JSON-LD structured data in index.html.

    Returns:
        List of error diagnostic messages (empty if valid).
    """
    errors: List[str] = []
    index_path = REPO_ROOT / "index.html"
    if not index_path.is_file():
        return ["index.html not found"]

    raw_html = index_path.read_text(encoding="utf-8")
    page_text = _plain_text(raw_html)

    # 1. Parse HTML structure.
    validator = SiteHTMLValidator()
    validator.feed(raw_html)

    # 2. Check canonical link.
    if validator.canonical_href != f"{BASE_URL}/":
        errors.append(
            f"index.html canonical link invalid: '{validator.canonical_href}'"
        )

    # 3. Check Open Graph and Twitter Card meta tags.
    meta_props = {
        m.get("property"): m.get("content") for m in validator.meta_tags
    }
    meta_names = {
        m.get("name"): m.get("content") for m in validator.meta_tags
    }

    required_og = [
        "og:title",
        "og:description",
        "og:url",
        "og:type",
        "og:image",
    ]
    for og_prop in required_og:
        if not meta_props.get(og_prop):
            errors.append(f"index.html missing Open Graph tag: '{og_prop}'")

    required_tw = [
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
    ]
    for tw_name in required_tw:
        if not meta_names.get(tw_name):
            errors.append(f"index.html missing Twitter Card tag: '{tw_name}'")

    # 4. Check presence of #faq section element id.
    if "faq" not in validator.element_ids:
        errors.append(
            "index.html missing required FAQ section element id='faq'"
        )

    # 5. Parse and validate Schema.org JSON-LD structured data.
    jsonld_blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', raw_html, re.S
    )
    if len(jsonld_blocks) != 1:
        return errors + [
            f"Expected 1 JSON-LD block in index.html, "
            f"found {len(jsonld_blocks)}"
        ]

    try:
        data = json.loads(jsonld_blocks[0])
    except json.JSONDecodeError as exc:
        return errors + [f"JSON-LD in index.html is invalid JSON: {exc}"]

    graph = data.get("@graph", [])
    if not graph:
        errors.append("JSON-LD in index.html is missing '@graph' list")

    types_present: Set[str] = set()
    faq_entity_count = 0

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
                        "FAQPage Question missing 'name' or "
                        "'acceptedAnswer.text'"
                    )
                # Verify verbatim existence in the visible page text.
                if q_name not in page_text:
                    errors.append(
                        f"FAQ Question not in HTML: '{q_name[:40]}...'"
                    )
                if ans_text not in page_text:
                    errors.append(
                        f"FAQ Answer not in HTML: '{ans_text[:40]}...'"
                    )

    if not ("ITService" in types_present or "LocalBusiness" in types_present):
        errors.append(
            "JSON-LD missing 'ITService' or 'LocalBusiness' in @graph"
        )
    if "FAQPage" not in types_present:
        errors.append("JSON-LD missing 'FAQPage' definition in @graph")
    if faq_entity_count < 4:
        errors.append(
            f"Expected at least 4 FAQ entries, found {faq_entity_count}"
        )

    return errors


def check_line_lengths() -> List[str]:
    """
    Verify that Markdown documentation files and code comments wrap at or
    below MAX_DOC_COLUMNS (80 characters), exempting standalone URLs.

    Returns:
        List of error diagnostic messages (empty if all lines comply).
    """
    errors: List[str] = []

    # 1. Check Markdown documentation files in repository.
    md_files = ["README.md", "llms.txt"]
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

    # 2. Check code comments in Python script.
    code_files = ["scripts/verify_site.py"]
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

    # Step 4: Check llms.txt content and service links.
    all_errors.extend(check_llms_txt())

    # Step 5: Check HTML canonical, Open Graph, and JSON-LD FAQ data.
    all_errors.extend(check_html_and_jsonld())

    # Step 6: Check 80-column line length restrictions.
    all_errors.extend(check_line_lengths())

    # Report results.
    if all_errors:
        print("VERIFICATION FAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("ALL VERIFICATION CHECKS PASSED (files, sitemap, robots, llms, "
          "HTML, JSON-LD, 80-col).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
