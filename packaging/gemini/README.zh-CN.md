# Adaptive Task Routing for Gemini CLI

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

**让 AI 的额度用在需要的地方，帮助减少后续工作的遗漏与返工。**

Adaptive Task Routing 会在下一个重要工作阶段开始前，建议是否开启新对话，以及合适的模型和推理强度，帮助你兼顾额度消耗与工作可靠性。

- **减少旧任务对新工作的干扰：** 判断何时应开启新对话，降低 AI 把上一个任务的假设或限制带入新工作的可能性，减少反复纠正与返工；需要延续的信息则整理后交接。
- **减少不必要的消耗：** 提供“最低足够”与“建议”两组模型及推理设置，说明升级是否值得，避免每个任务都使用最高设置。
- **降低遗漏与返工的风险：** 在复杂工作开始前，评估所需的模型能力和推理强度，降低设置不足造成的执行风险。
- **由你决定如何进行：** 可以先看建议再决定，也能选择在平台支持时自动应用设置。

换了主题不代表一定要开启新对话；重点是减少无关历史的干扰，同时保留下一个任务需要的信息。实际节省与可靠性改善取决于任务及采用的设置。

## 运作方式

1. AI 先提出可执行计划，或完成你要求的分析与检查结果。
2. Plugin 评估下一阶段：先建议保留或开启新对话，再提供最低足够与建议的模型、推理强度，以及升级价值。
3. 默认的 `ask` 模式会等待你的决定；`auto` 模式在平台支持且能验证时应用设置，无法切换时会说明并沿用当前设置，继续已授权的工作。

一般问答与微小操作会跳过路由，避免增加不必要的判断与等待。

## 安装

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

安装后请重新启动 Gemini CLI，并通过 `gemini extensions list` 确认 Extension。

## 第一次使用

开启新会话，输入一个有一定规模的任务，例如：

> 审核这个项目的发布流程，并为主要风险提出实施计划。

需要明确启用时，可要求 Gemini 使用 `adaptive-task-routing` Skill。

## 在对话中切换模式

- “这个对话的 Adaptive Task Routing 改用 auto。”
- “模型路由改成 ask。”
- “这次关闭对话路由。”
- “当前两个路由模式是什么？”

未指定 Router 的模式切换会同时应用到两者。默认为 `ask`；`auto` 只应用 Gemini 能执行并验证的变更；`off` 跳过指定 Router。

## 你会看到什么

以下以“检查 Plugin 的发布流程、跨平台一致性和测试缺口”为例。实际的计划和建议会依任务及平台调整。

### 回复示例

#### 1. AI 的任务计划

```text
1. 检查发布脚本和 Manifest。
2. 核对 CI 和测试缺口。
3. 整理风险并提出修改顺序。
```

#### 2. Adaptive Task Routing 的资源建议

```text
---

### Adaptive Task Routing｜任务资源建议

【对话设置】
* 建议：留在当前对话
* 是否切换窗口：否

【最低足够 AI 设置】
* Model：Flash
* Reasoning：使用模型默认值

【建议 AI 设置】
* Model：Pro
* Reasoning：使用模型默认值
* 升级价值：中。更适合追踪不易察觉的跨文件依赖。

当前环境无法代为切换模型。如需采用建议，可用 /model 选择模型；我先停在这里，等你决定调整或沿用当前设置。
```

模型别名仅为示例，会根据当前 Gemini 账号解析。只有会话提供明确思考控制时才显示该值，否则 Reasoning 使用模型默认值。`ask` 会停在此区块；`auto` 可以继续已经授权的工作。

## 移除

```bash
gemini extensions uninstall adaptive-task-routing
```

移除后请重新启动 Gemini CLI。

验证和 Gallery 细节请参阅[开发说明](DEVELOPMENT.md)。正式来源位于[主项目](https://github.com/zyzdev/adaptive-task-routing)。
