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


def owner_tasks_html() -> str:
    """Return the six owner task cards, done in order.

    Task 1 (verify identity) must be done first. Task 2 (update the
    software) gates tasks 3 to 6. Task 4 (check printers) must be done
    before task 5 (route categories). Task 6 (Wi-Fi check) is not a
    blocker but is included so the owner spots dropouts before they
    affect service. Each card has numbered steps, a stop box with the
    engineer's number, and a Done tick.
    """
    return """      <!-- Owner tasks: the first thing the owner reads on the
           Documentation page. Six numbered cards, done in order: task 1
           must be done first, task 2 gates tasks 3 to 6, and task 4
           gates task 5. Task 6 is not a blocker but should be checked.
           Each card is a separate job with its own Done tick. -->
      <section class="owner-tasks" aria-labelledby="owner-tasks-title">
        <header class="owner-tasks-heading">
          <h2 id="owner-tasks-title">Owner tasks: do these 6 in order</h2>
          <p class="owner-tasks-intro">Only the owner does these
            tasks. Work through one card at a time. Task 1 must be
            ticked before you start tasks 2 to 6. Task 2 must be
            ticked before you start tasks 3 to 6. Task 4 must be
            ticked before you start task 5. Task 6 is not a blocker,
            but dropouts can affect service. If a step does not match
            what you see, stop and ring Neville Bryce on
            020&nbsp;4520&nbsp;9114. Do not guess.</p>
        </header>
        <div class="owner-tasks-cards">
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 1 of 6</span>
            <span class="owner-task-first">Do this first</span>
            <span class="owner-task-chip">Owner only</span>
            <span class="owner-task-chip">Do it yourself</span>
          </div>
          <h3>Verify your identity</h3>
          <p><strong>When:</strong> early, in case the check takes
            time. Do not leave it until the last day.</p>
          <p><strong>You need:</strong> your own mobile phone, your own
            SumUp login, and a valid photo ID such as a passport or a
            photo driving licence.</p>
          <p class="owner-task-label">Follow these steps in order</p>
          <ol class="owner-steps">
            <li>Sign in to your own SumUp profile, in a web browser or
              in the SumUp app on your own phone.</li>
            <li>Look at the top of the screen for the verification
              banner. Tap it.</li>
            <li>If the form asks for them, fill in your details exactly
              as they appear on your ID.</li>
            <li>When asked, scan your photo ID.</li>
            <li>When asked, take a selfie and submit it.</li>
            <li>Submit everything, then wait for SumUp's message.</li>
          </ol>
          <p class="owner-task-rules"><strong>Rules:</strong> you do
            this yourself. Do not let staff or the engineer do it for
            you, and do not use anyone else's login or phone. Do not
            send a photo of your ID to anyone by text or e-mail,
            including Neville. Scan it only on SumUp's own screens.</p>
          <div class="owner-task-stop">Stop and ring Neville on
            <a href="tel:02045209114">020&nbsp;4520&nbsp;9114</a> if you cannot
            find the verification banner, the scan keeps failing, or
            SumUp asks for something you do not understand.</div>
          <label class="owner-task-done">
            <input type="checkbox">
            Done: SumUp shows that my identity is verified. Tick this
            only when SumUp says so.
          </label>
          <p class="owner-task-apart">This is owner task 1 of 6. It is
            separate from the other tasks. Verifying your identity does
            not update the software, turn on cash payments or set up the
            printers.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 2 of 6</span>
            <span class="owner-task-chip">Owner only</span>
          </div>
          <h3>Update the software</h3>
          <p class="owner-task-wait">Start only after task 1 is
            ticked.</p>
          <p><strong>When:</strong> before you open on Sunday 22
            November 2026, and again on the morning of that day.</p>
          <p><strong>Why:</strong> if the devices run different
            versions, orders can show different statuses on different
            devices.</p>
          <p class="owner-task-label">Follow these steps in order</p>
          <ol class="owner-steps">
            <li>Make sure no customer is waiting and no sale is on
              the register screen.</li>
            <li>On the register, tap More or Settings. If you cannot
              see either, stop and ring Neville. Then look for an
              update option. If an update is shown, tap it and follow
              the screens.</li>
            <li>Do the same on the card reader (SumUp Solo). If the
              reader shows an update, follow the screens.</li>
            <li>Do the same on the kitchen Terminal.</li>
            <li>Do not switch anything off while an update is
              running. Wait until each update has finished.</li>
            <li>Switch off each device, wait 10 seconds, then switch
              it on again. Wait until each screen is ready.</li>
            <li>On each device, find the app version number. Check
              that all three numbers are the same.</li>
          </ol>
          <div class="owner-task-stop">Stop and ring Neville on
            <a href="tel:02045209114">020&nbsp;4520&nbsp;9114</a> if an update
            fails, a device will not restart, the three version
            numbers differ, or you cannot find where to check the
            version.</div>
          <label class="owner-task-done">
            <input type="checkbox">
            Done: all three devices show the same version after a
            restart.
          </label>
          <p class="owner-task-apart">This is owner task 2 of 6. It is
            separate from the other tasks. Do not start tasks 3, 4, 5 or
            6 until this box is ticked.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 3 of 6</span>
            <span class="owner-task-chip">Owner only</span>
          </div>
          <h3>Turn on cash payments</h3>
          <p class="owner-task-wait">Start only after task 2 is
            ticked.</p>
          <p><strong>Why:</strong> until this is on, the till takes card
            payments only.</p>
          <p class="owner-task-label">Follow these steps in order</p>
          <ol class="owner-steps">
            <li>Make sure no customer is waiting and no sale is on the
              register screen.</li>
            <li>Look at the bottom-left corner of the screen. Tap the
              small round profile icon.</li>
            <li>In the menu that opens, tap <strong>Cash
              payments</strong>.</li>
            <li>Turn on the switch beside <strong>Accept cash
              payments</strong>. If it is already on, leave it on.</li>
            <li>Test it: start a new sale with one cheap item. Tap the
              button that takes payment, often labelled Charge or
              Pay.</li>
            <li>Look for <strong>Cash</strong> in the list of ways to
              pay. You should see it.</li>
            <li>Do not tap Cash and do not take any money. Leave the
              test sale without paying. If you are not sure how, ring
              Neville.</li>
          </ol>
          <div class="owner-task-stop">Stop and ring Neville on
            <a href="tel:02045209114">020&nbsp;4520&nbsp;9114</a> if you cannot
            find the profile icon, there is no Cash payments option, or
            the switch will not stay on.</div>
          <label class="owner-task-done">
            <input type="checkbox">
            Done: I can see Cash in the list of ways to pay.
          </label>
          <p class="owner-task-apart">This is owner task 3 of 6. It is
            separate from the other tasks. Finishing this card does not
            finish the printer check or category routing.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 4 of 6</span>
            <span class="owner-task-chip">Owner only</span>
          </div>
          <h3>Check the kitchen and bar printers</h3>
          <p class="owner-task-wait">Start only after task 2 is
            ticked.</p>
          <p><strong>Why:</strong> so the kitchen and bar tickets can
            be split by category.</p>
          <p class="owner-task-label">Follow these steps in order</p>
          <ol class="owner-steps">
            <li>Check that the register, the card reader and the kitchen
              Terminal are still on the same version as in task 2.</li>
            <li>On the register, open the printer settings for the
              kitchen printer. If you cannot find the printer settings,
              stop and ring Neville.</li>
            <li>Look for the words <strong>Select categories</strong>.</li>
            <li>Do the same for the bar printer.</li>
            <li>If you see <strong>Select categories</strong> on both
              printers, ring or text Neville and tell him. Do not change
              any category setting yourself.</li>
            <li>If you do not see <strong>Select categories</strong> on
              a printer, ring Neville before you open. Do not try to fix
              it yourself. Neville will agree another way to send food
              and drink orders to the right place.</li>
          </ol>
          <div class="owner-task-stop">Stop and ring Neville on
            <a href="tel:02045209114">020&nbsp;4520&nbsp;9114</a> if a device will
              not restart, you cannot find the printer settings, or the
              versions do not match.</div>
          <label class="owner-task-done">
            <input type="checkbox">
            Done: I have checked both printers and told Neville what I
            found.
          </label>
          <p class="owner-task-apart">This is owner task 4 of 6. It is
            separate from the other tasks. Finishing this card does not
            turn on cash payments, route categories or update the
            software.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 5 of 6</span>
            <span class="owner-task-chip">Owner only</span>
          </div>
          <h3>Route drinks to the bar printer and food to the kitchen
            printer</h3>
          <p class="owner-task-wait">Start only after task 4 is
            ticked.</p>
          <p><strong>Why:</strong> so drink orders print at the bar and
            food orders print in the kitchen. Staff then know where each
            item is made.</p>
          <p class="owner-task-label">Follow these steps in order</p>
          <ol class="owner-steps">
            <li>Make sure no customer is waiting and no sale is on the
              register screen.</li>
            <li>On the register, open the main menu (often three lines or
              the word More). Look for <strong>Settings</strong> or
              <strong>Printers</strong>. If you cannot find either, stop
              and ring Neville.</li>
            <li>Open the printer settings and choose the
              <strong>kitchen printer</strong>.</li>
            <li>Look for <strong>Select categories</strong>,
              <strong>Categories</strong> or <strong>Print categories</strong>.
              Tap it.</li>
            <li>Select only the food categories, for example
              <strong>Brunch</strong>, <strong>Lunch</strong>,
              <strong>Mains</strong> and <strong>Sides</strong>. Do not
              select drink categories here.</li>
            <li>Save the kitchen printer settings.</li>
            <li>Go back and choose the <strong>bar printer</strong>.</li>
            <li>Open its category selection and select only the drink
              categories, for example <strong>Coffee</strong>,
              <strong>Tea</strong>, <strong>Soft Drinks</strong>,
              <strong>Beers</strong> and <strong>Wine</strong>. Do not
              select food categories here.</li>
            <li>Save the bar printer settings.</li>
            <li>Test it: start a new sale with one drink and one food
              item. Send the order to the printers. Check that the bar
              printer prints only the drink and the kitchen printer
              prints only the food.</li>
          </ol>
          <div class="owner-task-stop">Stop and ring Neville on
            <a href="tel:02045209114">020&nbsp;4520&nbsp;9114</a> if you cannot
            find the printer settings, the Select categories option is
            missing, the category names do not match your menu, or a test
            order prints on the wrong printer.</div>
          <label class="owner-task-done">
            <input type="checkbox">
            Done: a drink-only ticket prints at the bar and a food-only
            ticket prints in the kitchen.
          </label>
          <p class="owner-task-apart">This is owner task 5 of 6. It is
            separate from the other tasks. Routing categories does not
            turn on cash payments or update the software.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 6 of 6</span>
            <span class="owner-task-chip">Owner only</span>
            <span class="owner-task-chip">Not a blocker</span>
          </div>
          <h3>Check the Wi-Fi for dropouts</h3>
          <p class="owner-task-wait">Start only after task 2 is
            ticked.</p>
          <p><strong>Why:</strong> if the till, card reader or kitchen
            Terminal lose Wi-Fi during service, payments can fail and
            orders can stop printing. This is not a blocker to opening,
            but it can impact business if it is not spotted early.</p>
          <p class="owner-task-label">Follow these steps in order</p>
          <ol class="owner-steps">
            <li>Stand at the till, the card reader's usual position and
              the kitchen Terminal's usual position. Look at the Wi-Fi
              symbol on each screen.</li>
            <li>If any device shows one bar, a cross, or the words
              <strong>No connection</strong>, note the exact spot.</li>
            <li>With each device in its normal place, start one test sale
              and send it to the printers.</li>
            <li>Watch the screen during the sale. If a spinner stays for
              more than 10 seconds, or the printer does not respond,
              note it.</li>
            <li>Do this at a quiet time and again during a busy period if
              possible, because dropouts often show up when the network
              is under load.</li>
            <li>If you see dropouts, write down when they happen and
              which device is affected, then ring Neville.</li>
          </ol>
          <div class="owner-task-stop">Stop and ring Neville on
            <a href="tel:02045209114">020&nbsp;4520&nbsp;9114</a> if a device keeps
            losing connection, a payment fails because of the network, or
            printers stop responding mid-service.</div>
          <label class="owner-task-done">
            <input type="checkbox">
            Done: I have checked all three devices in their normal
            positions and I am happy with the Wi-Fi.
          </label>
          <p class="owner-task-apart">This is owner task 6 of 6. It is
            not a blocker, but it is worth checking before you are busy.
            It is separate from the printer category routing.</p>
        </section>
        </div>
      </section>"""


