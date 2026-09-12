# Adaptive Task Routing — User Guide

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing helps an AI decide whether substantial work should stay in the current conversation and which model and reasoning effort fit the next phase. It presents the requested findings or plan first, followed by a clearly separated resource recommendation.

## Install

### Gemini CLI

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

Restart Gemini CLI after installation.

### Claude Code

The public directory submission is under review. Until it is listed, clone the dedicated repository and start Claude Code with the plugin directory:

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

### ChatGPT and Codex

Download `adaptive-task-routing-openai-0.4.2.zip` from the [v0.4.2 release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2). In a surface that supports local plugins, add the extracted plugin through its plugin or marketplace interface. Public directory availability is subject to OpenAI review.

## First use

Start a new conversation after installation and submit a substantial task, for example:

> Audit this project's release workflow, cross-platform consistency, and test gaps.

The AI should present useful findings or an actionable plan first. For a qualifying next phase, it then displays an **Adaptive Task Routing** resource section containing:

- whether to remain in the current conversation;
- the minimum sufficient model and reasoning setting;
- the recommended model and reasoning setting;
- the value of upgrading, when relevant.

In the default `ask` mode, the AI pauses after the recommendation and accepts a natural response. You may change the settings, ask it to continue as-is, or choose another approach. No fixed reply phrase is required.

## Explicit activation

- Codex surfaces with Skill mentions: `$adaptive-task-routing`
- Claude Code: `/adaptive-task-routing:adaptive-task-routing`
- Other surfaces: ask, “Use the adaptive-task-routing skill before starting this work.”

## Modes

- `ask` (default): recommend and wait before substantial execution.
- `auto`: apply only changes the current host permits and can verify, then continue.
- `off`: skip that router.

Context routing and model routing have independent modes. Edit `shared/defaults.yaml` in the installed plugin to change the defaults, then restart the host.

## Remove

Gemini CLI:

```bash
gemini extensions uninstall adaptive-task-routing
```

For Claude Code started with `--plugin-dir`, exit the session and delete the cloned directory. For ChatGPT or Codex, remove or disable the plugin from the same plugin or marketplace interface used to install it.

## Troubleshooting

- Start a new conversation after installing or updating.
- Confirm that `adaptive-task-routing`, `task-context-router`, and `research-model-router` appear in the Skill inventory.
- If no recommendation appears, try explicit activation once.
- A recommendation does not prove that the host changed the model or conversation. Automatic changes are reported only after verification.

For development and validation details, return to the [project README](../../README.md).
