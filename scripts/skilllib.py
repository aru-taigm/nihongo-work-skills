"""SKILL.md の読み取りと検証（標準ライブラリだけで動く）。"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_HEADINGS = ["先に確認すること", "手順", "出力形式", "例", "注意"]
RESERVED_WORDS = ("claude", "anthropic")


@dataclass
class Skill:
    path: Path
    name: str
    description: str
    body: str

    @property
    def title(self) -> str:
        for line in self.body.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return self.name


def parse_skill(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path}: 先頭に frontmatter（--- で囲んだ部分）がありません")
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"{path}: frontmatter の行が 'key: value' の形ではありません: {line!r}")
        meta[key.strip()] = value.strip()
    return Skill(path, meta.get("name", ""), meta.get("description", ""), m.group(2))


def load_all() -> list[Skill]:
    return [parse_skill(p) for p in sorted(SKILLS_DIR.glob("*/SKILL.md"))]


def validate(skill: Skill) -> list[str]:
    errs: list[str] = []
    where = skill.path.parent.name
    if skill.name != where:
        errs.append(f"{where}: name '{skill.name}' がフォルダ名と一致しません")
    if not NAME_RE.match(skill.name) or len(skill.name) > 64:
        errs.append(f"{where}: name は小文字・数字・ハイフンのみ、64文字以内にしてください")
    if any(w in skill.name for w in RESERVED_WORDS):
        errs.append(f"{where}: name に予約語が含まれています")
    if not skill.description:
        errs.append(f"{where}: description が空です")
    if len(skill.description) > 1024:
        errs.append(f"{where}: description が1024文字を超えています")
    if "<" in skill.description or ">" in skill.description:
        errs.append(f"{where}: description に < > は使えません")
    if "使" not in skill.description:
        errs.append(f"{where}: description に「どんなときに使うか」が書かれていません")

    headings = [h[3:].strip() for h in skill.body.splitlines() if h.startswith("## ")]
    for required in REQUIRED_HEADINGS:
        if not any(h.startswith(required) for h in headings):
            errs.append(f"{where}: 見出し「## {required}」がありません")

    example = _section(skill.body, "例")
    if example is not None and ("入力" not in example or "出力" not in example):
        errs.append(f"{where}: 「例」に入力と出力の両方を書いてください")

    if len(skill.body.splitlines()) > 500:
        errs.append(f"{where}: 本文が500行を超えています")
    if "TODO" in skill.body or "TBD" in skill.body:
        errs.append(f"{where}: TODO/TBD が残っています")
    return errs


def _section(body: str, heading: str) -> str | None:
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip().startswith(heading):
            start = i + 1
            break
    if start is None:
        return None
    out = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)
