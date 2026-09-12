# Shared Runtime Routing Policy

This is the canonical runtime policy for every routing skill in this plugin. It is loaded by the skills, not enforced globally by a manifest. The coordinator loads the independent routers in order. During that coordinated run, neither child calls the coordinator or another child. If a host directly selects a child for a general task, the child's direct-selection guard may dispatch once to the coordinator; coordinator-delegated markers prevent recursion. Instructions alone do not guarantee implicit host invocation.

## Separate intent, capability, and decision

Resolve three layers independently:

1. `user_policy`: `off`, `ask`, or `auto` for each router.
2. `runtime_capabilities`: what each exact operation can do in the current surface, session, tools, and permissions.
3. `routing_decision`: what context or model configuration best fits the next phase.

The current conversation already has a context and model configuration. When routing is off, or when an enabled router recommends no change, use that current state without asking for a separate fixed strategy.

## Capability snapshot and revalidation

On first use in an environment, look for a capability snapshot in a host- or user-managed settings store. If no snapshot exists, it is stale, or its environment fingerprint no longer matches, detect each relevant operation and record the result when the host provides a suitable persistence mechanism.

Do not store mutable observations inside the installed plugin package. A snapshot is a cache, never authority. Record enough provenance to judge freshness: surface, host or plugin version when exposed, tool/capability fingerprint, observation time, evidence source, and confidence.

At each routing gate, perform only a lightweight freshness check. Re-detect the affected operations when the surface, session, host/plugin version, permissions, exposed tools, or operation result changes. A failed automatic operation invalidates that capability immediately. Do not repeat the same failed automatic operation in the same gate.

Detect operations separately; never collapse a whole App or CLI to one executor:

```yaml
runtime_capabilities:
  surface: identified surface or unknown
  create_new_context: agent | orchestrator | user_only | unavailable | unknown
  create_handoff_context: agent | orchestrator | user_only | unavailable | unknown
  switch_current_model: agent | orchestrator | user_only | unavailable | unknown
  set_model_for_new_run: agent | orchestrator | user_only | unavailable | unknown
  set_reasoning_effort: agent | orchestrator | user_only | unavailable | unknown
  evidence: runtime metadata | user-provided settings | cached observation | unavailable
  observed_at: timestamp | unknown
  confidence: 0.00-1.00
```

One surface may expose mixed capabilities. For example, it may allow an orchestrator to create a new context with a selected model while requiring the user to change the current model or effort. Preserve that distinction in both decisions and execution.

In-scope read-only metadata checks may establish capability. An interactive command, visible selector, or launch flag is not agent capability unless the agent can invoke the exact operation and verify its outcome. Unknown capability falls back to user operation.

## Dynamic model catalog

### Scoped discovery

Identify the product, interface/mode, execution host (local, remote, sandbox, unknown), and effective conversation separately. Do not infer capabilities from an App/CLI label or assume a phone/web client executes on that device. Read only the relevant [host discovery guide](host-discovery.md) when metadata is missing or stale. Use bounded, in-scope read-only checks before calling an accessible catalog unknown; record an unavailable tool or denied permission instead of bypassing it. Do not probe when routing is off.

For each observation retain `status`, `source`, `scope`, `observed_at`, and applicability to the effective context. Distinguish `not_probed`, `available`, `partial`, `unavailable`, `permission_denied`, `error`, `stale`, and `scope_mismatch`. A fresh read of old settings is still old evidence. Keep live configured values, last-persisted thread values, disk defaults and per-turn execution telemetry separate. Never fill unknown current fields with a catalog default or another process's settings.

Read access is not write capability. Do not start/resume a conversation, send a model prompt, install a hook, change configuration or attach an unrelated session just to discover settings. Do not print credentials, full settings, transcripts or unrelated thread identifiers. A provided helper may cause normal host cache/log activity; it is not a promise of zero host filesystem activity.

Treat the current configuration, available model catalog, and model capability evidence as separate observations. A catalog does not identify the running model.

Prefer model information in this order:

1. Current runtime metadata or a callable host catalog.
2. A user-provided selector inventory, clearly labeled as user-provided.
3. A versioned, expiring fallback registry, only when bundled or configured for that purpose.

