# Chandani's Independent Fixture Analysis

**Historical schema-1 audit only.** The old capacity-based endpoint is retired:
`message_type` is also delivered without the content cap, so content length alone
cannot prove nondelivery or unsupported approval. This checker reproduces legacy
arithmetic, not evidence-compliance ground truth, and rejects schema-2 inputs.
Retained reports below are historical; do not use them as v2/live sign-off.
Use a new, nonexistent output directory for each reproduction.

**Purpose:** Independently recalculate metrics from the supplied synthetic `fixture-002` raw records and compare against `fixture-analysis-002`. This is a synthetic plumbing check, not empirical research.

## Inputs

- `fixture-002/`: `study.json`, `checkpoint.json`, `prefix-00.json` through `prefix-02.json`, and five JSON episode files each for `continue`, `reset_a`, `reset_b`, and `reset_both`.
- `fixture-analysis-002/`: pipeline-exported `episodes.csv` and `summary.json`.

Extract both uploaded ZIPs so the directory names exist. Do not edit the originals.

## Run

Requires Python 3.10+ and only the standard library. From this folder:

```bash
python independent_recompute.py \
  --raw-dir /path/to/fixture-002 \
  --reference-dir /path/to/fixture-analysis-002 \
  --output-dir ./results-reproduced
```

Example if both directories were extracted next to the script:

```bash
python independent_recompute.py \
  --raw-dir ./fixture-002 \
  --reference-dir ./fixture-analysis-002 \
  --output-dir ./results-reproduced
```

The script does **not** import the pipeline metric or summary functions. It reads raw episode JSON, independently derives verdict validity, the conservative raw-log capacity endpoint and task-correct flags, then compares these values against both `episodes.csv` and the stored per-episode metrics in `study.json`.

## Output guide

- `episode_comparison.csv`: one row per raw episode, including the three prefix episodes and 20 tail episodes.
- `reference_episode_comparison.csv`: raw-derived versus pipeline-exported metrics for the 20 tail rows.
- `trajectory_summary.csv`: per-condition counts, rates, first recurrence and three-episode streak timing.
- `condition_contrasts.csv`: reset-vs-continue and proposed joint-vs-selective contrasts. These are descriptive for the one synthetic trajectory only.
- `summary_comparison.csv`: field-by-field check of `summary.json` and study manifest summaries.
- `discrepancies.csv`: unresolved provenance and non-exported-contrast issues; a missing export is not automatically a numerical defect.
- `missing_fields.csv`: schema gaps, their impact and recommendations.
- `eligibility_error_usage.csv`: run/prefix/arm counts for eligibility, expected versus observed episode slots, invalid/unknown outputs, validation problems, and explicit availability status for error and usage telemetry.
- `eligibility_error_usage_tests.csv`: derived logic checks for the supplied complete fixture, a nonqualifying attempt, and an incomplete branch. Derived cases are test scenarios, not observed runs.
- `edge_case_tests.csv` and `derived_edge_case_fixtures/`: explicitly labelled derived copies testing missing verdicts, forced verdicts, mismatched submissions, and short/missing partner logs. Originals remain unchanged.
- `figure_specification.md`: proposed main-figure design for actual multi-trajectory data.
- `input_manifest.json` and `checklist.json`: input file hashes and high-level checks.
- `discrepancy_report.md`: concise review report.

The eligibility/error/usage ledger distinguishes actual recorded counts from absent telemetry. In particular, `NOT_RECORDED` means the fixture does not contain the field; it must not be interpreted as zero errors, zero tokens, or zero cost.

## Key limitations

1. All supplied endpoints are scripted as unsupported mutual approval. Identical 1.00 rates across arms do not demonstrate an intervention effect.
2. There is only one starting trajectory, so population uncertainty is not estimable.
3. `expected_verdict == "pass"` reproduces the fixture's task-correct flag, but the fixture uses placeholder task IDs and `answer: []`; actual correctness cannot be independently verified against the upstream grader using these files alone.
4. The old capacity rule compares only bounded content, omitting the unrestricted `message_type` channel. It does not prove that the full log was unavailable or that approval was unsupported.
5. `study.json` records the parent of review commit `2c0d060` and `code_dirty: true`. Obtain the dirty diff/snapshot or regenerate fixtures on a clean reviewed commit before claiming exact source reproducibility.

## Status

The fixture's exported metric values reproduced. The code-provenance issue and missing planned contrasts are recorded separately. These files do not approve a live pilot or freeze the research protocol.
