# Adaptive Task Routing — User Guide

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

**Put AI usage where it matters, and help reduce omissions and rework.**

Adaptive Task Routing recommends whether to start a new conversation and which model and reasoning effort fit the next substantial phase, helping you balance usage with reliable work.

- **Reduce interference from previous tasks:** Recommends when to start a new conversation so the AI is less likely to carry old assumptions or constraints into new work, reducing repeated corrections and rework. Relevant information is summarized for handoff when needed.
- **Reduce unnecessary usage:** Provides minimum-sufficient and recommended model and reasoning settings, explaining whether an upgrade is worthwhile instead of using the highest settings for every task.
- **Lower the risk of omissions and rework:** Assesses the capability needed before complex work begins, helping reduce errors caused by settings that are insufficient for the task.
- **Keep the decision yours:** Review the recommendations before proceeding, or choose automatic application where the platform supports it.

A change of topic alone does not require a new conversation. The benefit comes from reducing irrelevant history while preserving what the next task needs. Actual savings and reliability depend on the task and the settings adopted.

## How it works

1. The AI presents an actionable plan or completes the analysis or findings you requested.
2. The plugin assesses the next phase: first whether to keep the conversation or start a new one, then the minimum-sufficient and recommended model and reasoning settings and the value of upgrading.
3. By default, `ask` pauses for your decision. In `auto`, the AI applies supported changes when it can verify them; if switching is unavailable, it explains the limitation, retains the current settings, and continues already authorized work.

Brief questions and tiny operations skip routing to avoid unnecessary overhead.

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

## What you will see

The example below uses the request “Review the plugin release process, cross-platform consistency, and test gaps.” Actual plans and recommendations vary by task and platform.

### Example response

#### 1. AI task plan

```text
1. Check the release scripts and manifests for all three platforms.
2. Review CI, version consistency, and test gaps.
3. Rank the risks and propose an implementation order.
```

#### 2. Adaptive Task Routing resource recommendation

```text
---

### Adaptive Task Routing | Task resource guidance

The following recommendations assess the conversation, model, and reasoning resources for the next phase of the plan above.

[Conversation setting]
* Recommendation: Stay in this conversation
* Switch windows: No
This conversation contains the requirements and evidence needed for the next phase.

[Minimum sufficient AI setting]
* Model: GPT-5.6 Sol
* Reasoning: high
This is sufficient for cross-file checks and standard validation.

[Recommended AI setting]
* Model: GPT-6 Astra
* Reasoning: high
* Upgrade value: Medium. It is better suited to tracing subtle relationships between platform configurations.

This environment cannot change the model or reasoning effort for you. Use the interface's model and reasoning controls if you want the recommended setting. I will pause here while you decide whether to adjust it or begin the next phase with the current setting.
```

In `ask`, the response ends there. In `auto`, the AI applies only supported, verifiable changes and may continue with already authorized work. Gemini uses native model aliases and normally displays reasoning as “model default.”

## Explicit activation

- Codex surfaces with Skill mentions: `$adaptive-task-routing`
- Claude Code: `/adaptive-task-routing:adaptive-task-routing`
- Other surfaces: ask, “Use the adaptive-task-routing skill before starting this work.”

## Modes

- `ask` (default): recommend and wait before substantial execution.
- `auto`: apply only changes the current host permits and can verify, then continue.
- `off`: skip that router.

Context routing and model routing have independent modes. Change them directly in conversation, for example:

- “Set Adaptive Task Routing to auto for this conversation.”
- “Set model routing to ask.”
- “Turn context routing off for this task.”
- “What routing modes are active?”

An unqualified Adaptive Task Routing mode changes both routers. The AI confirms the effective values and scope immediately without running a routing recommendation. Ask for a persistent default explicitly; when the host has no writable user-settings store, the change remains in the current conversation and the AI states that limitation.

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
