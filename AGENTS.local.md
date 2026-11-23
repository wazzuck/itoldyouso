# Repository-Local Guidelines for AI Coding Agents (itoldyouso)

> Repository-specific rules and project facts for `itoldyouso`.
> Shared Artificial Intelligence (AI) coding agent rules live in the
> golden master, `../vunderland/settings/AGENTS.md`; this repository's
> `AGENTS.md` is a pointer to that file and holds no rules of its own.
> Keep all `itoldyouso`-specific rules here; common cross-repo rules
> belong in the golden master, never in this file or in `AGENTS.md`.
> Where this file refines or extends a common policy, both apply; if
> there is a conflict, stop and ask the operator.

---

## 1. Repository-specific policies

1. **Keep Search Engine Optimisation (SEO) and AI optimisation current.**
   - Every new or edited page or service must keep SEO, AI search
     optimisation, and discovery artefacts up to date in the same task:
     `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, service
     counts across `index.html`, `404.html`, and `services/*.html`,
     canonical and sitemap `<link>` tags, Open Graph (OG) and Twitter
     metadata, Schema.org JavaScript Object Notation for Linked Data
     (JSON-LD) (`hasOfferCatalog`, `Service`, `BreadcrumbList`, and
     `FAQPage` matched verbatim to visible HTML), sibling cross-links,
     and IndexNow readiness.
   - Every service must also keep rich alternative wording (synonyms) in
     `llms.txt`, `llms-full.txt` and the search index, enforced by
     `check_synonym_coverage()`.
   - Keep `scripts/verify_site.py` updated to enforce all new pages,
     Uniform Resource Locators (URLs), counts, and indexing checks
     automatically.

2. **Common rule changes go to the golden master.**
   - Any change to the common rule set must be made in
     `../vunderland/settings/AGENTS.md` and committed in the
     `vunderland` repository, whatever the change looks like.
   - Never add, edit or fork a common rule in this repository's
     `AGENTS.md` pointer, and never park one in this file to move
     later: `AGENTS.md` here names the golden master and nothing
     else.
   - There is nothing to regenerate afterwards. Every repository
     reads the golden master live through its pointer, so the new
     rule applies to all of them from the next session onward.

---

## 2. Project facts

1. **Language and spelling**:
   All user-facing copy, documentation, code comments, commit messages
   and pull requests must use British English conventions (for example:
   "optimisation", "customisation", "prioritisation", "synchronise",
   "colour", "licence" for noun, "practice" for noun, "programme").
   This policy is binding and applies across the entire repository.

2. **Technology stack**:
   Static HyperText Markup Language (HTML5), Cascading Style Sheets
   (CSS3), vanilla JavaScript (JS), and Python 3 for validation.
   Zero external JavaScript frameworks or third-party ad tracking
   scripts are permitted; first-party Google Analytics 4 (`gtag.js`,
   measurement ID `G-XP0QRKTWKZ`) is the sole permitted analytics tag.

3. **Verification command**:
   Run `python3 scripts/verify_site.py` before committing. All tests,
   link checks, Extensible Markup Language (XML) sitemaps, JSON-LD,
   and 80-column line-length rules must pass with code 0.

4. **Migena portal generators**:
   Files under `migena/` are partly generated: edit the source or the
   generator, never the outputs. `scripts/split_portal.py` writes
   `portal.css` and the standalone pages from `migena/index.html`;
   `scripts/build_search_index.py` writes `assets/search-index.js`
   and `migena/search-index.js`; `scripts/build_offline_doc.py`
   writes `migena/offline.html`, which embeds the credentials file
   and must be regenerated whenever the documents or
   `migena/sumup_password.txt` change. Run them in that order, or let
   the pre-commit hook do it; `scripts/verify_site.py` fails when any
   output is stale.
