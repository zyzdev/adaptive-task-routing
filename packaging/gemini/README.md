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
The manifest loads the packaged `GEMINI.md` after restart. Submit a cross-file release-flow,
cross-platform consistency, and test-gap scan without naming the Skill. Confirm Gemini does not
classify it as merely informational: the startup context applies the embedded coordinator contract,
then renders one final response with the findings or plan before the routing note and ends the
turn in default `ask`. Submit a separate execution request and confirm only `auto` may continue
through the gate. Explicit activation can be tested separately but remains host-dependent.

Gemini can limit consent to an activated Skill's directory. The generated coordinator therefore
contains a self-contained dependency appendix and must not activate sibling Skills during an
explicitly activated gate. The startup `GEMINI.md` also embeds the same compact contract because
Gemini CLI 0.59.0 can advertise `activate_skill` to the model while returning
`tool_not_registered` when that call executes. Automatic routing uses the startup contract directly;
the packaged Skill remains available for hosts where explicit activation executes correctly. A
missing or truncated appendix must produce an incomplete gate, not an invented routing result.

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
