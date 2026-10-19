# Team handoff: what we need before the pilot

This is a proposed work split for Daud, Emi, Chandni, Salor and Guru. Confirm
availability and review the decisions together. Emi has supplied a pilot episode manifest; its sampling script handoff and the
final model/provider decision remain pending. Do not repeat completed assignments. A working pipeline is not evidence of a scientific finding.

## Shared task: choose episodes, not just a model

The team owns episode selection. Return an explicit manifest in the upstream format:

Use the [ready-to-fill guide](episode-selection.md),
`configs/episode-selection.template.json` (15 empty pairs) and
`configs/episode-selection.example.json` (one existing engineering pair).
Replace task-ID placeholders only; return the rationale as a separate note.

```json
{"pairs": [{"tasks": ["task_id_for_A", "task_id_for_B"]}]}
```

For the provisional 10-prefix + 5-continuation design, each trajectory needs at
least 15 pairs, or 30 distinct tasks. Use existing `data_search` tasks for this
first pilot. The loader rejects reused task IDs within a sequence. Do not choose
episodes based on which ones produce the desired result. Specify a reproducible
sampling rule and separate pilot and main manifests. Current SQLite pool has 50
tasks, so a pilot can fit, but task reuse across trajectories must be documented.
Reusing tasks across trajectories limits task-level generalization.

The earlier one-episode pair is an engineering example only. It is not the chosen
study sequence. The runner will not select live episodes automatically.

## Emi: definitions and study protocol

- Review `docs/protocol.md`, `src/collusion_reset/study.py` and checkpoint semantics.
- Decide if three consecutive eligible episodes, ten-prefix cap and five-tail
  window are suitable. Give reasons and alternatives, not an invented power claim.
- Review valid, non-forced mutual ACCEPT as the behavioral endpoint. Keep task
  correctness and evidence compliance separate. Content capacity no longer certifies
  nondelivery because message_type is unrestricted and visible.
- Specify recurrence (first return versus sustained return), missing-data policy,
  primary contrast and whether task failures should interrupt eligibility.
- Validate your original feasibility numbers with a runnable script, dataset
  revision, exclusions and denominator. Historical rates are not our pilot rates.

Return: a short protocol decision sheet, analysis script for feasibility, and the
episode-selection recommendation, paired with Guru.

## Guru: controls, closest work and episode selection

- Co-select episodes with Emi and return the manifest plus sampling rationale.
- Define the neutral-exposure comparison precisely: what changes, what stays,
  what counts as legitimate evidence, and what the newcomer can still infer from
  feedback, rewards, task messages and turn order.
- Provide matched message examples and a reviewable fixture specification. Do
  not claim that free-form messages can already be split reliably into evidence
  and interaction. That is unresolved.
- Check 3–5 closest studies and their code for mid-run resets/replacement and
  transmission controls. Return exact citations and “they test X; we test Y”.
- Propose a same-information simple baseline: current deterministic endpoint
  already avoids an LLM judge. State what any additional detector would add.

Return: exposure-control specification, closest-work table, explicit recommendation
to keep it blocked or implement it. Four core arms run without this extension.

## Chandni: independent analysis and log validation

- Review raw episode files, `study.json`, `checkpoint.json`, and CSV export.
- Recalculate the endpoint and paired effects independently, without importing
  our metric function. Compare your numbers with ours on synthetic fixtures.
- Check unknown/forced/missing outputs, attempts that never qualify, incomplete
  branches, task correctness and exclusion counts. Do not convert unknown to zero.
- Propose the main paired plot and an eligibility/error/usage table. Uncertainty
  must resample starting trajectories, not individual episodes.
- Flag small-sample limitations and task overlap. Three exploratory contrasts
  are not three independent confirmatory discoveries.

Return: validation script, discrepancy report and one figure specification.
No Streamlit dashboard or Postgres needed for this pilot.

## Salor: reset integrity and safe execution

- Test checkpoint restoration, source-checkpoint immutability, deep-copy branch
  isolation, one-time resets and restoration of system instructions only.
- Place unique canary strings in A/B historical messages, reflections and tool
  outputs. Verify absence in reset histories, preservation in retained histories,
  and no reintroduction through wrappers, logs, summaries or globals.
- Inspect the actual outbound message payload with an offline mocked completion
  hook. A clean Python list alone is not sufficient for live validation.
- Verify read-only SQLite access, credential exclusions, unique output directories,
  failure preservation and no paid fallback. No generated code tasks in this pilot.

Return: runnable tests and a pass/fail/not-tested acceptance report with evidence.
Do not label unexecuted tests passed. Provider-side memory cannot be verified here.

## Daud: implementation, integration and execution

- Maintain the pipeline, merge reviewed manifests and resolve discrepancies.
- Choose a model after team recommendations; confirm route, quota, tool calling,
  context/output limits, billing safeguards and runtime with a small live episode.
- Check live task competence, forced verdicts, truncation/context dropping,
  reflection completion and authoritative log sizes before the checkpoint pilot.
- Run a small approved pilot. Freeze prompts/settings/manifests/analysis and code
  revision before the main run. Preserve all attempts, including ineligible ones.
- Finalize sample size from pilot feasibility and precision, not target results.
- Integrate writing after validated results. Everyone drafts their own methods
  and limitations; Daud integrates/finalizes. Confirm paper lead together.

## What to send back to Daud/ChatGPT

Use this structure for each handoff:

1. Name and task.
2. Files or accessible links, exact versions/revisions.
3. What you checked and how to reproduce it.
4. Results with denominators, or “not tested”.
5. Problems and unresolved decisions.
6. Your recommendation and why.

AI tools are fine for understanding papers, drafting code and checking your work.
Verify their citations, code and numbers yourself. Never paste API keys or private
team data into prompts. Sharing a document is not proof its analysis was validated.

## Pilot go/no-go checklist

- [ ] Team-selected manifest and task-sampling rule approved.
- [ ] Definitions, evidence criterion and primary contrast reviewed by Emi.
- [ ] Model/API capability and zero-new-spend settings checked by Daud.
- [ ] Reset and outbound-context tests reviewed by Salor.
- [ ] Independent metric checks reviewed by Chandni.
- [ ] Guru's extension either reviewed and tested or explicitly excluded.
- [ ] Small live episode inspected, then checkpoint pilot inspected.
- [ ] Main-run scope, missing-data rules and analysis frozen before execution.

For expansion to 100 cases, use versioned manifests from a larger validated task
pool, audit task difficulty/evidence lengths, retain the same endpoint and paired
branch design, and report clustering/task overlap. The current 50-task pool does
not provide 100 independent task cases by itself.

## Completed work and v2 follow-up

Emi supplied the episode JSON and rule verification. Chandni supplied PR #1,
whose legacy fixture comparisons were reproduced; its provenance concern is valid.
Salor supplied a 27-test execution report; source/log handoff remains pending.
These are completed contributions, not requests for new reports. After v2 is
published, ask for a focused endpoint regression check, not a repeated full audit.
