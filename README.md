# dev-intake-bot

開発要望をヒアリングして実装判断を出力するチャット Bot。

Claude API のマルチターン会話を使い、曖昧な開発要望を受け取って必要な情報を 1 問ずつヒアリングし、「実装可否・推定工数・スコープ・前提条件」を構造化して出力します。

## デモ

→ [GitHub Pages で試す](https://liatris000.github.io/liatris-20260504-dev-intake-bot/)

## ファイル構成

```
.
├── index.html   # ブラウザ版（GitHub Pages 対応）
└── bot.py       # CLI 版（Python スクリプト）
```

## CLI 版の使い方

```bash
pip install anthropic
ANTHROPIC_API_KEY=your_key python bot.py
```

## ブラウザ版の使い方

1. 上記デモリンクを開く
2. Anthropic API キーを入力して「保存」
3. 開発要望を入力して送信

API キーはブラウザのメモリにのみ保持されます。

## 技術スタック

- Python 3.11+ / `anthropic` SDK
- HTML + Vanilla JavaScript（ビルドツールなし）
- Claude claude-sonnet-4-6 (claude-sonnet-4-6)

## ライセンス

MIT
