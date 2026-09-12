# ChatGPT と Codex 向け Adaptive Task Routing

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing は、次の重要な作業段階に適した会話環境、モデル、推論強度を ChatGPT と Codex が選ぶためのプラグインです。AI は依頼された調査結果または計画を先に提示し、その後にリソース設定を提案します。

## インストール

公開プラグインは OpenAI Plugins portal で管理されます。公開前は、[最新リリース](https://github.com/zyzdev/adaptive-task-routing/releases/tag/v0.4.2)から `adaptive-task-routing-openai-0.4.2.zip` をダウンロードして展開し、そのディレクトリをローカルプラグインソースまたは Marketplace として登録してください。

Codex CLI では設定済み Marketplace からインストールできます。公開後は、ChatGPT と Codex App の Plugins Directory から選択できます。

## 最初の使い方

新しい会話を開始し、ある程度大きなタスクを入力します。例：

> このプロジェクトのリリース手順を監査し、主なリスクに対する実装計画を提案してください。

名前付き Skill に対応する画面では、`$adaptive-task-routing` で明示的に有効化できます。

## 会話内でモードを変更する

- 「この会話では Adaptive Task Routing を auto にしてください」
- 「モデルルーターを ask にしてください」
- 「このタスクでは会話ルーターを無効にしてください」
- 「現在のルーターモードを教えてください」

Router を指定しない変更は両方に適用されます。既定は `ask` です。`auto` は現在の OpenAI 画面で実行と検証が可能な変更だけを適用し、`off` は指定した Router を省略します。

## 表示される内容

以下は「プラグインのリリース工程、プラットフォーム間の整合性、テスト不足を確認する」という依頼の例です。実際の計画と提案は、タスクやプラットフォームに応じて変わります。

### 応答例

#### 1. AI のタスク計画

```text
1. リリーススクリプトと Manifest を確認する。
2. CI とテストの不足を確認する。
3. リスクを整理し、修正の順序を提案する。
```

#### 2. Adaptive Task Routing のリソース提案

```text
---

### Adaptive Task Routing｜タスクリソースの提案

【会話設定】
* 提案：現在の会話を続ける
* ウィンドウを切り替える：いいえ

【最低限十分な AI 設定】
* Model：GPT-5.6 Sol
* Reasoning：high

【推奨 AI 設定】
* Model：GPT-6 Astra
* Reasoning：high
* アップグレード価値：中。見落としやすいファイル間の依存関係を追跡しやすくなります。

現在の環境では設定を自動変更できません。必要に応じて ChatGPT または Codex App のモデルと推論強度の選択肢を使用し、Codex CLI では `/model` を使用してください。変更するか現在の設定を使うか決まるまで、ここで待機します。
```

モデル名と強度は例です。実際の提案では現在の OpenAI 環境で確認できた選択肢だけを使用します。`ask` はここで停止し、`auto` は承認済みの作業を続けられます。

## 削除

Plugins Directory または設定済みの Codex Marketplace から削除できます。手動で展開したローカル版は、Marketplace の登録を解除してからディレクトリを削除してください。

パッケージ、検証、公開の詳細は[開発者向け情報](DEVELOPMENT.md)を参照してください。
