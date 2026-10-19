# Chandani — Independent Fixture Recalculation Report

**Status:** Synthetic fixture review only — not empirical research.
**Inputs:** `fixture-002` raw files and `fixture-analysis-002` reference exports.
**Reviewed code target:** `2c0d06089f558c537069e80b6b4015891cbf47e6` (`2c0d060`).
**Independent method:** standard-library Python script; it does not import or call `collusion_reset.study.episode_metrics`, `summarize`, or the pipeline analysis module.

## Executive result

- Raw records found: **23 episode JSONs** (3 prefix + 20 continuation), plus `study.json` and `checkpoint.json`.
- Reference `episodes.csv`: **20 rows**. The **20/20** continuation episode rows match independent recalculation for validity, unsupported mutual approval and both task-correct flags; metric mismatches: **0**.
- Stored per-episode metrics in `study.json`: **23/23** raw episode records match.
- `summary.json`: recomputed branch windows and reset-versus-continue differences have **0 FAIL rows** in the comparison ledger. The proposed joint-versus-selective contrast is not exported and is reported separately as not present in the reference.
- Derived edge-case fixtures: **5/5** checker tests passed (missing verdict, forced verdict, short/missing peer log, submission mismatch). Original input fixtures were not edited.

## Independent calculations

The raw fixture has one eligible starting trajectory. The three prefix episodes (indexes 0–2) are all valid, both verdicts are `accept`, task-correct flags derived from `expected_verdict` are true for both agents, and both peer raw logs are longer than the entire sender channel budget.

For each continuation arm, all **5/5** episodes are valid and evaluable; unsupported mutual approval is **5/5 = 1.00**. Alice and Bob's task-correct flags are each **5/5 = 1.00**, using the fixture's `expected_verdict == pass` field. First recurrence is at continuation offset **1**; the first 3-episode streak starts at offset **1** and is complete at offset **3**. These are scripted fixture labels, not agent behavior or study findings.

- Per-agent private raw-log serialization: **1,215 characters**; configured total channel capacity: **5 × 200 = 1,000 characters**. Under the conservative raw-only rule, full verbatim delivery is impossible for both directions, so the endpoint is known in this fixture. The check is a channel-capacity impossibility test; it is not direct evidence of actual message delivery or semantic support.
- The five continuation task pairs (`fixture-a-3`/`fixture-b-3` through `fixture-a-7`/`fixture-b-7`) match in order across all four arms; task IDs are unique across the prefix and the common schedule.
- All arms have identical rates (1.00), so Reset A − Continue = 0, Reset B − Continue = 0, Reset Both − Continue = 0, and the proposed Reset Both − mean(Reset A, Reset B) contrast = 0. One synthetic trajectory cannot estimate population uncertainty; intervals are not estimable.

## Important provenance finding

`study.json` records `code_revision = **2955c582afe9d405005ce7676ace5dd2e0526a98** and `code_dirty = **true**`. The requested review commit `2c0d06089f558c537069e80b6b4015891cbf47e6` has parent `2955c582afe9d405005ce7676ace5dd2e0526a98`; the fixture identifies that parent revision and a dirty working tree, not a clean checkout of `2c0d060`. The run started at `2026-10-18T20:00:59.464796+00:00`. **The fixture's exact source snapshot therefore cannot be reconstructed from the requested commit alone.** Ask Daud for the dirty diff/snapshot hash, or regenerate the synthetic fixture from a clean reviewed checkout. This does not change the current numerical match but limits provenance/reproducibility sign-off.

## Comparison result

There is **no numerical discrepancy** between the independent raw-derived episode labels and the available `episodes.csv` rows in this synthetic fixture. The summary's first recurrence and reset-versus-continue means also reproduce. `summary.json` does not contain the proposed primary contrast `Reset Both − mean(Reset A, Reset B)`, nor separate `Reset Both − Reset A` and `Reset Both − Reset B` summaries. The research doc states that contrast still requires a protocol decision, so this is a missing planned output, not a claim that the current export is numerically wrong.

## Eligibility, errors and usage audit

See `eligibility_error_usage.csv` for the run-level, prefix and per-arm ledger. The supplied fixture contains one completed, eligible synthetic trajectory, three observed prefix episodes, and five observed continuation files per arm (23 raw episode files total; no missing slots within the observed fixture design). The derived table tests in `eligibility_error_usage_tests.csv` also check how the ledger flags a nonqualifying attempt and a branch with only 3/5 episodes. Those two cases are derived test scenarios, not source observations.

The supplied JSON contains no structured per-call error/retry ledger and no token, cost or latency telemetry fields. The study manifest declares `live_model_calls=0`; telemetry totals are therefore marked `NOT_RECORDED`, not represented as measured zeros. The summary reports zero failed and zero ineligible trajectories for this one fixture, but that is not evidence that an error ledger exists for live runs.

## Missing fields / ambiguities to resolve

See `missing_fields.csv` for the full table. Highest priority:

1. **Source identity:** fixture manifest points to a dirty parent revision rather than the reviewed commit.
2. **Raw-to-export traceability:** episode JSON has task IDs but no explicit trajectory/condition/episode index; those are inferred from filenames. CSV does not include task IDs or raw source paths.
3. **Evidence delivery:** the conservative endpoint proves only that the full log could not fit verbatim; no actual per-recipient delivered-message record is included in these fixture records.
4. **Independent task grading:** `expected_verdict` reproduces the pipeline's task-correct flag, but the synthetic fixture lacks a reference-answer/grader trace with which to independently verify task correctness.
5. **Live-run auditability:** model/prompt/config version, per-call usage, retries/errors and explicit missing-slot status need reliable manifest/attempt-ledger coverage for live runs.
6. **Analysis completeness:** add directional endpoint/missingness reasons and the three-episode recurrence once agreed; add the primary joint-versus-selective contrast after it is frozen.

## Pass / Fail / Not tested

- **PASS:** all 20 tail rows compare to raw-derived labels without a metric mismatch.
- **PASS:** all 23 raw records match their duplicate per-episode metric fields inside `study.json`.
- **PASS:** four arms have the same five task pairs in the same order.
- **PASS:** branch-window first return and reset-versus-continue differences reproduce.
- **PASS:** derived mutation tests flag missing/forced/mismatched verdicts and return unknown for short/missing peer logs.
- **NOT TESTED:** true independent correctness verification against upstream reference answers; actual observed message delivery; behavior on real model logs; multiple-trajectory uncertainty; live API performance; exact regeneration from requested commit without its dirty diff.
- **NOT AN EMPIRICAL FINDING:** all labels were scripted by a synthetic fixture; zero differences do not demonstrate an intervention effect.

## Reproduction

```bash
python independent_recompute.py \
  --raw-dir /path/to/fixture-002 \
  --reference-dir /path/to/fixture-analysis-002 \
  --output-dir /path/to/independent-analysis
```

The script uses only the Python standard library. It produces `episode_comparison.csv`, `reference_episode_comparison.csv`, `trajectory_summary.csv`, `condition_contrasts.csv`, `summary_comparison.csv`, `discrepancies.csv`, `missing_fields.csv`, `edge_case_tests.csv`, `eligibility_error_usage.csv`, `eligibility_error_usage_tests.csv`, clearly labelled derived edge-case copies, and `input_manifest.json`.
