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
    """Return the three owner task cards, done in order.

    Task 1 (verify identity) must be done first. Task 2 (update the
    software) gates task 3 (turn on cash payments). The printer routing
    and the Wi-Fi check belong to Neville; engineer_tasks_html builds
    them. Each card has numbered steps, a stop box with the engineer's
    number, and a Done tick.
    """
    return """      <!-- Owner tasks: the first thing the owner reads on the
           Documentation page. Three numbered cards, done in order: task 1
           must be done first, and task 2 gates task 3. Each card is a
           separate job with its own Done tick. The tasks owned by Neville
           sit in their own section below. -->
      <section class="owner-tasks" aria-labelledby="owner-tasks-title">
        <header class="owner-tasks-heading">
          <h2 id="owner-tasks-title">Owner tasks: do these 3 in order</h2>
          <p class="owner-tasks-intro">Only the owner does these
            tasks. Work through one card at a time. Task 1 must be
            ticked before you start tasks 2 and 3. Task 2 must be
            ticked before you start task 3. If a step does not match
            what you see, stop and ring Neville Bryce on
            020&nbsp;4520&nbsp;9114. Do not guess.</p>
        </header>
        <div class="owner-tasks-cards">
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 1 of 3</span>
            <span class="owner-task-first">Do this first</span>
            <span class="owner-task-chip">Owner only</span>
            <span class="owner-task-chip">Do it yourself</span>
          </div>
          <h3>Verify your identity</h3>
          <p><strong>When:</strong> ASAP</p>
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
          <p class="owner-task-apart">This is owner task 1 of 3. It is
            separate from the other tasks. Verifying your identity does
            not update the software, turn on cash payments or set up the
            printers.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 2 of 3</span>
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
          <p class="owner-task-apart">This is owner task 2 of 3. It is
            separate from the other tasks. Do not start task 3 until this
            box is ticked.</p>
        </section>
        <section class="owner-task-card">
          <div class="owner-task-card-head">
            <span class="owner-task-tag">Owner task 3 of 3</span>
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
          <p class="owner-task-apart">This is owner task 3 of 3. It is
            separate from the other tasks. Finishing this card does not
            finish the work that Neville owns.</p>
        </section>
        </div>
      </section>"""


