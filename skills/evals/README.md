# Skill evals

Evals for every xystack skill live here, outside the skill folders, so installing a skill never ships its expected answers.

- `evals.json` has one entry per skill under `skills`, each with a `skill_name` and its `evals`, in the [agentskills.io format](https://agentskills.io/skill-creation/evaluating-skills).
- `files/<skill>/` holds each skill's fixtures. Paths in `evals.json` are relative to this folder.

Each eval has:

- `prompt`: what the agent receives, written the way a real caller would ask.
- `expected_output`: a plain description of a good result, for whoever reviews the run.
- `files`: the fixtures the agent needs.
- `assertions`: pass/fail statements about the output. A grader checks each one against the run's output and records whether it passed, with evidence.

Run outputs go in a `<skill>-workspace/` folder, which git ignores.
