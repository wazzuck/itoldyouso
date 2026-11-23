#!/usr/bin/env python3
"""
FILE: scripts/build_offline_doc.py

Purpose:
    Generates migena/offline.html: one self-contained copy of the
    Migena client documentation for a phone with no connection. It
    holds all seven official documents, the documentation search (box,
    styles, query tower and document tower all inlined) and the User
    Passwords page built from migena/sumup_password.txt.

    The client downloads it once from the portal and keeps it in the
    phone's Files app; every link inside jumps to a section of the
    same file, so it never needs the network again.

Deliberately NOT for:
    Hand-editing migena/offline.html (it is generated: change this
    script or the sources, then regenerate), and not for the online
    pages, which are produced by scripts/split_portal.py.

Invariants relied upon:
    1. Every id inside a copied document is prefixed with its page
       stem (padmin, ptill-procedures, ...) and every link is
       rewritten to match, so the anchors in the inlined search index
       resolve inside this one file.
    2. The interactive terms-acceptance form is stripped: it needs
       the portal script and a live mailbox, and a button that does
       nothing on a phone would be a defect. The terms themselves
       remain as plain text.
    3. The search maths comes from scripts/build_search_index.py, so
       the offline copy and the online portal rank results the same
       way.

Usage:
    python3 scripts/build_offline_doc.py          # regenerate
    python3 scripts/build_offline_doc.py --check  # exit 1 if stale
"""
import html
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Make the sibling generator importable when this file is run directly
# (python3 scripts/build_offline_doc.py puts scripts/ on sys.path).
from build_search_index import (  # noqa: E402
    MIGENA_DIR,
    MIGENA_PAGES,
    TITLE_REPEAT,
    build_payload,
    concept_stems,
    documentation_lexicon,
    portal_main,
    read_migena_docs,
    render,
    sheet_body,
)

# The single generated file, and the credentials file it embeds.
# Both live inside migena/ so a copied portal folder stays complete.
OFFLINE_OUTPUT = MIGENA_DIR / "offline.html"
CREDENTIALS_FILE = MIGENA_DIR / "sumup_password.txt"

# Page file to id prefix. Value: "p" plus the file stem, for example
# admin.html -> padmin. Consumed by rewrite_content() and by the
# search-index href rewrite in build(); every document in the offline
# copy and every result link uses the same prefixes.
PAGE_STEMS: Dict[str, str] = {
    filename: "p" + filename[:-5] for filename, _ in MIGENA_PAGES
}

# Anchor used by rewritten links that pointed at index.html or at
# this file itself. Value: the id of the offline page header, which
# always sits at the top of the document.
TOP_ANCHOR = "offline-top"

# Anchor of the passwords article, the target of every link that
# pointed at offline.html (the Admin Guide's note links here).
PASSWORDS_ANCHOR = "puserpasswords"


def rewrite_content(content: str, stem: str) -> str:
    """Prefix ids and repoint links inside one copied document.

    Args:
        content: the document's HTML with tags intact.
        stem: this document's id prefix, for example padmin.

    Returns:
        The same HTML with every id="X" turned into id="stem-X",
        every in-page href="#X" turned into href="#stem-X", links to
        other portal pages turned into links to their offline
        anchors, and links to index.html or offline.html turned into
        the header or the passwords article.
    """
    # Step 1: prefix this document's own ids so sections from seven
    # documents can coexist in one file without colliding.
    content = re.sub(r'id="([^"]+)"', f'id="{stem}-\\1"', content)

    # Step 2: in-page anchors now point at the prefixed ids.
    content = re.sub(r'href="#([^"]+)"', f'href="#{stem}-\\1"', content)

    # Step 3: links to sibling pages become in-file jumps.
    def page_link(match: "re.Match[str]") -> str:
        target = match.group(1)
        if target in ("index.html", "offline.html"):
            return (f'href="#{TOP_ANCHOR}"' if target == "index.html"
                    else f'href="#{PASSWORDS_ANCHOR}"')
        page, _, anchor = target.partition("#")
        page_stem = PAGE_STEMS.get(page)
        if page_stem is None:
            return match.group(0)
        if anchor:
            return f'href="#{page_stem}-{anchor}"'
        return f'href="#{page_stem}"'

    return re.sub(r'href="([^"]+\.html(?:#[^"]*)?)"', page_link, content)


