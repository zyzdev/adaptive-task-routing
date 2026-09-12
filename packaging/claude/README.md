# Adaptive Task Routing for Claude Code

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing helps Claude choose the conversation context, model, and reasoning effort for the next substantial phase. Claude presents the requested findings or plan first, then shows the resource recommendation.

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

## Change modes in conversation

- “Set Adaptive Task Routing to auto for this conversation.”
- “Set model routing to ask.”
- “Turn context routing off for this task.”
- “What routing modes are active?”

An unqualified mode change applies to both independent routers. The default is `ask`; `auto` applies only changes Claude can perform and verify; `off` skips the selected router.

## What you will see

```text
Plan
1. Inspect release scripts and manifests.
2. Review CI and test gaps.

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

## Remove

For a `--plugin-dir` session, exit Claude Code and delete the cloned directory. Marketplace users can remove it through `/plugin` after the public listing becomes available.

For validation and publication details, see [Development notes](DEVELOPMENT.md). The canonical source is the [main project](https://github.com/zyzdev/adaptive-task-routing).
