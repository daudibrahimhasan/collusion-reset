# Groq execution handoff

Status: local adapter prepared; live compatibility and final-study readiness are NOT established.
This supplements measurement-v2.md, not a new experimental protocol.

Live update (2026-10-19): partial Qwen task calls succeeded, but no complete episode
finished because of HTTP 429 input-token rate limits. The tested account reported
7,000 input tokens/minute. A paced partial sample used 13,697 total tokens across
three successful Alice task calls; this is NOT an episode budget. Preserve failed
smoke directories 001–004. Windows subprocess execution needs UTF-8 mode (`-X utf8`)
for upstream Unicode progress output. Credential errors now retain numeric HTTP
status while withholding raw provider error text. Full-run readiness remains blocked.

## Credentials

Edit the repository-root `.env` in a local editor. The empty file has been created.
`GROK_1` through `GROK_5` are user-requested names for **Groq** keys, not xAI Grok keys.
Only the slot named by `GROQ_KEY_SLOT` is used. Other slots are not a fallback pool.
Prefer each teammate retaining their own key locally. Only store keys you are authorized to use.
Never paste them into Discord, Google Docs, tracked files, screenshots, or results.
The `.env` is Git-ignored; `.env.example` contains placeholders only.
Existing shell variables take priority over the file.

Before setting `GROQ_FREE_TIER_CONFIRMED=true`, check that the selected account
has no paid billing enabled. This is a human confirmation, NOT an API billing check.
Groq model routes are not inherently free: account billing decides whether requests cost money.

`GROQ_MODEL=groq/qwen/qwen3.8-27b` is the proposed candidate, not a validated model choice.
`GROQ_MAX_REQUESTS=100` caps attempted completion calls per process/backend, not tokens.
It is a safety cap, not an estimate that an episode or trajectory will fit.
The adapter disables provider/outer retries for Groq, uses a 60-second request timeout,
and stops on failure without switching accounts or models. Upstream invalid/empty-output
handling may retry within its configured logic, but every completion attempt passes the cap.
Rate-limit failures are not experimental REJECTs. Preserve failed attempts and their logs.
Automatic resume is NOT implemented. Do not relabel a fresh rerun as continuation.

## Commands (PowerShell, repository root)

```powershell
$env:PYTHONPATH='src'
$env:LITELLM_LOCAL_MODEL_COST_MAP='True'
```

Offline tests, then configuration/task preflight (no inference):

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
.\.venv\Scripts\python.exe -m collusion_reset.run
```

One engineering episode, ONLY after credentials and free-tier access are checked:

```powershell
.\.venv\Scripts\python.exe -m collusion_reset.run --stage smoke --execute --output results/groq-smoke-001
```

Inspect `episode.json`, `metrics.json`, `settings.json`, and `usage.jsonl`.
Check tool execution, task correctness, voluntary verdicts, provider errors, tokens and runtime.
The default pair is an engineering check, not the team-selected study sample.

After installing and reviewing Emi's existing manifest as `configs/pilot-001.json`,
and only after the smoke passes, one pilot trajectory:

```powershell
.\.venv\Scripts\python.exe -m collusion_reset.run --stage trajectory --manifest configs/pilot-001.json --trajectory-id pilot-001 --seed 0 --output results/groq-pilot-001 --execute
.\.venv\Scripts\python.exe -m collusion_reset.analyze results/groq-pilot-001/study.json --output results/groq-pilot-analysis-001
```

Every output path must be new. Default trajectory settings remain 3 consecutive valid,
non-forced mutual ACCEPTs, prefix cap 10, and 5 matched continuation pairs across four arms.
Guru's additional exposure condition is still disabled, not silently included.

## Gates before the final cohort

- Credentials and actual account quotas; no account-rotation assumption.
- Emi's already-created 15-pair manifest installed and validated; obtain her existing sampling
  script for reproducibility. Do not ask her to redo her family/seed rationale.
- One measured live smoke, followed by a pilot including longer retained history.
- Salor's existing test source/logs and tested revision for independent reproduction.
- Chandni's focused v2 regression against the clean v2 fixtures; v1 audit remains completed.
- Freeze primary contrast, sample/attempt budget, seeds/task sequence, missing-data handling,
  token/request limits and stopping rules based on pilot feasibility BEFORE main runs.
- Review and commit this adapter so final outputs can identify a clean tested revision.
  No new changes have been pushed by this handoff.

No main-cohort automation, provider access verification, empirical findings or completed
final study is claimed. Run one trajectory at a time only after these gates; do not select
successful trajectories and discard failures. New branches and episodes are not independent
replicates. Account slot is recorded as operational metadata, never the key.

Provider references:
- https://console.groq.com/docs/tool-use/overview
- https://console.groq.com/docs/rate-limits
