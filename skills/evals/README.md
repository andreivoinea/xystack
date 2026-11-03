# Skill evals

Evals for every xystack skill live here, outside the skill folders, so installing a skill never ships its expected answers.

## Chained review scenarios

`review-with-mode` is tested with chained scenarios: a micro, a macro and an inquisitive reviewer review one PR together over two rounds, the way a team lead would run them. Between rounds, a scripted author pushes a new revision and replies on the threads. The team lead (whoever runs the scenario) rules from a script. Each scenario is graded twice: an **initial** grade after round 1 and a **final** grade after round 2. The final grade matters more.

- `scenarios/<skill>/<name>.json`: one scenario. It names its fixtures, its revisions, the author's stance on each issue, the team lead's rulings, and the `assertions` for each grade.
- `files/<skill>/`: fixtures. Each PR folder has `pr.md`, a diff per revision (`change.diff` for v1 against the base project, `change-v2.diff` for v1 to v2) and `seed-threads/`, comments a coworker had already posted before the review started.
- `chain.py`: the deterministic parts of a run. Run `python3 chain.py` for its commands.

### Running a scenario

A run folder holds `target/` (the base project, each revision and its diff, which reviewers must not modify), `threads/` (the review interface, one file per thread) and `reports/` (completion reports). Use one run folder per scenario and configuration (`with_skill`, `without_skill`).

1. `chain.py init <scenario> <run>`, which checks out v1 and posts the seed threads.
2. Round 1:
   1. Spawn micro and macro in parallel with `chain.py prompt <run> review <mode> <config>`.
   2. Spawn inquisitive with the same command.
   3. Spawn micro and macro again with `chain.py prompt <run> respond <mode> <config>`, but only those with new replies on their threads.
   4. Apply the scenario's `round-1` rulings with `chain.py rule`.
   5. Run `chain.py check <run>` and record whether `target/` is unchanged, then `chain.py snapshot <run> <out>` for the initial grade.
3. `chain.py push <run> v2`, then spawn the author with `chain.py prompt <run> author - -`. Then apply the `after-author` rulings.
4. Round 2: repeat round 1's steps 1–4 with the `round-2` rulings, then check and snapshot for the final grade.

Every spawned agent starts fresh; the threads and its earlier reports carry its state. A ruling whose condition isn't met is skipped. An escalation no ruling covers is logged in the run notes, not judged.

### Grading

Each grade is a test case in skill-creator's layout: `<skill>-workspace/iteration-<n>/<scenario>-initial/` and `<scenario>-final/`, each with `eval_metadata.json` and a `with_skill/` and `without_skill/` folder holding the snapshot in `outputs/` and `grading.json`. Keep the run folders in `iteration-<n>/chain-runs/` (not `runs/`, which the benchmark script reads as the test-case folder). A grader checks each assertion against the snapshot and records whether it passed, with evidence.

`<skill>-workspace/` folders are git-ignored.

### Known gaps

The scenarios don't yet isolate the configurations, reach fight-back or escalation, repeat runs, or grade blind, so treat their scores as a rough signal. The planned fixes are in issue #7.
