# Adaptive Task Routing — Claude Code

[English](../../docs/usage/README.md) · [繁體中文](../../docs/usage/README.zh-TW.md) · [简体中文](../../docs/usage/README.zh-CN.md) · [日本語](../../docs/usage/README.ja.md) · [한국어](../../docs/usage/README.ko.md)

Three Skills route substantial work through context, model and reasoning recommendations.
Both independent routers default to ask. A packaged `UserPromptSubmit` hook injects a short
reminder before each prompt so Claude first presents the requested analysis or plan, then invokes
the coordinator before any qualifying next phase. For an execution request, Claude presents an
actionable plan before the gate.

## Local installation

Extract this ZIP into an adaptive-task-routing directory. Its root contains
.claude-plugin/plugin.json, skills/ and shared/. Run:

```bash
claude plugin validate /absolute/path/to/adaptive-task-routing --strict
claude --plugin-dir /absolute/path/to/adaptive-task-routing
```

In the new session, first submit a substantial plan-only task without naming the Skill and confirm
the useful plan appears before the localized `Adaptive Task Routing` task-resource divider and
routing note, and default `ask` ends the turn there. Submit a
separate execution request and confirm retain/nonblocking defer may continue authorized work in `ask`, while proposed changes require confirmation. Explicit
invocation is /adaptive-task-routing:adaptive-task-routing.
The individual routers are /adaptive-task-routing:task-context-router and
/adaptive-task-routing:research-model-router. Verify all three are discovered.
Keep the entire plugin together: shared files and sibling Skills are required.
The hook prints fixed reminder text only and does not inspect files, call a model, or execute
the routers. It can be inspected with `/hooks` and disabled through Claude Code settings.
No MCP server is bundled. The common model Skill carries an
optional Codex-only Python helper; do not run it to discover Claude settings.

## Model discovery

Follow the [Claude guide](../../shared/hosts/claude.md). Prefer current session metadata
or an already exposed status-line observation; use `/model` and, on supported versions,
`/effort` as user controls when needed. Saved defaults and subagent overrides are not
the main thread's live settings. No status-line integration is performed.
Unknown settings still yield task capability guidance. Record acceptance in the
[surface matrix](../../tests/surface-matrix.json).

## Contents and evaluation

- [Architecture](../../docs/architecture.md)
- [Traditional Chinese architecture](../../docs/architecture.zh-TW.md)
- [Full example](../../docs/full-example.md)
- [Behavioral cases and cross-platform matrix](../../tests/behavioral-cases.md)
- [Shared policy](../../shared/runtime-routing-policy.md)
- [Defaults](../../shared/defaults.yaml)
- [Changelog](../../CHANGELOG.md)

The version is in .claude-plugin/plugin.json. Run explicit and implicit activation
tests separately, record model/effort as unknown when unreadable, and verify each
operation before reporting an applied change.

## Distribution

After owner approval, place this generated directory at the root of a dedicated
public plugin repository, or point a marketplace entry to this directory. Do not
use the source monorepo root as the plugin. For marketplace installation, add the
marketplace first, then install adaptive-task-routing@marketplace-name.

For public catalog review, follow the current submission link in the official
[plugin creation guide](https://code.claude.com/docs/en/plugins).
Third-party submissions go to claude-community after review. The Console form is
https://platform.claude.com/plugins/submit. Team/Enterprise organizations with directory
management access can also use https://claude.ai/admin-settings/directory/submissions/plugins/new.
Submit the generated plugin's source, version and test evidence. The curated
claude-plugins-official catalog has no application process. A local validation pass
is not catalog acceptance. Once approved and listed, users add
anthropics/claude-plugins-community and install adaptive-task-routing@claude-community.
See [plugin reference](https://code.claude.com/docs/en/plugins-reference).
