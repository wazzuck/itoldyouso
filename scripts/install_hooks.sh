#!/bin/sh
# FILE: scripts/install_hooks.sh
# Purpose: point this clone's Git at the committed .githooks directory so
# the search index refreshes before every commit. Run once per clone.
cd "$(git rev-parse --show-toplevel)" || exit 1
git config core.hooksPath .githooks
echo "Git hooks installed from .githooks"
