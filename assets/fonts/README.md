# Self-hosted site font

## What is here

| File | Purpose |
| --- | --- |
| `inter-latin-wght-normal.woff2` | Inter variable font, latin subset. |
| | Weights 100-900 in one file. |
| `OFL.txt` | SIL Open Font License 1.1 text. |

## Why the font is stored here

The project rules forbid third-party scripts and trackers. Loading Inter
from Google Fonts would send a visitor's request to a third party on
every page load, so the font file is hosted on our own origin instead.

One file covers every weight the site uses, because it is a variable
font. That keeps the download to about 48 kilobytes.

## Who consumes it

`header.css` declares the `@font-face` rule. That file is loaded by every
public page: `index.html` links it directly, and `services/styles.css`
pulls it in with `@import url("../header.css")`. The font stacks in
`index.html` and `services/styles.css` then name `"Inter"` first.

## Licence and attribution

Inter is copyright (c) 2016 The Inter Project Authors
(https://github.com/rsms/inter), licensed under the SIL Open Font
License 1.1. The licence permits redistribution and web embedding, so
hosting the file in this repository is allowed. `OFL.txt` carries the
full licence text, as the licence requires.

## Regenerating or upgrading

1. Download the latin subset variable Web Open Font Format (WOFF2) file
   from the Fontsource package for Inter, file
   `inter-latin-wght-normal.woff2`.
2. Replace the existing file in this directory, keeping the name.
3. Fetch the current licence text from
   `https://raw.githubusercontent.com/rsms/inter/master/LICENSE.txt`
   and save it as `OFL.txt`.
4. Run `python3 scripts/verify_site.py` before committing.
