"""Unit tests for the non-invasive MediaCrawler availability checker."""

from contextlib import redirect_stdout
from importlib.util import module_from_spec, spec_from_file_location
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "ai-pm-interview-coach" / "scripts" / "check_mediacrawler.py"
SPEC = spec_from_file_location("check_mediacrawler_under_test", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class MediaCrawlerCheckerTests(unittest.TestCase):
    def make_checkout(self, root: Path, name: str = "checkout") -> Path:
        checkout = root / name
        checkout.mkdir()
        (checkout / "main.py").write_text("# marker\n", encoding="utf-8")
        (checkout / "pyproject.toml").write_text("[project]\nname = 'marker'\n", encoding="utf-8")
        return checkout

    def test_explicit_path_takes_precedence_over_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            explicit = self.make_checkout(root, "explicit")
            environment = self.make_checkout(root, "environment")

            path, source = CHECKER.resolve_path(str(explicit), {"AI_PM_MEDIACRAWLER_PATH": str(environment)})

        self.assertEqual(path, explicit.resolve())
        self.assertEqual(source, "explicit")

    def test_environment_path_is_used_without_explicit_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            environment = Path(temporary) / "crawler"
            path, source = CHECKER.resolve_path(None, {"AI_PM_MEDIACRAWLER_PATH": str(environment)})

        self.assertEqual(path, environment.absolute())
        self.assertEqual(source, "environment")

    def test_explicit_tilde_is_expanded(self) -> None:
        with patch.dict("os.environ", {"HOME": "/tmp/test-home"}):
            path, source = CHECKER.resolve_path("~/crawler", {})

        self.assertEqual(path, Path("/tmp/test-home/crawler").resolve())
        self.assertEqual(source, "explicit")

    def test_environment_tilde_is_not_expanded(self) -> None:
        path, source = CHECKER.resolve_path(None, {"AI_PM_MEDIACRAWLER_PATH": "~/crawler"})

        self.assertEqual(path, Path("~/crawler").absolute())
        self.assertEqual(source, "environment")

    def test_no_path_is_missing_without_executable_lookup(self) -> None:
        with patch.object(CHECKER.shutil, "which") as which:
            result = CHECKER.check_mediacrawler(None, {})

        self.assertEqual(result.status, "missing")
        self.assertIsNone(result.path)
        which.assert_not_called()

    def test_nonexistent_path_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = CHECKER.check_mediacrawler(str(Path(temporary) / "absent"), {}, "uv")

        self.assertEqual(result.status, "invalid")

    def test_directory_without_both_marker_files_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = Path(temporary) / "incomplete"
            checkout.mkdir()
            (checkout / "main.py").write_text("", encoding="utf-8")
            result = CHECKER.check_mediacrawler(str(checkout), {}, "uv")

        self.assertEqual(result.status, "invalid")

    def test_pyproject_without_main_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = Path(temporary) / "pyproject-only"
            checkout.mkdir()
            (checkout / "pyproject.toml").write_text("[project]\nname = 'marker'\n", encoding="utf-8")
            result = CHECKER.check_mediacrawler(str(checkout), {}, "uv")

        self.assertEqual(result.status, "invalid")

    def test_valid_checkout_without_uv_is_uv_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = self.make_checkout(Path(temporary))
            with patch.object(CHECKER.shutil, "which", return_value=None) as which:
                result = CHECKER.check_mediacrawler(str(checkout), {}, None)

        self.assertEqual(result.status, "uv-missing")
        which.assert_called_once_with("uv")

    def test_valid_checkout_with_uv_is_ready_with_safety_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = self.make_checkout(Path(temporary))
            result = CHECKER.check_mediacrawler(str(checkout), {}, "/usr/local/bin/uv")

        self.assertEqual(result.status, "ready")
        self.assertEqual(result.path, str(checkout.resolve()))
        self.assertEqual(result.source, "explicit")
        warnings = " ".join(result.messages).lower()
        for topic in ("dependencies", "browser availability", "login state", "cookies", "live-site access"):
            self.assertIn(topic, warnings)
        self.assertIn("not verified", warnings)

    def test_json_output_is_stable_and_non_ready_exits_two(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = self.make_checkout(Path(temporary))
            output = io.StringIO()
            with patch.dict("os.environ", {}, clear=True), patch.object(CHECKER.shutil, "which", return_value="uv"):
                with redirect_stdout(output):
                    exit_code = CHECKER.main(["--path", str(checkout), "--json"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            json.loads(output.getvalue()),
            {
                "messages": [
                    "Dependencies, browser availability, login state, cookies, and live-site access were not verified."
                ],
                "path": str(checkout.resolve()),
                "source": "explicit",
                "status": "ready",
            },
        )
        self.assertEqual(
            output.getvalue(),
            '{"messages":["Dependencies, browser availability, login state, cookies, and live-site access were not verified."],'
            f'"path":"{checkout.resolve()}","source":"explicit","status":"ready"}}\n',
        )

        missing_output = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), redirect_stdout(missing_output):
            missing_exit_code = CHECKER.main(["--json"])
        self.assertEqual(missing_exit_code, 2)
        self.assertEqual(json.loads(missing_output.getvalue())["status"], "missing")


if __name__ == "__main__":
    unittest.main()
