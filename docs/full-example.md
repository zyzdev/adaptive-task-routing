# Complete routing example

## 1. Request and first gate

> Inspect this app's slow startup and give me an improvement plan. Do not implement it yet. Use the adaptive-task-routing skill.

The agent performs the authorized read-only inspection first: it traces startup entry points, examines existing timing evidence, and presents a concrete improvement plan. The routers do not inspect the app themselves. Before the proposed implementation phase begins, the coordinator loads the context router and then the model router. Both modes default to `ask`. This example runs in an App whose orchestrator can create contexts but cannot change the current model or effort.

The following model names are **fictional test-fixture labels**, not installable models or real recommendations. The example runtime reports current `fixture-balanced` / `medium`, and lists `fixture-fast` and `fixture-balanced`, each supporting `low`, `medium`, and `high`.

Suppose the inspection finds serialized initialization and proposes three dependent changes: defer optional services, parallelize independent reads, and test startup ordering. The agent first explains that evidence and the complete improvement plan. It then identifies a substantial **next phase**: implementing and validating those changes. The context router finds recent requirements relevant and recommends staying in this conversation. The model router recommends more reasoning effort for that next phase. The routing note follows the plan:

```text
The inspection found serialized initialization. The plan is to defer optional services, parallelize independent reads, and add startup-ordering tests. No implementation has started.

---

### Adaptive Task Routing | Task resource guidance

The following recommendations assess the conversation, model, and reasoning resources for the next phase of the plan above.

Conversation setting
Recommendation: Stay in this conversation
Switch window: no
Recent requirements are still relevant.

Minimum sufficient AI setting
Model: fixture-balanced
Reasoning: medium
Enough to implement the defined edits and tests.

Recommended AI setting
Model: fixture-balanced
Reasoning: high
Upgrade value: medium; extra checking helps with initialization ordering and regression interactions.

If desired, choose high effort in the known App selector. I will stop here while you decide whether to adjust it or keep the current setting for the next phase.
```

Default `ask` ends the turn here even though the current pair might already be sufficient. The user can reply naturally; no fixed confirmation word is required. Advice does not authorize implementation, and the plan-only request does not start it.

## 2. User authorizes the next phase

> I selected high effort. Implement the plan.

The agent revalidates the current setting using runtime metadata if available; otherwise it records the user-provided value and its source without claiming independent verification. It does not repeat unchanged context analysis. A brief model note confirms the intended pair or reports any mismatch, then implementation proceeds under the user's authorization.

If the user instead says “Use the current setting and start,” that is also a valid natural response. If the App selector location is unknown, the agent describes the available control without inventing an exact menu path.

If the user had instead said only “What does deferred initialization mean?”, the agent would answer without starting another gate or implementing anything.

## 3. Completion

Before a demanding final interpretation of benchmark results, the model router may run again if the phase materially changes. When the agent finishes with a complete conclusion and no substantial next phase, it stops normally. No artificial next task or new window is proposed solely to keep routing active.

## Unknown configuration variant

If the host exposes neither current settings nor a model catalog, the model result still appears:

```yaml
skill: research-model-router
phase: proposed implementation and validation
current_configuration:
  model: unknown
  reasoning_effort: unknown
  evidence: unavailable
model_catalog:
  availability: unknown
  source: unavailable
  observed_at: unknown
  cache_scope: none
assessment: unverified
minimum_sufficient_setting:
  model: null
  reasoning_effort: null
  availability: unknown
  reason: No applicable catalog exists from which to name a supported pair.
recommended_setting:
  model: null
  reasoning_effort: null
  availability: unknown
upgrade_value: low
upgrade_reason: Capability cannot compensate for missing candidate evidence.
confidence: 0.30
mode: ask
disposition: awaiting_user_confirmation
```

This is not a claim that the current model is sufficient. On a host without an applicable bundled reference, the agent can request actual selector options once if selecting a configuration becomes necessary. On a recognized OpenAI surface with a matching unexpired bundled reference, it gives two concrete availability-unverified pairs without requesting a copied selector, then presents the surface-appropriate control as an option. A catalog alone must not be used to guess the running model.

## Context and executor variants

- With context `ask` and a `HANDOFF` recommendation, ask whether to move. A decline keeps work current; acceptance uses an available context-creation operation or provides a user action when none is callable.
- With context `ask` and an unresolved destination catalog, show the model gate as deferred, then evaluate it in the confirmed destination. Do not mark the gate complete.
- With both modes `off`, skip routing and its output. Model-off alone suppresses model recommendations while leaving the context router active.
- In a CLI with `auto`, each callable, authorized configuration operation may be executed and verified. An interactive command alone does not establish that capability. A failed automatic operation gets a manual fallback after one attempt.
- In an App with `auto`, an exposed context operation may run automatically while current-model or effort changes degrade to user action. Capability is resolved per operation, not from the App label.
