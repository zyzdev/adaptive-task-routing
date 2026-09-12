# Adaptive Task Routing

[繁體中文](README.zh-TW.md)

Adaptive Task Routing is a cross-platform Agent Skills plugin that makes two decisions before expensive or context-heavy work begins:

1. **Where should the work continue?** `task-context-router` recommends the current conversation, a new context with a compact handoff, or a clean context.
2. **How much model capability should the next phase use?** `research-model-router` recommends a supported model and reasoning effort for coding, debugging, architecture, validation, research, and analysis.

The routers stay independent. A third, thin `adaptive-task-routing` skill coordinates their order and visible results. All three read the shared runtime policy; the coordinator has no separate autonomy mode or decision algorithm.

## Why it exists

Long agentic sessions can waste context and compute when every phase stays in one conversation or always uses the strongest available model. This project adds a small routing gate after task understanding and before substantial execution:

```text
understand → rough plan → context routing → resolve context
→ model routing → resolve model configuration → execute
```

It never assumes that a host can perform a switch. A recommendation, user authorization, runtime capability, and verified execution are separate states.

## Included skills

### `adaptive-task-routing` — start here

After understanding a substantial task and forming a rough plan, this coordinator reads the context router, resolves the effective working context, then reads the model router. It also routes a concrete substantial next phase when delivering an improvement plan, before yielding to the user. It does not authorize implementing a plan-only request.

It skips brief explanations, status checks, tiny edits, and questions merely about the plugin. At later phase changes it loads only the needed router. A completed answer with no substantial next phase does not need a new routing note.

### `task-context-router`

Chooses one of:

- `CURRENT`: continue in the present conversation.
- `HANDOFF`: open a new context with a compact, task-specific handoff.
- `CLEAN`: start independently without carrying task history.

It does not select a model or perform the task. Direct context-only requests stay here; if a host selects this child for a general task, it dispatches once to the coordinator.

### `research-model-router`

Recommends a model and reasoning-effort pair supported by the current environment. It considers task difficulty, ambiguity, error cost, validation needs, compute cost, and stage transitions.

It does not decide where the task runs or perform the task. Direct model-only requests stay here; if a host selects this child for a general task before Context routing, it dispatches once to the coordinator. Every enabled invocation reports concrete minimum-sufficient and recommended settings when evidence supports them. Unreadable current values and discovery diagnostics stay out of compact output. `off` skips the decision and its output.

## Invocation and visibility

For the full workflow, explicitly select the **adaptive-task-routing skill** in your host's skill picker, or ask: “Use the adaptive-task-routing skill before starting this work.” Codex surfaces supporting `$` mentions can use `$adaptive-task-routing`; Claude Code uses `/adaptive-task-routing:adaptive-task-routing`. Individual routers remain available for context-only or model-only requests.

Implicit selection depends on the host matching a skill's description. Installing the plugin, selecting its display name, or adding a shared policy file does not create an always-on hook. The coordinator is marked as the primary entrypoint for general substantial tasks. If a host still selects a child, that child dispatches once to the coordinator unless the request is explicitly context-only or model-only. Coordinator-delegated markers prevent recursion. Missing children or a pending destination must be reported explicitly.

When diagnosing a missing note, inspect the skill inventory, actual loaded Skill paths, modes, and response. No visible note alone does not prove whether a skill loaded. An older conversation alone does not prove an outdated inventory either. A new task after reinstall is the recommended test boundary.

Compact output follows the user's language. Context enums remain internal evidence; the visible recommendation uses a plain description such as “Stay in this conversation” and does not show `CURRENT`, `HANDOFF`, or `CLEAN`.

## User-control modes

Each router has one of three independent modes:

| Mode | Behavior |
|---|---|
| `off` | Skip the router entirely. |
| `ask` | Evaluate and continue when no change is needed. Before a recommended change, ask the user whether to adjust. This is the default. |
| `auto` | Evaluate and apply each supported change when that exact operation is permitted, callable, and verifiable; degrade only unavailable parts to user action. |

The present conversation state is the fallback; no second fixed strategy is required. In `ask`, declining a change continues with current settings. `auto` is permission, not proof of capability. Capabilities are resolved per operation rather than per surface: an App may allow automatic context creation while current-model or effort changes remain user-only. Unknown controls are reported as unknown, not invented.

## Runtime behavior

On first use, the plugin loads a capability snapshot from a host- or user-managed settings store. It detects and records missing or stale operations when persistence is available. Later gates perform only a lightweight freshness check; cached observations remain hints and are invalidated by surface, session, permission, tool, host, catalog, or operation-result changes.

