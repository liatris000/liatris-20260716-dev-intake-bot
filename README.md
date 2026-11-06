# dev-intake-bot

開発要望をヒアリングして実装判断を出力するチャット Bot。

Claude API のマルチターン会話を使い、曖昧な開発要望を受け取って必要な情報を 1 問ずつヒアリングし、「実装可否・推定工数・スコープ・前提条件」を構造化して出力する。

記事: https://zenn.dev/liatris/articles/20260716-dev-intake-bot

## 前提

- Python 3.11 以上と `anthropic` SDK(CLI 版)
- Anthropic の API キー(CLI 版・ブラウザ版のどちらも必要)
- 使うモデルは `claude-sonnet-4-6`(`bot.py` と `index.html` に書いてある)

## デモ

→ [GitHub Pages で試す](https://liatris000.github.io/liatris-20260716-dev-intake-bot/)

## 動かし方

### CLI 版

```bash
git clone https://github.com/liatris000/liatris-20260716-dev-intake-bot.git
cd liatris-20260716-dev-intake-bot
pip install anthropic
ANTHROPIC_API_KEY=sk-ant-... python3 bot.py
```

### ブラウザ版

1. 上のデモリンクを開く
2. Anthropic API キーを入力して「保存」
3. 開発要望を入力して送信

API キーはブラウザのメモリにだけ保持する。ブラウザから Anthropic API を直接呼ぶ構成なので、個人のデモ用途に限る。本番で使うならバックエンドのプロキシを挟む。

## 期待される出力

API キーを設定せずに CLI 版を起動すると、API を呼ぶ前に次を出して終了コード 1 で止まる。

```text
環境変数 ANTHROPIC_API_KEY を設定してください
```

キーを設定すると「あなた: 」の入力待ちになり、1 問ずつ質問が返ってくる。最後に実装可否・推定工数レンジ・スコープ・前提条件が出る。

## 確かめていない範囲

- API キーを使った実行(CLI 版・ブラウザ版とも)は、このリポジトリの見直しでは行っていない。上の出力例はキーなしの場合だけ
- 判断の精度(工数の見積もりが当たっているか)は検証していない
- テストコードは無い

## ファイル構成

```
.
├── index.html   # ブラウザ版(GitHub Pages)
└── bot.py       # CLI 版(Python スクリプト)
```

## ライセンス

MIT
