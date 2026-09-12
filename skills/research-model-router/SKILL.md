---
name: research-model-router
description: Model-only child router for substantial coding, debugging, architecture, validation, research, or analysis. Use when the user explicitly asks only for model/reasoning advice, when adaptive-task-routing delegates with a resolved context, or at a later model-only phase transition. For a general task needing both context and model routing, dispatch to adaptive-task-routing instead. Skip ordinary chat and tiny operations; do not choose context.
---

# Research Model Router

Match an upcoming work phase to enough model capability for reliable work without unnecessary time or compute. The historical name is retained for compatibility; the scope includes implementation and validation as well as research and analysis. This skill routes configuration; it does not perform the task itself.

For Traditional Chinese guidance, read [references/zh-TW.md](references/zh-TW.md) only when the user prefers Chinese or the Chinese explanation is needed.

## Required shared runtime policy

Before making a routing decision, read and follow [../../shared/runtime-routing-policy.md](../../shared/runtime-routing-policy.md) and [../../shared/defaults.yaml](../../shared/defaults.yaml). They define environment detection, preference precedence, executor selection, persistence boundaries, and fallback behavior for every router in this plugin.

If the host cannot load a plugin-level reference, preserve these minimum invariants: separate user intent from runtime capability; lightly revalidate capability at every routing gate; treat saved capability as a non-authoritative hint; default unknown capability to user operation; and claim `applied` only after verified host execution.

## Direct-selection dispatch guard

Before doing model discovery or emitting output, determine why this Skill was loaded. Continue locally only when the user explicitly requested model/reasoning-only routing, the `adaptive-task-routing` coordinator supplied a resolved effective context and marked this call as coordinator-delegated, or a previously completed coordinator gate is being revisited for a genuine model-only phase transition. For any general substantial task where Context and Model routing have not both been resolved, stop this child workflow, read [adaptive-task-routing](../adaptive-task-routing/SKILL.md), and follow that coordinator once. Do not emit a standalone model result before dispatch. Pass an internal `delegated_from: research-model-router` marker; when the coordinator reads this Skill again with its coordinator-delegated resolved-context marker, continue here and never dispatch again.

## Routing gate

Run after the rough plan and effective working context are known, before costly research, large data work, implementation, debugging, architecture work, or validation. A caller can supply the resolved context. Direct use stays model-only only under the direct-selection guard above.

When delivering an improvement plan with a concrete substantial next phase, include a model/effort recommendation for that phase before yielding, even if execution awaits approval. Advice does not authorize implementation. If a final answer has no substantial next phase, do not invent one or add a new routing gate just to end the response. Before difficult final evidence synthesis, route before doing that synthesis.

Re-run only at a meaningful stage transition: pilot to expanded workload, retrieval or execution to interpretation, robustness or adversarial testing, routine transformation to difficult reasoning, or final evidence synthesis. Do not re-route for every tool call or ordinary chat.

## Decide

First describe `task_requirements`: the phase's capability needs, relative reasoning demand, quality/validation needs and latency/usage constraints. This judgment does not depend on knowing the current model. Then produce two independent task-based results: `minimum_sufficient_setting`, the least costly pair likely to meet those requirements, and `recommended_setting`, the best-value pair after considering ambiguity, error cost, validation depth, latency and usage. The two pairs may be identical. Always give `upgrade_value` (`low`, `medium`, or `high`) and a concrete `upgrade_reason` describing what the recommended pair is expected to add over the minimum. Do not suppress useful task guidance when discovery is incomplete.

When observations are missing or stale, follow the matching [host discovery guide](../../shared/host-discovery.md). Resolve `../../shared` from the directory containing this `SKILL.md`: it is `<plugin-root>/shared`, not `skills/shared`. In a permitted Codex environment the guide links to [the optional read-only probe](scripts/probe_codex.py); do not run that helper on Claude/Gemini or assume ChatGPT has access to the user's CLI. Excluding a subagent menu only rejects that source: continue to an applicable host read path or fresh, scoped observation. Do not conclude that the main-context catalog is unavailable merely because the visible menu is for subagents. If the Codex helper identifies a project-sandbox state-access failure, stop after that attempt and follow the host guide's versioned bundled-registry fallback without requesting extra read permission. In a positively identified OpenAI host, including ChatGPT desktop/web and Codex App/CLI, unavailable runtime metadata does not suppress the two concrete settings: use the unexpired bundled registry as a cross-surface recommendation reference and label account availability `unverified` only in structured evidence. Its CLI observation proves availability only for that observed CLI, while its dated official capability source supports recommendations on the listed OpenAI surfaces. Do not ask the user to transcribe selector options before giving those recommendations. Record any attempted read and outcome before falling back. Prefer an applicable runtime catalog, use official model descriptions only as scoped capability evidence, and use relevant task evaluations when available. Keep inferred recommendations distinct from measured results.

