---
name: adaptive-task-routing
description: Primary routing entrypoint for substantial multi-step coding, debugging, architecture, validation, research, and analysis. Use before broad execution or for an improvement plan's substantial next phase when both conversation context and model/reasoning should be assessed. Prefer this coordinator over either child router for general tasks. Skip brief explanations, status checks, tiny edits, and plugin-only questions.
---

# Adaptive Task Routing

Coordinate two independent decision skills. Do not choose a context, model, or reasoning effort yourself. Host-native startup context or prompt hooks may remind the model to invoke this entrypoint, but all eligibility and routing decisions remain in this Skill. Mentioning the plugin is not evidence that this Skill ran.

Read [references/zh-TW.md](references/zh-TW.md) when Chinese guidance is needed.

## Gate and controls

Identify the upcoming phase after a lightweight understanding of the request and a rough plan, before substantial execution. If a response delivers an improvement plan with a concrete substantial next phase, route that next phase before yielding even when its execution needs later approval. Do not invent extra work after a complete answer. Reuse a gate already completed for the same phase, context, catalog, preferences, and capabilities.

Read [shared policy](../../shared/runtime-routing-policy.md) and [defaults](../../shared/defaults.yaml). Resolve these paths from the directory containing this `SKILL.md`: the plugin root is three directories above this file, and shared resources are under `<plugin-root>/shared`, never `<plugin-root>/skills/shared`. Resolve the two user modes independently: `off`, `ask`, or `auto`. There is no third coordinator mode or separate fixed-routing policy. If both are `off`, skip routing, capability probing, and routing output. For one disabled router, skip its decision and continue with the other; the context stays current when context routing is off.

## Sequence

1. For an enabled context gate, load and follow [task-context-router](../task-context-router/SKILL.md) as a coordinator-delegated call. The generated Gemini package appends a dependency appendix to this file because one Skill activation grants access only to that Skill directory; when that appendix is present, use its complete context-router instructions directly and do not attempt a second Skill activation. Otherwise read the packaged child file or use the host-provided Skill resource. Supply the fact that the full coordinator is active so the child's direct-selection guard does not dispatch back. It alone owns `CURRENT`, `HANDOFF`, `CLEAN`, and any handoff. A later model-only phase transition can reuse the resolved context.
2. Resolve the effective working context under that router's mode. In `ask`, continue immediately when the recommendation is `CURRENT`; when a change is recommended, pause and ask whether the user wants it. If declined, retain the current context and continue. If accepted, perform callable and verifiable operations; for `user_only` parts, provide the necessary handoff and let the user resume naturally in the destination without requiring a confirmation word. If a destination is awaiting confirmation, combine recommendations only when its model options are known; otherwise report model routing as deferred pending destination confirmation, with currently observable model/effort or `unknown`. Recheck in the destination before execution.
3. For an enabled model gate, load and follow [research-model-router](../research-model-router/SKILL.md) as a coordinator-delegated call, explicitly supplying the resolved effective context so its direct-selection guard does not dispatch back. When the generated Gemini dependency appendix is present, use its complete model-router, host, registry, and shared-policy instructions directly. It alone owns model/effort judgment. Load the child even if the host did not independently select it. If neither packaged content, generated appendix, nor a host Skill resource is accessible, report that component as unavailable rather than inventing its result. Never synthesize a child result from the coordinator description or memory.
4. Present the two router results in one compact routing note. Put the context result first in its own localized conversation-setting block with a plain-language recommendation and an explicit yes/no answer for whether to switch windows. Keep `CURRENT`, `HANDOFF`, and `CLEAN` only in structured evidence; never show those English enum tokens in normal user-facing output. Then show the model router's minimum-sufficient setting, recommended setting, upgrade value, and actual next action. Omit unreadable current model/effort fields. An enabled model gate must not disappear just because both pairs match the current configuration. Explicitly report deferred or unavailable components. Do not label such a gate complete.
5. Continue authorized work or wait only for a decision the selected mode or task scope requires. A plan-only request authorizes routing advice, not implementing the plan. Revalidate before execution after a manual switch, changed environment, or materially revised plan.

During an active coordinated run, child routers do not call this coordinator or each other. A child selected directly by the host may dispatch once to this coordinator under its direct-selection guard; the coordinator-delegated marker prevents recursion. Read only the children needed for the gate, and reuse an already loaded policy without repeating identical work. Keep gate state in the current session and persist only capability/catalog cache records allowed by the shared policy; do not create persistent activity logs.

Identify the effective host surface once and carry that evidence into both children. For OpenAI surfaces, never default to Codex App merely because the prompt does not name the interface. If host metadata or the user does not identify CLI versus App, the model router must use the bounded automatic surface check in the OpenAI host guide before choosing a probe scope.

When combining results, preserve the model router's task requirements, discovery limitation and evidence scope in structured evidence. In the compact user-facing note, never surface the probe, fallback/registry source, freshness, account/surface applicability, or unreadable current values unless the user asks for diagnostics. Show only the localized conversation-setting block, the two AI-setting blocks, and the actionable capability outcome. Unknown current settings do not erase its capability recommendation. Distinguish a completed provisional assessment from a missing child or unresolved destination; do not convert the latter into `CURRENT`. Do not trigger model discovery when only context routing is enabled, and do not duplicate a child's probe.

For Traditional Chinese, use this compact conversation format before the two AI-setting blocks:

```text
【對話設定】
* 建議：留在目前對話
* 是否切換視窗：否
目前對話保留了完成下一階段所需的需求與證據，因此直接繼續。
```

Replace the values and explanation with the actual decision. Localize every label and description to the user's language. Render `CURRENT` as the local equivalent of “stay in this conversation,” `HANDOFF` as “switch to a new conversation with a concise handoff,” and `CLEAN` as “start a new conversation without the current context.” Do not append the enum token in parentheses. `HANDOFF` and `CLEAN` normally mean switching windows; `CURRENT` normally means staying, unless the host's concrete context operation requires a different presentation.

## Later phases and limitations

Revisit model routing when implementation becomes validation, a pilot expands, mechanical processing becomes interpretation, or difficult evidence synthesis begins. Revisit context routing only when there is also a genuine context boundary. Do not repeat a routing note on every tool call or unchanged follow-up.

Resolve every host operation separately. A desktop/web/mobile App may allow automatic context creation while keeping current-model or effort changes user-only; a CLI can also expose mixed capabilities. Act only through available, authorized operations and verify the outcome. An interactive command intended for the user is not agent capability. Shared settings and injected reminders are instructions, not proof that the host invoked the Skill; the packaged host integrations make the reminder deterministic where those integrations are supported.