Cache a runtime catalog for the current session or another explicitly short host-defined lifetime instead of fetching it at every unchanged gate. Refresh it on a new session, host or catalog change, a selector mismatch, an unsupported-model error, or expiry. Never treat a cached or fallback catalog as proof that a model still exists.

Keep the task-scoring rubric stable and model-neutral: difficulty, ambiguity, dependent reasoning, error cost, validation needs, latency, and compute preference. Map those needs to capabilities declared by the current catalog. Do not permanently assign scores to model names in user policy. If only identifiers are available and no reliable capability metadata or current fallback entry exists, do not invent a ranking or named recommendation.

### Capability evidence and task needs

Describe the upcoming task's capability and reasoning needs even if configuration or catalog discovery fails. This is task guidance, not proof that the current model is suitable. Every enabled model decision has two task-based outputs: the **minimum sufficient setting**, which is the least costly supported pair likely to meet the phase's quality and validation needs, and the **recommended setting**, which is the best-value pair after considering ambiguity, error cost, validation depth, latency and usage. They may be identical. Always state `upgrade_value: low | medium | high` and explain what additional result quality the recommended pair is expected to buy over the minimum; when the pairs are identical, upgrade value is `low`.

Map those needs to normal named settings after confirming destination availability when possible and always require relevant capability evidence. On a recognized OpenAI surface, a matching unexpired bundled registry may produce both named settings when runtime discovery cannot complete; its official cross-surface capability reference supports the recommendation, while account availability remains unverified. On Gemini CLI, its matching registry may recommend only the recorded stable aliases while leaving account-dependent backend resolution unverified. Do not ask the user to transcribe selector options before giving an applicable fallback recommendation. A fallback never authorizes or triggers a switch. If a model is known but its supported effort options are not, retain effort as `CURRENT` with an explicit unknown; do not invent an effort value.

Runtime descriptions are a starting point. When insufficient, consult the vendor's official documentation for the exact model and product, record URL/date/product scope, and label the resulting recommendation as an inference. Documentation can describe capability but cannot establish account availability. API pricing, reasoning options and model aliases do not automatically describe a ChatGPT/Claude/Gemini consumer or CLI product. Do not silently equate aliases, Auto routing policies or subagent settings with the main model's actual execution.

Reasoning output uses the destination's native configuration. Relative task-demand labels are never selector values by themselves. In Gemini CLI, show an observed `thinkingBudget` or `thinkingLevel` only when it is configurable for the effective session; otherwise show the localized equivalent of `model default`. Do not emit bare Codex effort labels as Gemini settings and do not guess a backend model behind an account-dependent alias.

Use relevant task evaluations when available; do not turn short descriptions into precise quality scores or claim an untested pair is optimal. Use the lowest effort likely to succeed for the minimum setting. Raise the recommended setting only when the task has concrete ambiguity, coupled decisions, difficult checking, high error cost, or useful parallel work that the stronger pair can address. Missing source data, unavailable history, unclear business rules, external bottlenecks, or deterministic execution often make upgrade value low because a stronger model cannot supply the missing evidence. Cache capability references with model/product/source/date and an explicit expiry (default at most seven days); recheck earlier on model, host or selector changes. Do not browse at every unchanged gate or require network access to complete useful routing advice.

### Capability-limited Codex discovery

Use the capabilities already available in the current execution. When the bounded Codex metadata helper succeeds, use its complete catalog and any matching live current configuration it can establish. When it reports `codex_state_unwritable` or `permission_denied`, stop after that attempt and use the matching unexpired bundled registry; do not interrupt the routing result to request broader read access. On a positively identified OpenAI surface, including ChatGPT desktop/web and Codex App/CLI, the registry may be used as a cross-surface recommendation reference because its capability descriptions cover those listed surfaces. Record only in structured evidence that account availability is unverified and that the inventory itself was observed in CLI; do not present it as live App metadata. Ignore unreadable current fields when forming the recommendation and omit them from the compact user-facing result. Do not turn a failed read, missing permission, or unresolved Codex surface into `CURRENT / CURRENT`, and do not ask for the selector inventory before recommending.

