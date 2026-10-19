# Source and Scope

Current scope clarification (20 October 2026): this is a legacy schema-1 arithmetic
audit. Its capacity-based classifications are not valid evidence-policy certificates.
Schema-2 mutual-accept-v2 and subsequent analysis require a separate focused check.
Existing result files are preserved unchanged as the record of the original audit.

- Requested review commit: `2c0d06089f558c537069e80b6b4015891cbf47e6` in `daudibrahimhasan/collusion-reset`.
- The raw fixture's `study.json` declares `code_revision=2955c582afe9d405005ce7676ace5dd2e0526a98` and `code_dirty=true`. That SHA is the parent of the requested review commit. Exact generation from commit `2c0d060` is therefore not verified; request the dirty diff/snapshot or regenerate the fixture from a clean checkout.
- The checker was written as a standalone Python standard-library script and does not import `collusion_reset.study.episode_metrics`, `summarize`, or other pipeline metrics.
- Raw fixture and reference-analysis ZIPs are intentionally not duplicated in this bundle. Supply the two extracted directories via CLI arguments as documented in README.md.
- The eligibility/error/usage ledger labels missing error/retry and token/cost/latency telemetry as `NOT_RECORDED`; missing telemetry is not treated as a zero value. It also includes derived logic tests for a nonqualifying attempt and an incomplete branch.
- All results are synthetic, not agent/model findings.
