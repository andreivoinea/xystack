skills_install_help() {
  cat <<HELP
Usage: xystack skills install [options]
       xystack skills i [options]

Install every skill (a folder containing SKILL.md) found under the xystack
skills folder, including skills nested in organizational folders.
Skills that are already installed are skipped.

Options:
  -g, --global            Install to \$HOME/.agents/skills and \$HOME/.claude/skills (default)
  -p, --project           Install to ./.agents/skills and ./.claude/skills
  -h, --help              Show this help
HELP
}

skills_clean_install_help() {
  cat <<HELP
Usage: xystack skills clean-install [options]
       xystack skills ci [options]

Install every skill (a folder containing SKILL.md) found under the xystack
skills folder, including skills nested in organizational folders.
Skills that are already installed are replaced.

Options:
  -g, --global            Install to \$HOME/.agents/skills and \$HOME/.claude/skills (default)
  -p, --project           Install to ./.agents/skills and ./.claude/skills
  -h, --help              Show this help
HELP
}

find_skills() {
  local dir="$1" entry
  if [ -f "$dir/SKILL.md" ]; then
    case "${dir##*/}" in
      *$'\n'*) die "skill names must not contain line breaks: $(printf '%q' "$dir")" ;;
    esac
    found_skills+=("$dir")
    return
  fi
  for entry in "$dir"/*/; do
    entry="${entry%/}"
    [ -d "$entry" ] || continue
    if [ -L "$entry" ]; then
      echo "xystack: skipping symlinked folder: $entry" >&2
      continue
    fi
    find_skills "$entry"
  done
}

skills_install_main() {
  skills_install_run install skills_install_help false "$@"
}

skills_clean_install_main() {
  skills_install_run clean-install skills_clean_install_help true "$@"
}

skills_install_run() {
  local cmd="$1" help_fn="$2" overwrite="$3"
  shift 3

  local scope="global"
  while [ $# -gt 0 ]; do
    case "$1" in
      -g | --global) scope="global" ;;
      -p | --project) scope="project" ;;
      -h | --help) "$help_fn"; return 0 ;;
      *) die "unknown option '$1'. Run 'xystack skills $cmd --help'." ;;
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

  local found_skills=()
  find_skills "$source_dir"

  if [ ${#found_skills[@]} -eq 0 ]; then
    info "No skills found in $source_dir"
    return 0
  fi

  local skills=("${found_skills[@]}") skill
  local names
  names="$(for skill in "${skills[@]}"; do basename "$skill"; done | sort | uniq -d)"
  [ -z "$names" ] || die "duplicate skill names: $(echo $names)"

  local target name installed skipped
  for target in "${targets[@]}"; do
    mkdir -p "$target"
    installed=0
    skipped=0
    for skill in "${skills[@]}"; do
      name="$(basename "$skill")"
      if [ -e "$target/$name" ] || [ -L "$target/$name" ]; then
        if [ "$overwrite" = true ]; then
          rm -rf "${target:?}/$name"
        else
          skipped=$((skipped + 1))
          continue
        fi
      fi
      cp -R "$skill" "$target/$name"
      installed=$((installed + 1))
    done
    info "Installed $installed skill(s) to $target ($skipped already installed, skipped)"
  done
}
