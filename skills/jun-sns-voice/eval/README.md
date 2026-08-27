# jun-sns-voice eval — 스킬이 잘 동작하는지 검증하는 골든셋

**SKILL.md를 고칠 때마다 여기부터 다시 돌린다.**
실패하는 테스트 없이 스킬을 고치지 않는다 (writing-skills Iron Law).

## 무엇을 재나 — 4축

| 축 | 질문 | 채점 |
|---|---|---|
| 탐지 | 심어 둔 냄새(planted)가 수정본에서 사라졌나 | grade.py |
| 분별 | 함정(trap)이 수정본에 원문 그대로 남았나 | grade.py (**부재 = 즉시 FAIL**) |
| 규율 | 경계를 보류로 넘겼나, 덮어쓰기 없이 새 버전인가, 기록표가 있나 | grade.py + judge-rubric.md |
| 문체·품질 | 수정본이 원문 문체를 유지하고 새 냄새를 안 들여오나 | grade.py 휴리스틱 + judge-rubric.md |

## 케이스

| 케이스 | 축 | 핵심 |
|---|---|---|
| 01-플랫폼-접속 | 탐지+분별 | 소문자 x/threads, 물론·하지만을 고치고 단정 오프너는 남긴다 |
| 02-호흡-명사형 | 탐지+분별 | 짧은+긴 호흡을 고르게 하고 ~적인 측면은 남긴다 |
| 03-클린대조군 | 분별 | 한 편 시험에서 저자가 채택한 수정본. 과잉 적용 상한 |
| 04-경계보류 | 규율+분별 | 체감상·~것은 보류. 적용하면 FAIL |

라벨: `planted` / `traps` / `known_borderline`.

## 아직 안 한 것

`results/`가 비어 있다. 케이스 4개와 함정 2개는 저자 확인을 지났고 한 편 시험도 통과했지만, **깨끗한 문맥에서의 실제 실행은 아직 없다.** baseline도 없다. 그래서 v1은 초안이다.

## 실행 프로토콜

전체 규율은 [../../../eval/RUN.md](../../../eval/RUN.md). 요점: **케이스를 쓴 쪽이 결과 파일까지 쓰지 않는다.** 실행자에게 `expected.json`을 주지 않는다.

케이스마다 baseline(스킬 없이)과 with-skill을 돌린다. 반복 3회 권장.

**baseline.** 스킬·도구 없이 “AI 티를 사람 글로 고치라” + input 본문.

**with-skill.** SKILL.md 전문 + AUTHOR-TRAPS 확정 목록 + 출력 두 절(`## 수정본`, `## 변경 기록`).

결과는 `results/{날짜}/{케이스}-{조건}-r{회차}.md`.

## 채점

```bash
python3 grade.py cases/01-플랫폼-접속 results/YYYY-MM-DD/01-withskill-r1.md
```

규율·품질은 [judge-rubric.md](judge-rubric.md). 종합은 `results/{날짜}/판정-종합-*.md`.

## 합격 기본값

- planted 고침율 ≥ 케이스별 `recall_min` (0.66 전후)
- trap 훼손 0
- 규율 위반 0
- 클린대조군 **적용** ≤ 3 (보류 건수는 상한 없음, 기록은 남김)

적용 모드에서는 오탐이 본문 훼손이므로 precision 우선이 기본이다.

## 케이스 추가

1. `cases/{NN-슬러그}/input.md` — 잠가 둔 문체. 주석에 축·근거.
2. `expected.json` — planted/traps/borderline + thresholds. trap은 실전 보존에서.
3. baseline이 이미 통과하면 그 케이스는 버린다.