def extract_document(filename: str) -> str:
    """Read one portal page or sheet and return its offline body.

    Args:
        filename: a file listed in MIGENA_PAGES.

    Returns:
        The document's content with the article wrapper removed (the
        offline copy supplies its own card), the interactive terms
        form stripped, and ids and links rewritten for in-file use.

    Raises:
        FileNotFoundError: if the page has not been generated yet.
        ValueError: if a portal page has no main area.
    """
    page_html = (MIGENA_DIR / filename).read_text(encoding="utf-8")
    if '<main class="doc-main">' in page_html:
        content = portal_main(page_html)
        # Step 1a: the standalone pages open <main> with the source's
        # banner comment ("DOCUMENT 1: ..."), which would otherwise
        # sit above the card. Strip every leading comment.
        while True:
            stripped = re.sub(r"^\s*<!--.*?-->\s*", "", content,
                              count=1, flags=re.S)
            if stripped == content:
                break
            content = stripped
        # Step 1b: drop the wrapping <article> tag; the offline copy
        # puts every document in its own styled article card, and a
        # card inside a card would double the padding and read badly
        # on a phone.
        content = re.sub(r"^\s*<article\b[^>]*>", "", content, count=1)
        content = re.sub(r"</article>\s*$", "", content)
        if "<article" in content or "</article>" in content:
            raise ValueError(
                f"{filename}: unexpected nested article after stripping"
            )
    else:
        content = sheet_body(page_html)

    # Step 2: the terms form only works in the live portal (it saves
    # to the browser and opens a mailbox), so the offline copy keeps
    # the terms as text and drops the controls. The hidden
    # confirmation box is left in place: it is display:none, so it
    # never shows without the portal script.
    content = re.sub(r'<form id="terms-form".*?</form>', "",
                     content, flags=re.S)

    # Step 3: make every anchor work inside this single file.
    return rewrite_content(content, PAGE_STEMS[filename])


def read_password_rows() -> List[Tuple[str, str]]:
    """Read the credentials file into table rows.

    The file alternates an account line (an e-mail address) with a
    line holding that account's login details, separated by blank
    lines. Each pair is kept verbatim: nothing is reworded, split or
    interpreted, so what the engineer wrote is what the client reads.

    Returns:
        Pairs of (account, login details).

    Raises:
        FileNotFoundError: if migena/sumup_password.txt is missing.
    """
    rows: List[Tuple[str, str]] = []
    account = ""
    for line in CREDENTIALS_FILE.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        if not account:
            account = text
        else:
            rows.append((account, text))
            account = ""
    if account:
        # A trailing account with no details line still deserves to be
        # shown rather than silently dropped.
        rows.append((account, ""))
    return rows


def build() -> str:
    """Build the full text of migena/offline.html.

    Returns:
        The complete offline document as one HTML string: styles,
        header, contents list, the seven documents, the passwords
        page, the footer and the inlined search pair.
    """
    # Step 1: shared styles. portal.css carries the portal look and
    # doc-search.css the search box; both are read from disk so the
    # offline copy cannot drift from the online pages.
    portal_css = (MIGENA_DIR / "portal.css").read_text(encoding="utf-8")
    search_css = (MIGENA_DIR / "doc-search.css").read_text(encoding="utf-8")

    # Step 2: the query tower, inlined verbatim.
    search_js = (MIGENA_DIR / "doc-search.js").read_text(encoding="utf-8")

    # Step 3: the document tower, rebuilt from the same corpus with
    # every href rewritten to an in-file anchor, so a result tap
    # scrolls within this file instead of trying to open a page that
    # is not on the phone.
    records = read_migena_docs()
    for record in records:
        page, _, anchor = str(record["href"]).partition("#")
        page_stem = PAGE_STEMS[page]
        record["href"] = (f"#{page_stem}-{anchor}" if anchor
                          else f"#{page_stem}")
    index_js = render(
        build_payload(records, concept_stems(documentation_lexicon()),
                      TITLE_REPEAT),
        "MIGENA_SEARCH_INDEX",
    )
    index_js = index_js.replace(
        "/* GENERATED by scripts/build_search_index.py. Do not edit. */",
        "/* GENERATED index (scripts/build_search_index.py), inlined by\n"
        "   scripts/build_offline_doc.py. Do not edit. */",
        1,
    )

    # Step 4: the footer is copied from a portal page so the contact
    # details can never disagree with the online pages.
    any_page = (MIGENA_DIR / "contract.html").read_text(encoding="utf-8")
    footer_match = re.search(r'<footer class="site-footer">.*?</footer>',
                             any_page, re.S)
    if not footer_match:
        raise ValueError("portal page has no site footer to copy")
    footer = footer_match.group(0)

    # Step 5: one styled article per document, in portal order.
    documents = []
    toc = []
    for filename, display in MIGENA_PAGES:
        stem = PAGE_STEMS[filename]
        documents.append(
            f'      <article class="doc-article" id="{stem}">\n'
            f'        <p class="offline-doc-label">{html.escape(display)}'
            f"</p>\n"
            f"{extract_document(filename)}\n"
            f"      </article>"
        )
        toc.append(
            f'        <li><a href="#{stem}">{html.escape(display)}</a></li>'
        )

    # Step 6: the passwords page, built from the credentials file.
    rows = read_password_rows()
    password_rows = "\n".join(
        f"            <tr><td>{html.escape(account)}</td>"
        f"<td>{html.escape(details)}</td></tr>"
        for account, details in rows
    )
    documents.append(f"""      <article class="doc-article" id="{PASSWORDS_ANCHOR}">
        <p class="offline-doc-label">User Passwords</p>
        <div class="article-header">
          <span class="article-badge badge-management">Keep Private
          &mdash; Owner and Manager Only</span>
          <h2>User Names and Passwords</h2>
          <p class="article-lead">
            Every account the till depends on, in one place. This is
            the separate page the Admin Guide points to; nothing here
            is written into any other document.
          </p>
        </div>
        <div class="callout warning">
          <h4>Keep This File Private</h4>
          <p>
            Anyone who reads this page can sign in as you. Do not
            forward the file, post it in a group chat, or leave it
            open on a shared screen. If a login ever leaks, change it
            at once in the SumUp dashboard at
            <strong>sumup.me</strong>.
          </p>
        </div>
        <table>
          <thead>
            <tr><th>Account</th><th>Login details</th></tr>
          </thead>
          <tbody>
{password_rows}
          </tbody>
        </table>
      </article>""")
    toc.append(
        f'        <li><a href="#{PASSWORDS_ANCHOR}">User Passwords'
        f"</a></li>"
    )

    # Step 7: assemble the page. Everything is inlined, so the file
    # works from the phone's Files app with no connection and no
    # sibling files.
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>EGGI'S Till Documentation (Offline Copy) | IToldYouSo
 Computing</title>
  <style>
{portal_css}