For verified runtime decisions, recommend only a `model` and `reasoning_effort` supported by the current environment. For a matching unexpired registry fallback, recommend only pairs recorded in that registry and label their account availability `unverified`. Never invent identifiers.

Resolve the catalog's scope instead of copying a probe's initial `unverified` label. Follow the host guide's surface-specific invocation and criteria. In an identified Codex CLI task, invoke the helper with `--surface codex-cli`. When CLI versus App is not explicitly identified, invoke it with `--surface auto`; do not guess App. Automatic detection may use a standalone CLI process ancestor or the exact thread's stable `source: cli` when tool isolation hides that ancestor; the latter identifies the interface without treating saved model/effort as live. Accept a fresh successful CLI catalog marked `applicability: verified` unless positive evidence shows an availability-changing launch mismatch. The helper's separate process, unreadable live settings, absence of an App bridge, or inability to prove that no hidden override exists must not invalidate that CLI catalog. Runtime descriptions and supported effort options can support a capability-based recommendation without benchmarks. If scope is still unresolved, name the actual conflicting evidence; neither unknown current values nor an unrelated failed metadata read is a catalog failure.

Judge technical difficulty, ambiguity, dependent reasoning steps, evidence volume and heterogeneity, validation needs, consequence of subtle errors, synthesis or critique demands, latency and compute cost, and whether the phase is execution-heavy or interpretation-heavy.

- Prefer fast, economical settings for clear retrieval, formatting, extraction, and deterministic transformations.
- Prefer balanced settings for ordinary multi-step research and analysis.
- Prefer stronger capability and higher effort for ambiguous methodology, difficult synthesis, robustness review, consequential conclusions, or tightly coupled technical decisions.
- Lower the setting again after the demanding phase ends.
- Treat missing source data, unavailable history, unresolved definitions and external bottlenecks as limits on upgrade value: more model capability cannot manufacture evidence.

Treat model and effort as a pair. Use the lowest effort likely to satisfy the task for the minimum setting. A stronger model does not automatically require maximum effort, and most tasks do not require `max` or `ultra`. If the current pair is known and suitable, list that observed pair by name in the two setting blocks and retain it; do not hide the concrete recommendation behind `CURRENT / CURRENT`.

Read current configuration and available options separately from exposed runtime metadata or user-provided settings. A catalog of supported models is not evidence of which model is running. Mark each unreadable current field `unknown`; use `unsupported` only when the host confirms that reasoning effort is not configurable.

Resolve the recommendation independently of whether it can be compared or applied:

| Available evidence | Decision |
| --- | --- |
| Applicable candidates, supported effort options and capability evidence are sufficient; current pair is unknown | Give concrete minimum and recommended pairs. Current values and whether a switch is needed remain unknown. Do not substitute `CURRENT / CURRENT` solely because live settings cannot be read. |
| Current pair is known and supported by capability evidence | Give both task-based pairs by their concrete names, compare the observed pair with them, and assess switching value. Retain the current pair when justified. Recommend an alternative only with sufficient evidence. |
| A model recommendation is supported, but its effort options are unknown | Give the model in both blocks, retain effort as `CURRENT`, and explicitly report the unknown effort options. Relative task demand is not an invented selector value. |
| Runtime discovery is blocked on a recognized OpenAI surface, but the unexpired bundled registry has model descriptions and effort options | Stop after the failed read and give concrete minimum and recommended fallback pairs without asking the user to transcribe the selector. Treat the registry as cross-surface recommendation evidence, while keeping account availability and current settings unverified. Apply only through independently verified switch controls in `auto`; otherwise present the surface-appropriate user control and wait for the user to adjust or choose to continue. |
| Relevant bounded discovery leaves insufficient catalog or capability evidence to choose a pair, and no recognized-product bundled reference applies | Show task requirements, the attempted source and outcome or concrete access limitation, and the missing evidence. Provisionally retain `CURRENT / CURRENT` with `assessment: unverified`, or ask once for selector options when an exact choice is necessary. Do not call this proof of suitability. |

