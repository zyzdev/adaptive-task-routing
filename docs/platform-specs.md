# Platform specifications checked on 2026-09-11

## OpenAI

The [official packaging specification](https://developers.openai.com/plugins/build/plugins)
requires root plugin.json with the Agent Plugins schema for the portable layout.
Skills are discovered under root skills/. Presentation goes under extensions.com.openai;
the legacy .codex-plugin/plugin.json remains a fallback. An inline OpenAI extension
replaces the fallback overlay as a whole, so both are generated from one interface object.

The [official submission guide](https://developers.openai.com/plugins/deploy/submission)
supports Skills only submissions and specifies five positive and three negative test
cases, verified publisher identity, public listing assets/URLs, availability and attestations.
Local package validity does not prove submission readiness or account access.

The [skill guide](https://developers.openai.com/plugins/build/skills) defines name and
description frontmatter and description-based activation.
The [testing guide](https://developers.openai.com/plugins/deploy/connect-chatgpt) calls for
installed-host testing of triggers, resources, outcomes and negative cases.
The current Codex runtime exposes plugin lifecycle hooks, including `UserPromptSubmit`;
the compatibility manifest uses that event for a fixed activation reminder. Hook trust
and installed-host delivery remain runtime checks rather than portable schema guarantees.

The pinned schema in tests/schemas/plugin.schema.json was fetched from
https://agent-plugins.org/schemas/1.0.0/plugin.schema.json, linked by OpenAI's packaging
guide. It is validation data, not bundled into released plugins. No network is required
by the build or portable validator.

## Claude Code

The [plugin reference](https://code.claude.com/docs/en/plugins-reference) defines
.claude-plugin/plugin.json and root skills/. Use slash commands namespaced by plugin.
The [hooks reference](https://code.claude.com/docs/en/hooks) permits plugin
`hooks/hooks.json` and `UserPromptSubmit` context injection.
The [creation guide](https://code.claude.com/docs/en/plugins) covers local --plugin-dir
loading and catalog submission. CLI capabilities must be checked locally: newer
documentation can describe flags not available in an installed version. Third-party
submissions are reviewed for claude-community; claude-plugins-official is curated
separately and has no application form. Individual authors can use the Console form;
the claude.ai directory submission form requires Team/Enterprise directory access.

## Gemini CLI

The [extension reference](https://geminicli.com/docs/extensions/reference/) requires
root gemini-extension.json and supports persistent extension context through
`contextFileName` and `GEMINI.md`. [Agent Skills](https://geminicli.com/docs/cli/skills/)
describes extension Skill discovery and activation consent scoped to the Skill directory.
Cross-Skill and plugin-level shared reference access therefore remains an installed-host
permission test; file existence alone does not establish access.

The [release guide](https://geminicli.com/docs/extensions/releasing/) requires manifests
at the absolute archive/repository root. Public GitHub repositories tagged
gemini-cli-extension are discovered by the gallery crawler. Use a dedicated generated
Gemini repository/tree; the source monorepo has no root extension manifest.

## Local audit baseline

Routing-discovery references updated for 0.4.1: [OpenAI](../shared/hosts/openai.md),
[Claude Code](../shared/hosts/claude.md), [Gemini CLI](../shared/hosts/gemini.md).
Their official sources were checked on 2026-09-11. The 2026-09-12 implementation uses
version-sensitive, optional read paths, not a fixed model/effort catalog. Official
descriptions establish capability guidance, never account availability or measured rankings.
The [Skill guide](https://learn.chatgpt.com/docs/build-skills) permits optional scripts;
the new helper is on-demand Skill support, not a startup component or MCP connection.

CLI versions observed before changes: Codex 0.154.0, Claude Code 2.1.152, Gemini CLI 0.59.0.
Actual native validation and loading evidence is in [release verification](release-verification.md).
The public sources above were re-opened for this audit; submission forms were not accessed.
