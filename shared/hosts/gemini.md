# Gemini CLI discovery

Specification check: 2026-09-11. Prefer live metadata exposed by the current CLI.

1. Distinguish the configured model/alias from actual per-turn routing. Auto is a
   host routing policy, not evidence that every turn uses one concrete model. Preserve
   Auto when appropriate instead of forcing a named alternative without evidence.
2. If the catalog is missing, `/model` lets the user inspect the current selector;
   use the actual inventory, not model names copied from documentation examples.
   It is an interactive user command, not a shell command to run in a child process.
3. A known launch flag, `GEMINI_MODEL`, or applicable `model.name` setting is only a
   configuration observation with its source and scope. Do not dump environment or
   full settings. Session changes, Auto, overrides and fallback can affect execution.
4. Reasoning configuration is model/host-specific. Advanced `modelConfigs` can carry
   `thinkingConfig`, including budget controls. Do not rename those as Codex effort
   levels, infer support from a missing field, or treat display controls such as
   inline thinking as a reasoning budget. Report the actual verified control/value;
   use `unknown` if not observable, `unsupported` only on explicit host evidence.

There is no assumed public non-interactive equivalent of the current selector in
this guide. Do not invent `gemini models list`, start an inference prompt, write
settings, install hooks, or invoke a routing model just to detect options. On a
missing/denied read path, explain task capability needs and ask once if an exact
choice is necessary. A subagent's model and a new invocation's `--model` do not
identify or change the running parent session.

Keep the full extension together. If Skill activation consent does not cover sibling
or shared resources, request the required access without bypassing that boundary.

Sources: [model selector](https://geminicli.com/docs/cli/model/),
[model routing](https://geminicli.com/docs/cli/model-routing/), and
[advanced model configuration](https://geminicli.com/docs/cli/generation-settings/).
