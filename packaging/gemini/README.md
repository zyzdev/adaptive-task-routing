# Adaptive Task Routing — Gemini CLI

This skills-based extension contains adaptive-task-routing, task-context-router,
and research-model-router under skills/. It uses the same descriptions and routing
policy as the other platforms. Both independent routers default to ask.

## Local installation

Extract this ZIP into an adaptive-task-routing directory, keeping gemini-extension.json
at its root. Retain skills/ and shared/ together.

```bash
gemini extensions validate /absolute/path/to/adaptive-task-routing
gemini extensions link /absolute/path/to/adaptive-task-routing
gemini extensions list
gemini skills list
```

Linking changes the local extension registry. Use install instead of link if you
want a copied installation. Start a new interactive session and inspect /skills list.
The manifest loads the packaged `GEMINI.md` after restart. Submit a substantial plan-only task
without naming the Skill and confirm Gemini presents the useful plan, requests or performs
adaptive-task-routing activation for the next phase, then shows the routing note and ends the
turn in default `ask`. Submit a separate execution request and confirm only `auto` may continue
through the gate. Explicit activation remains available for comparison.

Gemini can limit consent to an activated Skill's directory. The generated coordinator therefore
contains a self-contained dependency appendix and must not activate sibling Skills during the
coordinated gate. Verify that one coordinator activation can produce both decisions without an
additional sibling/shared-resource permission prompt. A missing or truncated appendix must
produce an incomplete gate, not an invented routing result. The startup context contains only
the eligibility reminder; the Skill remains the source of routing policy and output rules.

## Contents and evaluation

- [Architecture](../../docs/architecture.md)
- [Traditional Chinese architecture](../../docs/architecture.zh-TW.md)
- [Full example](../../docs/full-example.md)
- [Behavioral cases and cross-platform matrix](../../tests/behavioral-cases.md)
- [Shared policy](../../shared/runtime-routing-policy.md)
- [Defaults](../../shared/defaults.yaml)
- [Changelog](../../CHANGELOG.md)

Version is in gemini-extension.json. No MCP service, executable hook or credential prompt is bundled.
The common model Skill carries an optional Codex-only Python helper, not a Gemini
probe or startup executable. Real model/context changes depend on observed host capabilities.

## Model discovery

Follow the [Gemini guide](../../shared/hosts/gemini.md). Use current host metadata or the
user's `/model` inventory, then the dated Gemini CLI alias registry when live metadata
is unavailable. Auto is a configured policy, not a fixed execution model. Do not
equate thinking budgets or display toggles with Codex reasoning levels; without an
observed native control, Reasoning is reported as the model default.
Unknown settings still yield task capability guidance. Record acceptance in the
[surface matrix](../../tests/surface-matrix.json); do not run the Codex helper here.

## Distribution and gallery

After owner approval, publish only this generated extension tree at the root of a
public GitHub repository. Add the topic gemini-cli-extension to request automatic
gallery discovery. Keep gemini-extension.json at the absolute repository root.
Users install the repository URL, optionally with --ref for a tag.

If using GitHub Releases, attach only the Gemini ZIP as the generic extension archive.
Do not attach the OpenAI and Claude ZIPs to that extension release: multiple generic
archives can make asset selection ambiguous. The ZIP has no wrapper folder, as required.
Gallery listing depends on validation and crawler processing; no listing was submitted here.

See the official [release guide](https://geminicli.com/docs/extensions/releasing/)
and [extension reference](https://geminicli.com/docs/extensions/reference/).
