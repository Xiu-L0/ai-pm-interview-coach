"""Machine-consumed contract checks for the explicit-only skill entrypoint."""

from pathlib import Path
import re
import unittest


class SkillContractTests(unittest.TestCase):
    """Protect invocation metadata and reference discoverability, not coaching prose."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[2]
        cls.skill_dir = cls.repo_root / "ai-pm-interview-coach"
        cls.skill_path = cls.skill_dir / "SKILL.md"
        cls.openai_yaml_path = cls.skill_dir / "agents" / "openai.yaml"
        cls.skill_text = cls.skill_path.read_text(encoding="utf-8")
        cls.openai_yaml_text = cls.openai_yaml_path.read_text(encoding="utf-8")

    def test_entrypoint_exposes_required_name_and_mode_triggers(self) -> None:
        """Fails if the entrypoint stops advertising a supported invocation mode."""
        frontmatter = re.match(r"\A---\n(.*?)\n---", self.skill_text, re.DOTALL)
        self.assertIsNotNone(frontmatter, "SKILL.md must begin with YAML frontmatter")
        metadata = frontmatter.group(1)
        self.assertRegex(metadata, r"(?m)^name: ai-pm-interview-coach$")

        description = re.search(r"(?m)^description: (.+)$", metadata)
        self.assertIsNotNone(description, "frontmatter must include a description")
        description_text = description.group(1).lower()
        for trigger in (
            "interview preparation",
            "question-bank",
            "simulation",
            "real-interview review",
            "later-round preparation",
            "longitudinal review",
        ):
            self.assertIn(trigger, description_text)

    def test_openai_metadata_requires_explicit_invocation(self) -> None:
        """Fails if normal conversation can implicitly load this explicit-only skill."""
        self.assertRegex(
            self.openai_yaml_text,
            r"(?m)^\s*allow_implicit_invocation: false\s*$",
        )
        self.assertIn("$ai-pm-interview-coach", self.openai_yaml_text)

    def test_entrypoint_links_its_created_reference_files(self) -> None:
        """Fails if a created reference is absent, unlinked, or points nowhere."""
        expected_references = (
            "references/input-contract.md",
            "references/preparation-and-simulation.md",
            "references/interview-review.md",
            "references/interviewer-style.md",
            "references/longitudinal-analysis.md",
            "references/mediacrawler-integration.md",
            "references/xhs-research.md",
        )
        linked_references = set(re.findall(
            r"\[[^]]+\]\((references/[^)]+)\)",
            self.skill_text,
        ))

        for reference in expected_references:
            with self.subTest(reference=reference):
                self.assertTrue((self.skill_dir / reference).is_file())
                self.assertIn(reference, linked_references)
        for reference in linked_references:
            with self.subTest(reference=reference):
                self.assertTrue((self.skill_dir / reference).is_file())

    def test_skill_files_contain_no_initializer_placeholders(self) -> None:
        """Fails if generated scaffold prose remains in a shipped skill file."""
        forbidden_phrases = (
            "Replace with",
            "Skill description here",
            "Add your instructions here",
            "[TODO:",
        )
        text_suffixes = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
        for path in self.skill_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in text_suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden_phrases:
                with self.subTest(path=path.relative_to(self.repo_root), phrase=phrase):
                    self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
