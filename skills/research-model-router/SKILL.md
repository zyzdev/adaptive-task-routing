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

Run after the plan or preceding analysis for the upcoming phase and the effective working context are known, before that phase begins. For a plan-only or analysis-only request, the recommendation follows the requested deliverable and applies to its concrete substantial next phase. For an execution request, a concise actionable plan appears first, and this gate runs before mutation or substantial execution. A caller can supply the resolved context. Direct use stays model-only only under the direct-selection guard above.

When delivering an improvement plan with a concrete substantial next phase, include a model/effort recommendation for that phase before yielding, even if execution awaits approval. Advice does not authorize implementation. If a final answer has no substantial next phase, do not invent one or add a new routing gate just to end the response. Before difficult final evidence synthesis, route before doing that synthesis.

Re-run only at a meaningful stage transition: pilot to expanded workload, retrieval or execution to interpretation, robustness or adversarial testing, routine transformation to difficult reasoning, or final evidence synthesis. Do not re-route for every tool call or ordinary chat.

## Decide

First describe `task_requirements`: the phase's capability needs, relative reasoning demand, quality/validation needs and latency/usage constraints. This judgment does not depend on knowing the current model. Then produce two independent task-based results: `minimum_sufficient_setting`, the least costly pair likely to meet those requirements, and `recommended_setting`, the best-value pair after considering ambiguity, error cost, validation depth, latency and usage. The two pairs may be identical. Always give `upgrade_value` (`low`, `medium`, or `high`) and a concrete `upgrade_reason` describing what the recommended pair is expected to add over the minimum. Do not suppress useful task guidance when discovery is incomplete.

When observations are missing or stale, follow the matching [host discovery guide](../../shared/host-discovery.md). Resolve `../../shared` from the directory containing this `SKILL.md`: it is `<plugin-root>/shared`, not `skills/shared`. In a permitted Codex environment the guide links to [the optional read-only probe](scripts/probe_codex.py); do not run that helper on Claude/Gemini or assume ChatGPT has access to the user's CLI. Excluding a subagent menu only rejects that source: continue to an applicable host read path or fresh, scoped observation. Do not conclude that the main-context catalog is unavailable merely because the visible menu is for subagents. If the Codex helper identifies a project-sandbox state-access failure, stop after that attempt and follow the host guide's versioned bundled-registry fallback without requesting extra read permission. In a positively identified OpenAI host, including ChatGPT desktop/web and Codex App/CLI, unavailable runtime metadata does not suppress the two concrete settings: use the unexpired bundled registry as a cross-surface recommendation reference and label account availability `unverified` only in structured evidence. Its CLI observation proves availability only for that observed CLI, while its dated official capability source supports recommendations on the listed OpenAI surfaces. Do not ask the user to transcribe selector options before giving those recommendations. Record any attempted read and outcome before falling back. Prefer an applicable runtime catalog, use official model descriptions only as scoped capability evidence, and use relevant task evaluations when available. Keep inferred recommendations distinct from measured results.

For verified runtime decisions, recommend only a `model` and `reasoning_effort` supported by the current environment. For a matching unexpired registry fallback, recommend only pairs recorded in that registry and label their account availability `unverified`. Never invent identifiers.

Reasoning controls are platform-native. The rubric's `low`, `moderate`, and `high` task demand is internal analysis, not proof that those strings are selectable settings. On Gemini CLI, use an exact observed `thinkingBudget` or `thinkingLevel` only when it is configurable in the effective session. Otherwise render `Reasoning: model default`, localized to the user. Never output bare Codex-style `low`, `medium`, or `high` as a Gemini setting without matching Gemini control evidence.

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
| Runtime discovery is blocked on a recognized OpenAI surface, but the unexpired bundled registry has model descriptions and effort options | Stop after the failed read and give concrete minimum and recommended fallback pairs without asking the user to transcribe the selector. Treat the registry as cross-surface recommendation evidence, while keeping account availability and current settings unverified. Apply only through independently verified switch controls in `auto`; in `ask`, present the surface-appropriate control and wait for the user's decision. |
| Gemini CLI live selector metadata is unavailable, but the unexpired Gemini CLI registry applies | Recommend only its stable aliases (`auto`, `pro`, `flash`, or `flash-lite`) using the recorded task guidance. Never guess a concrete backend model because alias resolution is account-dependent. Use the model's default reasoning behavior unless an exact native thinking control is observed. Do not ask for `/model` before giving the fallback recommendation. |
| Relevant bounded discovery leaves insufficient catalog or capability evidence to choose a pair, and no recognized-product bundled reference applies | Show task requirements, the attempted source and outcome or concrete access limitation, and the missing evidence. Provisionally retain `CURRENT / CURRENT` with `assessment: unverified`, or ask once for selector options when an exact choice is necessary. Do not call this proof of suitability. |