def doc_download_html() -> str:
    """Return the prominent offline-copy download banner.

    This sits at the very top of the Documentation page so the owner
    can grab the phone copy before reading any tasks or guides.
    """
    return """      <!-- Download the offline copy: placed at the top of the
           Documentation page and styled as a button so it cannot be
           missed. -->
      <section class="doc-download" aria-labelledby="doc-download-title">
        <h2 id="doc-download-title" class="visually-hidden">Download the
          offline copy</h2>
        <a class="doc-download-btn" href="offline.html"
           download="EGGIs-Till-Documentation.html">
          <span class="doc-download-icon">&#11015;</span>
          <span class="doc-download-text">
            <strong>Download the offline copy for your phone</strong>
            <span>All the guides and the User Passwords page in one file,
              for when you have no connection.</span>
          </span>
        </a>
      </section>"""


def doc_guides_html() -> str:
    """Return the three documentation guide buttons.

    These sit below the owner tasks on the Documentation page and open
    the Admin Guide, Management Guide and Till Procedures & Features.
    """
    return """      <!-- The three documentation guides, opened from the same
           Documentation page as the owner tasks. -->
      <section class="doc-guides" aria-labelledby="doc-guides-title">
        <h2 id="doc-guides-title">Choose a guide</h2>
        <ul class="portal-buttons">
          <li>
            <a href="admin.html">&#128736; Admin Guide</a>
            <p>Adding and removing staff, changing what they can do, and
              their Personal Identification Numbers (PINs).</p>
          </li>
          <li>
            <a href="management.html">&#128200; Management Guide</a>
            <p>The accounts behind the till, who holds each one, and the
              daily, weekly and monthly routines.</p>
          </li>
          <li>
            <a href="till.html">&#128424; Till Procedures &amp; Features</a>
            <p>How to do each till task, step by step, and what each
              feature of the till does.</p>
          </li>
        </ul>
      </section>"""


def hub_body() -> str:
    """Return the main content of the Documentation page.

    Returns:
        The offline download banner first, then the owner task cards,
        then the three guide buttons. The owner can grab the phone
        copy, do the tasks, then choose a guide.
    """
    return "\n\n".join([doc_download_html(), owner_tasks_html(),
                        doc_guides_html()])


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
        out[name] = shell(title, body, "&larr; Main page", True,
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
