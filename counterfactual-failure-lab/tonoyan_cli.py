from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from lasuch_patterns import InfectionCounter, detect_patterns


def analyze_text(text: str, context_mode: str = "executable") -> Dict[str, Any]:
    matches = detect_patterns(text, context_mode=context_mode)
    counter = InfectionCounter()
    statuses: List[Dict[str, Any]] = []

    for match in matches:
        status = counter.register(match.family)
        statuses.append(
            {
                "family": match.family,
                "tag": match.tag,
                "severity": match.severity,
                "action": match.action,
                "status": status,
                "span": match.span,
            }
        )

    return {
        "context_mode": context_mode,
        "match_count": len(matches),
        "matches": statuses,
        "counter_status": counter.status(),
    }


def read_input(text: str | None, file_path: str | None) -> str:
    if text:
        return text
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(description="Tonoyan CLI — test Łasuch pattern detection")
    parser.add_argument("--text", type=str, help="Direct text input")
    parser.add_argument("--file", type=str, help="Path to input file")
    parser.add_argument("--context", type=str, default="executable", choices=["executable", "quoted", "documentation", "analysis"], help="Context mode")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    text = read_input(args.text, args.file)
    result = analyze_text(text, context_mode=args.context)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print(f"Tonoyan CLI — context={result['context_mode']}")
    print(f"Matches: {result['match_count']}")

    if not result["matches"]:
        print("No active patterns detected.")
        return 0

    for item in result["matches"]:
        print(
            f"- {item['family']} | tag={item['tag']} | severity={item['severity']} | action={item['action']} | status={item['status']} | span={item['span']}"
        )

    print("Counter:")
    print(json.dumps(result["counter_status"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
