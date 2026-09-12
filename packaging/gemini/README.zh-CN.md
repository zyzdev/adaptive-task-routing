# Adaptive Task Routing for Gemini CLI

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing 帮助 Gemini 为下一个实质阶段选择对话环境和模型。Gemini 会先给出你要求的发现或计划，再显示资源建议。

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