{search_css}

    /* Offline-copy-only rules: the kicker above each document and
       the contents list. Everything else comes from portal.css. */
    .offline-doc-label {{
      margin: 0 0 10px 0;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #0f766e;
    }}
    .offline-toc ol {{
      margin: 8px 0 0;
      padding-left: 22px;
    }}
    .offline-toc li {{
      margin: 4px 0;
    }}
    .offline-note {{
      margin-top: 14px;
      font-size: 0.88rem;
      color: #6b7280;
    }}

    /* Phone layout. The breakpoint matches doc-search.css (760px) so
       the search box and these rules switch together. The staff,
       pricing and password tables scroll sideways instead of
       stretching the page; long account e-mails and addresses break
       mid-word rather than push it wider; and the contents list gets
       full-height tap targets, because a link a thumb cannot hit is a
       link that does not exist on a phone. Desktop keeps the normal
       in-flow tables from portal.css. */
    @media (max-width: 760px) {{
      .doc-main table {{
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
      }}
      .doc-main th,
      .doc-main td {{
        overflow-wrap: anywhere;
      }}
      .offline-toc li a {{
        display: block;
        padding: 10px 0;
        font-size: 1rem;
      }}
    }}
  </style>
</head>
<body>
  <header class="site-header" id="{TOP_ANCHOR}">
    <div class="header-top">
      <div class="header-titles">
        <h1>EGGI'S &mdash; Till Documentation (Offline Copy)</h1>
        <div class="subtitle">All seven guides, the documentation
        search and the User Passwords page in one file &bull; opens
        with no connection</div>
      </div>
    </div>
    <div class="header-meta">
      <div class="meta-item">Client: <strong>Migena Lika &amp; Egzon
        Quilia</strong></div>
      <div class="meta-item">Engineer &amp; Trainer:
        <strong>Neville Bryce</strong></div>
      <div class="meta-item">Copy saved for offline use &bull;
        November 2026</div>
    </div>
    <p class="offline-note">Read-only copy: to accept the contract
    terms or change a setting, open the online portal. Search below
    works exactly like the portal search.</p>
  </header>

  <div class="doc-search-bar">
    <form class="doc-search" role="search"
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
  </div>

  <main class="doc-main">
    <nav class="doc-article offline-toc" aria-label="Contents">
      <div class="article-header">
        <span class="article-badge badge-spec">Contents</span>
        <h2>What Is in This File</h2>
      </div>
      <ol>
{chr(10).join(toc)}
      </ol>
    </nav>

{chr(10).join(documents)}
  </main>

  {footer}

  <script>
{index_js}  </script>
  <script>
{search_js}  </script>
</body>
</html>
"""


def main(argv: List[str]) -> int:
    """Entry point: regenerate the offline copy, or check for staleness.

    Args:
        argv: command-line arguments; "--check" switches from writing
            to comparing.

    Returns:
        0 on success or when the file is current, 1 when --check
        finds it stale.
    """
    content = build()
    if "--check" in argv:
        current = (OFFLINE_OUTPUT.read_text(encoding="utf-8")
                   if OFFLINE_OUTPUT.is_file() else "")
        if current != content:
            print("migena/offline.html is stale; rerun the builder.")
            return 1
        return 0
    OFFLINE_OUTPUT.write_text(content, encoding="utf-8")
    print("Wrote %s (%d bytes)" % (OFFLINE_OUTPUT, len(content)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