The model catalog is dynamic and separate from the running configuration. Runtime metadata is preferred, then clearly labeled user-provided options, then an explicitly versioned and expiring fallback registry. On recognized OpenAI surfaces, that registry's dated official cross-surface descriptions can produce concrete recommendations when App metadata is inaccessible, without claiming account availability or asking the user to copy the selector first. A runtime catalog may be cached for the session or another short host-defined lifetime, and is refreshed after relevant changes or errors. Task scoring stays model-neutral; the plugin does not permanently assign scores to model names.

The normal fallback path does not ask for broader permission. If the user later questions a recommendation, the router explains the source, date, applicability limit and task mapping. It asks once for narrowly scoped read permission only when that permission can query the same App or session; permission that can only inspect another process is not requested. A declined request returns to the fallback without repeated prompts.

Default settings are in [`shared/defaults.yaml`](shared/defaults.yaml). The normative shared policy is [`shared/runtime-routing-policy.md`](shared/runtime-routing-policy.md).

### Evidence-based discovery

The router first describes task capability needs, then maps them to evidenced available
model/effort choices. Unknown current settings do not suppress task guidance. Official
descriptions inform capability, not account availability; no fixed model ranking is bundled.
Read the matching [host guide](shared/host-discovery.md) only when discovery is needed.

The optional Python 3.10+ [Codex helper](skills/research-model-router/scripts/probe_codex.py)
reads metadata without inference or configuration writes. It keeps CLI catalogs, disk
defaults and persisted thread settings separate; App applicability requires verification.
It runs only on demand, not on installation or Skill loading. No daemon, hook or MCP
service is bundled. Claude and Gemini use their own host guides, not this helper.

[Seven-surface acceptance records](tests/surface-matrix.json) cover 34 cases (238 cells):
ChatGPT web/desktop/mobile, Codex App/CLI, Claude Code and Gemini CLI. Metadata probe
success is not a conversational pass, live App verification, or switching capability.

## Source and releases

Version **0.4.0** is a locally prepared release candidate. The only maintained Skill and
policy sources are root skills/ and shared/. The three stable Skill names remain unchanged;
their descriptions now distinguish the general coordinator from context-only and model-only children.
Bodies and translations provide scoped discovery and task-needs guidance.
release.json provides metadata for every generated manifest.

| Platform | Generated root | Manifest | Installation |
|---|---|---|---|
| OpenAI / ChatGPT / Codex | dist/openai/adaptive-task-routing | plugin.json + .codex-plugin/plugin.json | [OpenAI guide](packaging/openai/README.md) |
| Claude Code | dist/claude/adaptive-task-routing | .claude-plugin/plugin.json | [Claude guide](packaging/claude/README.md) |
| Gemini CLI | dist/gemini/adaptive-task-routing | gemini-extension.json | [Gemini guide](packaging/gemini/README.md) |

The source monorepo is not directly installable on any platform. Build first and use
the correct generated root. ZIP names are adaptive-task-routing-<platform>-<version>.zip;
each has its manifest directly at ZIP root. There are exactly three ZIPs plus SHA256SUMS.
No separate Codex marketplace ZIP, runtime script, MCP service or always-on hook is shipped.

## Build and verify

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_release.py --source-only
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
.venv/bin/python scripts/validate_release.py --require-archives
claude plugin validate dist/claude/adaptive-task-routing --strict
gemini extensions validate dist/gemini/adaptive-task-routing
(cd dist && shasum -a 256 -c SHA256SUMS)
```

Build inputs are explicit. Every rebuild starts fresh and preserves previous dist in
.release-backups/. Generated trees and ZIPs must match current source byte-for-byte.
The validator checks relative links/anchors, versions, frontmatter, trigger preservation,
shared dependencies, platform isolation, ZIP members and hashes.

The [behavioral matrix](tests/behavioral-cases.md) includes the five positive
and three negative OpenAI submission tests. Native loading and structural validation
do not prove behavioral success. Account-specific model controls, implicit activation
and cross-Skill permission prompts need installed-host evidence.

## Documentation and publication

- [Architecture](docs/architecture.md) and [full example](docs/full-example.md)
- [Platform specifications and sources](docs/platform-specs.md)
- [Inventory and migration recovery](docs/inventory.md)
- [Release verification](docs/release-verification.md)
- [Release and actual submission steps](docs/release.md)
- [Contribution guide](CONTRIBUTING.md) and [security policy](SECURITY.md)

No remote repository, push, release, listing or review submission was performed.
Public publisher identity, production listing URLs/assets and live behavioral results
remain owner prerequisites. License: [MIT](LICENSE).
