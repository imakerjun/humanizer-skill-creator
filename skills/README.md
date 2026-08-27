# skills/ — 각자 만든 퇴고 스킬

한 폴더가 한 사람의(또는 한 장르의) 퇴고 스킬이다. 서로 참고하려고 한곳에 모으는 것이지, 하나로 합치려는 게 아니다.

## 규칙 네 개

1. **남의 폴더를 고치지 않는다.** 그 사람 목소리다. 제안은 이슈나 PR 코멘트로.
2. **체크리스트를 복사하지 않는다.** 시퀀스를 가져가서 자기 샘플로 다시 뽑는다. 복사하면 그 사람 흉내 스킬이 된다.
3. **이름은 소문자·숫자·하이픈**, 저자나 장르가 보이게. `minji-blog-voice`, `team-notice-voice`. `humanizer` 단독은 범용과 충돌한다.
4. **`eval/results/`에 실제 실행이 있어야 v1이다.** 채점기 통과만으로는 아니다 ([../eval/RUN.md](../eval/RUN.md)).

## 폴더 모양

```
{skill-name}/
├── SKILL.md              # 퇴고 절차. 체크리스트 표가 정본
├── STYLE-PROFILE.md      # 관찰된 문체 사실
└── eval/
    ├── AUTHOR-TRAPS.md   # 저자가 남기기로 확정한 표현
    ├── README.md
    ├── judge-rubric.md
    ├── grade.py
    ├── cases/{NN-슬러그}/
    └── results/
```

## 쓰기

개인 스킬 폴더로 심링크한다. 저장소가 갱신되면 그대로 따라온다.

```bash
ln -s "$PWD/skills/내-스킬" ~/.claude/skills/내-스킬
```

## 지금 있는 것

| 폴더 | 저자·장르 | 문체 잠금 | 상태 |
|---|---|---|---|
| [jun-sns-voice](jun-sns-voice/SKILL.md) | 임동준 / 블로그·에세이·SNS | 평어 `~다` | v1 초안. 실제 실행 대기 |
