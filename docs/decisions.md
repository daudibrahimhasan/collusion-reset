# Decisions and deviations

## Initial repository setup

Planning documents and empty implementation directories only. No pipeline, empirical results, dependencies or model access are implied. No license for original team contributions has been selected yet.

## Guru exposure-control addition

User requested implementation of Guru's suggestion before Emi/Guru review.
Added a provisional fifth arm, offline branching and review-gated message routing.
No live experiment, model calls or review approval is claimed. A matched neutral
replay changes only a designated peer-interaction segment; evidence changes fail
closed. Remaining exposure channels prevent interpreting this as no exposure.
The original four-arm primary comparison remains unchanged. Review checklist:
`docs/exposure-control.md`.

## Entry template

- Date:
- Decision or deviation:
- Reason:
- Owner and reviewer:
- Affected protocol version, code revision or run IDs:
- Consequence for interpretation:
- Status:

## 19 October 2026: measurement v2

Primary behavior and checkpoint are now valid, non-forced mutual ACCEPT.
The upstream message_type field is unrestricted and visible to the recipient,
so content length alone does not certify nondelivery or unsupported approval.
Agent instructions and transport remain unchanged; evidence compliance is a
separate, currently unadjudicated secondary outcome. Schema 2 / mutual-accept-v2
rejects legacy schema-1 inputs rather than silently reinterpreting them.
Retain fixture-002 and Chandni's PR #1 as legacy audit evidence, not v2 approval.
Recheck independent metrics after this change; do not rerun old data under a
new label without a separately documented reanalysis.

## 20 October 2026: implementation alignment, not protocol freeze

- Preserve Emi's agreed 15-pair schedule; PR #2 fixes only paths, import safety,
  overwrite protection and source validation. Seed, IDs, order and role assignments are unchanged.
- Export separate Reset Both minus Reset Alice/Bob fraction contrasts as proposed;
  Emi/Chandni still approve the estimand, sample scope and two-comparison inference plan.
- Preserve observed recurrence after later missingness; unknown earlier episodes make
  exact recurrence time unknown. Incomplete windows do not become negative observations.
- Resume remains unsupported. Partial live attempts remain incomplete and retained.
- Partial Groq tests did not complete an episode. No model competence, intervention
  effect, transmission or full-run token budget is established by those attempts.
