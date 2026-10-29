#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${XYSTACK_BIN_DIR:-$HOME/.local/bin}"

mkdir -p "$BIN_DIR"
ln -sf "$ROOT/bin/xystack" "$BIN_DIR/xystack"
echo "Linked $BIN_DIR/xystack -> $ROOT/bin/xystack"

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) echo "Add $BIN_DIR to your PATH to use the xystack command." ;;
esac
