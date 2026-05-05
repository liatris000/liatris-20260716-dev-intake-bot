#!/usr/bin/env python3
"""
dev-intake-bot: 開発要望をヒアリングして実装判断を出力する CLI Bot

使い方:
    ANTHROPIC_API_KEY=your_key python bot.py

依存:
    pip install anthropic
"""

import json
import os
import sys

try:
    import anthropic
except ImportError:
    print("anthropic パッケージが必要です: pip install anthropic", file=sys.stderr)
    sys.exit(1)

SYSTEM_PROMPT = """\
あなたは経験豊富なソフトウェアエンジニアリングコンサルタントです。
ユーザーから開発要望を受け取り、実装判断に必要な情報をヒアリングします。

## 役割
1. ユーザーの開発要望を受け取る
2. 実装判断に必要な情報を 1 問ずつヒアリングする（最大 4 ターン）
3. 情報が揃ったら [READY_TO_JUDGE] マーカーを出力し、続けて JSON を出力する

## ヒアリングで確認すること（優先順）
- 技術スタック・既存システムの状況（フレームワーク、言語、インフラ）
- Done の定義（どうなれば完了と言えるか）
- デザイン・UI の制約（既存コンポーネントがあるか）
- セキュリティ・権限の要件
- 期日・優先度

1 ターンに 1 つの質問だけ投げる。複数の質問を一度に投げない。

## 出力タイミング
「実装可否を判断するのに情報が揃った」と判断したら、
ヒアリングを終了して以下の形式で出力する:

[READY_TO_JUDGE]
{
  "feasibility": "high | medium | low",
  "reason": "判断の根拠（1〜2文）",
  "effort_min_days": 数値,
  "effort_max_days": 数値,
  "scope": ["スコープ項目1", "スコープ項目2"],
  "out_of_scope": ["今回の対象外1"],
  "prerequisites": ["前提条件1"],
  "risks": ["リスク1"]
}

情報収集中は JSON を出力しない。ヒアリングだけ行う。
"""

READY_MARKER = "[READY_TO_JUDGE]"
MAX_TURNS = 6


def parse_judgment(text: str) -> dict | None:
    """[READY_TO_JUDGE] マーカー以降の JSON を抽出してパース"""
    idx = text.find(READY_MARKER)
    if idx == -1:
        return None
    raw = text[idx + len(READY_MARKER):].strip()
    # コードブロック (```json ... ```) で囲まれている場合を除去
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"raw": raw}


def print_judgment(judgment: dict) -> None:
    """実装判断を整形して出力"""
    print("\n" + "=" * 55)
    print("  📋  実装判断レポート")
    print("=" * 55)

    feasibility_label = {
        "high": "✅  実装可能",
        "medium": "⚠️   条件付き可能",
        "low": "❌  要再検討",
    }
    feasibility = judgment.get("feasibility", "")
    print(f"実装可否  : {feasibility_label.get(feasibility, feasibility)}")
    print(f"根拠      : {judgment.get('reason', '')}")

    lo = judgment.get("effort_min_days", "?")
    hi = judgment.get("effort_max_days", "?")
    print(f"推定工数  : {lo}〜{hi} 日")

    for label, key in [
        ("スコープ", "scope"),
        ("今回の対象外", "out_of_scope"),
        ("前提条件", "prerequisites"),
        ("リスク", "risks"),
    ]:
        items = judgment.get(key, [])
        if items:
            print(f"\n{label}:")
            markers = {"スコープ": "✓", "今回の対象外": "✗", "前提条件": "⚡", "リスク": "⚠"}
            for item in items:
                print(f"  {markers.get(label, '-')} {item}")

    print("=" * 55)


def run() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("環境変数 ANTHROPIC_API_KEY を設定してください", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    messages: list[dict] = []

    print("=== 開発要望ヒアリング Bot ===")
    print("開発したいもの・改善したいことを教えてください。(終了: Ctrl+C)\n")

    try:
        user_input = input("あなた: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if not user_input:
        return

    messages.append({"role": "user", "content": user_input})

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        assistant_text = response.content[0].text
        messages.append({"role": "assistant", "content": assistant_text})

        if READY_MARKER in assistant_text:
            # マーカー前の発言（あれば）を表示
            pre_text = assistant_text[:assistant_text.index(READY_MARKER)].strip()
            if pre_text:
                print(f"\nBot: {pre_text}")

            judgment = parse_judgment(assistant_text)
            if judgment and "raw" not in judgment:
                print_judgment(judgment)
            else:
                print("\n--- 判断出力 ---")
                print(judgment.get("raw", "") if judgment else assistant_text)
            return

        print(f"\nBot: {assistant_text}\n")

        try:
            user_input = input("あなた: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not user_input:
            return

        messages.append({"role": "user", "content": user_input})

    print("\n⚠️ ターン数の上限に達しました。続きは直接 Claude にお問い合わせください。")


if __name__ == "__main__":
    run()
