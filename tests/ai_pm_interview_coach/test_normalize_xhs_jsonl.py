"""Behavior tests for deterministic Xiaohongshu JSONL normalization."""

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "ai-pm-interview-coach" / "scripts" / "normalize_xhs_jsonl.py"
SPEC = spec_from_file_location("normalize_xhs_jsonl_under_test", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
NORMALIZER = module_from_spec(SPEC)
sys.modules[SPEC.name] = NORMALIZER
SPEC.loader.exec_module(NORMALIZER)

FIXTURE = REPO_ROOT / "tests" / "ai_pm_interview_coach" / "fixtures" / "xhs_contents.jsonl"


class NormalizeXhsJsonlTests(unittest.TestCase):
    def test_parse_jsonl_continues_after_malformed_line_with_numbered_warning(self):
        records, warnings = NORMALIZER.parse_jsonl(FIXTURE)
        self.assertEqual(len(records), 3)
        self.assertEqual(warnings, ["line 4: malformed JSON object"])

    def test_parse_jsonl_warns_for_non_object_and_missing_identity_then_continues(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.jsonl"
            path.write_text('[]\n{"title":"orphan"}\n{"note_id":"kept","title":"valid"}\n', encoding="utf-8")
            records, warnings = NORMALIZER.parse_jsonl(path)
        self.assertEqual([record["note_id"] for record in records], ["kept"])
        self.assertEqual(warnings, [
            "line 1: malformed JSON object",
            "line 2: missing note_id and note_url",
        ])

    def test_normalize_epoch_accepts_seconds_and_milliseconds(self):
        self.assertEqual(NORMALIZER.normalize_epoch(1735689600), "2025-01-01T00:00:00Z")
        self.assertEqual(NORMALIZER.normalize_epoch(1735689600000), "2025-01-01T00:00:00Z")
        self.assertEqual(NORMALIZER.normalize_epoch(10_000_000_000), "1970-04-26T17:46:40Z")
        self.assertIsNone(NORMALIZER.normalize_epoch(True))
        self.assertIsNone(NORMALIZER.normalize_epoch(False))
        self.assertIsNone(NORMALIZER.normalize_epoch(0))
        self.assertIsNone(NORMALIZER.normalize_epoch("not-a-time"))

    def test_non_positive_update_time_does_not_displace_newer_publication_before_truncation(self):
        """Fails if a zero update timestamp overrides a real publication timestamp."""
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.jsonl"
            path.write_text(
                '{"note_id":"a-older","title":"same relevance","time":10,"last_update_time":0}\n'
                '{"note_id":"z-newer","title":"same relevance","time":20,"last_update_time":0}\n',
                encoding="utf-8",
            )
            payload = NORMALIZER.build_payload(path, ["missing"], 1)

        self.assertEqual([note["note_id"] for note in payload["notes"]], ["z-newer"])
        self.assertIsNone(payload["notes"][0]["last_update_time"])

    def test_split_csv_trims_blanks_and_handles_non_strings(self):
        self.assertEqual(NORMALIZER.split_csv(" a, ,b ,, c "), ["a", "b", "c"])
        self.assertEqual(NORMALIZER.split_csv(["a"]), [])
        self.assertEqual(NORMALIZER.split_csv(None), [])

    def test_relevance_score_counts_each_keyword_in_each_field(self):
        note = {"title": "AI ai", "description": "AI产品", "source_keyword": "ai,产品"}
        self.assertEqual(NORMALIZER.relevance_score(note, ["AI", "产品"]), 9)

    def test_normalize_note_requires_note_id_or_url_and_preserves_provenance(self):
        self.assertIsNone(NORMALIZER.normalize_note({"title": "orphan"}, ["AI"]))
        note = NORMALIZER.normalize_note(json.loads(FIXTURE.read_text(encoding="utf-8").splitlines()[0]), ["AI产品经理"])
        self.assertEqual(note["note_id"], "n1")
        self.assertEqual(note["note_url"], "https://www.xiaohongshu.com/explore/n1")
        self.assertEqual(note["image_urls"], ["https://img.example/n1.jpg"])
        self.assertEqual(note["tags"], ["AI产品经理", "面试", "复盘"])
        self.assertEqual(note["time"], "2025-01-01T00:00:00Z")
        self.assertEqual(note["raw_engagement"], {"liked_count": "12", "collected_count": "3", "comment_count": "4", "share_count": "1"})

    def test_build_payload_deduplicates_ranks_truncates_and_marks_image_candidate(self):
        payload = NORMALIZER.build_payload(FIXTURE, ["AI产品经理", "面试"], 2)
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["source"], "mediacrawler-xhs-jsonl")
        self.assertEqual([note["note_id"] for note in payload["notes"]], ["n1", "n2"])
        self.assertEqual(payload["notes"][0]["title"], "AI产品经理面试复盘")
        self.assertEqual(payload["image_review_candidates"], ["n2"])
        self.assertEqual(payload["warnings"], ["line 4: malformed JSON object"])

    def test_build_payload_deduplicates_by_url_and_uses_identifier_tiebreak(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.jsonl"
            path.write_text(
                '{"note_url":"https://x/one","title":"same","time":2}\n'
                '{"note_url":"https://x/one","title":"same","time":3}\n'
                '{"note_id":"b","title":"same","time":3}\n'
                '{"note_id":"a","title":"same","time":3}\n', encoding="utf-8")
            payload = NORMALIZER.build_payload(path, ["missing"], 100)
        self.assertEqual([note["stable_id"] for note in payload["notes"]], ["a", "b", "https://x/one"])
        self.assertEqual(payload["notes"][-1]["time"], "1970-01-01T00:00:03Z")

    def test_duplicate_ties_have_same_result_when_input_order_is_reversed(self):
        lines = [
            '{"note_id":"same","title":"first","time":3}',
            '{"note_id":"same","title":"second","time":3}',
        ]
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.jsonl"
            second = Path(temporary) / "second.jsonl"
            first.write_text("\n".join(lines) + "\n", encoding="utf-8")
            second.write_text("\n".join(reversed(lines)) + "\n", encoding="utf-8")
            first_payload = NORMALIZER.build_payload(first, [], 100)
            second_payload = NORMALIZER.build_payload(second, [], 100)
        self.assertEqual(first_payload, second_payload)
        self.assertEqual(first_payload["notes"][0]["title"], "second")

    def test_main_validates_max_notes_and_writes_deterministic_utf8_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "payload.json"
            self.assertEqual(NORMALIZER.main(["--input", str(FIXTURE), "--output", str(output), "--keyword", "AI产品经理", "--max-notes", "2"]), 0)
            written = output.read_text(encoding="utf-8")
            self.assertTrue(written.endswith("\n"))
            self.assertEqual(json.loads(written)["query_keywords"], ["AI产品经理"])
            self.assertEqual(NORMALIZER.main(["--input", str(FIXTURE), "--output", str(output), "--max-notes", "0"]), 2)
            self.assertEqual(NORMALIZER.main(["--input", str(FIXTURE), "--output", str(output), "--max-notes", "101"]), 2)

    def test_main_requires_input_and_output_flags(self):
        self.assertEqual(NORMALIZER.main([]), 2)
        self.assertEqual(NORMALIZER.main(["--input", str(FIXTURE)]), 2)
        self.assertEqual(NORMALIZER.main(["--output", "/tmp/unused-payload.json"]), 2)

    def test_repeatable_keywords_are_retained_and_each_changes_score(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "payload.json"
            self.assertEqual(NORMALIZER.main([
                "--input", str(FIXTURE), "--output", str(output),
                "--keyword", "AI产品经理", "--keyword", "图片", "--max-notes", "100",
            ]), 0)
            payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(payload["query_keywords"], ["AI产品经理", "图片"])
        notes = {note["note_id"]: note for note in payload["notes"]}
        self.assertEqual(notes["n2"]["score"], 4)


if __name__ == "__main__":
    unittest.main()
