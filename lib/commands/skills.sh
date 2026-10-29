source "$XYSTACK_ROOT/lib/commands/skills_install.sh"

skills_help() {
  cat <<HELP
Usage: xystack skills <command> [options]

Commands:
  install, i              Install skills from the xystack skills folder, skipping installed ones
  clean-install, ci       Install skills from the xystack skills folder, replacing installed ones

Options:
  -h, --help              Show this help
HELP
}

skills_main() {
  local cmd="${1:-}"
  case "$cmd" in
    "" | -h | --help) skills_help ;;
    install | i) shift; skills_install_main "$@" ;;
    clean-install | ci) shift; skills_clean_install_main "$@" ;;
    *) die "unknown skills command '$cmd'. Run 'xystack skills --help'." ;;
  esac
}
