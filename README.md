# Collusion Reset

Testing how selective history resets affect sustained mutual approval in LLM agents.

**Status: offline-tested study orchestration and an unvalidated live adapter.** Synthetic runs cover checkpoint save/reload, four reset branches, matched continuations and analysis. The live adapter is connected to pinned upstream code but has not made model requests. The exposure extension remains blocked. No empirical findings are claimed. Current endpoint is schema 2 / `mutual-accept-v2`; see [the measurement change](docs/measurement-v2.md).

## Research question

Once two agents repeatedly approve each other's work, does resetting one agent's history stop the pattern, or does retaining the other agent's history help it return? Evidence-policy compliance is a separate secondary question.

Working project title: **Does Replacing One Agent Break a Collusive Convention?** The core experiment tests history resets; replacing an agent with a different model is an optional extension and has not been implemented.

Prepared for the [AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25). Proposed primary track: Collusion Carriers and Countermeasures.

## Proposed experiment

Build on the peer-verification setting from [Shi et al., Emergent Collusion in Long-Horizon LLM Agent Interaction](https://arxiv.org/abs/2609.24967), with [upstream code](https://github.com/SALT-NLP/agent-collusion).

Agents complete separate tasks and evaluate each other's work. The protocol requires the complete execution log before approval. Restricted communication prevents complete log exchange, creating tension between protocol compliance and rewards for correct judgments.

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
