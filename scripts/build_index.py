#!/usr/bin/env python3
"""README.md の一覧表（<!-- skills:start --> と <!-- skills:end --> の間）を skills/ から作り直す。

  python scripts/build_index.py          # README を更新
  python scripts/build_index.py --check  # 古ければ終了コード 1（CI 用）
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import ROOT, load_all  # noqa: E402

START, END = "<!-- skills:start -->", "<!-- skills:end -->"


def render() -> str:
    rows = ["| スキル | できること |", "|---|---|"]
    for s in load_all():
        first = s.description.split("。")[0]
        rows.append(f"| `{s.name}` | {first} |")
    return "\n".join(rows)


def updated(readme: str) -> str:
    a, b = readme.find(START), readme.find(END)
    if a < 0 or b < a:
        raise SystemExit("README.md に <!-- skills:start --> / <!-- skills:end --> がありません")
    return readme[: a + len(START)] + "\n" + render() + "\n" + readme[b:]


def main(argv: list[str]) -> int:
    path = ROOT / "README.md"
    old = path.read_text(encoding="utf-8")
    new = updated(old)
    if "--check" in argv:
        if old != new:
            print("README.md の一覧が古いです。python scripts/build_index.py を実行してください")
            return 1
        return 0
    path.write_text(new, encoding="utf-8")
    print(f"README.md を更新しました（{len(load_all())} 本）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
