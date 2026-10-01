#!/bin/sh
# Install this repo's git hooks. Hooks live in .git/hooks/, which git does NOT
# clone -- so every machine that checks this repo out has to run this once.
#
#     sh security/install_hooks.sh
set -e
repo=$(git rev-parse --show-toplevel)
cp "$repo/security/pre-commit" "$repo/.git/hooks/pre-commit"
chmod +x "$repo/.git/hooks/pre-commit"
echo "installed $repo/.git/hooks/pre-commit"
echo "test it:  python3 security/scan_secrets.py --staged"
