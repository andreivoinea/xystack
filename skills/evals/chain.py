#!/usr/bin/env python3
"""Helper for chained review scenarios. See README.md for the stages.

  chain.py init SCENARIO RUN_DIR             set up target/ (base, v1), threads/ (seeds), reports/
  chain.py push RUN_DIR REV                  check out the next revision and its diff
  chain.py prompt RUN_DIR STAGE MODE CONFIG  print a stage prompt (CONFIG: with_skill | without_skill)
  chain.py rule RUN_DIR THREAD STATUS TEXT   post a team-lead comment; STATUS: open | fixed | withdrawn | accepted | keep
  chain.py snapshot RUN_DIR OUT_DIR          copy threads/ and reports/ to OUT_DIR
  chain.py check RUN_DIR                     check that target/ is unchanged
"""

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
REPO_SKILLS = EVALS_DIR.parent

INTERFACE = """The review interface for this PR is the folder {threads}/:
- Each thread is a file `<id>.md`. Its first line is `# <id>: <location>`, its second line is the status (`Status: open`, `Status: fixed`, `Status: withdrawn` or `Status: accepted`), and comments follow, each under a `### <who>` line.
- Open a thread by creating `{mode}-<n>.md` with the next free number. Reply by appending a comment to the thread's file. Close a thread by changing its status line and appending a comment that gives the reason.
- Don't edit anyone else's comments, and don't write anywhere except {threads}/ and your report."""

REVIEW = """You're a reviewer I'm spawning as team lead.

Mode: {mode}
Department: code
Target: the PR in {target}/. pr.md is its description, revision {rev} is checked out in {target}/{rev}/, the base project is in {target}/base/, and {target}/{rev}.diff is the change.
Model slug: eval-model

{interface}

Post your review there, then write your completion report to {report} and return it to me."""

REVIEW_AGAIN = """You're a reviewer I'm spawning as team lead. This is a new round.

Mode: {mode}
Department: code
Target: the PR in {target}/, now at revision {rev}, checked out in {target}/{rev}/. pr.md is its description, the base project is in {target}/base/, {target}/v1.diff is v1 against the base, and {target}/{prev}-to-{rev}.diff is the change since {prev}.
Model slug: eval-model

You reviewed {prev} last round. Your completion reports so far: {prev_reports}.

{interface}

Post your review there, then write your completion report to {report} and return it to me."""

INQUISITIVE_EXTRA = "The other reviewers' findings are the threads in {threads}/."

RESPOND = """You're the {mode} reviewer on the PR in {target}/, at revision {rev}. I'm the team lead.

Mode: {mode}
Department: code
Model slug: eval-model

Your completion reports so far: {prev_reports}. Since your last report, others have replied on your threads.

{interface}

Respond on your threads, then write a short update to your completion report at {report} and return it to me."""

AUTHOR = """You're the author of the PR in {target}/. You've just pushed revision {rev}: {target}/{prev}-to-{rev}.diff is the change, and your note on it is: "{note}"

Reply once on every open thread in {threads}/ by appending a comment under a `### Author` line. Don't change any status line or anything else. Follow this stance on each issue:

{stances}

On any thread that matches none of these: {default}

Return a one-line summary per thread to me."""

WRAP_SKILL = """You are running one stage of a skill test. Do the task below exactly as a real agent would.

- Skill: read {skill}/SKILL.md and follow it, including the reference files it tells you to read.
- Read only {run}/ and the skill's own files. Don't read anything else under {skills}/.
- Put scratch work under /tmp. Never modify {run}/target/.

Task (the prompt you received):
\"\"\"
{task}
\"\"\""""

WRAP_BASELINE = """You are running one stage of a test as a baseline. Do the task below as a capable agent would, with no special instructions.

- Read only {run}/. Don't read anything under {skills}/ (in particular no SKILL.md files).
- Put scratch work under /tmp. Never modify {run}/target/.

Task (the prompt you received):
\"\"\"
{task}
\"\"\""""


def load_state(run: Path) -> dict:
    return json.loads((run / "state.json").read_text())


def save_state(run: Path, state: dict) -> None:
    (run / "state.json").write_text(json.dumps(state, indent=2) + "\n")


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(file.relative_to(path)).encode())
        digest.update(file.read_bytes())
    return digest.hexdigest()


def apply_diff(tree: Path, diff: Path) -> None:
    subprocess.run(["git", "apply", "--unsafe-paths", f"--directory={tree}", str(diff)], check=True, cwd="/")


