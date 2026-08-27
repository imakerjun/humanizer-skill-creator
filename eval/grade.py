#!/usr/bin/env python3
"""메타 스킬(humanizer-skill-creator) 절차 채점기.

사용법: python3 grade.py <case_dir> <result_file>

generated humanizer의 planted/trap 채점이 아니다.
결과에 required 문자열이 있고 forbidden이 없는지만 본다.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def normalize(text: str) -> str:
    text = re.sub(r"\*\*|__", "", text)
    return re.sub(r"\s+", " ", text).lower()


def main() -> int:
    if len(sys.argv) != 3:
        print("사용법: python3 grade.py <case_dir> <result_file>", file=sys.stderr)
        return 2

    case_dir, result_file = Path(sys.argv[1]), Path(sys.argv[2])
    exp = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
    result = normalize(result_file.read_text(encoding="utf-8"))
    failures: list[str] = []

    print(f"=== {exp['case']} — {result_file.name} ===")

    for item in exp.get("required", []):
        needle = normalize(item["match"])
        if needle in result:
            print(f"[필수] 있음 {item['id']} — PASS")
        else:
            print(f"[필수] ✗ 없음 {item['id']}: “{item['match']}” — FAIL")
            print(f"        {item.get('reason', '')}")
            failures.append(f"missing:{item['id']}")

    for item in exp.get("forbidden", []):
        needle = normalize(item["match"])
        if needle in result:
            print(f"[금지] ✗ 등장 {item['id']}: “{item['match']}” — FAIL")
            print(f"        {item.get('reason', '')}")
            failures.append(f"forbidden:{item['id']}")
        else:
            print(f"[금지] 없음 {item['id']} — PASS")

    if exp.get("must_stop"):
        stop_ok = any(normalize(s) in result for s in exp.get("stop_signals", ["멈춘다", "정지", "샘플"]))
        if stop_ok:
            print("[정지] 부족 입력에서 정지 신호 — PASS")
        else:
            print("[정지] ✗ 정지 신호가 없다 — FAIL")
            failures.append("no-stop")

    for j in exp.get("judge_items", []):
        print(f"[판정 필요] {j}")

    print("결과:", "요확인/실패 → " + ", ".join(failures) if failures else "프로그램 채점 전부 PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
