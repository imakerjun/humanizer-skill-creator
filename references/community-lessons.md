# 공개 humanizer에서 가져올 것, 버릴 것

범용 “AI 글 사람처럼” 스킬은 이미 많다. 이 메타 스킬은 그걸 복제하지 않는다. **자기 문체용 루브릭 + planted/trap eval**이 빈칸이다.

## 참고한 것

| 출처 | 역할 | 가져올 점 | 이 시퀀스에서 버리는 점 |
|---|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | 공개 범용 humanizer | 위키백과 Signs of AI writing 기반 패턴, **무엇을 깃발로 보지 말지**, 사실 추가 금지, 샘플이 있으면 샘플이 규칙보다 우선 | 30~50개 패턴 통째 이식. 백과 문체(중요성 부풀리기, 매체 이름 나열)는 장르가 맞을 때만 |
| [AshwinSathian/humanize-writing-skill](https://github.com/AshwinSathian/humanize-writing-skill) `oss-skills-review.md` | 공개 humanizer 분해 | 금칙어 목록이 중앙값이자 최약점. 구조 > 어휘. 숫자 임계값 날조 금지. 탐지기 우회를 목표로 두지 말 것 | “연구 인용”만 있고 출처가 없는 권위 |
| Anthropic [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | 공식 메타 스킬 | 인터뷰 → 초안 → eval → 반복. **eval = 프롬프트 실행 + 별도 grader 판정**(executor·grader·comparator·analyzer 4역). 깨끗한 문맥에서 병렬 실행. blind A/B로 “정말 나아졌나”를 본다. description 트리거를 샘플 프롬프트로 튜닝 | 코드 없는 자연어 assertion만으로 문체를 재려는 부분. 여기선 planted/trap을 문자열로 떼어내 회귀를 만든다 |
| obra/superpowers [writing-skills](https://github.com/obra/superpowers) | Iron Law의 출처. 이 저장소 eval README가 인용 | 스킬 없는 실패를 보기 전에 스킬을 쓰지 않는다. 스킬은 그 실패를 겨냥한 최소 문서 | 일반 스킬 저술의 전부. humanizer 특수 축(함정·클린대조군)은 여기 없음 |
| 이 저장소 `사람냄새` | 완성된 개인/도서 humanizer | 적용/보류, AUTHOR-TRAPS, 4축, grade.py 문자열 채점 + 사람 루브릭, 같은 표면형의 문맥 분별 | 우테코 도서 체크리스트 자체. 다른 저자에게 복사 금지 |

그 밖: [vvalisoy/claude-humanizer-skill](https://github.com/vvalisoy/claude-humanizer-skill) (blader 계열 + voice calibration), [hannsxpeter/humanizer](https://github.com/hannsxpeter/humanizer) (목소리 보호·절제), [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) (탐지기 오탐 연구 인용, detect 전용 모드). 메커니즘이 금칙어면 어휘만 빌려 오지 않는다.

## 가져올 설계

1. **거짓양성 가드레일이 실력을 가른다.** blader가 앞선 이유다. “대시 하나”, “however 하나”, “짧은 문장 하나”는 증거가 아니다. 여러 패턴이 겹칠 때, 또는 그 저자가 안 쓰는 버릇일 때만 냄새다.
2. **샘플이 규칙보다 우선이다.** 저자가 대시를 쓰면 대시 금지가 아니라 빈도·용법을 맞춘다.
3. **사실 가드.** 사람 글처럼 보이게 숫자·인용·고유명사를 만들지 않는다. 빈 구체는 묻거나 더 단순한 문장으로.
4. **투명.** 무엇을 왜 고쳤는지 표로 남긴다. “규칙을 숨겨라”는 탐지 우회 프레임이라 넣지 않는다.
5. **장르.** 학술·위키·마케팅·도서는 정상 표현이 다르다. 시드는 장르로 걸러진다.
6. **판정자를 실행자와 분리한다.** Anthropic의 grader는 “표면 준수가 아니라 진짜로 해냈다는 증거”를 요구하고, 약한 assertion 자체를 비판하라고 지시받는다. 케이스를 쓴 쪽이 답까지 쓰면 그 요구가 통째로 무력해진다.

## 버릴 설계

1. **금칙어 목록이 본체.** robust, delve, tapestry를 무조건 지우면 기술 글이 망가진다. 남용·군집만 신호다.
2. **날조된 숫자 규칙.** “500단어에 대시 1개”, “같은 길이 문장 3개 금지” — 출처 없는 임계값은 쓰지 않는다. 저자가 자기 글에서 센 빈도만 프로필에 적는다.
3. **위키백과 목록 통째.** Signs of AI writing은 백과 항목용이다. 에세이·메일·코드 블로그에 “매체 이름 나열 = 냄새”를 기본 장착하지 않는다.
4. **탐지기 점수 최적화.** 표면 고치기로 분류기를 이기겠다는 주장은 빼다. 독자가 이 사람 글인가가 목표다.
5. **한 가지 “사람 톤”.** 범용 humanizer는 짧은 평어 단문을 사람처럼 본다. `사람냄새`가 그걸 명시적으로 금지한 이유다. 원문 문체를 유지하는 것이 기본이다.

## 이 시퀀스가 채우는 빈칸

공개 스킬의 voice calibration은 보통 “2~3문단을 붙여 넣으면 리듬을 맞춘다”에서 끝난다. 그건 일회성 흉내이고, 회귀 테스트가 없다.

여기 시퀀스는 다음을 파일로 고정한다.

- 저자만 아는 보존 목록 (AUTHOR-TRAPS)
- 심어 둔 냄새 / 건드리면 실패하는 함정 / 잡아도 그만 안 잡아도 그만인 경계
- 스킬 없는 실패(RED)와 스킬 있는 통과(GREEN)
- 스킬을 고칠 때마다 같은 채점기를 다시 돌리는 규율
