# Adaptive Task Routing

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](docs/usage/README.zh-CN.md) · [日本語](docs/usage/README.ja.md) · [한국어](docs/usage/README.ko.md)

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

Choose the guide for your platform:

| Platform | Installation and usage guide |
| --- | --- |
| ChatGPT / Codex | [OpenAI edition](packaging/openai/README.md) |
| Claude Code | [Claude edition](packaging/claude/README.md) |
| Gemini CLI | [Gemini edition](packaging/gemini/README.md) |

## First use

After installing and enabling the plugin, start a new conversation and submit a substantial task, for example:

> I want to review this plugin's release process, cross-platform consistency, and test gaps. Please propose an execution plan first.

If no recommendation appears, you can explicitly ask: “Use the adaptive-task-routing skill before starting the next phase.”

## What you will see

The following response illustrates the task above. Actual plans, models, and reasoning settings vary by task and platform.

### Example response

#### 1. AI task plan

```text
1. Check the release scripts and manifests for each platform.
2. Review CI, version consistency, and test gaps.
3. Rank the risks and propose an implementation order.
```

#### 2. Adaptive Task Routing resource recommendation

```text
---

### Adaptive Task Routing | Task resource guidance

The following recommendations assess the conversation, model, and reasoning resources for the next phase of the plan above.

[Conversation setting]

- Recommendation: Stay in this conversation
- Switch windows: No

This conversation already contains the project location and review goals, so it is suitable for the next phase.

[Minimum sufficient AI setting]

- Model: GPT-5.6 Sol
- Reasoning: high

Sufficient for reviewing release scripts, platform differences, and existing test coverage.

[Recommended AI setting]

- Model: GPT-6 Astra
- Reasoning: high
- Upgrade value: Medium. Better suited to tracing release workflows, platform-specific branches, and subtle failure paths together.

This environment cannot change the model or reasoning effort for you. Use the interface's model and reasoning controls if you want the recommendation. I will pause here while you decide whether to adjust the settings or continue with the current ones.
```

This example shows `ask` mode when automatic switching is unavailable. Claude and Gemini use their own model options; control instructions also vary by interface.

## Change modes in conversation

Tell the AI directly:

- “Set Adaptive Task Routing to auto for this conversation.”
- “Set model routing to ask.”
- “Turn context routing off for this task.”
- “What routing modes are active?”

| Mode | Behavior |
| --- | --- |
| `ask` (default) | Shows recommendations, then pauses for your decision. |
| `auto` | Applies authorized, supported, verifiable changes and continues already authorized work; explains what happens when an operation cannot be performed automatically. |
| `off` | Disables the selected router. |

Context and model routing can be configured separately. A mode change that does not name a router applies to both. You can reply naturally, revise the recommendation, or ask to keep the current settings; no fixed reply phrase is required.

## What are recommendations based on?

- **Conversation context:** Assesses which information the next task needs and whether old assumptions or constraints might interfere, then recommends staying, handing off relevant information, or starting fresh.
- **Model and reasoning effort:** Considers task difficulty, ambiguity, error cost, and verification needs to provide minimum-sufficient and recommended settings and explain whether an upgrade is worthwhile.
- **Model information:** Prioritizes information available from the current environment. When unavailable, uses valid bundled references appropriate to the platform. A reference does not guarantee that your account can select that model.

See [Design and architecture](docs/architecture.md) for the full decision principles and platform limitations.

## More information

- [Full user guide and removal instructions](docs/usage/README.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Development and validation](DEVELOPMENT.md)
- [Release workflow](docs/release.md)
- [Security policy](SECURITY.md)
- [MIT license](LICENSE)
