# Development guide

[English](DEVELOPMENT.md) · [繁體中文](DEVELOPMENT.zh-TW.md)

[User-facing overview](README.md)

## Included skills

### `adaptive-task-routing` — start here

The coordinator first lets the agent complete and present the requested analysis or plan. If that deliverable defines a concrete substantial next phase, it then reads the context router, resolves the effective working context, and reads the model router for that next phase. For an execution request, the agent presents a concise actionable plan before the routing note and does not begin substantial execution yet. Model `ask` stops after the note and waits for a natural user response; model `auto` may apply supported settings and continue. A plan-only request never authorizes implementation.

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

The generated packages now add a short host-native activation reminder. Codex and Claude Code run a `UserPromptSubmit` plugin hook; Gemini CLI loads the extension's `GEMINI.md` in every restarted session. The reminder tells the host to present the requested analysis or plan first, then invoke the coordinator for a qualifying next phase before that phase begins. It also preserves the `ask` hold and `auto` continuation boundary. It does not duplicate the routing policy or run the routers itself. Codex can require one-time review before an installed hook runs, and any host or administrator can disable hooks or extensions. ChatGPT surfaces that consume only the portable Agent Plugins manifest do not expose a local prompt hook, so their implicit activation still depends on description matching or explicit Skill selection.

For explicit use, select the **adaptive-task-routing skill** in the host's skill picker, or ask: “Use the adaptive-task-routing skill before starting this work.” Codex surfaces supporting `$` mentions can use `$adaptive-task-routing`; Claude Code uses `/adaptive-task-routing:adaptive-task-routing`. Individual routers remain available for context-only or model-only requests. The coordinator remains the primary entrypoint; a child selected for a general task dispatches once to it unless the request is explicitly context-only or model-only.

When diagnosing a missing note, inspect the skill inventory, actual loaded Skill paths, modes, and response. No visible note alone does not prove whether a skill loaded. An older conversation alone does not prove an outdated inventory either. A new task after reinstall is the recommended test boundary.

Compact output follows the user's language. Context enums remain internal evidence; the visible recommendation uses a plain description such as “Stay in this conversation” and does not show `CURRENT`, `HANDOFF`, or `CLEAN`.

## Runtime behavior

On first use, the plugin loads a capability snapshot from a host- or user-managed settings store. It detects and records missing or stale operations when persistence is available. Later gates perform only a lightweight freshness check; cached observations remain hints and are invalidated by surface, session, permission, tool, host, catalog, or operation-result changes.

The model catalog is dynamic and separate from the running configuration. Runtime metadata is preferred, then clearly labeled user-provided options, then an explicitly versioned and expiring fallback registry. On recognized OpenAI surfaces, that registry's dated official cross-surface descriptions can produce concrete recommendations when App metadata is inaccessible, without claiming account availability or asking the user to copy the selector first. Gemini CLI has its own dated registry of stable model aliases; it never borrows OpenAI effort levels or guesses the account-dependent backend model. A runtime catalog may be cached for the session or another short host-defined lifetime, and is refreshed after relevant changes or errors. Task scoring stays model-neutral; the plugin does not permanently assign scores to model names.

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
It runs only on demand, not on installation or Skill loading. The activation hooks do not
run this helper; they only print a fixed reminder. No daemon or MCP service is bundled.
Claude and Gemini use their own host guides, not this helper.

[Seven-surface acceptance records](tests/surface-matrix.json) cover 35 cases (245 cells):
ChatGPT web/desktop/mobile, Codex App/CLI, Claude Code and Gemini CLI. Metadata probe
success is not a conversational pass, live App verification, or switching capability.

## Source and releases

Version **0.4.2** is the current public release. The only maintained Skill and
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
No separate Codex marketplace ZIP, runtime service, or MCP service is shipped.

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
and Gemini's single-activation coordinator behavior need installed-host evidence.

## Documentation and publication

- [Architecture](docs/architecture.md) and [full example](docs/full-example.md)
- [Platform specifications and sources](docs/platform-specs.md)
- [Inventory and migration recovery](docs/inventory.md)
- [Release verification](docs/release-verification.md)
- [Release and actual submission steps](docs/release.md)
- [Contribution guide](CONTRIBUTING.md) and [security policy](SECURITY.md)

Release packages are available from the [v0.4.2 release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2).
The dedicated [Gemini repository](https://github.com/zyzdev/adaptive-task-routing-gemini)
is publicly installable. The dedicated [Claude repository](https://github.com/zyzdev/adaptive-task-routing-claude)
has been submitted for Claude Code directory review. OpenAI directory availability remains
subject to platform review. License: [MIT](LICENSE).
