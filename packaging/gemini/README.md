# Adaptive Task Routing for Gemini CLI

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing helps Gemini choose the conversation context and model for the next substantial phase. Gemini presents the requested findings or plan first, then shows the resource recommendation.

## Install

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

Restart Gemini CLI after installation and confirm the extension with `gemini extensions list`.

## First use

Start a new session and ask a substantial question, such as:

> Audit this project's release workflow and propose an implementation plan for the main risks.

If explicit activation is needed, ask Gemini to use the `adaptive-task-routing` Skill.

## Change modes in conversation

- “Set Adaptive Task Routing to auto for this conversation.”
- “Set model routing to ask.”
- “Turn context routing off for this task.”
- “What routing modes are active?”

An unqualified mode change applies to both independent routers. The default is `ask`; `auto` applies only changes Gemini can perform and verify; `off` skips the selected router.

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
* Model: Flash
* Reasoning: Model default

[Recommended AI setting]
* Model: Pro
* Reasoning: Model default
* Upgrade value: Medium. Better for subtle cross-file dependencies.

This environment cannot change the model for you. Use /model if you want the recommended model. I will pause while you decide whether to adjust it or continue with the current setting.
```

The model aliases are illustrative and resolve according to the current Gemini account. Gemini shows an exact thinking control only when the session exposes one; otherwise reasoning remains the model default. In `ask`, Gemini stops after this block; `auto` may continue already authorized work.

## Remove

```bash
gemini extensions uninstall adaptive-task-routing
```

Restart Gemini CLI after removal.

For validation and gallery details, see [Development notes](DEVELOPMENT.md). The canonical source is the [main project](https://github.com/zyzdev/adaptive-task-routing).
