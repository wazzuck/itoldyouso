#!/usr/bin/env python3
"""Split the remaining Migena portal documents into standalone pages.

The portal originally held every document behind one password curtain.
Management Guide (management.html) and Till Procedures & Features
(till.html) now live as standalone pages rather than inside index.html,
and Operations Cards has been removed. This script builds standalone
pages for the documents that remain in index.html.

What the script does:

1. Copies the shared stylesheet out of index.html into portal.css.
   The rules that hid three documents are dropped, because each is now
   its own page and has to render.
2. Writes one HTML file per remaining document in index.html, each
   holding its own article and the portal's own script, so the terms
   form, the questionnaire and the password curtain keep working
   exactly as they did.
3. Rewrites links that pointed at a section of the portal so they point
   at the standalone page instead.

Run: python3 scripts/split_portal.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent / "migena"
SOURCE = ROOT / "index.html"

# Document id in the portal, output file, page title.
# management.html and till.html are maintained as standalone pages.
DOCS = [
    ("trainer", "contract.html",
     "Service Contract &amp; Scope of Work"),
    ("hb-pricing", "pricing.html", "Pricing &amp; Commercial Terms"),
    ("questionnaire", "questionnaire.html",
     "Initial Intake Questionnaire"),
    ("handbook", "handbook.html", "Cafe Client Handbook"),
    ("cheatsheet", "cheat-sheet.html", "Countertop Cheat Sheet"),
    ("doc-admin", "admin.html", "Administration Guide"),
]

# Links inside a document that pointed at a section of the portal.
ANCHOR_LINKS = {
    "href=\"#doc-admin\"": "href=\"admin.html\"",
    "href=\"#doc-management\"": "href=\"management.html\"",
    "href=\"#doc-operations\"": "href=\"till.html\"",
    "href=\"#doc-till\"": "href=\"till.html\"",
    "href=\"#trainer\"": "href=\"contract.html\"",
    "href=\"#hb-pricing\"": "href=\"pricing.html\"",
    "href=\"#handbook\"": "href=\"handbook.html\"",
    "href=\"#cheatsheet\"": "href=\"cheat-sheet.html\"",
    "href=\"#questionnaire\"": "href=\"questionnaire.html\"",
}

GATE = '  <div id="auth-gate">'


def extract(src: str, start_marker: str, end_marker: str) -> str:
    """Return the text between two markers, markers included.

    start_marker and end_marker must each occur exactly once, so a
    mismatch fails loudly instead of writing half a page.
    """
    assert src.count(start_marker) == 1, start_marker
    assert src.count(end_marker) == 1, end_marker
    a = src.index(start_marker)
    b = src.index(end_marker) + len(end_marker)
    return src[a:b]


def main() -> None:
    src = SOURCE.read_text(encoding="utf-8")

    # 1. Shared stylesheet.
    css = extract(src, "  <style>", "  </style>")
    css = css[len("  <style>"): -len("  </style>")]
    # The portal hid three documents. Each is now its own page, so those
    # rules are dropped.
    css = re.sub(r"\n    /\* Hide completed intake questionnaire.*?\n    \}\n",
                 "\n", css, flags=re.S)
    (ROOT / "portal.css").write_text(
        "/* Generated from index.html by scripts/split_portal.py.\n"
        "   Edit index.html or the script, not this file. */\n" + css,
        encoding="utf-8")

    # 2. The portal's own script, reused as-is. It handles the password
    #    curtain, the questionnaire save and the terms form, and each of
    #    its functions returns quietly when the element is not on the
    #    page, so one copy serves every page.
    scripts = re.findall(r'  <script>\n(.*?)\n  </script>', src, flags=re.S)
    script = "\n".join("  <script>\n" + s + "\n  </script>" for s in scripts)

    # 3. One page per document.
    gate = extract(src, "  <div id=\"auth-gate\">",
                   "      </form>\n    </div>\n  </div>")
    footer = extract(src, "    <footer class=\"site-footer\">",
                     "    </footer>")
    for doc_id, name, title in DOCS:
        start = src.index(f'<article id="{doc_id}"')
        start = src.rindex("      <", 0, start)
        end = src.index("</article>", start) + len("</article>")
        body = src[start:end]
        # Each page shows its own document, so the portal's hiding rule
        # is removed from the markup too.
        body = body.replace(' style="display: none;" aria-hidden="true"', '')
        for old, new in ANCHOR_LINKS.items():
            body = body.replace(old, new)
        body = re.sub(r'\n\s*<!-- =+\n\s+DOCUMENT \d+:.*?=+ -->\n',
                      '\n', body, flags=re.S)

        page = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>{title} | EGGI'S Till Documentation | IToldYouSo Computing</title>
  <link rel="stylesheet" href="portal.css">
</head>
<body>
{gate}

  <div id="document-content">
    <header class="site-header">
      <div class="header-top">
        <div class="header-titles">
          <h1>EGGI'S &mdash; Till Documentation</h1>
          <div class="subtitle">{title}</div>
        </div>
      </div>
    </header>

    <nav class="doc-nav" aria-label="Document Navigation">
      <div class="nav-container">
        <ul class="nav-links">
          <li><a href="index.html">&larr; All documents</a></li>
        </ul>
      </div>
    </nav>

    <main class="doc-main">
{body}
    </main>

{footer}
  </div>
{script}
</body>
</html>
"""
        (ROOT / name).write_text(page, encoding="utf-8")

    print(f"portal.css and {len(DOCS)} pages written to {ROOT}")


if __name__ == "__main__":
    main()
