# Complete routing examples

These are designed UX examples, not model-test results. Model names below are fictional fixture
labels, not selectable product options. All routing notes follow the findings or actionable plan
requested by the user. Both routers use `ask` unless stated otherwise.

## Keep after a plan-only request

The user requests a startup inspection and improvement plan, without implementation. The inspection
finds serialized initialization. The observed `fixture-balanced / medium` meets the remaining
phase's quality floor; a higher task-fit effort offers too little benefit to repay setup costs.

```text
The plan is to defer optional services, parallelize independent reads and validate startup order.

---

### Adaptive Task Routing | Task resource guidance

✓ Keep current
The current setup meets the requirements; changing it offers little benefit for the remaining work.

Conversation: Stay here. Switch windows: No.
Current AI: fixture-balanced / medium.

The analysis and plan are complete. Implementation has not started.
```

No “keep current?” question is needed, and no implementation is authorized by retention.
When execution has already been requested, the ending instead identifies and performs the next
approved check. A completed plan is not a material routing blocker.

## Provisional retention

The catalog supports `fixture-balanced / high`, but the current model is unreadable. A bounded
check is already authorized and its results can be verified; no material quality blocker exists.

```text
---

### Adaptive Task Routing | Task resource guidance

Keep provisionally
The benefit of switching is not established; the bounded checks can proceed with validation.

Conversation: Stay here. Switch windows: No.
Task-fit setting: fixture-balanced / high; this is not a request to switch now.

Continuing the authorized checks.
```

If failed validation makes responsible progress impossible, replace this action with **Need your
decision**, name the blocking choice and ask one concrete question. Unknown metadata alone is not
such a blocker. Do not certify an unreadable pair as suitable.

## Change and mixed handoff

The current fixture model fails the next phase's quality requirement. A supported target has a
justified advantage. In `ask`, propose the change before applying it:

```text
---

### Adaptive Task Routing | Task resource guidance

Change AI setting
The next phase requires validation that the observed current setup has not handled reliably.

Conversation: Stay here. Switch windows: No.
Task-fit setting: fixture-balanced / high.

Would you like to apply this setting, or revise the next phase?
```

If a new conversation is also recommended, lead with **New conversation with handoff** and answer
“Switch windows: Yes, pending your decision.” Carry only the objective, confirmed findings, API
constraints, relevant artifacts and next step. Show destination settings only when supported
there; otherwise defer model selection explicitly. A retained model never settles the context
question. A clean start carries no old task-history handoff.

`auto` can apply only justified, authorized, callable and verifiable changes. Without those
controls, state the actual fallback rather than “applying.” Continue authorized work only if no
material quality or destination blocker remains. Explicitly accepted targets need no second
routing confirmation.

## Details and disabled components

A detail request reuses the gate and adds minimum needed, task-fit settings and upgrade rationale.
The internal `recommended_setting` name stays compatible. Switch scores and diagnostic provenance
are not ordinary detailed output. Context-off removes the entire conversation/window assessment;
Model-off removes model guidance and controls; both-off emits no routing note. Compact/detailed
are display preferences, not new modes.
