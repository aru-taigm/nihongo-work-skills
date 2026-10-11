#!/usr/bin/env python3
"""README.md の一覧表（<!-- skills:start --> と <!-- skills:end --> の間）を skills/ から作り直す。

  python scripts/build_index.py          # README を更新
  python scripts/build_index.py --check  # 古ければ終了コード 1（CI 用）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skilllib import ROOT, load_all  # noqa: E402

START, END = "<!-- skills:start -->", "<!-- skills:end -->"
COUNT_RE = re.compile(r"(<!-- count:start -->)\d+(<!-- count:end -->)")
DESC_RE = re.compile(r"(Agent Skills )\d+(本)")


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
    out = readme[: a + len(START)] + "\n" + render() + "\n" + readme[b:]
    return COUNT_RE.sub(lambda m: f"{m.group(1)}{len(load_all())}{m.group(2)}", out)


def updated_description(text: str) -> str:
    return DESC_RE.sub(lambda m: f"{m.group(1)}{len(load_all())}{m.group(2)}", text)


def _utf8_stdio() -> None:
    """Windows の既定の文字コード（cp1252 など）でも日本語の出力でこけないようにする。"""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv: list[str]) -> int:
    _utf8_stdio()
    path = ROOT / "README.md"
    desc_path = ROOT / "DESCRIPTION"
    old = path.read_text(encoding="utf-8")
    new = updated(old)
    old_desc = desc_path.read_text(encoding="utf-8")
    new_desc = updated_description(old_desc)
    if "--check" in argv:
        if old != new or old_desc != new_desc:
            print("README.md / DESCRIPTION の一覧や本数が古いです。python scripts/build_index.py を実行してください")
            return 1
        return 0
    path.write_text(new, encoding="utf-8")
    desc_path.write_text(new_desc, encoding="utf-8")
    print(f"README.md を更新しました（{len(load_all())} 本）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
