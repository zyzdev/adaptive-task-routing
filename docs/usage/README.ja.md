# Adaptive Task Routing — ユーザーガイド

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing は、大規模な作業を現在の会話で続けるべきか、次の段階にどのモデルと推論強度が適しているかを AI が判断するためのプラグインです。AI は依頼された分析または計画を先に提示し、その後、明確に区切られたセクションでリソース設定を提案します。

## インストール

### Gemini CLI

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

インストール後、Gemini CLI を再起動してください。

### Claude Code

公開ディレクトリへの申請は審査中です。掲載されるまでは、専用リポジトリをクローンし、プラグインディレクトリを指定して Claude Code を起動できます。

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

### ChatGPT と Codex

[v0.4.2 Release](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2) から `adaptive-task-routing-openai-0.4.2.zip` をダウンロードしてください。ローカルプラグインに対応した画面では、展開したプラグインを Plugin または Marketplace の機能から追加します。公開ディレクトリでの提供は OpenAI の審査結果によります。

## 最初の使い方

インストール後に新しい会話を開始し、ある程度大きなタスクを入力します。例：

> このプロジェクトのリリース手順、プラットフォーム間の整合性、テストの不足を調査してください。

AI は先に有用な調査結果または実行可能な計画を提示します。次の段階がルーティング対象の場合、続けて **Adaptive Task Routing** のリソース提案が表示されます。

- 現在の会話を継続するか
- 最低限十分なモデルと推論強度
- 推奨モデルと推論強度
- 必要な場合はアップグレードの価値

既定の `ask` モードでは、提案後に一時停止して自然な返答を待ちます。設定を変更する、そのまま続ける、別の方法を指定する、のいずれも選べます。決められた返信文は不要です。

## 明示的に起動する

- Skill メンション対応の Codex：`$adaptive-task-routing`
- Claude Code：`/adaptive-task-routing:adaptive-task-routing`
- その他：「この作業を始める前に adaptive-task-routing Skill を使用してください」と依頼します。

## モード

- `ask`（既定）：提案を表示し、大規模な実行の前にユーザーの返答を待ちます。
- `auto`：現在のホストが許可し、結果を検証できる変更だけを適用して続行します。
- `off`：該当 Router を実行しません。

会話ルーティングとモデルルーティングは別々に設定できます。既定値を変更するには、インストール済みプラグインの `shared/defaults.yaml` を編集し、ホストを再起動してください。

## アンインストール

Gemini CLI：

```bash
gemini extensions uninstall adaptive-task-routing
```

Claude Code を `--plugin-dir` で起動した場合は、そのセッションを終了してクローンしたディレクトリを削除します。ChatGPT または Codex では、インストールに使用した Plugin または Marketplace の画面から無効化または削除してください。

## トラブルシューティング

- インストールまたは更新後は、新しい会話を開始してください。
- Skill 一覧に `adaptive-task-routing`、`task-context-router`、`research-model-router` があることを確認してください。
- 提案が表示されない場合は、一度明示的に Skill を起動してください。
- 提案の表示だけでは、モデルや会話が切り替わったことを意味しません。検証できた自動変更だけが適用済みとして報告されます。

開発と検証の詳細は[プロジェクト README](../../README.md)を参照してください。