Lack of an automatic switching tool affects execution, not the ability to recommend evidenced pairs. `upgrade_value` compares the recommended pair with the minimum sufficient pair, never with an unknown current setting. In `ask`, ask the user to use the recommended pair when the current pair is unknown; do not describe it as an upgrade or downgrade from the unknown setting.

## When the user questions a recommendation

Do not request broader read permission during the normal fallback path. If the user says the recommended model or effort looks wrong, asks why it was chosen, or explicitly requests an account-specific check, then disclose the useful diagnostic facts: whether the recommendation used runtime data or the bundled reference, the reference observation and expiry dates, that account availability is unverified when applicable, and the task factors that led to both pairs.

After that explanation, ask once for narrowly scoped read permission only when the current host exposes a concrete path that the permission would unlock and that path can query the same effective App/session with `model/list` or equivalent metadata. Name the exact read and why it would improve the answer. Generic filesystem, network, CLI, or approval permission is not useful if it can only inspect another process or cannot reach the current selector; do not request it. If no matching read path exists, say so and optionally ask the user to share the selector only when they still want an account-specific comparison. If the user declines, continue with the reference recommendation and do not ask again until the surface, permission state, or explicit request changes.

## Apply the user's control mode

Resolve this router's mode independently of the context router. A current-turn instruction wins over stored preferences. If no mode is available, default to `ask`.

- `off`: do not evaluate; keep the current model and effort and emit no recommendation.
- `ask`: when the known current pair meets the recommended setting, retain it and continue. Otherwise show both pairs, provide the known manual control, and wait for the user to finish setting it or choose to continue unchanged.
- `auto`: apply the recommended pair when both model and effort changes are callable, authorized and verifiable. If either operation is user-only or unavailable, provide the manual control and wait for the user to reply “continue.” A fallback catalog may inform the recommendation but never proves that a switch succeeded.

`off` performs no routing evaluation and is the exception to the visibility requirement. `ask` is the default interactive mode. When both routers require confirmation, combine their choices into one concise prompt when accurate, while preserving independent controls.

## Output

Every enabled invocation must visibly report the minimum sufficient model/effort, the recommended model/effort, upgrade value, a short reason, and what actually happened. Use the two headings `Minimum sufficient AI setting` and `Recommended AI setting`, translated to the user's language. Show a current-setting block only when matching live or user-provided values are known and useful for the switch decision; never print `Current: unknown / unknown` in the compact result. Unless the user asks for diagnostics, do not mention the probe, fallback/registry source, freshness, surface/account applicability, unreadable current values, confidence, assessment or mode in the compact result. The compact output contains only the task-specific setting blocks plus the useful capability outcome: either verified automatic application or the exact user action. When manual action is needed, the final line must tell the user to reply “continue” after setting it, or to reply “continue” to proceed unchanged. A second gate in the same response may reuse an unchanged result, but cannot silently omit the enabled model result.

