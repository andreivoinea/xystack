die() {
  echo "xystack: $*" >&2
  exit 1
}

info() {
  echo "$*"
}
