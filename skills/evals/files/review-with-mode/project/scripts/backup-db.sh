#!/usr/bin/env bash
# Copies the data directory (orders.json) to backups/<timestamp>/. Use from the repository root.
set -euo pipefail

data_dir="${DATA_DIR:-data}"
backup_dir="backups/$(date -u +%Y%m%dT%H%M%SZ)"

if [ ! -d "$data_dir" ]; then
  echo "backup-db.sh: no data directory at $data_dir" >&2
  exit 1
fi

mkdir -p "$backup_dir"
cp -R "$data_dir/." "$backup_dir/"
echo "Backed up $data_dir to $backup_dir"
