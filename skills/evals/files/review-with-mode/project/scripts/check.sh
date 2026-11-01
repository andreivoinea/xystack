#!/usr/bin/env bash
# Runs what CI runs. Use from the repository root.
set -euo pipefail

npm run --silent typecheck
npm test --silent
