#!/usr/bin/env python3
"""Normalize MediaCrawler Xiaohongshu JSONL exports without external I/O."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import List, Mapping, Optional, Sequence, Tuple


ENGAGEMENT_FIELDS = ("liked_count", "collected_count", "comment_count", "share_count")


def parse_jsonl(path: Path) -> Tuple[List[dict], List[str]]:
    records = []
    warnings = []
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                warnings.append(f"line {line_number}: malformed JSON object")
                continue
            if not isinstance(value, dict):
                warnings.append(f"line {line_number}: malformed JSON object")
                continue
            record = dict(value)
            if not _text(record.get("note_id")).strip() and not _text(record.get("note_url")).strip():
                warnings.append(f"line {line_number}: missing note_id and note_url")
                continue
            record["__line_number"] = line_number
            records.append(record)
    return records, warnings


def normalize_epoch(value: object) -> Optional[str]:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if number <= 0:
        return None
    if number >= 10000000000:
        number /= 1000
    try:
        return datetime.fromtimestamp(number, tz=timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return None


def split_csv(value: object) -> List[str]:
    if not isinstance(value, str):
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def _text(value: object) -> str:
    return value if isinstance(value, str) else ""


def relevance_score(note: Mapping[str, object], keywords: Sequence[str]) -> int:
    title = _text(note.get("title")).casefold()
    description = _text(note.get("description", note.get("desc"))).casefold()
    source = _text(note.get("source_keyword")).casefold()
    score = 0
    for keyword in keywords:
        term = _text(keyword).strip().casefold()
        if not term:
            continue
        if term in title:
            score += 3
        if term in description:
            score += 1
        if term in source:
            score += 2
    return score


def normalize_note(record: Mapping[str, object], keywords: Sequence[str]) -> Optional[dict]:
    note_id = _text(record.get("note_id")).strip()
    note_url = _text(record.get("note_url")).strip()
    if not note_id and not note_url:
        return None
    stable_id = note_id or note_url
    time = normalize_epoch(record.get("time"))
    last_update_time = normalize_epoch(record.get("last_update_time"))
    engagement = {field: record[field] for field in ENGAGEMENT_FIELDS if field in record}
    note = {
        "note_id": note_id,
        "note_url": note_url,
        "title": _text(record.get("title")),
        "description": _text(record.get("desc", record.get("description"))),
        "type": _text(record.get("type")),
        "source_keyword": _text(record.get("source_keyword")),
        "time": time,
        "last_update_time": last_update_time,
        "tags": split_csv(record.get("tag_list", record.get("tags"))),
        "image_urls": split_csv(record.get("image_list", record.get("image_urls"))),
        "raw_engagement": engagement,
        "score": relevance_score(record, keywords),
        "stable_id": stable_id,
    }
    return note


def _newer_timestamp(note: Mapping[str, object]) -> str:
    return _text(note.get("last_update_time")) or _text(note.get("time"))


def build_payload(input_path: Path, keywords: Sequence[str], max_notes: int) -> dict:
    records, warnings = parse_jsonl(input_path)
    normalized = []
    for record in records:
        note = normalize_note(record, keywords)
        if note is not None:
            normalized.append(note)

    by_identity = {}
    for note in normalized:
        identity = note["stable_id"]
        previous = by_identity.get(identity)
        if previous is None or _duplicate_priority(note) > _duplicate_priority(previous):
            by_identity[identity] = note

    ranked = sorted(by_identity.values(), key=lambda note: (-note["score"], -_timestamp_key(note), note["stable_id"]))
    selected = ranked[:max_notes]
    return {
        "schema_version": 1,
        "source": "mediacrawler-xhs-jsonl",
        "query_keywords": list(keywords),
        "notes": selected,
        "image_review_candidates": [note["stable_id"] for note in selected if note["image_urls"] and len(note["description"].strip()) < 24],
        "warnings": warnings,
    }


def _timestamp_key(note: Mapping[str, object]) -> float:
    value = _text(note.get("last_update_time")) or _text(note.get("time"))
    if not value:
        return float("-inf")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return float("-inf")


def _duplicate_priority(note: Mapping[str, object]) -> tuple:
    canonical = json.dumps(note, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (note["score"], _timestamp_key(note), canonical)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--max-notes", type=int, default=20)
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return int(error.code)
    if not 1 <= args.max_notes <= 100:
        return 2
    payload = build_payload(args.input, args.keyword, args.max_notes)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
