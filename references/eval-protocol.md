# Eval 프로토콜 — 두 종류의 eval을 섞지 않는다

이 저장소에는 eval이 **두 겹**이다. 헷갈리면 엉뚱한 걸 재게 된다.

| | 무엇을 재나 | 어디 |
|---|---|---|
| **메타 스킬의 eval** | 개인 humanizer를 만들 때 절차를 지키는가 — 골든셋 먼저, 금칙어 통째 이식 거부, 함정 분리 | 이 저장소 [`eval/`](../eval/) |
| **생성된 스킬의 eval** | 그 저자의 퇴고가 맞나 — planted 제거, trap 보존, 과잉 적용 | 만들어진 스킬 안의 `eval/` |

create가 끝나면 **생성된 쪽**을 돈다. 이 저장소 `eval/`은 메타 스킬을 고칠 때 돈다.

## 나머지는 어디에

중복을 두지 않으려고 한곳씩만 둔다.

- **4축·라벨·합격선·케이스 구성** → [`../templates/eval/README.md`](../templates/eval/README.md)가 정본. 생성된 스킬에 그대로 복사된다.
- **실행 규율·프롬프트 골격·채점 명령** → [`../eval/RUN.md`](../eval/RUN.md)가 정본.
- **판정 축** → 메타는 [`../eval/judge-rubric.md`](../eval/judge-rubric.md), 생성 스킬은 [`../templates/eval/judge-rubric.md`](../templates/eval/judge-rubric.md).

## 왜 문자열 채점을 쓰나

Anthropic skill-creator도 eval을 **프롬프트 실행 + 별도 grader 판정**으로 정의하고, 문체처럼 주관적인 축을 assertion으로 억지로 만들지 말라고 한다.

여기 프로토콜은 그 경고를 받아들이면서, 문체 중 **문자열로 결정적으로 잴 수 있는 부분**(심어 둔 냄새의 부재, 함정의 존재)만 기계 채점으로 떼어낸 것이다. 나머지는 루브릭이 본다. 채점기 출력만으로 통과를 주장하지 않는다.

Iron Law (obra/superpowers writing-skills): 스킬 없는 실패를 보기 전에 스킬을 쓰지 않는다. 실패하는 테스트 없이 스킬을 고치지 않는다.
