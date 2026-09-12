# Adaptive Task Routing for Claude Code

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

The Claude Code directory submission is under review. Until it is listed, clone the public repository and launch Claude Code with the plugin directory:

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

## First use

Start a new session and ask a substantial question, such as:

> Audit this project's release workflow and propose an implementation plan for the main risks.

Explicit activation is available as `/adaptive-task-routing:adaptive-task-routing`.

## What you will see

The example below uses the request “Review the plugin release process, cross-platform consistency, and test gaps.” Actual plans and recommendations vary by task and platform.

### Example response

#### 1. AI task plan

```text
1. Inspect release scripts and manifests.
2. Review CI and test gaps.
3. Rank the risks and propose an implementation order.
```

#### 2. Adaptive Task Routing resource recommendation

```text
---

### Adaptive Task Routing | Task resource guidance

[Conversation setting]
* Recommendation: Stay in this conversation
* Switch windows: No

[Minimum sufficient AI setting]
* Model: Sonnet
* Reasoning: high

[Recommended AI setting]
* Model: Opus
* Reasoning: high
* Upgrade value: Medium. Better for subtle cross-file dependencies.

This environment cannot change the settings for you. Use Claude's model and effort controls if desired; I will pause while you decide whether to adjust them or continue with the current setting.
```

The model names and effort values are illustrative. Actual recommendations use options evidenced for the current Claude environment. In `ask`, Claude stops after this block; `auto` may continue already authorized work.

## Change modes in conversation

- “Set Adaptive Task Routing to auto for this conversation.”
- “Set model routing to ask.”
- “Turn context routing off for this task.”
- “What routing modes are active?”

An unqualified mode change applies to both independent routers. The default is `ask`; `auto` applies only changes Claude can perform and verify; `off` skips the selected router.

## What are recommendations based on?

- **Conversation context:** Assesses which information the next task needs and whether old assumptions or constraints might interfere, then recommends staying, handing off relevant information, or starting fresh.
- **Model and reasoning effort:** Considers task difficulty, ambiguity, error cost, and verification needs to provide minimum-sufficient and recommended settings and explain whether an upgrade is worthwhile.
- **Model information:** Prioritizes information available from the current environment. When unavailable, uses valid bundled references appropriate to the platform. A reference does not guarantee that your account can select that model.

See [Design and architecture](../../docs/architecture.md) for the full decision principles and platform limitations.

## Remove

For a `--plugin-dir` session, exit Claude Code and delete the cloned directory. Marketplace users can remove it through `/plugin` after the public listing becomes available.

For validation and publication details, see [Development notes](DEVELOPMENT.md). The canonical source is the [main project](https://github.com/zyzdev/adaptive-task-routing).