```yaml
skill: research-model-router
phase: short description of the upcoming work phase
task_requirements:
  capabilities: [phase-specific needs, not model names]
  reasoning_demand: low | moderate | high
  quality_and_validation: short requirement
  latency_and_usage: user constraints or unspecified
discovery:
  status: not_probed | available | partial | unavailable | permission_denied | error | stale | scope_mismatch
  attempts: [source, outcome and limitation, without secrets]
  scope: product, surface, execution host and effective context
  observed_at: timestamp | unknown
  missing_information: []
capability_evidence:
  source: runtime description | official documentation | task evaluation | unavailable
  reference: source identifier or URL | null
  observed_at: timestamp | unknown
  recommendation_basis: inferred | measured | insufficient
current_configuration:
  model: observed model name | unknown
  reasoning_effort: observed effort | unknown | unsupported
  evidence: runtime metadata | user-provided settings | cached observation | unavailable
  scope: matching live configuration | user-reported | unknown
model_catalog:
  availability: available | unknown
  source: runtime metadata | user-provided settings | cached observation | versioned fallback | unavailable
  observed_at: timestamp | unknown
  cache_scope: current session | host-defined short lifetime | none
  applicable_to_context: verified | unverified | mismatch
assessment: suitable | change_recommended | unverified | deferred
minimum_sufficient_setting:
  model: supported model name | CURRENT | null
  reasoning_effort: supported effort | CURRENT | null
  availability: verified | unverified | unknown
  reason: why this is sufficient for the task
recommended_setting:
  model: supported model name | CURRENT | null
  reasoning_effort: supported effort | CURRENT | null
  availability: verified | unverified | unknown
upgrade_value: low | medium | high
upgrade_reason: additional value over the minimum, or why a stronger pair would not help
confidence: 0.00-1.00
reason: one concise phase-specific explanation
mode: off | ask | auto
disposition: skipped | awaiting_user_confirmation | awaiting_user_action | applied | kept_current
revisit_at: meaningful next stage transition | null
runtime_capabilities:
  surface: identified surface or unknown
  switch_current_model: agent | orchestrator | user_only | unavailable | unknown
  set_model_for_new_run: agent | orchestrator | user_only | unavailable | unknown
  set_reasoning_effort: agent | orchestrator | user_only | unavailable | unknown
  evidence: runtime metadata | user-provided settings | cached observation | unavailable
  observed_at: timestamp | unknown
  confidence: 0.00-1.00
execution:
  requested_owner: agent | orchestrator | user | none
  effective_owner: agent | orchestrator | user | none
  status: skipped | awaiting_user_confirmation | awaiting_user_action | applied | retained_current | blocked
  reason: concise explanation
  manual_action: null | surface-specific instruction
```

Distinguish both settings from what was actually applied. With a bundled registry, `availability: unverified` means the identifiers and efforts were observed and documented recently, while availability to this account has not been verified. For a deferred destination decision in `ask`, use null setting fields, `assessment: deferred`, `disposition: awaiting_user_confirmation`, and the matching execution status; explain the dependency instead of presenting `CURRENT` as an evaluated destination choice. Never claim a switch occurred unless the host applied it. Provide concise rationale, not hidden chain-of-thought.

Keep persisted settings and disk defaults in structured evidence, not as verified current values. The compact result focuses on actionable routing information: task need, both pairs, upgrade value, actual disposition and the next action. When current values cannot be read, omit them instead of explaining that they are unknown. Use only models and efforts present in the applicable runtime catalog or unexpired registry, and never claim a setting was applied without verification.

In Traditional Chinese, the compact result should follow this structure:

```text
【最低足夠 AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high
這一步包含資料取得、公式核對及時間偏誤判斷，我判斷此設定足夠。

【建議 AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high
* 升級價值：低。目前主要瓶頸是歷史資料可用性與口徑一致性，提高設定不會補出缺失的資料。
```

The explanation must describe the actual phase rather than copying this example. When the two pairs differ, `upgrade_reason` must say what the recommended pair adds. When they are equal, explain why further capability has low value.

When manual action is required, name the control appropriate to the identified surface. On ChatGPT desktop or web with a visible model/reasoning selector, mention only that selector; do not include the CLI-only `/model` command. For Traditional Chinese use: “請使用介面中的模型與推理強度選單完成設定。完成後請回覆「繼續」。若決定不調整，也請回覆「繼續」。” On an identified Codex CLI where `/model` is the documented control, use: “請用 `/model` 完成設定；完成後請回覆「繼續」。若決定不調整，也請回覆「繼續」。” If the surface is unresolved, refer generically to the interface's model controls and do not mention `/model` until CLI support is established.

Immediately before that instruction, state the capability outcome in plain language: “目前環境無法代為切換模型與推理強度。” If `auto` successfully applied and verified both operations, replace the manual instruction with: “已自動套用建議設定，現在繼續執行。”

When the host exposes only user controls, provide the exact action for that surface. An interactive model selector or command visible to the user is not an agent capability unless the agent can actually invoke and verify it.

## Coordination boundary

This skill decides **how much model capability the work needs**. `task-context-router` decides **where the work runs**. Keep them separate and use this order:

```text
understand → rough plan → task-context-router → resolve context
→ research-model-router → resolve model configuration → execute
```

The [coordinator](../adaptive-task-routing/SKILL.md) owns this full sequence. This Skill dispatches to it only when the host selected the child for a general task before Context routing; it never performs the Context decision itself. Explicit model-only invocation remains valid. At later substantial phase transitions, re-run only this Skill when a completed Context decision is still valid; use the coordinator when a genuine context-boundary question also appears. Neither router expands permissions or authorizes unrelated external actions.
