#!/usr/bin/env python3
"""개인 humanizer eval 채점기 — 결정적으로 잴 수 있는 것만 잰다.

사람냄새 eval/grade.py를 장르 무관하게 일반화한 템플릿이다.
사용법: python3 grade.py <case_dir> <result_file>

두 모드를 자동 판별한다.
- apply 모드(결과에 수정본 절이 있으면): 수정본에서 planted 부재(=고침)와
  trap 원문 존재(=보존)를 문자열로 검사한다 — trap 부재는 즉시 FAIL.
- propose 모드(그 외): 검토표에 planted 등장(=잡음)과 trap 등장(사람 확인)을 검사한다.

규율(전면 재작성·덮어쓰기·보류 분류)·after 품질은 judge-rubric.md로 사람/LLM이 판정한다.

expected.json 선택 필드:
- headings.revised / headings.log  (기본: 수정본 / 변경 기록)
- tone_forbidden_regex  (문체 이탈. 없으면 tone=="~한다"일 때만 한국어 존댓말 휴리스틱)
- thresholds.recall_min / max_total_flags / max_trap_fp
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def normalize(text: str) -> str:
    text = re.sub(r"\*\*|__", "", text)
    return re.sub(r"\s+", " ", text)


def split_section(result: str, title: str) -> tuple[str | None, str]:
    """제목 섹션을 위치 기반으로 분리해 (섹션 본문, 나머지 전체)를 반환한다."""
    lines = result.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^#{{1,4}}\s*{re.escape(title)}", line.strip()):
            start = i
            break
    if start is None:
        return None, result
    end = start + 1
    while end < len(lines) and not re.match(r"^#{1,3}\s", lines[end]):
        end += 1
    section = "\n".join(lines[start + 1 : end])
    rest = "\n".join(lines[:start] + lines[end:])
    return section, rest


def extract_section(result: str, title: str) -> str | None:
    return split_section(result, title)[0]


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def after_column(text: str) -> list[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    if not lines:
        return []
    header = [c.strip().lower() for c in lines[0].strip("|").split("|")]
    idx = next(
        (i for i, h in enumerate(header) if "after" in h or "제안" in h or "수정" in h),
        None,
    )
    if idx is None:
        return []
    return [r[idx] for r in table_rows(text) if len(r) > idx]


POLITE = re.compile(r"(습니다|합니다|세요|네요|거든요|지요|어요|아요|죠)\s*[.!?'\"』」]*\s*$")


def polite_sentences(chunks: list[str]) -> list[str]:
    hits = []
    for chunk in chunks:
        stripped = re.sub(r"[\"“'‘][^\"”'’]*[\"”'’]", "", chunk)
        for sent in re.split(r"(?<=[.!?])\s+", stripped):
            if sent and POLITE.search(sent.strip()):
                hits.append(sent.strip())
    return hits


def forbidden_tone_hits(text: str, pattern: str) -> list[str]:
    cre = re.compile(pattern)
    hits = []
    for sent in re.split(r"(?<=[.!?。])\s+", text):
        if sent and cre.search(sent):
            hits.append(sent.strip())
    return hits


def main() -> int:
    if len(sys.argv) != 3:
        print("사용법: python3 grade.py <case_dir> <result_file>", file=sys.stderr)
        return 2

    case_dir, result_file = Path(sys.argv[1]), Path(sys.argv[2])
    exp = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
    result_raw = result_file.read_text(encoding="utf-8")
    headings = exp.get("headings", {})
    revised_title = headings.get("revised", "수정본")
    log_title = headings.get("log", "변경 기록")

    failures: list[str] = []
    revised, rest_raw = split_section(result_raw, revised_title)
    mode = "apply" if revised is not None else "propose"
    print(f"=== {exp['case']} — {result_file.name} [{mode} 모드] ===")

    planted = exp.get("planted", [])
    traps = exp.get("traps", [])
    thresholds = exp.get("thresholds", {})

    if mode == "apply":
        revised = re.sub(r"<!--[\s\S]*?-->", "", revised)
        rev_norm = normalize(revised)
        rest_norm = normalize(re.sub(r"<!--[\s\S]*?-->", "", rest_raw))
        if planted:
            caught, missed = [], []
            for p in planted:
                m = normalize(p["match"])
                if m not in rev_norm:
                    caught.append((p, "적용"))
                elif m in rest_norm:
                    caught.append((p, "보류/제안"))
                else:
                    missed.append(p)
            recall = len(caught) / len(planted)
            thr = thresholds.get("recall_min")
            ok = thr is None or recall >= thr
            napply = sum(1 for _, s in caught if s == "적용")
            print(
                f"[탐지] 잡음 {len(caught)}/{len(planted)} = {recall:.2f}"
                f" (적용 {napply} · 보류 {len(caught) - napply})"
                + (f" (기준 {thr}) {'PASS' if ok else 'FAIL'}" if thr is not None else "")
            )
            for p in missed:
                print(f"  - 놓침 {p['id']}: “{p['span']}” ({p['type']})")
            if not ok:
                failures.append("recall")
        for t in traps:
            if normalize(t["match"]) in rev_norm:
                print(f"[분별] trap 보존 {t['id']} — PASS")
            else:
                print(f"[분별] ✗ trap 훼손 {t['id']}: “{t['match']}” 이 수정본에 없다 — FAIL")
                print(f"        보존 이유: {t['reason']}")
                failures.append(f"trap:{t['id']}")
        for b in exp.get("known_borderline", []):
            status = (
                "보존"
                if normalize(b["span"][:12]) in rev_norm
                else "수정/삭제(저자 판정 대상이었음 — 기록 확인)"
            )
            print(f"[경계] {status}: “{b['span'][:30]}…”")
        log = extract_section(result_raw, log_title) or result_raw
        rows = table_rows(log)
        applied = [r for r in rows if any("적용" in c and "보류" not in c for c in r)]
        held = [r for r in rows if any(c.strip().startswith("보류") for c in r)]
        print(
            f"[형식] 변경 기록 {len(rows)}행 (적용 {len(applied)} · 보류 {len(held)})"
            + (" — 기록표 없음(형식 위반?)" if not rows else "")
        )
        if not rows:
            failures.append("format")
        max_flags = thresholds.get("max_total_flags")
        if max_flags is not None and len(applied) > max_flags:
            print(f"[분별] 적용 {len(applied)}건 > 상한 {max_flags} — FAIL (사람 글 과잉 수정)")
            failures.append("noise")
        tone_hits = []
        custom_re = exp.get("tone_forbidden_regex")
        if custom_re:
            prose = "\n".join(l for l in revised.splitlines() if not l.strip().startswith(">"))
            tone_hits = forbidden_tone_hits(prose, custom_re)
        elif exp.get("tone") == "~한다":
            prose = [l for l in revised.splitlines() if not l.strip().startswith(">")]
            tone_hits = polite_sentences(prose)
        if exp.get("tone") or custom_re:
            if tone_hits:
                print(f"[문체] 문체 이탈 의심 {len(tone_hits)}건(사람 확인 필요):")
                for s in tone_hits[:5]:
                    print(f"  - {s[:60]}")
                failures.append("tone-review")
            else:
                print("[문체] 잠금 위반 없음 — PASS")
    else:
        result = normalize(result_raw)
        if planted:
            found = [p for p in planted if normalize(p["match"]) in result]
            recall = len(found) / len(planted)
            thr = thresholds.get("recall_min")
            ok = thr is None or recall >= thr
            print(
                f"[탐지] recall {len(found)}/{len(planted)} = {recall:.2f}"
                + (f" (기준 {thr}) {'PASS' if ok else 'FAIL'}" if thr is not None else "")
            )
            for p in planted:
                if p not in found:
                    print(f"  - 놓침 {p['id']}: “{p['span']}” ({p['type']})")
            if not ok:
                failures.append("recall")
        for t in traps:
            if normalize(t["match"]) in result:
                print(f"[분별] ⚠ trap 등장(사람 확인 필요) {t['id']}: “{t['match']}”")
                print(f"        보존 이유: {t['reason']}")
                failures.append(f"trap-review:{t['id']}")
            else:
                print(f"[분별] trap 미등장 {t['id']} — PASS")
        for b in exp.get("known_borderline", []):
            status = (
                "지적함(저자 판정 대기)"
                if normalize(b["span"][:12]) in result
                else "안 잡음(정답)"
            )
            print(f"[경계] {status}: “{b['span'][:30]}…”")
        rows = table_rows(result_raw)
        print(f"[형식] 검토표 행 {len(rows)}건" + (" — 표 없음(형식 위반?)" if not rows else ""))
        max_flags = thresholds.get("max_total_flags")
        if max_flags is not None and len(rows) > max_flags:
            print(f"[분별] 총 지적 {len(rows)}건 > 노이즈 상한 {max_flags} — FAIL")
            failures.append("noise")
        custom_re = exp.get("tone_forbidden_regex")
        if custom_re:
            polite = forbidden_tone_hits("\n".join(after_column(result_raw)), custom_re)
        elif exp.get("tone") == "~한다":
            polite = polite_sentences(after_column(result_raw))
        else:
            polite = []
        if exp.get("tone") or custom_re:
            if polite:
                print(f"[문체] after에 문체 이탈 의심 {len(polite)}건(사람 확인 필요):")
                for s in polite[:5]:
                    print(f"  - {s[:60]}")
                failures.append("tone-review")
            else:
                print("[문체] after 문체 잠금 유지 — PASS")

    for j in exp.get("judge_items", []):
        print(f"[판정 필요] {j}")

    print("결과:", "요확인/실패 → " + ", ".join(failures) if failures else "프로그램 채점 전부 PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