Lack of an automatic switching tool affects execution, not the ability to recommend evidenced pairs. `upgrade_value` compares the recommended pair with the minimum sufficient pair, never with an unknown current setting. In `ask`, present the recommended pair and any known control as an option when the current pair is unknown; do not describe it as an upgrade or downgrade from the unknown setting.

## When the user questions a recommendation

Do not request broader read permission during the normal fallback path. If the user says the recommended model or effort looks wrong, asks why it was chosen, or explicitly requests an account-specific check, then disclose the useful diagnostic facts: whether the recommendation used runtime data or the bundled reference, the reference observation and expiry dates, that account availability is unverified when applicable, and the task factors that led to both pairs.

After that explanation, ask once for narrowly scoped read permission only when the current host exposes a concrete path that the permission would unlock and that path can query the same effective App/session with `model/list` or equivalent metadata. Name the exact read and why it would improve the answer. Generic filesystem, network, CLI, or approval permission is not useful if it can only inspect another process or cannot reach the current selector; do not request it. If no matching read path exists, say so and optionally ask the user to share the selector only when they still want an account-specific comparison. If the user declines, continue with the reference recommendation and do not ask again until the surface, permission state, or explicit request changes.

## Apply the user's control mode

Resolve this router's mode independently of the context router. A current-turn instruction wins over stored preferences. If no mode is available, default to `ask`.

- `off`: do not evaluate; keep the current model and effort and emit no recommendation.
- `ask`: show both pairs, present any useful surface-specific control, then stop and wait for the user's natural response. Do this even when the known current pair meets the recommendation. The user may request the recommended setting, say they changed it, or explicitly continue with the current setting; do not require a fixed confirmation word.
- `auto`: apply the recommended pair when both model and effort changes are callable, authorized and verifiable. If either operation is user-only or unavailable, present the manual control as an option, retain the current setting, and continue authorized work. A fallback catalog may inform the recommendation but never proves that a switch succeeded.

`off` performs no routing evaluation and is the exception to the visibility requirement. `ask` is the default interactive mode. When both routers require confirmation, combine their choices into one concise prompt when accurate, while preserving independent controls.

## Output

Every enabled invocation must visibly report the minimum sufficient model/effort, the recommended model/effort, upgrade value, a short reason, and what actually happened. Put the requested plan or preceding findings before these blocks. For a standalone invocation, start the routing note with a Markdown horizontal rule, a localized level-three heading meaning `Adaptive Task Routing | Task resource guidance`, and one localized sentence saying the recommendations assess resources for the planned next phase. Keep the product name `Adaptive Task Routing` unchanged. For a coordinator-delegated invocation, return the setting blocks within the coordinator's single routing note and let the coordinator supply this shared introduction; never emit a second divider or heading. Use the two headings `Minimum sufficient AI setting` and `Recommended AI setting`, translated to the user's language. Traditional Chinese must use the exact literal headings `【最低足夠 AI 設定】` and `【建議 AI 設定】`; do not replace the two setting labels with Markdown `#` headings. It must also use the exact branded heading and introductory sentence shown below. Show a current-setting block only when matching live or user-provided values are known and useful for the switch decision; never print `Current: unknown / unknown` in the compact result. Unless the user asks for diagnostics, do not mention the probe, fallback/registry source, freshness, surface/account applicability, unreadable current values, confidence, assessment or mode in the compact result. The compact output contains only the branded resource-guidance introduction, task-specific setting blocks, and useful capability outcome: either verified automatic application, an optional surface-appropriate control, or the `ask` hold. In `ask`, stop after the blocks and wait for a natural user response without requiring a confirmation word. In `auto`, continue authorized downstream work after verified application or the documented current-setting fallback. A second gate in the same response may reuse an unchanged result, but cannot silently omit the enabled model result.

Keep internal observations in the [structured evidence schema](references/evidence-schema.md). Read that reference only when the user requests diagnostics or when maintaining the router implementation. Never render the schema or internal evidence in ordinary compact output.

