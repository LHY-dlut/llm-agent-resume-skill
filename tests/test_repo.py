"""Deterministic asset checks only. These do not run models or certify resume claims."""
from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "llm-agent-resume"
sys.path.insert(0, str(ROOT / "scripts"))
from export_prompt import OUTPUT, SOURCE, render_prompt  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def marked(path: Path, start: str, end: str) -> str:
    text = read(path)
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected one marker pair in {path.name}")
    return text.split(start, 1)[1].split(end, 1)[0].strip()


class RepositoryTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        required = [
            "README.md", "LICENSE", "CHANGELOG.md", ".gitignore",
            ".github/workflows/validate.yml", "scripts/export_prompt.py",
            "tests/behavior-cases.md", "skills/llm_agent_resume_prompt.md",
            "skills/llm-agent-resume/SKILL.md",
            "skills/llm-agent-resume/references/evidence-and-metrics.md",
            "skills/llm-agent-resume/references/sources.md",
            "skills/llm-agent-resume/templates/project-intake.md",
            "skills/llm-agent-resume/templates/evidence-ledger.md",
            "skills/llm-agent-resume/templates/resume-project.md",
            "skills/llm-agent-resume/examples/rag-before-after.md",
            "skills/llm-agent-resume/examples/post-training-before-after.md",
            "skills/llm-agent-resume/examples/demo-metrics.json",
        ]
        for relative in required:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())
                self.assertGreater((ROOT / relative).stat().st_size, 0)

    def test_frontmatter_and_skill_name(self) -> None:
        text = read(SOURCE)
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text[4:].split("\n---\n", 1)[0]
        name = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        self.assertIsNotNone(name)
        self.assertIsNotNone(description)
        assert name is not None and description is not None
        value = name.group(1).strip()
        self.assertRegex(value, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(value), 64)
        self.assertEqual(value, SKILL.name)
        self.assertTrue(1 <= len(description.group(1).strip()) <= 1024)
        self.assertLess(len(text.splitlines()), 500)

    def test_generated_prompt_matches(self) -> None:
        self.assertEqual(read(OUTPUT), render_prompt(read(SOURCE)))
        self.assertNotIn("RESOURCE_INDEX_START", read(OUTPUT))
        self.assertNotIn("](", read(OUTPUT))  # The standalone prompt needs no relative resources.

    def test_export_check_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/export_prompt.py"), "--check"],
            capture_output=True, text=True, encoding="utf-8", timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK:", result.stdout)

    def test_export_rejects_malformed_source(self) -> None:
        for bad in ["no metadata", "---\nname: x\n", "---\nname: x\n---\nbody"]:
            with self.subTest(source=bad), self.assertRaises(ValueError):
                render_prompt(bad)

    def test_relative_markdown_links(self) -> None:
        # Inspect file targets; heading-anchor correctness and external HTTP availability
        # are intentionally not included. Ignore code fences and non-file URL schemes.
        for path in ROOT.rglob("*.md"):
            if any(part in {".git", ".agents", ".claude", "outputs"} for part in path.parts):
                continue
            text = re.sub(r"(?ms)^```.*?^```[^\n]*$", "", read(path))
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                target = target.strip().split(' "', 1)[0]
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve()
                with self.subTest(file=path.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists())

    def test_skill_resources_are_portable(self) -> None:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(SOURCE)):
            if urlsplit(target).scheme:
                continue
            resolved = (SKILL / target).resolve()
            self.assertTrue(resolved.is_relative_to(SKILL), target)
            self.assertTrue(resolved.is_file(), target)

    def test_five_layer_template_order(self) -> None:
        snippet = marked(SKILL / "templates/resume-project.md", "<!-- TEMPLATE_START -->", "<!-- TEMPLATE_END -->")
        labels = ["- 底盘层：", "- 架构层：", "- 治理层：", "- 评测层：", "项目成果：", "边界说明："]
        positions = [snippet.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(sum(line.startswith("- ") for line in snippet.splitlines()), 4)

    def test_readme_contains_canonical_examples(self) -> None:
        readme = read(ROOT / "README.md")
        for filename in ["rag-before-after.md", "post-training-before-after.md"]:
            snippet = marked(SKILL / "examples" / filename, "<!-- RESUME_START -->", "<!-- RESUME_END -->")
            self.assertIn(snippet, readme)
        template = marked(SKILL / "templates/resume-project.md", "<!-- TEMPLATE_START -->", "<!-- TEMPLATE_END -->")
        self.assertIn(template, readme)

    def test_demo_provenance_is_explicit(self) -> None:
        data = json.loads(read(SKILL / "examples/demo-metrics.json"))
        self.assertIs(data["synthetic"], True)
        self.assertIs(data["training_executed"], False)
        self.assertIs(data["questions_or_model_outputs_provided"], False)
        self.assertIn("DEMO", data["warning"])
        self.assertIn("完全假设案例", read(SKILL / "examples/post-training-before-after.md"))
        self.assertIn("合成", read(ROOT / "README.md"))

    def test_demo_arithmetic_and_ranges(self) -> None:
        data = json.loads(read(SKILL / "examples/demo-metrics.json"))
        configs = data["configs"]
        expected = {
            "G0": (40, 62, 800, 10.4), "G1": (42, 65, 760, 10.7),
            "G2": (44, 67, 560, 11.1), "G3": (45, 70, 540, 11.3),
            "G4": (47, 72, 520, 11.5),
        }
        keys = ["pass_at_1_pct", "pass_at_8_pct", "dev_threshold_steps", "gpu_hours"]
        for name, wanted in expected.items():
            rows = configs[name]
            self.assertEqual([row["seed"] for row in rows], data["training_seeds"])
            for key, value in zip(keys, wanted):
                self.assertAlmostEqual(statistics.mean(row[key] for row in rows), value)
            for row in rows:
                self.assertTrue(0 <= row["pass_at_1_pct"] <= row["pass_at_8_pct"] <= 100)
                self.assertLessEqual(row["dev_threshold_steps"], data["fixed_optimizer_steps"])
                self.assertGreater(row["gpu_hours"], 0)
        self.assertAlmostEqual(47.0 - 40.0, 7.0)
        self.assertAlmostEqual(72.0 - 62.0, 10.0)
        self.assertAlmostEqual((800 - 520) / 800 * 100, 35.0)
        self.assertEqual(round((11.5 / 10.4 - 1) * 100, 1), 10.6)
        self.assertEqual(round(56.5 - 71.7, 1), -15.2)

    def test_behavior_specs_are_complete_and_labeled(self) -> None:
        text = read(ROOT / "tests/behavior-cases.md")
        ids = re.findall(r"^## (B\d{2}) —", text, re.MULTILINE)
        self.assertEqual(ids, [f"B{i:02d}" for i in range(1, 23)])
        for part in re.split(r"^## B\d{2} —", text, flags=re.MULTILINE)[1:]:
            self.assertIn("输入", part)
            self.assertIn("期望：", part)
            self.assertIn("禁止：", part)
        self.assertIn("不是已通过", text)

    def test_skill_keeps_workflow_and_downgrade_guards(self) -> None:
        text = read(SOURCE)
        for term in ["GAP_CHECK", "WAITING_FOR_INPUT", "READY", "明确没做", "不循环追问", "待补证草稿", "示例", "内部核对"]:
            self.assertIn(term, text)

    def test_no_input_image_or_private_evidence_is_bundled(self) -> None:
        forbidden_dirs = {"private", "evidence-private", "outputs"}
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            self.assertFalse(any(part in forbidden_dirs for part in relative.parts))
            self.assertNotIn(path.suffix.lower(), {".jpg", ".jpeg", ".png", ".pdf", ".docx"})
            self.assertNotEqual(path.name, ".env")


if __name__ == "__main__":
    unittest.main()