def engineer_tasks_html() -> str:
    """Return the six task cards that Neville owns, not the owner.

    The cards sit in their own section below the owner tasks, so the
    owner never mistakes them for duties. The owner does not tick them.
    Cards 1 and 2 are on-site checks. Cards 3 to 6 are documentation and
    set-up tasks. Card 1 starts only after owner task 2 (update the
    software) is ticked, because the category option appears only on
    updated software.

    Returns:
        The HTML for the section owned by Neville.
    """
    return """      <!--
           Tasks owned by Neville. They sit below the owner tasks so the
           owner never mistakes them for duties. The owner does not tick
           these cards. -->
      <section class="engineer-tasks" aria-labelledby="engineer-tasks-title">
        <header class="engineer-tasks-heading">
          <h2 id="engineer-tasks-title">Tasks owned by Neville</h2>
          <p class="engineer-tasks-intro">Neville Bryce owns these six
            tasks, so you do not need to do them. He will tell you when
            each one is done. Where he needs a decision from you, he will
            ask. If you notice a printer, Wi-Fi or till problem before he
            has finished, ring him on 020&nbsp;4520&nbsp;9114.</p>
        </header>
        <div class="engineer-tasks-cards">
        <section class="engineer-task-card">
          <div class="engineer-task-card-head">
            <span class="owner-task-tag">Neville task 1 of 6</span>
            <span class="owner-task-chip">Owned by Neville</span>
          </div>
          <h3>Route drinks to the bar printer and food to the kitchen
            printer</h3>
          <p class="owner-task-wait">Start only after the owner has ticked
            owner task 2.</p>
          <p><strong>Why:</strong> so drink orders print at the bar and
            food orders print in the kitchen.</p>
          <p class="owner-task-label">Neville checks these steps in order</p>
          <ol class="owner-steps">
            <li>Check that the register, the card reader and the kitchen
              Terminal are on the same software version.</li>
            <li>On each device that holds a printer, open the printer
              settings. If they cannot be found, check the software
              versions again before going on.</li>
            <li>Look for <strong>Select categories</strong> on each
              printer. If it is missing, stop. Agree another way to send
              food and drink orders to the right place with the owner
              before going on.</li>
            <li>On the kitchen printer, select only the food categories,
              01 to 11. Save the settings.</li>
            <li>On the bar printer, select only the drink categories, 12
              to 18 and 20 to 22. Do not select 19 Drink Extras, which is
              empty. Save the settings.</li>
            <li>Test: park one order with a food item and one drink. The
              bar printer should print only the drink, and the kitchen
              printer only the food.</li>
          </ol>
          <div class="owner-task-stop">Stop if a device will not restart,
            the printer settings cannot be found, or the software versions
            do not match. Do not change the routing until they match.</div>
          <p class="owner-task-apart"><strong>Status:</strong> to do, on
            site. The owner does not need to do this task.</p>
        </section>
        <section class="engineer-task-card">
          <div class="engineer-task-card-head">
            <span class="owner-task-tag">Neville task 2 of 6</span>
            <span class="owner-task-chip">Owned by Neville</span>
            <span class="owner-task-chip">Not a blocker</span>
          </div>
          <h3>Check the Wi-Fi for dropouts</h3>
          <p class="owner-task-wait">Start only after the owner has ticked
            owner task 2.</p>
          <p><strong>Why:</strong> if the till, card reader or kitchen
            Terminal lose Wi-Fi during service, payments can fail and
            orders can stop printing. It is not a blocker to opening, but
            it can affect business if it is not spotted early.</p>
          <p class="owner-task-label">Neville checks these steps in order</p>
          <ol class="owner-steps">
            <li>Stand at the till, at the card reader's usual position and
              at the kitchen Terminal's usual position. Check the Wi-Fi
              symbol on each screen.</li>
            <li>If any device shows one bar, a cross or <strong>No
              connection</strong>, note the exact spot.</li>
            <li>With each device in its normal place, start one test sale
              and send it to the printers.</li>
            <li>Watch the screen during the sale. If a spinner stays for
              more than 10 seconds, or a printer does not respond, note
              it.</li>
            <li>Repeat at a quiet time and again during a busy period if
              possible, because dropouts often show up when the network
              is under load.</li>
            <li>Record when each dropout happens and which device is
              affected.</li>
          </ol>
          <div class="owner-task-stop">Stop and investigate if a device
            keeps losing connection, a payment fails because of the
            network, or a printer stops responding mid-service. Tell the
            owner what you found.</div>
          <p class="owner-task-apart"><strong>Status:</strong> to do, on
            site. The owner should ring Neville about any dropout they
            see.</p>
        </section>
        <section class="engineer-task-card">
          <div class="engineer-task-card-head">
            <span class="owner-task-tag">Neville task 3 of 6</span>
            <span class="owner-task-chip">Owned by Neville</span>
          </div>
          <h3>Write down how to print the bill before payment</h3>
          <p><strong>Why:</strong> so the customer can check the bill on
            paper before paying.</p>
          <p class="owner-task-label">Neville to do</p>
          <ol class="owner-steps">
            <li>Find how to print the bill from the till before payment,
              and check which printer prints it.</li>
            <li>Confirm the steps on the till, using a test order and
              without taking payment. Then write them into the Till
              Procedures &amp; Features guide in plain steps.</li>
            <li>Check that the printed bill shows each item, its modifiers
              and the prices, so the customer can check it.</li>
          </ol>
          <p class="owner-task-apart"><strong>Status:</strong> to do. The
            owner does not need to do this task.</p>
        </section>
        <section class="engineer-task-card">
          <div class="engineer-task-card-head">
            <span class="owner-task-tag">Neville task 4 of 6</span>
            <span class="owner-task-chip">Owned by Neville</span>
          </div>
          <h3>Print each modifier under its food or drink item on
            tickets</h3>
          <p><strong>Why:</strong> at the moment each modifier, such as oat
            milk or an extra shot, prints as a separate item. The kitchen
            and bar need to see it under the item it belongs to.</p>
          <p class="owner-task-label">Neville to do</p>
          <ol class="owner-steps">
            <li>Check the ticket and modifier settings on each device that
              prints tickets, and find the setting that prints a modifier
              under its item.</li>
            <li>If the till cannot do this, ask SumUp support, and tell the
              owner before changing the menu.</li>
            <li>Test with a mixed order: a drink with a modifier, such as
              oat milk, and a food item. Each modifier should print under
              its item on the right ticket.</li>
          </ol>
          <p class="owner-task-apart"><strong>Status:</strong> to do. The
            owner does not need to do this task.</p>
        </section>
        <section class="engineer-task-card">
          <div class="engineer-task-card-head">
            <span class="owner-task-tag">Neville task 5 of 6</span>
            <span class="owner-task-chip">Owned by Neville</span>
          </div>
          <h3>Print the name of the member of staff on each order
            ticket</h3>
          <p><strong>Why:</strong> the kitchen has asked for it, so that any
            query from the kitchen or bar can go to the right person.</p>
          <p class="owner-task-label">Neville to do</p>
          <ol class="owner-steps">
            <li>Check whether the order tickets can show the name of the
              member of staff who placed the order.</li>
            <li>If they can, check what the name is taken from. It may need
              each person to sign in with their own Personal Identification
              Number (PIN). PIN login was off when the till was checked on
              19 November 2026.</li>
            <li>If the tickets cannot show the name, tell the owner before
              deciding what to do.</li>
          </ol>
          <p class="owner-task-apart"><strong>Status:</strong> to do. The
            owner does not need to do this task.</p>
        </section>
        <section class="engineer-task-card">
          <div class="engineer-task-card-head">
            <span class="owner-task-tag">Neville task 6 of 6</span>
            <span class="owner-task-chip">Owned by Neville</span>
          </div>
          <h3>Add a payout method so the owner can withdraw cash
            from SumUp</h3>
          <p><strong>Why:</strong> so the owner can take the takings out of
            the SumUp account as cash.</p>
          <p class="owner-task-label">Neville to do</p>
          <ol class="owner-steps">
            <li>Ask the owner which withdrawal method they want. The payout
              destination is currently the SumUp Business Account. Ask
              whether a different destination, such as a bank account, is
              wanted.</li>
            <li>Check whether the owner's identity check (owner task 1) must
              be finished before a new payout destination can be added.</li>
            <li>Set up the method in the payout settings, under Profile, then
              Payouts. Check that the first payout arrives as expected.</li>
          </ol>
          <p class="owner-task-apart"><strong>Status:</strong> to do. The
            owner needs to decide which method to use.</p>
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
        then the cards owned by Neville, then the three guide buttons.
        The owner can grab the phone
        copy, do the tasks, then choose a guide.
    """
    return "\n\n".join([doc_download_html(), owner_tasks_html(),
                        engineer_tasks_html(), doc_guides_html()])


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
