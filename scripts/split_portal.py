#!/usr/bin/env python3
"""Build the standalone Migena portal pages from migena/index.html.

The portal originally held every document behind one password curtain.
Management Guide (management.html) and Till Procedures & Features
(till.html) live as standalone pages rather than inside index.html, and
the three documents that used to be hidden in the background DOM
(Technical Intake Questionnaire, Cafe Client Handbook, Countertop Cheat
Sheet) have been removed entirely at the client's request. This script
builds the standalone pages for the documents that remain in index.html,
plus the Documentation hub that the main page's Documentation link opens.

What the script does:

1. Copies the shared stylesheet out of index.html into portal.css.
2. Writes one HTML file per remaining document in index.html, each
   holding its own article and the portal's own script, so the terms
   form and the password curtain keep working exactly as they did.
   Every document page also receives the documentation search box, the
   link to its stylesheet (doc-search.css) and the two search scripts,
   so all seven official document pages share one search.
3. Rewrites links that pointed at a section of the portal so they point
   at the standalone page instead.
4. Writes documentation.html, the Documentation hub. It is password
   gated like every other page and lists the guides. It has no search
   box, because it is a list of documents rather than a document.

Run:
    python3 scripts/split_portal.py          # regenerate
    python3 scripts/split_portal.py --check  # exit 1 if stale
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent / "migena"
SOURCE = ROOT / "index.html"

# Document id in the portal, output file, page title.
# management.html and till.html are maintained as standalone pages, and
# till-procedures.html / till-features.html are hand-maintained printable
# sheets, so none of those four are produced here.
DOCS = [
    ("trainer", "contract.html",
     "Service Contract &amp; Scope of Work"),
    ("hb-pricing", "pricing.html", "Pricing &amp; Commercial Terms"),
    ("doc-admin", "admin.html", "Administration Guide"),
]

# The Documentation hub: the page the main page's Documentation link
# opens. Its file name is also checked by scripts/verify_site.py.
HUB_FILE = "documentation.html"
HUB_TITLE = "Documentation"

# Links inside a document that pointed at a section of the portal.
# The questionnaire, handbook and cheat-sheet entries are gone with the
# documents they pointed at.
ANCHOR_LINKS = {
    "href=\"#doc-admin\"": "href=\"admin.html\"",
    "href=\"#doc-management\"": "href=\"management.html\"",
    "href=\"#doc-operations\"": "href=\"till.html\"",
    "href=\"#doc-till\"": "href=\"till.html\"",
    "href=\"#trainer\"": "href=\"contract.html\"",
    "href=\"#hb-pricing\"": "href=\"pricing.html\"",
}

# The documentation search box, placed in the sticky bar of each of the
# seven document pages. Its ids must match migena/doc-search.js.
SEARCH_FORM = """        <form class="doc-search" role="search"
              aria-label="Search the documentation"
              onsubmit="return false;">
          <label class="doc-search-label" for="doc-search-input">
            Search the documentation
          </label>
          <input type="search" id="doc-search-input"
                 class="doc-search-input" autocomplete="off"
                 spellcheck="false" enterkeyhint="search"
                 placeholder="e.g. refunds, PIN, closing up">
          <p id="doc-search-status" class="doc-search-status"
             role="status" aria-live="polite"></p>
          <ul id="doc-search-results" class="doc-search-results"
              hidden></ul>
        </form>
"""

# The two search scripts, loaded after the portal script. The index
# comes first so the query tower finds its data when it runs.
SEARCH_SCRIPTS = """  <script src="search-index.js" defer></script>
  <script src="doc-search.js" defer></script>
