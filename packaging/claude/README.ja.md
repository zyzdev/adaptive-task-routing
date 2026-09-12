# Adaptive Task Routing for Claude Code

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing は、次の重要な作業段階に適した会話環境、モデル、推論強度を Claude が選ぶためのプラグインです。Claude は依頼された調査結果または計画を先に提示し、その後にリソース設定を提案します。

## インストール

Claude Code 公開ディレクトリへの申請は審査中です。掲載されるまでは、公開リポジトリをクローンし、プラグインディレクトリを指定して起動できます。

```bash
git clone --branch v0.4.2 https://github.com/zyzdev/adaptive-task-routing-claude.git
claude --plugin-dir "$PWD/adaptive-task-routing-claude"
```

## 最初の使い方

新しいセッションを開始し、ある程度大きなタスクを入力します。例：

> このプロジェクトのリリース手順を監査し、主なリスクの実装計画を作成してください。

明示的に起動する場合は `/adaptive-task-routing:adaptive-task-routing` を使用します。

## 会話でモードを変更する

- 「この会話では Adaptive Task Routing を auto にしてください」
- 「モデルルーティングを ask にしてください」
- 「今回だけ会話ルーティングを off にしてください」
- 「現在の二つのルーティングモードを教えてください」

Router を指定しない変更は両方に適用されます。既定は `ask`、`auto` は Claude が実行して検証できる変更だけを適用し、`off` は指定した Router を省略します。

## 表示される内容

以下は「プラグインのリリース工程、プラットフォーム間の整合性、テスト不足を確認する」という依頼の例です。実際の計画と提案は、タスクやプラットフォームに応じて変わります。

### 応答例

#### 1. AI のタスク計画

```text
1. リリーススクリプトと Manifest を確認する。
2. CI とテストの不足を確認する。
```

#### 2. Adaptive Task Routing のリソース提案

```text
---

### Adaptive Task Routing｜タスクリソースの提案

【会話設定】
* 提案：現在の会話を続ける
* ウィンドウを切り替える：いいえ

【最低限十分な AI 設定】
* Model：Sonnet
* Reasoning：high

【推奨 AI 設定】
* Model：Opus
* Reasoning：high
* アップグレード価値：中。見落としやすいファイル間の依存関係を追跡しやすくなります。

現在の環境では設定を自動変更できません。必要に応じて Claude のモデルと推論強度の操作を使用してください。変更するか現在の設定を使うか決まるまで、ここで待機します。
```

モデル名と強度は例です。実際の提案では現在の Claude 環境で確認できた選択肢だけを使用します。`ask` はここで停止し、`auto` は承認済みの作業を続けられます。

## アンインストール

`--plugin-dir` で起動した場合は Claude Code を終了し、クローンしたディレクトリを削除します。公開後の Marketplace 版は `/plugin` から削除できます。

検証と公開については[開発者向け情報](DEVELOPMENT.md)を参照してください。正式なソースは[メインプロジェクト](https://github.com/zyzdev/adaptive-task-routing)にあります。
