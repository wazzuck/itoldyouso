# AGENTS.md — pointer to the golden master

This repository does not carry its own copy of the agent rules.

Golden master, the only file in which common rules are ever edited:

    ../vunderland/settings/AGENTS.md

Before reading or editing anything in this repository:

1. Read the golden master in full. Its rules are binding here.
2. Read `AGENTS.local.md` in this repository, if present. It holds
   this repository's own rules; on a conflict, stop and ask the
   operator which one wins.
3. If the golden master is missing on this machine, stop and ask the
   operator where the `vunderland` repository is. Never work from
   memory or from an older copy.

Why this file is a pointer: GitHub Pages refuses to deploy a
repository whose `AGENTS.md` links to a file outside it, so a
symlink here broke every deploy of itoldyouso.tech. Keeping the
rules in `vunderland` alone also means one edit reaches every
repository, with no copy to drift and nothing to synchronise.