Permission escalation is diagnostic, not part of the default recommendation path. When a user questions the recommendation or explicitly requests an account-specific check, explain the actual evidence source, relevant dates, applicability limit, and task mapping. Then request narrowly scoped read permission at most once only if that permission unlocks a concrete same-surface `model/list` or equivalent path. Do not request generic permission that can only inspect another process or cannot reach the current selector. After a decline, continue with the fallback and do not repeat the request until the environment or explicit user intent changes.

Read capability and switch capability are separate. In `ask`, show the two settings and the surface-appropriate user control, then wait for the user's natural decision without requiring a fixed confirmation word. In `auto`, apply the recommended pair only when the exact model and effort operations are callable, authorized, and verifiable; otherwise retain the current setting, show the control as an optional action, and continue authorized work. ChatGPT desktop and web use their visible model/reasoning selector and must not be given the CLI-only `/model` command. Use `/model` only for an identified Codex CLI that documents it. Never claim a switch from catalog access alone.

## Resolve the mode and executor

- `off`: skip that router's evaluation and output; retain the current context or model settings.
- `ask`: evaluate and present both settings, then stop and wait for the user's natural response even when the current setting appears suitable. Retain the current setting unless the user explicitly requests a change. Provide an exact manual action when useful, but never require a fixed reply keyword. If a verified change is requested, perform each authorized operation when callable and verifiable.
- `auto`: evaluate and perform each permitted, callable, verifiable operation. Degrade unsupported, unavailable, or user-only operations to an optional user action while continuing authorized work with the current setting. Mixed capability may therefore produce a partially automatic result, but every reported result must identify what actually happened.

Only report `applied` after observing evidence that the host completed that exact operation. A direct user request to perform a particular host action is explicit authorization but still does not create missing capability.

Use these execution states consistently:

```yaml
execution:
  requested_owner: agent | orchestrator | user | none
  effective_owner: agent | orchestrator | user | none
  status: skipped | awaiting_user_confirmation | awaiting_user_action | applied | retained_current | blocked
  reason: concise explanation
  manual_action: null | concise surface-specific instruction
```

## Preferences and persistence

Use this precedence order:

1. Explicit instruction in the current user turn.
2. Host- or user-managed routing preferences.
3. Project-level routing preferences.
4. Packaged defaults.

Persist only the two modes, user preferences such as latency/cost emphasis, and cache records with provenance. Do not require a second fixed model strategy: the current conversation settings are the fallback. If no settings store exists, use packaged defaults and session-local observations without repeatedly asking onboarding questions.

## Interaction rules

- Present the requested findings or plan before routing advice. The recommendation governs the next substantial phase, not work already completed to produce the plan.
- In model `ask`, the routing note ends the turn and downstream execution waits for a natural user response. In model `auto`, apply or retain settings according to capability and continue.

- Keep stable context enums in structured evidence. In compact user-facing output, render the recommendation as a plain description in the user's language and omit the raw enum token.
- Combine pending context and model questions when both recommendations are reliable for the same effective destination.
- If the destination catalog is unknown, defer model selection visibly and evaluate it after the context is confirmed.
- `off` emits no result for that router. Every enabled model invocation displays model and reasoning effort, including `CURRENT`, unknown, and deferred states.
- Every enabled model invocation labels both the minimum sufficient and recommended settings, plus upgrade value and a task-specific reason. Do not collapse the result to one `CURRENT / CURRENT` line merely because current settings are unknown, and do not print unreadable current fields in the compact result.
- Keep diagnostic provenance in structured evidence. Unless the user asks for diagnostics, the compact result must not mention the probe, fallback/registry source, freshness, surface/account applicability, unreadable current values, confidence scores, internal assessment labels, or mode names. Do not justify the recommendation with discovery mechanics. State only the useful capability outcome: whether the setting was applied automatically or requires the user's control.
- When the user questions a recommendation, disclose its actual evidence and limitations. Offer one scoped permission request only if it can unlock a same-surface model read; otherwise do not ask for permission that cannot improve the result.
- Provide only controls actually known for the current surface. Do not fabricate menu names or commands.
- A recommendation attached to an improvement plan does not authorize implementation.
- Avoid repeated gates while phase, effective context, policy, capability snapshot, and catalog remain unchanged.
- Routing never expands task scope, permissions, or authorization for external side effects.
