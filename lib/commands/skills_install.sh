skills_install_help() {
  cat <<HELP
Usage: xystack skills install [options]
       xystack skills i [options]

Install every skill (a folder containing SKILL.md) found under the xystack
skills folder, including skills nested in organizational folders.

Options:
  -g, --global            Install to \$HOME/.agents/skills and \$HOME/.claude/skills (default)
  -p, --project           Install to ./.agents/skills and ./.claude/skills
  -h, --help              Show this help
HELP
}

find_skills() {
  local dir="$1" entry
  if [ -f "$dir/SKILL.md" ]; then
    echo "$dir"
    return
  fi
  for entry in "$dir"/*/; do
    [ -d "$entry" ] || continue
    find_skills "${entry%/}"
  done
}

skills_install_main() {
  local scope="global"
  while [ $# -gt 0 ]; do
    case "$1" in
      -g | --global) scope="global" ;;
      -p | --project) scope="project" ;;
      -h | --help) skills_install_help; return 0 ;;
      *) die "unknown option '$1'. Run 'xystack skills install --help'." ;;
    esac
    shift
  done

  local base
  if [ "$scope" = "global" ]; then
    base="$HOME"
  else
    base="$(pwd)"
  fi
  local targets=("$base/.agents/skills" "$base/.claude/skills")

  local source_dir="$XYSTACK_ROOT/skills"
  [ -d "$source_dir" ] || die "skills folder not found: $source_dir"

  local skills=()
  local skill
  while IFS= read -r skill; do
    [ -n "$skill" ] && skills+=("$skill")
  done < <(find_skills "$source_dir")

  if [ ${#skills[@]} -eq 0 ]; then
    info "No skills found in $source_dir"
    return 0
  fi

  local names
  names="$(for skill in "${skills[@]}"; do basename "$skill"; done | sort | uniq -d)"
  [ -z "$names" ] || die "duplicate skill names: $(echo $names)"

  local target name
  for target in "${targets[@]}"; do
    mkdir -p "$target"
    for skill in "${skills[@]}"; do
      name="$(basename "$skill")"
      rm -rf "${target:?}/$name"
      cp -R "$skill" "$target/$name"
    done
    info "Installed ${#skills[@]} skill(s) to $target"
  done
}
