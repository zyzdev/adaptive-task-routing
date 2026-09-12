# Adaptive Task Routing for Claude Code

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 帮助 Claude 为下一个实质阶段选择对话环境、模型和推理强度。Claude 会先给出你要求的发现或计划，再显示资源建议。

## 安装

Claude Code 公开目录申请正在审核中。正式上架前，可克隆公开仓库并通过插件目录启动 Claude Code：

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

## 第一次使用

开启新会话，输入一个有一定规模的任务，例如：

> 审核这个项目的发布流程，并为主要风险提出实施计划。

需要明确启用时，可使用 `/adaptive-task-routing:adaptive-task-routing`。

## 在对话中切换模式

- “这个对话的 Adaptive Task Routing 改用 auto。”
- “模型路由改成 ask。”
- “这次关闭对话路由。”
- “当前两个路由模式是什么？”

未指定 Router 的模式切换会同时应用到两者。默认为 `ask`；`auto` 只应用 Claude 能执行并验证的变更；`off` 跳过指定 Router。

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
* Model：Sonnet
* Reasoning：high

【建议 AI 设置】
* Model：Opus
* Reasoning：high
* 升级价值：中。更适合追踪不易察觉的跨文件依赖。

当前环境无法代为切换设置。如有需要，可使用 Claude 的模型和推理强度控制；我先停在这里，等你决定调整或沿用当前设置。
```

模型名称和强度仅为示例；实际建议只使用当前 Claude 环境中有依据的选项。`ask` 会停在此区块；`auto` 可以继续已经授权的工作。

## 移除

如果通过 `--plugin-dir` 启动，结束 Claude Code 并删除克隆目录即可。公开上架后，Marketplace 用户可通过 `/plugin` 移除。

验证和发布细节请参阅[开发说明](DEVELOPMENT.md)。正式来源位于[主项目](https://github.com/zyzdev/adaptive-task-routing)。
