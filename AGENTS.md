# Repository Guidelines for AI Coding Agents (itoldyouso)

> Repository-specific rules and project facts for `itoldyouso`.
> Global Artificial Intelligence (AI) coding agent rules live in the
> golden source (`~/vunderland/settings/AGENTS.md`), loaded via each
> agent's global configuration.
> Where this file refines or extends a global policy, both apply; if
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
