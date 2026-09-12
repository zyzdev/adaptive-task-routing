# Adaptive Task Routing — 使用指南

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

### Gemini CLI

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

安装完成后，请重新启动 Gemini CLI。

### Claude Code

公开目录申请正在审核中。正式上架前，可克隆专用仓库并通过插件目录启动 Claude Code：

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

### ChatGPT 和 Codex

从 [v0.4.2 Release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2) 下载 `adaptive-task-routing-openai-0.4.2.zip`。如果当前界面支持本地插件，请解压后通过插件或 Marketplace 功能添加。公开目录是否可用仍取决于 OpenAI 的审核结果。

## 第一次使用

安装后开启新对话，输入一个有一定规模的任务，例如：

> 扫描这个项目的发布流程、跨平台一致性和测试缺口。

AI 应先给出有效的检查结果或可执行计划。如果下一阶段符合路由条件，随后会显示 **Adaptive Task Routing** 资源建议，包括：

- 是否留在当前对话；
- 最低足够的模型和推理强度；
- 推荐的模型和推理强度；
- 必要时说明升级价值。

默认 `ask` 模式会在建议后暂停，等待你的自然回复。你可以先调整设置、要求沿用当前设置，或选择其他做法，不需要使用指定回复词。

## 你会看到什么

以下以“检查 Plugin 的发布流程、跨平台一致性和测试缺口”为例。实际的计划和建议会依任务及平台调整。

### 回复示例

#### 1. AI 的任务计划

```text
1. 核对发布脚本和三个平台的 Manifest。
2. 检查 CI、版本和测试缺口。
3. 整理风险并提出修改顺序。
```

#### 2. Adaptive Task Routing 的资源建议

```text
---

### Adaptive Task Routing｜任务资源建议

以下建议根据上述计划的下一阶段，评估合适的对话环境、模型和推理设置。

【对话设置】
* 建议：留在当前对话
* 是否切换窗口：否
当前对话保留了下一阶段需要的需求和证据，因此直接继续。

【最低足够 AI 设置】
* Model：GPT-5.6 Sol
* Reasoning：high
足以完成跨文件核对和常规验证。

【建议 AI 设置】
* Model：GPT-6 Astra
* Reasoning：high
* 升级价值：中。更适合追踪跨平台设置之间的隐性关联。

当前环境无法代为切换模型和推理强度。如需采用建议，可使用界面中的模型和推理强度选单调整；我先停在这里，等你决定是否调整，或沿用当前设置开始下一阶段。
```

`ask` 模式会停在这里；`auto` 模式只应用平台支持且能够验证的变更，并可继续已经授权的工作。Gemini 会使用平台原生模型别名，Reasoning 通常显示为“使用模型默认值”。

## 模式

- `ask`（默认）：显示建议，并在大量执行前等待用户回复。
- `auto`：只应用当前宿主允许且能够验证的变更，然后继续。
- `off`：跳过该 Router。

对话路由和模型路由可以分别设置，并且能够直接在 AI 对话中切换，例如：

- “这个对话的 Adaptive Task Routing 改用 auto。”
- “模型路由改成 ask。”
- “这次关闭对话路由。”
- “当前两个路由模式是什么？”

没有指定 Router 的 Adaptive Task Routing 模式会同时应用到两者。AI 会立即确认实际模式和作用范围，不会为了切换模式额外运行一次 Routing 建议。若要在新对话中继续使用，请明确要求设为默认；宿主没有可写入的用户设置区时，设置只保留在当前对话，AI 会说明这一限制。

## 建议根据什么？

- **对话环境：** 评估下一个任务需要沿用哪些信息，以及旧任务的假设或限制是否可能干扰新工作，再建议保留对话、整理信息后交接，或从新对话开始。
- **模型和推理强度：** 考量任务难度、模糊程度、错误成本和验证需求，提供最低足够及建议设置，并说明提高设置是否值得。
- **模型信息来源：** 优先使用当前环境可取得的信息；无法取得时，根据平台使用套件内有效的参考资料。参考资料不代表你的账号一定能选用该模型。

完整判断原则与平台限制可查阅[设计与架构（英文）](../architecture.md)。

## 明确启用

- 支持 Skill 提及的 Codex 界面：`$adaptive-task-routing`
- Claude Code：`/adaptive-task-routing:adaptive-task-routing`
- 其他界面：输入“开始这项工作前，请使用 adaptive-task-routing Skill。”

## 移除

Gemini CLI：

```bash
gemini extensions uninstall adaptive-task-routing
```

Claude Code 如果通过 `--plugin-dir` 启动，结束该会话并删除克隆目录即可。ChatGPT 或 Codex 则从安装时使用的插件或 Marketplace 界面停用或移除。

## 故障排查

- 安装或更新后，请开启新对话。
- 确认 Skill 列表包含 `adaptive-task-routing`、`task-context-router` 和 `research-model-router`。
- 没有出现建议时，可先明确启用 Skill 测试一次。
- 显示建议不代表宿主已经切换模型或对话；只有经过验证的自动变更才会报告为已应用。

开发和验证细节请返回[开发说明（英文）](https://github.com/zyzdev/adaptive-task-routing/blob/main/DEVELOPMENT.md)。
