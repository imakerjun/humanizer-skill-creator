# demo — 퇴고 스킬이 원고를 통과하는 과정

`index.html` 하나. 브라우저로 바로 열면 된다.

```bash
open demo/index.html
```

## 무엇을 보여주나

우테코 도서 원고 3문단을 **사람냄새**(`woowacourse-book-human-voice`) 스킬로 통과시킨 실제 기록이다. 체크리스트에 걸린 곳이 아홉 군데 나왔고, 그중 다섯 곳만 고쳤다.

이 저장소가 만드는 스킬의 값은 고친 다섯 건이 아니라 **두고 간 네 건**에 있다. 페이지는 그 판단이 어디서 갈렸는지를 단계별로 펼쳐 둔 것이다.

| 단계 | 하는 일 |
|---|---|
| 1 | 문체를 잠근다 — 여기서 범용 humanizer와 갈린다 |
| 2 | 통독하며 표시만 한다. 고치지 않는다 |
| 3 | 가드레일 넷으로 적용/보류를 가른다 |
| 4~5 | 적용 5건 · 보류 4건 |
| 6~7 | 수정본, 그리고 새 냄새가 들어왔는지 재통독 |
| 8 | 저자가 확정한 보류 건이 회귀 테스트가 된다 |

## 디자인 시스템

화면은 [notion-design-system](https://github.com/imakerjun/notion-design-system)(Folio)의 토큰·컴포넌트를 쓴다. `folio/`는 그 저장소 `css/`의 **복사본**이다.

- `folio/fonts.css` · `tokens.css` · `components.css` — 정본 복사. 여기서 값을 고치지 않는다.
- `demo.css` — 이 페이지 레이아웃만. 색·간격·라운딩은 `var(--fl-*)`만 쓰고 새 hex를 두지 않는다.

갱신할 때는 정본을 먼저 고치고 다시 복사한다. 반대 방향으로 병합하지 않는다.

```bash
cp ../../notion-design-system/css/{fonts,tokens,components}.css folio/
```
