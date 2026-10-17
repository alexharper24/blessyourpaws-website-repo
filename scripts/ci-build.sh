#!/usr/bin/env bash
# What Workers Builds runs before `npx wrangler deploy`.
#
# THIS IS THE STEP THAT MAKES THE OWNER EDITOR WORK. The editor publishes data/*.json and
# any new photographs under uploads/; it cannot run Python, so it never touches an .html
# file. Without this script the deploy ships whatever HTML is committed, and an owner's
# change reaches GitHub and stops there, which is exactly how Teapup's first publish failed
# on 2026-09-12.
#
# Set as the Build command in the dashboard:  bash scripts/ci-build.sh
set -euo pipefail

echo "=== python"
python3 --version

echo "=== pillow"
python3 -m pip install --quiet --disable-pip-version-check Pillow

echo "=== new photos"
python3 scripts/encode_uploads.py

echo "=== pages"
python3 scripts/scaffold.py

echo "=== done"
