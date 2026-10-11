import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_index  # noqa: E402
import install  # noqa: E402
import skilllib  # noqa: E402


class SkillFilesTest(unittest.TestCase):
    def test_there_are_skills(self):
        self.assertGreaterEqual(len(skilllib.load_all()), 60)

    def test_every_skill_is_valid(self):
        problems = []
        for s in skilllib.load_all():
            problems += skilllib.validate(s)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_names_are_unique(self):
        names = [s.name for s in skilllib.load_all()]
        self.assertEqual(len(names), len(set(names)))

    def test_every_skill_uses_jp_prefix(self):
        for s in skilllib.load_all():
            self.assertTrue(s.name.startswith("jp-"), s.name)

    def test_no_stray_files_in_skills_dir(self):
        for p in skilllib.SKILLS_DIR.iterdir():
            self.assertTrue(p.is_dir(), p)
            self.assertTrue((p / "SKILL.md").is_file(), p)


class ValidatorTest(unittest.TestCase):
    def _skill(self, text, dirname="jp-x"):
        d = Path(tempfile.mkdtemp()) / dirname
        d.mkdir()
        (d / "SKILL.md").write_text(text, encoding="utf-8")
        return skilllib.parse_skill(d / "SKILL.md")

    GOOD = (
        "---\nname: jp-x\ndescription: 何かを作る。「作って」と言われたときに使う。\n---\n# X\n"
        "## 先に確認すること\n-\n## 手順\n1.\n## 出力形式\n```\n```\n## 例\n入力：a\n出力：b\n## 注意\n-\n"
    )

    def test_good(self):
        self.assertEqual(skilllib.validate(self._skill(self.GOOD)), [])

    def test_name_mismatch(self):
        errs = skilllib.validate(self._skill(self.GOOD.replace("name: jp-x", "name: jp-y")))
        self.assertTrue(any("フォルダ名" in e for e in errs))

    def test_missing_section(self):
        errs = skilllib.validate(self._skill(self.GOOD.replace("## 注意\n-\n", "")))
        self.assertTrue(any("注意" in e for e in errs))

    def test_example_needs_input_and_output(self):
        errs = skilllib.validate(self._skill(self.GOOD.replace("入力：a\n出力：b\n", "ただの文\n")))
        self.assertTrue(any("入力と出力" in e for e in errs))

    def test_description_with_angle_brackets(self):
        errs = skilllib.validate(self._skill(self.GOOD.replace("何かを作る", "<b>を作る")))
        self.assertTrue(any("< >" in e for e in errs))

    def test_missing_frontmatter(self):
        with self.assertRaises(ValueError):
            self._skill("# no frontmatter\n")

    def test_reserved_word(self):
        errs = skilllib.validate(self._skill(self.GOOD.replace("jp-x", "jp-claude-x"), "jp-claude-x"))
        self.assertTrue(any("予約語" in e for e in errs))


class IndexTest(unittest.TestCase):
    def test_readme_is_up_to_date(self):
        self.assertEqual(build_index.main(["--check"]), 0)


class InstallTest(unittest.TestCase):
    def test_install_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(install.main(["jp-invoice", "--dest", tmp]), 0)
            self.assertTrue((Path(tmp) / "jp-invoice" / "SKILL.md").is_file())
            self.assertFalse((Path(tmp) / "jp-ringi").exists())

    def test_install_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(install.main(["--dest", tmp]), 0)
            self.assertEqual(len(list(Path(tmp).iterdir())), len(skilllib.load_all()))

    def test_unknown_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(install.main(["nope", "--dest", tmp]), 2)

    def test_script_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install.py"), "jp-ringi", "--dest", tmp],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
