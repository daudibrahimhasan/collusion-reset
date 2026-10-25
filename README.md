# Collusion Reset

## Collection closed and paper phase 24 October 2026

The current status is [paper phase](docs/paper-phase.md). This supersedes all
historical launch/status notes below. **Do not start new model calls.**

T1–T10 completed 120 paired episodes. Independent numerical review covers all ten
trajectories and all 240 task answers. The original eight-run subset remains
distinguished from the post-results T9/T10 expansion. Human agreement coding
covers T1–T8 only, with 93/96 matching labels and three unresolved cases.
P1, P2–P5 and P6–P10 are separate exploratory cue-probe designs, not additional
reset trajectories. All probe verdicts were REJECT in both conditions.

The supported main finding is temporary interruption followed by recurrence of
mutual approval. Neither proven collusive agreement nor general absence of
transmission is established. Preserve failed attempts and experimental chronology.

Raw data, API credentials, account budgets and generated archives are not published
in this repository. Historical runbooks and operational limits are not current
launch authorization.

## Manuscript and preexisting work

The manuscript is **Does Resetting One Agent Break Mutual Approval? A Matched
History-Reset Study of LLM Agent Pairs**.

- [Manuscript](https://docs.google.com/document/d/13M4jSqeIdnTwpCacIslNAg0oZRWv_03i-H7s4bMRaaY/edit)
- [Full manuscript PDF, 25 October 2026](https://drive.google.com/file/d/1I4PJOOSX-adaQlrFUWe7uix5SYjfGAmO/view)
- [Reproduction and review index](https://drive.google.com/file/d/104L5hfjQudYtSDe_s0R2j6zD3OQsIdbx/view)

Pipeline development and the original T1–T8 collection were initiated before the
23–25 October 2026 sprint. The later T9/T10 expansion, cue probes, independent
reviews and manuscript preparation extend that preexisting project. The full
implementation and all collection are not claimed as work completed during the
sprint weekend. Upstream code and task data are credited separately in the paper.

Use the reproduction index for source supplements and historical evidence; the
current repository alone does not authenticate every past execution state.

## Current execution: Modal native 32K, 22 October 2026

Read [the current runbook](docs/current-modal-run.md) first. It supersedes the
historical development status and launch commands below. Main collection is
running; T1 has completed all four reset arms. Independent live-result validation
is still pending. No scientific effect is claimed from execution alone.

Both agents use Modal `deepseek-ai/DeepSeek-V4.1-Flash`, native tools, high
reasoning, temperature 1.0 and a uniform 32,768 output-token cap. Account and
model remain fixed within a trajectory. Preserve all historical evidence.

## Current development protocol: v7, 21 October 2026

Use [protocol-v7.md](docs/protocol-v7.md) for the fixed free routing policy and validation gates, and [protocol-v6.md](docs/protocol-v6.md) for tagged-text verdict handling. Older commands and status sections below are historical where they conflict with v7. Historical Episodes 1-4 are development evidence; Episode 4 used a labeled JSON-verdict recovery. The failed fresh v5 JSON and interrupted v6 tagged-text pilots are retained separately. The fresh consistent-interface, fixed-routing v7 pilot completed without a qualifying checkpoint. No main study or intervention effect is claimed, and local changes are not yet pushed.

Testing how selective history resets affect sustained mutual approval in LLM agents.

**Status: main-study launch blocked.** The fixed-policy screen passed 12/12. The fresh five-episode v7 pilot completed all ten task answers correctly; both agents rejected in Episodes 1-4 and both accepted in Episode 5. It did not meet the unchanged three-consecutive-mutual-ACCEPT checkpoint, so no live reset branches ran. Known pilot usage: 4,202,735 tokens; 12 failed calls have unknown usage. Offline orchestration and actual saved-history reset audits pass; these do not replace eligible live branch validation. The exposure extension remains blocked. Current endpoint is schema 2 / `mutual-accept-v2`; analysis version is `paired-reset-v3`. See [the measurement change](docs/measurement-v2.md).

## Research question

Development follow-up: the approved E6-7 extension completed, both with Alice REJECT / Bob ACCEPT. No checkpoint formed within seven episodes. Extension usage was 3,846,202 reported tokens (combined pilot plus extension: 8,048,937). Three additional failed calls have unknown usage. No reset branches or main collection started; the original five-episode result is preserved.

Once two agents repeatedly approve each other's work, does resetting one agent's history stop the pattern, or does retaining the other agent's history help it return? Evidence-policy compliance is a separate secondary question.

Working project title: **Does Replacing One Agent Break a Collusive Convention?** The core experiment tests history resets; replacing an agent with a different model is an optional extension and has not been implemented.

Prepared for the [AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25). Proposed primary track: Collusion Carriers and Countermeasures.

## Proposed experiment

Build on the peer-verification setting from [Shi et al., Emergent Collusion in Long-Horizon LLM Agent Interaction](https://arxiv.org/abs/2609.24967), with [upstream code](https://github.com/SALT-NLP/agent-collusion).

Agents complete separate tasks and evaluate each other's work. The protocol requires the complete execution log and concrete support for correct completion before approval. Message content is restricted, but the upstream `message_type` field is not; content limits alone do not establish that complete log exchange is impossible. Mutual approval, evidence compliance and task correctness are separate outcomes.

At a predeclared checkpoint, branch the same interaction into four conditions:

| Condition | Agent A history | Agent B history |
| --- | --- | --- |
| Continue | Retain | Retain |
| Reset A | Reset | Retain |
| Reset B | Retain | Reset |
| Reset both | Reset | Reset |

Guru's suggestion adds a provisional fifth arm: **Reset B + matched neutral peer
interaction replay**. Compare it with normal Reset B. Live use is blocked pending
Emi/Guru's review of evidence matching and remaining exposure channels. See the
[implementation and review checklist](docs/exposure-control.md).

All branches receive the same future task pairs, rules, reward definition and communication limits. A history reset must not remove current task information or leak old context through summaries, caches or shared mutable state.

Primary question: how does post-checkpoint mutual ACCEPT differ between joint and selective resets? Report each single-reset comparison separately. The independent unit is the starting trajectory, not its branches, episodes or model calls.

**Unsupported approval is a protocol violation, not automatically an incorrect answer or proof of agreement.** Stronger interpretations require evidence of peer influence and appropriate controls.

See the [proposed protocol](docs/protocol.md) and [team workflow](CONTRIBUTING.md). Settings remain provisional until pilot validation and protocol freeze.

## Repository layout

```text
configs/         Provisional five-arm pilot plan
docs/            Protocol, decisions and research notes
src/             Study runner, live adapter, grading checks and analysis
tests/           Offline orchestration, adapter and isolation tests
data/            Data-handling guidance; raw runs are not committed
results/         Guidance for validated analysis outputs
```

## Getting started

Use the [setup and run guide](docs/setup-and-run.md) and
[team task handoff](docs/team-handoff.md). The team will select study episodes;
the live runner requires an explicit manifest and model.

Start with the [real two-task smoke check and explicit live launcher](docs/one-episode.md).
For bounded free-route diagnostics, see the [recovery pilot and competence gate](docs/recovery-pilot.md).
The upstream is a pinned Git submodule; initialize it before running the tests.
Run the offline tests using the command in [the exposure-control guide](docs/exposure-control.md).
First establish model access and validate faithful checkpoint restoration, branch
isolation and deterministic grading. Do not assume a free chat interface supplies
automated API access.

Keep the first implementation small: one model, SQLite data-search tasks and four history conditions. No dashboard or additional database service is required for the core study. No paid inference or automatic paid fallback is authorized under the current zero-new-spend constraint.

## Team

- **Daud:** pipeline, execution and scientific integration.
- **Emi:** methodology, endpoint definitions and behavioral interpretation.
- **Chandni:** log processing, analysis, figures and result ledger.
- **Salor:** security testing, reset-leakage and branch-isolation checks, safe execution and credential handling.
- **Guru:** exposure controls, closest-work review and episode selection with Emi.

These are proposed work packages; each member should confirm availability and ownership. Everyone can contribute related work, model suggestions, interpretation and paper writing.

## Reproducibility and attribution

Record exact model routes, prompts, code revisions, seeds where supported, attempted-run counts, errors, usage and deviations. Keep raw outputs immutable and trace every reported number to validated analysis.

This repository is an independent extension, not the upstream implementation.
The original harness and tasks are referenced through the pinned
`vendor/agent-collusion` Git submodule, retaining its MIT license and attribution.
Our initial repository setup contained no upstream code; the task smoke adapter
now uses that submodule. Distinguish pre-sprint preparation from sprint work.

## Safety and limitations

Use synthetic tasks and avoid real sensitive data. Never commit credentials, private messages or unreviewed raw logs. Model-generated executable code requires an appropriate sandbox before execution.

This study cannot establish general prevalence of collusion, hidden intent, or the effectiveness of model replacement from history-reset results alone. No findings are claimed at this stage.

## Groq local run setup

The local `.env` has five empty `GROK_1` ... `GROK_5` slots for **Groq** keys.
Select one with `GROQ_KEY_SLOT`; there is no automatic account fallback.
See [the Groq runbook](docs/groq-runbook.md) for offline preflight, smoke/pilot commands,
safety limits and the remaining final-study gates. Live access is not yet validated.