"""


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


def hub_body() -> str:
    """Return the main content of the Documentation hub.

    Returns:
        One article holding a list of the guides. Each entry is a link
        and one plain sentence saying what the guide covers, so the
        owner can choose without opening each guide first.
    """
    return """      <article class="doc-article">
        <div class="article-header">
          <span class="article-badge badge-spec">Documentation</span>
          <h2>Choose a guide</h2>
          <p class="article-lead">Tap a guide to open it. The owner tasks
            are on the main page.</p>
        </div>
        <ul class="hub-links">
          <li>
            <a href="admin.html">Admin Guide</a>
            <p>Adding and removing staff, changing what they can do, and
              their Personal Identification Numbers (PINs).</p>
          </li>
          <li>
            <a href="management.html">Management Guide</a>
            <p>The accounts behind the till, who holds each one, and the
              daily, weekly and monthly routines.</p>
          </li>
          <li>
            <a href="till.html">Till Procedures &amp; Features</a>
            <p>How to do each till task, step by step, and what each
              feature of the till does.</p>
          </li>
          <li>
            <a href="offline.html"
               download="EGGIs-Till-Documentation.html">Download the offline
              copy</a>
            <p>All the guides and the User Passwords page in one file, for
              your phone. It opens with no connection.</p>
          </li>
        </ul>
      </article>"""


def shell(title: str, body: str, back_label: str, search: bool,
          gate: str, footer: str, script: str) -> str:
    """Wrap one page's body in the frame every portal page shares.

    Args:
        title: page title, used in the browser tab and as the subtitle.
        body: the page's own main content, already indented.
        back_label: text of the link back to the main page, with its
            HTML entity, for example "&larr; All documents".
        search: True to add the documentation search box with its
            stylesheet and scripts; False for the hub, which is a list.
        gate: the password gate markup copied from index.html.
        footer: the site footer copied from index.html.
        script: the portal's own script, copied from index.html.

    Returns:
        The complete HTML document as one string.
    """
    head_search = ('  <link rel="stylesheet" href="doc-search.css">\n'
                   if search else "")
    nav_search = SEARCH_FORM if search else ""
    tail_scripts = SEARCH_SCRIPTS if search else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>{title} | EGGI'S Till Documentation | IToldYouSo Computing</title>
  <link rel="stylesheet" href="portal.css">
{head_search}</head>
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
          <li><a href="index.html">{back_label}</a></li>
        </ul>
{nav_search}      </div>
    </nav>

    <main class="doc-main">
{body}
    </main>

{footer}
  </div>
{script}
{tail_scripts}</body>
</html>
"""


def build() -> dict:
    """Build portal.css and every standalone page in memory.

    Returns:
        Mapping of file name (relative to migena/) to the full file
        text. Nothing is written here, so --check can compare against
        what is on disk before anything is overwritten.
    """
    src = SOURCE.read_text(encoding="utf-8")

    # 1. Shared stylesheet, taken straight out of index.html.
    css = extract(src, "  <style>", "  </style>")
    css = css[len("  <style>"): -len("  </style>")]
    out = {
        "portal.css": (
            "/* Generated from index.html by scripts/split_portal.py.\n"
            "   Edit index.html or the script, not this file. */\n" + css
        ),
    }

    # 2. The portal's own script, reused as-is. It handles the password
    #    curtain and the terms form, and each of its functions returns
    #    quietly when the element is not on the page, so one copy
    #    serves every page.
    scripts = re.findall(r'  <script>\n(.*?)\n  </script>', src, flags=re.S)
    script = "\n".join("  <script>\n" + s + "\n  </script>" for s in scripts)

    # 3. The password gate and the footer, shared by every page.
    gate = extract(src, "  <div id=\"auth-gate\">",
                   "      </form>\n    </div>\n  </div>")
    footer = extract(src, "    <footer class=\"site-footer\">",
                     "    </footer>")

    # 4. One page per document.
    for doc_id, name, title in DOCS:
        start = src.index(f'<article id="{doc_id}"')
        start = src.rindex("      <", 0, start)
        end = src.index("</article>", start) + len("</article>")
        body = src[start:end]
        for old, new in ANCHOR_LINKS.items():
            body = body.replace(old, new)
        body = re.sub(r'\n\s*<!-- =+\n\s+DOCUMENT \d+:.*?=+ -->\n',
                      '\n', body, flags=re.S)
        out[name] = shell(title, body, "&larr; All documents", True,
                          gate, footer, script)

    # 5. The Documentation hub, reached from the main page.
    out[HUB_FILE] = shell(HUB_TITLE, hub_body(), "&larr; Main page",
                          False, gate, footer, script)
    return out


def main(argv: list) -> int:
    """Entry point: regenerate every page, or with --check compare."""
    files = build()
    if "--check" in argv:
        stale = [
            name for name, text in files.items()
            if not (ROOT / name).is_file()
            or (ROOT / name).read_text(encoding="utf-8") != text
        ]
        if stale:
            print("split_portal.py outputs are stale: "
                  + ", ".join(sorted(stale)))
            return 1
        return 0
    for name, text in files.items():
        (ROOT / name).write_text(text, encoding="utf-8")
    print(f"portal.css and {len(files) - 1} pages written to {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
