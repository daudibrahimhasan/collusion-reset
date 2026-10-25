# Evaluating a history reset

This checklist is an output of the Collusion Reset study, not a validated safety standard.
The recorded finding is immediate disruption followed by mutual-approval recurrence in
the second continuation episode of ten selected completed trajectories. It does not
establish a durable countermeasure, a transmission mechanism or general collusion.

## Before collection

- Define the measured behavior. Keep answer correctness, approval, evidence-policy
  compliance, explicit agreement and causal peer influence as separate outcomes.
- Freeze model, prompts, tools, every delivered message field, reward/feedback rules,
  checkpoint eligibility, branch order, stopping rules and the attempt budget.
- Keep an eligible checkpoint after feedback and both reflections. Preserve the exact
  source, configuration, histories and schedule hashes, including local changes.
- Use the same future task pairs in matched Continue, Reset A, Reset B and Reset Both
  branches. Verify that reset removes only the intended history and that new history
  accumulates independently after branching.
- Reserve development tasks for acceptance-positive and incorrect-answer controls.
  Include a same-information simple verifier where feasible. Do not count an offline
  relabelling of fixed answers as an interactive policy baseline.

## During collection

- Record every starting attempt and every failure/replacement. Keep scientific
  trajectory IDs separate from operational recovery/replay IDs and file copies.
- Record serialized requests, delivered content AND metadata, responses, forced flags,
  usage, errors and recovery decisions. A failed send is not delivered evidence.
- Keep a no-reset branch and observe several subsequent interactions. One immediate
  post-reset decision cannot establish durability. Randomize branch execution order
  in future experiments; the present study used a fixed order.
- Preserve unknown outcomes and unknown provider usage. Do not turn unavailable
  observations into negative results or reset cumulative accounting.

## Analysis and release

- Recalculate verdict outcomes from raw records. Check matched future tasks, the
  first eligible checkpoint, both reflections and branch-start history fingerprints.
- Audit evidence delivery before the recipient verdict, including retained peer
  messages and unmetered metadata. A literal-log check is not semantic adjudication.
- Use starting trajectories as the analysis unit; disclose schedule/task overlap.
  Report first and subsequent episodes separately. Treat schedule-weighting and
  leave-one-out checks performed after results as descriptive sensitivity analyses.
- Report all recoverable attempts and missing records. A directory census is not an
  exhaustive scientific-attempt denominator or a provider invoice.
- Preserve original human coding sheets, separate reviewer labels, prior-exposure
  limits, exact quotes and event IDs. Only call a disagreement resolved when the
  necessary human confirmations are recorded.
- Release the current manuscript, frozen-data index, audit scripts, source hashes,
  scope of independent review and remaining Not tested/Not verified items. Check links
  and exclude credentials from public bundles.

## Current reproducible checks

Place the accompanying audit folder under `AI Collusion Research Sprint/chat/` with
the original `collusion-reset/results/` tree beside `chat/`. From the audit folder:

```powershell
python -m unittest -v test_audit.py
python audit.py
```

These commands use Python's standard library, read existing records, and write derived
tables to their own audit folder. They do not import the experiment runner or make model
calls. They do not reconstruct missing historical records or reproduce provider internals.

Paper: https://docs.google.com/document/d/13M4jSqeIdnTwpCacIslNAg0oZRWv_03i-H7s4bMRaaY/edit

Reproduction index: https://drive.google.com/file/d/104L5hfjQudYtSDe_s0R2j6zD3OQsIdbx/view
