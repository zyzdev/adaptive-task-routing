# Adaptive Task Routing — 使用指南

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 帮助 AI 判断大型任务是否应留在当前对话，以及下一阶段适合使用哪个模型和推理强度。AI 会先给出你要求的分析或计划，再用独立区块显示资源建议。

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

## 明确启用

- 支持 Skill 提及的 Codex 界面：`$adaptive-task-routing`
- Claude Code：`/adaptive-task-routing:adaptive-task-routing`
- 其他界面：输入“开始这项工作前，请使用 adaptive-task-routing Skill。”

## 模式

- `ask`（默认）：显示建议，并在大量执行前等待用户回复。
- `auto`：只应用当前宿主允许且能够验证的变更，然后继续。
- `off`：跳过该 Router。

对话路由和模型路由可以分别设置模式。若要更改默认值，请编辑已安装插件中的 `shared/defaults.yaml`，然后重新启动宿主。

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

开发和验证细节请返回[项目 README](../../README.md)。
