# Adaptive Task Routing for Gemini CLI

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

Adaptive Task Routing は、次の重要な作業段階に適した会話環境とモデルを Gemini が選ぶための拡張機能です。Gemini は依頼された調査結果または計画を先に提示し、その後にリソース設定を提案します。

## インストール

```bash
gemini extensions install https://github.com/zyzdev/adaptive-task-routing-gemini --ref v0.4.2
```

インストール後に Gemini CLI を再起動し、`gemini extensions list` で確認してください。

## 最初の使い方

新しいセッションを開始し、ある程度大きなタスクを入力します。例：

> このプロジェクトのリリース手順を監査し、主なリスクの実装計画を作成してください。

明示的に起動する場合は、`adaptive-task-routing` Skill を使用するよう Gemini に依頼します。

## 会話でモードを変更する

- 「この会話では Adaptive Task Routing を auto にしてください」
- 「モデルルーティングを ask にしてください」
- 「今回だけ会話ルーティングを off にしてください」
- 「現在の二つのルーティングモードを教えてください」

Router を指定しない変更は両方に適用されます。既定は `ask`、`auto` は Gemini が実行して検証できる変更だけを適用し、`off` は指定した Router を省略します。

## 表示される内容

```text
計画
1. リリーススクリプトと Manifest を確認する。
2. CI とテストの不足を確認する。

---

### Adaptive Task Routing｜タスクリソースの提案

【会話設定】
* 提案：現在の会話を続ける
* ウィンドウを切り替える：いいえ

【最低限十分な AI 設定】
* Model：Flash
* Reasoning：モデル既定値

【推奨 AI 設定】
* Model：Pro
* Reasoning：モデル既定値
* アップグレード価値：中。見落としやすいファイル間の依存関係を追跡しやすくなります。

現在の環境ではモデルを自動変更できません。推奨モデルを使う場合は /model で選択してください。変更するか現在の設定を使うか決まるまで、ここで待機します。
```

モデル別名は例であり、現在の Gemini アカウントに応じて解決されます。セッションに明示的な思考設定がある場合だけその値を表示し、それ以外はモデル既定値を使用します。`ask` はここで停止し、`auto` は承認済みの作業を続けられます。

## アンインストール

```bash
gemini extensions uninstall adaptive-task-routing
```

削除後に Gemini CLI を再起動してください。

検証と Gallery については[開発者向け情報](DEVELOPMENT.md)を参照してください。正式なソースは[メインプロジェクト](https://github.com/zyzdev/adaptive-task-routing)にあります。
