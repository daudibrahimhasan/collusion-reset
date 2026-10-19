# Episode selection handoff

Owners: Emi and Guru, with team review. The team chooses the episodes. These files
standardize the handoff; they do not select the research sample.

## Return these two files

1. Copy `configs/episode-selection.template.json` to `configs/pilot-001.json`.
   Replace all 30 placeholder IDs with existing upstream `data_search` task IDs.
   Keep the JSON keys and structure unchanged. First ID is A/Alice, second is B/Bob.
2. Copy the decision sheet below into a note. Keep rationale and review information
   out of the runnable JSON. Return both files to Daud.

The 15 pairs are an ordered schedule, not 15 independent trajectories. A prefix
can consume at most 10 pairs, followed by 5 continuations. If the checkpoint is
reached at episode 3, rows 4–8 become the continuations. Rows 11–15 are not fixed
continuation slots. All four branches reuse exactly the same next five pairs.

Do not repeat any task ID within a sequence. Both tasks must be data_search.
Use exact IDs from `vendor/agent-collusion/task/data-search/task_manifest_data_search50.json`.
Do not rewrite prompts, expected answers or database paths in the selection file.
The loader resolves those from the pinned upstream resources.

`configs/episode-selection.example.json` is a valid one-pair engineering example.
It is not a complete study schedule and is not approved as the research sample.
The 15-pair template deliberately contains placeholders and cannot run until filled.

## Decision sheet: copy and fill

Schedule ID: pilot-001
Purpose: pilot / main (choose one)
Prepared by:
Reviewed by:
Status: Draft / In review / Approved
Upstream revision: 5afb2c595aa3eff6b9b829a032f4f117b36ee54d
Manifest filename:
Number of pairs: 15 (provisional default)
Task type: data_search
Selection rule and reason:
Ordering rule and seed, if used:
Task IDs excluded and reasons:
Overlap with pilot or other trajectories:
Known task-difficulty or ambiguity concerns:
Reference grading checked: Not tested / Pass / Fail, with evidence
Model competence checked: Not tested / Pass / Fail, with evidence
Delivered-field/evidence audit: Not tested / Pass / Fail, with evidence
Endpoint version: mutual-accept-v2; content-only capacity is not a certificate
Unresolved questions:
Recommendation:

The three checks above can remain Not tested before model access. Do not invent
competence or evidence-length results from the task name. Do not select tasks
because they generate more mutual approvals. Freeze the selection rule before
the main outcomes. A valid manifest is not methodological approval.