def init(scenario_path: str, run_dir: str) -> None:
    scenario_file = Path(scenario_path).resolve()
    scenario = json.loads(scenario_file.read_text())
    run = Path(run_dir).resolve()
    if run.exists():
        sys.exit(f"{run} already exists")
    target = run / "target"
    fixtures = EVALS_DIR / scenario["fixtures"]
    shutil.copytree(EVALS_DIR / scenario["base"], target / "base")
    first = scenario["revisions"][0]
    shutil.copytree(target / "base", target / first["id"])
    apply_diff(target / first["id"], fixtures / first["diff"])
    shutil.copy(fixtures / first["diff"], target / f"{first['id']}.diff")
    shutil.copy(fixtures / "pr.md", target / "pr.md")
    shutil.copytree(fixtures / "seed-threads", run / "threads")
    (run / "reports").mkdir()
    save_state(run, {"scenario": str(scenario_file), "revision": first["id"], "target_hash": tree_hash(target)})
    print(f"Initialised {run} at {first['id']}")


def push(run_dir: str, rev: str) -> None:
    run = Path(run_dir).resolve()
    state = load_state(run)
    scenario = json.loads(Path(state["scenario"]).read_text())
    revision = next(r for r in scenario["revisions"] if r["id"] == rev)
    target, prev = run / "target", state["revision"]
    if tree_hash(target) != state["target_hash"]:
        sys.exit("target/ was modified; not pushing")
    shutil.copytree(target / prev, target / rev)
    diff = EVALS_DIR / scenario["fixtures"] / revision["diff"]
    apply_diff(target / rev, diff)
    shutil.copy(diff, target / f"{prev}-to-{rev}.diff")
    state.update(previous=prev, revision=rev, target_hash=tree_hash(target))
    save_state(run, state)
    print(f"Pushed {rev}")


def prompt(run_dir: str, stage: str, mode: str, config: str) -> None:
    run = Path(run_dir).resolve()
    state = load_state(run)
    scenario = json.loads(Path(state["scenario"]).read_text())
    rev, prev = state["revision"], state.get("previous")
    reports = run / "reports"
    prev_reports = ", ".join(str(p) for p in sorted(reports.glob(f"*-{mode}.md"))) or "none"
    values = dict(
        mode=mode, rev=rev, prev=prev, target=run / "target", threads=run / "threads",
        report=reports / f"{rev}-{stage}-{mode}.md", prev_reports=prev_reports,
    )
    values["interface"] = INTERFACE.format(**values)
    if stage == "review":
        task = (REVIEW_AGAIN if prev else REVIEW).format(**values)
        if mode == "inquisitive":
            task = task.replace("\n\nPost your review", "\n\n" + INQUISITIVE_EXTRA.format(**values) + "\n\nPost your review")
    elif stage == "respond":
        task = RESPOND.format(**values)
    elif stage == "author":
        revision = next(r for r in scenario["revisions"] if r["id"] == rev)
        author = scenario["author"]
        stances = "\n".join(f"- {s['issue']}: {s['reply']}" for s in author["stances"])
        print(AUTHOR.format(**values, note=revision["note"], stances=stances, default=author["default"]))
        return
    else:
        sys.exit(f"unknown stage {stage}")
    wrap = WRAP_SKILL if config == "with_skill" else WRAP_BASELINE
    print(wrap.format(task=task, run=run, skills=REPO_SKILLS, skill=REPO_SKILLS / scenario["skill_path"]))


def rule(run_dir: str, thread: str, status: str, text: str) -> None:
    path = Path(run_dir).resolve() / "threads" / f"{thread}.md"
    lines = path.read_text().splitlines()
    if status != "keep":
        lines[1] = f"Status: {status} (team lead)"
    path.write_text("\n".join(lines).rstrip() + f"\n\n### Team lead\n\n{text}\n")
    print(f"Ruled on {thread}")


def snapshot(run_dir: str, out_dir: str) -> None:
    run, out = Path(run_dir).resolve(), Path(out_dir).resolve()
    for name in ("threads", "reports"):
        if (out / name).exists():
            shutil.rmtree(out / name)
        shutil.copytree(run / name, out / name)
    print(f"Snapshot in {out}")


def check(run_dir: str) -> None:
    run = Path(run_dir).resolve()
    unchanged = tree_hash(run / "target") == load_state(run)["target_hash"]
    print("target unchanged" if unchanged else "target MODIFIED")
    sys.exit(0 if unchanged else 1)


if __name__ == "__main__":
    commands = {"init": init, "push": push, "prompt": prompt, "rule": rule, "snapshot": snapshot, "check": check}
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    commands[sys.argv[1]](*sys.argv[2:])
