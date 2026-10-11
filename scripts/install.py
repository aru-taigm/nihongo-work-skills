#!/usr/bin/env python3
"""skills/ の中身を Claude Code のスキルフォルダにコピーする。

  python scripts/install.py                 # ~/.claude/skills に全部入れる
  python scripts/install.py --project       # ./.claude/skills に入れる
  python scripts/install.py jp-invoice jp-ringi   # 指定のものだけ
  python scripts/install.py --dest DIR      # 入れ先を指定
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import SKILLS_DIR  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="入れるスキル名（省略で全部）")
    ap.add_argument("--project", action="store_true", help="カレントの .claude/skills に入れる")
    ap.add_argument("--dest", help="入れ先フォルダ")
    args = ap.parse_args(argv)

    if args.dest:
        dest = Path(args.dest)
    elif args.project:
        dest = Path.cwd() / ".claude" / "skills"
    else:
        dest = Path.home() / ".claude" / "skills"

    available = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").is_file())
    names = args.names or available
    unknown = [n for n in names if n not in available]
    if unknown:
        print("見つからないスキル: " + ", ".join(unknown), file=sys.stderr)
        return 2

    dest.mkdir(parents=True, exist_ok=True)
    for n in names:
        shutil.copytree(SKILLS_DIR / n, dest / n, dirs_exist_ok=True)
        print(f"入れました: {dest / n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