Distinguish both settings from what was actually applied. With a bundled registry, `availability: unverified` means the identifiers and efforts were observed and documented recently, while availability to this account has not been verified. For a deferred destination decision in `ask`, use null setting fields, `assessment: deferred`, `disposition: awaiting_user_confirmation`, and the matching execution status; explain the dependency instead of presenting `CURRENT` as an evaluated destination choice. Never claim a switch occurred unless the host applied it. Provide concise rationale, not hidden chain-of-thought.

Keep persisted settings and disk defaults in structured evidence, not as verified current values. The compact result focuses on actionable routing information: task need, both pairs, upgrade value, actual disposition and the next action. When current values cannot be read, omit them instead of explaining that they are unknown. Use only models and efforts present in the applicable runtime catalog or unexpired registry, and never claim a setting was applied without verification.

In Traditional Chinese, the compact result should follow this structure. This first example uses OpenAI values:

```text
---

### Adaptive Task Routing｜任務資源建議

以下建議是根據上述計畫的下一階段，評估適合的對話環境、模型與推理設定。

【最低足夠 AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high
這一步包含資料取得、公式核對及時間偏誤判斷，我判斷此設定足夠。

【建議 AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high
* 升級價值：低。目前主要瓶頸是歷史資料可用性與口徑一致性，提高設定不會補出缺失的資料。
```

On Gemini CLI, keep the same headings but use Gemini-native values. When no independent thinking control is verified, use this form instead of inventing an effort level:

```text
---

### Adaptive Task Routing｜任務資源建議

以下建議是根據上述計畫的下一階段，評估適合的對話環境、模型與推理設定。

【最低足夠 AI 設定】
* Model：Flash
* Reasoning：使用模型預設
這一步範圍清楚，一般的模型推理能力足以完成。

【建議 AI 設定】
* Model：Pro
* Reasoning：使用模型預設
* 升級價值：中。較適合需要多步判斷、交叉核對與較高錯誤成本的工作。
```

The explanation must describe the actual phase rather than copying this example. When the two pairs differ, `upgrade_reason` must say what the recommended pair adds. When they are equal, explain why further capability has low value.

When a manual control is useful, name the control appropriate to the identified surface. On ChatGPT desktop or web with a visible model/reasoning selector, mention only that selector; do not include the CLI-only `/model` command. In Traditional Chinese `ask` mode use: “目前環境無法代為切換模型與推理強度。如需採用建議，可使用介面中的模型與推理強度選單調整；我先停在這裡，等你決定是否調整，或沿用目前設定開始下一階段。” On an identified Codex CLI where `/model` is the documented control, use: “目前環境無法代為切換模型與推理強度。如需採用建議，可用 `/model` 調整；我先停在這裡，等你決定是否調整，或沿用目前設定開始下一階段。” On Gemini CLI, `/model` changes only the model or alias unless a separate native thinking control is actually available. With model-default reasoning, use: “目前環境無法代為切換模型；Reasoning 使用模型預設。如需採用建議，可用 `/model` 選擇模型；我先停在這裡，等你決定是否調整，或沿用目前設定開始下一階段。” If the surface is unresolved, refer generically to the interface's model controls and do not mention `/model` until CLI support is established. These are natural choices, not a required reply keyword.

In `auto`, if switching is unavailable, present the same surface control as optional and say that the current setting will be retained while work continues. If `auto` successfully applied and verified both operations, use: “已自動套用建議設定，現在繼續執行。”

When the host exposes only user controls, provide the exact action for that surface. An interactive model selector or command visible to the user is not an agent capability unless the agent can actually invoke and verify it.

## Coordination boundary

This skill decides **how much model capability the work needs**. `task-context-router` decides **where the work runs**. Keep them separate and use this order:

```text
requested analysis or plan → task-context-router → resolve context
→ research-model-router → ask: wait | auto: resolve configuration and execute
```

The [coordinator](../adaptive-task-routing/SKILL.md) owns this full sequence. This Skill dispatches to it only when the host selected the child for a general task before Context routing; it never performs the Context decision itself. Explicit model-only invocation remains valid. At later substantial phase transitions, re-run only this Skill when a completed Context decision is still valid; use the coordinator when a genuine context-boundary question also appears. Neither router expands permissions or authorizes unrelated external actions.
