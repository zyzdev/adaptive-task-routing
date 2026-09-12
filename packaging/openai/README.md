# Adaptive Task Routing for ChatGPT and Codex

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing helps ChatGPT and Codex choose the conversation context, model, and reasoning effort for the next substantial phase. The AI presents the requested findings or plan first, then shows the resource recommendation.

## Install

The public plugin submission is managed through the OpenAI Plugins portal. Until it is listed, download `adaptive-task-routing-openai-0.4.2.zip` from the [latest release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2), extract it, and register the extracted directory as a local plugin source or marketplace.

In Codex CLI, install it from the configured marketplace. In ChatGPT or the Codex app, select it from the Plugins Directory after the public listing becomes available.

## First use

Start a new conversation and ask a substantial question, such as:

> Audit this project's release workflow and propose an implementation plan for the main risks.

Explicit activation is available as `$adaptive-task-routing` on surfaces that support named skills.

## Change modes in conversation

- “Set Adaptive Task Routing to auto for this conversation.”
- “Set model routing to ask.”
- “Turn context routing off for this task.”
- “What routing modes are active?”

An unqualified mode change applies to both independent routers. The default is `ask`; `auto` applies only changes the current OpenAI surface can perform and verify; `off` skips the selected router.

## What you will see

The example below uses the request “Review the plugin release process, cross-platform consistency, and test gaps.” Actual plans and recommendations vary by task and platform.

### Example response

#### 1. AI task plan

```text
1. Inspect release scripts and manifests.
2. Review CI and test gaps.
```

#### 2. Adaptive Task Routing resource recommendation

```text
---

### Adaptive Task Routing | Task resource guidance

[Conversation setting]
* Recommendation: Stay in this conversation
* Switch windows: No

[Minimum sufficient AI setting]
* Model: GPT-5.6 Sol
* Reasoning: high

[Recommended AI setting]
* Model: GPT-6 Astra
* Reasoning: high
* Upgrade value: Medium. Better for subtle cross-file dependencies.

This environment cannot change the settings for you. Use the model and reasoning controls in ChatGPT or the Codex app, or `/model` in Codex CLI, if desired; I will pause while you decide whether to adjust them or continue with the current setting.
```

The model names and effort values are illustrative. Actual recommendations use options evidenced for the current OpenAI environment. In `ask`, the AI stops after this block; `auto` may continue already authorized work.

## Remove

Remove the plugin through the Plugins Directory or the configured Codex marketplace. For a manually extracted local copy, remove its marketplace entry and delete the extracted directory.

For packaging, validation, and publication details, see [Development notes](DEVELOPMENT.md).
