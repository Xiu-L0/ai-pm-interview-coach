"""Safely report whether a local MediaCrawler checkout appears available.

This checker intentionally inspects only a caller-supplied directory and its
two expected marker files. It never imports, runs, installs, or authenticates
against the checkout.
"""

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import shutil
from typing import Mapping, Optional, Sequence, Tuple


@dataclass(frozen=True)
class CheckResult:
    status: str
    path: Optional[str]
    source: Optional[str]
    messages: Tuple[str, ...]


def resolve_path(
    explicit_path: Optional[str], environ: Mapping[str, str]
) -> Tuple[Optional[Path], Optional[str]]:
    """Resolve only the explicit path or the configured environment path."""
    if explicit_path:
        return Path(explicit_path).expanduser().resolve(), "explicit"

    environment_path = environ.get("AI_PM_MEDIACRAWLER_PATH")
    if environment_path:
        return Path(environment_path).absolute(), "environment"

    return None, None


def check_mediacrawler(
    explicit_path: Optional[str],
    environ: Mapping[str, str],
    uv_executable: Optional[str] = None,
) -> CheckResult:
    path, source = resolve_path(explicit_path, environ)
    if path is None:
        return CheckResult("missing", None, None, ("No MediaCrawler path was provided.",))

    if not path.is_dir():
        return CheckResult(
            "invalid", str(path), source, ("The configured path is not a directory.",)
        )

    missing_markers = tuple(
        marker for marker in ("main.py", "pyproject.toml") if not (path / marker).is_file()
    )
    if missing_markers:
        return CheckResult(
            "invalid",
            str(path),
            source,
            ("Required marker files are missing: " + ", ".join(missing_markers) + ".",),
        )

    if uv_executable is None:
        uv_executable = shutil.which("uv")
    if not uv_executable:
        return CheckResult(
            "uv-missing",
            str(path),
            source,
            ("The uv executable was not found.",),
        )

    return CheckResult(
        "ready",
        str(path),
        source,
        (
            "Dependencies, browser availability, login state, cookies, and live-site access were not verified.",
        ),
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check local MediaCrawler availability safely.")
    parser.add_argument("--path", help="Explicit checkout directory to inspect.")
    parser.add_argument("--json", action="store_true", help="Print a stable JSON result.")
    args = parser.parse_args(argv)

    result = check_mediacrawler(args.path, __import__("os").environ)
    if args.json:
        print(json.dumps(asdict(result), sort_keys=True, separators=(",", ":")))
    else:
        print(f"{result.status}: {result.path or 'no path'}")
        for message in result.messages:
            print(message)
    return 0 if result.status == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
