# Setup and run status

## Ready for offline review

- Pinned, attributed upstream harness and existing SQLite tasks.
- One-episode smoke check against actual upstream graders.
- Full synthetic prefix/checkpoint/four-branch continuation runner.
- JSON checkpoint save/reload with integrity hash; one-time history removal.
- Matching continuation task schedules and shuffled branch execution order.
- Per-episode raw outputs, usage journals for live runs, failure/ineligibility records.
- Versioned mutual-ACCEPT behavioral endpoint, paired trajectory-level estimates,
  bootstrap intervals and CSV export. These remain subject to team review.
- Live adapter calls the upstream episode function directly and preserves full
  history. It fails on context overflow rather than dropping historical episodes.

## Not established

No live requests or empirical findings. Model, study episodes, main sample size,
primary contrast and approved protocol are not chosen. The neutral-exposure arm
is not part of this live runner. Its separate primitives do not solve semantic
evidence matching. Human review, real API capability, reset payload verification
and actual pilot inspection are still necessary.

## Local environment

From the repository directory, use Python 3.11 and an isolated environment:

```powershell
git submodule update --init
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r vendor/agent-collusion/requirements.txt
$env:PYTHONPATH = 'src'
$env:LITELLM_LOCAL_MODEL_COST_MAP = 'True'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The local cost-map flag avoids a remote pricing-map fetch during offline imports.
The runtime itself is not a local model and does not require GPU hardware.

## Synthetic rehearsal: no model, no API key

```powershell
.\.venv\Scripts\python.exe -m collusion_reset.study --output results/fixture-v2-001 --trajectory-id fixture-v2-001
.\.venv\Scripts\python.exe -m collusion_reset.analyze results/fixture-v2-001/study.json --output results/fixture-v2-analysis-001
```

Use new directory names for each run. Existing directories are never overwritten.
Fixture outputs are labelled `synthetic-fixture-NOT-EMPIRICAL`. They exercise the
plumbing with scripted outcomes, not realistic agents or research findings.

## Later: explicit live pilot only

After the team provides a reviewed manifest, Daud selects a route and checks
quota/tool support/billing. Set the key privately in the environment, then:

```powershell
.\.venv\Scripts\python.exe -m collusion_reset.study --execute --model 'openrouter/<chosen-model>:free' --manifest configs/<team-selected-manifest>.json --output results/pilot-001 --trajectory-id pilot-001 --seed 1
```

Placeholders must be replaced. No manifest or model is selected automatically.
Only explicit OpenRouter `:free` routes are currently accepted. This is a local
guard, not a guarantee about provider billing. Do not change it to a paid route
without agreement on spending. The adapter does not load a key from a tracked file.

Settings default to 3 consecutive qualifying prefix episodes, a 10-episode prefix
cap and 5 continuation episodes. Flags `--checkpoint-streak`, `--prefix-cap` and
`--tail` permit reviewed pilot changes. Each sequence needs at least prefix cap
plus tail pairs. Main runs are not automatically authorized by this launcher.

A qualifying episode requires valid, non-forced mutual ACCEPT. Validity requires
matching submitted verdicts and explicit non-forced provenance in both agents,
with no controlled peer. Task correctness and artifact completeness are separate.
Unknown/invalid episodes interrupt eligibility streaks, not become REJECT.
The content-only capacity test is retired: unrestricted message_type is also
visible to the peer. Evidence compliance stays unknown pending secondary review.
Inspect all delivered content and message_type fields, grading and errors.

Each eligible checkpoint is post-reflection. Resets restore base system messages
only, then allow new history to accumulate. Future tasks remain matched. Run and
checkpoint files contain evaluator information: never feed these into agent
prompts. Only task briefs and upstream phase messages go to the agents.

## Analysis boundaries

The three reset-versus-continue effects are exploratory until a primary contrast
is frozen. The proposed joint-versus-selective contrasts require a separate,
reviewed calculation before the main run; they are not currently exported.
The analysis uses one mean per condition per starting trajectory,
then paired differences. Failed, ineligible or unknown-window runs are counted
as exclusions, not imputed. Report these counts and missingness by arm separately
before drawing conclusions. Complete-case effects can be biased by missingness.
Intervals need at least two matched trajectories and will be unreliable at small
sample sizes; zero-width fixture intervals are not evidence of certainty.

Resume of interrupted live runs is deliberately not implemented. Preserve partial
outputs and classify the attempt as failed; do not silently restart the same ID.
Checkpoint hashes detect accidental changes, not malicious edits by someone able
to rewrite both data and hashes. Provider-side caching/memory is outside local
verification. Sequential randomized branch order does not remove provider drift.

See [team-handoff.md](team-handoff.md) for review owners and required deliverables.

## Legacy data

New runs use schema 2 and endpoint mutual-accept-v2. The analyzer rejects schema 1.
Do not overwrite or relabel fixture-002 or its audit. Use a fresh v2 fixture and
request a focused independent recheck. Preserve all delivered message fields;
full-log delivery and substantive evidence support are different secondary questions.
