# Proposed Figure Specification — Main Outcome

**Purpose:** Show post-checkpoint unsupported-mutual-approval rate by condition (Continue, Reset A, Reset B, Reset Both).

**Mark:** One point per starting trajectory × condition, where the point is that trajectory's fraction of evaluable post-checkpoint episodes meeting the frozen endpoint rule. Connect the four within-trajectory points with thin lines to show the paired design. Overlay condition means and trajectory-level 95% uncertainty intervals using the team-approved method.

**Axes:** x = condition; y = unsupported-mutual-approval fraction (0–1). Show evaluable episode count / planned episode count under each condition, and report missing/invalid/unknown episode counts separately. Do not code missing/invalid episodes as zero.

**Endpoint prerequisites:** freeze whether unsupported approval requires only a valid agent-issued ACCEPT plus demonstrably unavailable complete evidence under the conservative capacity rule; preserve UNKNOWN where evidence status cannot be established. Keep task correctness and directional approvals in separate panels or supplemental tables.

**Inference:** resample/estimate uncertainty across independent starting trajectories, not episodes or branches. The present fixture has n=1 and all four rates equal 1.00; do not show a population confidence interval or interpret this fixture as a treatment effect. Treat this output as a code-path validation only. A secondary recurrence plot may show first recurrence and completion of a three-consecutive-episode streak on the five-episode horizon, with incomplete follow-up marked as indeterminate/censored under the frozen rule.
