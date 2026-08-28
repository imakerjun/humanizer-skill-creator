#!/usr/bin/env bash
# humanizer-skill-creator 설치 — 스킬과 커맨드를 개인 폴더로 심링크한다.
# 심링크라서 git pull 하면 갱신이 그대로 따라온다.
#
#   ./install.sh              설치 (또는 갱신)
#   ./install.sh --uninstall  이 저장소를 가리키는 링크만 제거
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
NAME="humanizer-skill-creator"
MODE="${1:-install}"

skill_targets=()
[ -d "$HOME/.claude" ] && skill_targets+=("$HOME/.claude/skills")
[ -d "$HOME/.codex" ] && skill_targets+=("$HOME/.codex/skills")
[ -d "$HOME/.cursor" ] && skill_targets+=("$HOME/.cursor/skills")

cmd_targets=()
[ -d "$HOME/.claude" ] && cmd_targets+=("$HOME/.claude/commands")

if [ ${#skill_targets[@]} -eq 0 ]; then
  echo "✗ ~/.claude, ~/.codex, ~/.cursor 중 아무것도 없다. Claude Code나 Codex를 먼저 설치한다." >&2
  exit 1
fi

# 이 저장소를 가리키는 링크만 지운다. 남의 파일은 건드리지 않는다.
unlink_ours() {
  local path="$1"
  [ -L "$path" ] || return 0
  case "$(readlink "$path")" in
    "$REPO"|"$REPO"/*) rm "$path"; echo "  − $path" ;;
  esac
}

# 이 저장소를 가리키지만 원본이 사라진 링크를 지운다 (리네임·삭제 뒤처리).
# 설치 때마다 돈다 — git pull 은 파일 추가는 옮겨 오지만 삭제는 옮겨 오지 않는다.
# $1: 훑을 디렉터리 (예: ~/.claude/commands)
prune_stale() {
  local dir="$1" f
  [ -d "$dir" ] || return 0
  # (a) 심링크만 훑는다. find -print0 이라 이름에 공백이 있어도 안전하고,
  #     빈 디렉터리에서도 글롭 실패 없이 그냥 0건이 된다.
  while IFS= read -r -d "" f; do
    if [ -e "$f" ]; then        # (c) 대상이 살아 있으면 둔다 (-e 는 링크를 따라간다)
      continue
    fi
    case "$(readlink "$f")" in  # (b) 우리 저장소를 가리키던 것만
      "$REPO"|"$REPO"/*) rm "$f"; echo "  − 끊긴 링크 $f" ;;
    esac
  done < <(find "$dir" -maxdepth 1 -type l -print0 2>/dev/null)
}

if [ "$MODE" = "--uninstall" ]; then
  echo "제거"
  for t in "${skill_targets[@]}"; do unlink_ours "$t/$NAME"; done
  for t in "${cmd_targets[@]}"; do
    for f in "$REPO"/commands/*.md; do unlink_ours "$t/$(basename "$f")"; done
  done
  echo "완료. 만든 스킬(~/.claude/skills/*)은 그대로 둔다."
  exit 0
fi

echo "설치 — $REPO"

for t in "${skill_targets[@]}"; do
  mkdir -p "$t"
  # 심링크가 아닌 실제 폴더가 있으면 덮어쓰지 않는다.
  if [ -e "$t/$NAME" ] && [ ! -L "$t/$NAME" ]; then
    echo "  ! $t/$NAME 이 실제 폴더다. 직접 옮기거나 지운 뒤 다시 실행한다." >&2
    continue
  fi
  ln -sfn "$REPO" "$t/$NAME"
  echo "  ✓ 스킬  $t/$NAME"
done

for t in "${cmd_targets[@]}"; do
  mkdir -p "$t"
  prune_stale "$t"   # 리네임된 옛 커맨드의 끊긴 링크를 먼저 치운다
  for f in "$REPO"/commands/*.md; do
    base="$(basename "$f")"
    if [ -e "$t/$base" ] && [ ! -L "$t/$base" ]; then
      echo "  ! $t/$base 이 이미 있다(내 파일 아님). 건너뛴다." >&2
      continue
    fi
    ln -sfn "$f" "$t/$base"
    echo "  ✓ 커맨드 /${base%.md}"
  done
done

echo
if command -v python3 >/dev/null 2>&1; then
  echo "python3 있음 — eval 채점기(grade.py)를 쓸 수 있다."
else
  echo "python3 없음 — 채점기 없이도 된다. eval/judge-rubric.md로 사람이 판정한다."
fi

cat <<'EOF'

시작하기
  Claude Code를 다시 열고 /말투-만들기 를 실행한다.
  (커맨드 없이 "내 말투 스킬 만들어 줘"라고 해도 스킬이 켜진다.)

준비물 두 개
  1. 본인이 쓴 글 1편 (대략 200자 이상)
  2. 지금 고치고 싶은 AI 초안 1편
EOF
