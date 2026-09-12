# Adaptive Task Routing for ChatGPT 和 Codex

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 帮助 ChatGPT 和 Codex 为下一个实质阶段选择对话环境、模型和推理强度。AI 会先给出你要求的发现或计划，再显示资源建议。

## 安装

公开 Plugin 通过 OpenAI Plugins portal 管理。正式上架前，可从[最新版本](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2)下载 `adaptive-task-routing-openai-0.4.2.zip`，解压后将该目录注册为本地 Plugin 来源或 Marketplace。

Codex CLI 可从已设置的 Marketplace 安装；公开上架后，ChatGPT 和 Codex App 可直接从 Plugins Directory 选择。

## 第一次使用

开始新对话并输入有一定规模的任务，例如：

> 审查这个项目的发布流程，并针对主要风险提出实施计划。

支持具名 Skill 的界面也可使用 `$adaptive-task-routing` 明确启用。

## 在对话中切换模式

- “这个对话的 Adaptive Task Routing 改用 auto。”
- “模型路由改成 ask。”
- “这次关闭对话路由。”
- “目前两个路由模式是什么？”

未指定 Router 的模式切换会同时应用到两者。默认为 `ask`；`auto` 只应用当前 OpenAI 界面能执行并验证的变更；`off` 跳过指定 Router。

## 你会看到什么

以下以“检查 Plugin 的发布流程、跨平台一致性和测试缺口”为例。实际的计划和建议会依任务及平台调整。

### 回复示例

#### 1. AI 的任务计划

```text
1. 检查发布脚本和 Manifest。
2. 核对 CI 和测试缺口。
```

#### 2. Adaptive Task Routing 的资源建议

```text
---

### Adaptive Task Routing｜任务资源建议

【对话设置】
* 建议：留在当前对话
* 是否切换窗口：否

【最低足够 AI 设置】
* Model：GPT-5.6 Sol
* Reasoning：high

【建议 AI 设置】
* Model：GPT-6 Astra
* Reasoning：high
* 升级价值：中。更适合追踪不易察觉的跨文件依赖。

当前环境无法代为切换设置。如有需要，可使用 ChatGPT 或 Codex App 的模型和推理强度选单，Codex CLI 则可使用 `/model`；我先停在这里，等你决定调整或沿用当前设置。
```

模型名称和强度仅为示例；实际建议只使用当前 OpenAI 环境中有依据的选项。`ask` 会停在此区块；`auto` 可以继续已经授权的工作。

## 移除

可通过 Plugins Directory 或已设置的 Codex Marketplace 移除。若是手动解压的本地版本，请移除 Marketplace 项目并删除该目录。

打包、验证和发布细节请参阅[开发说明](DEVELOPMENT.md)。
