# Xiaohongshu research analysis

Use this two-stage workflow only for a user-selected MediaCrawler export or explicitly supplied Xiaohongshu research material. It supports likely interview themes and targeted preparation; it never creates candidate facts, scores candidate performance, or replaces the selected real-interview evidence.

## Stage 1: text and metadata

Normalize the selected JSONL before analysis. Unless the user has explicitly requested retention at a named safe destination, create a task-specific temporary artifact directory outside the Skill repository and worktree, then print and disclose its exact path before use:

```bash
task_xhs_normalizer_artifact_dir="$(mktemp -d /tmp/ai-pm-xhs-normalizer.XXXXXX)"
printf 'Xiaohongshu normalizer temporary artifact directory: %s\n' "$task_xhs_normalizer_artifact_dir"
```

Do not stage, commit, or silently promote the selected export or normalized output. Retain or copy either only after the user explicitly requests it and names a safe destination; the Skill repository and worktree are never valid output destinations.

Normalize the selected JSONL into that temporary directory:

```bash
python3 ai-pm-interview-coach/scripts/normalize_xhs_jsonl.py \
  --input /absolute/path/to/search_contents_YYYY-MM-DD.jsonl \
  --output "$task_xhs_normalizer_artifact_dir/xhs-normalized.json" \
  --keyword "公司名" \
  --keyword "岗位名" \
  --keyword "AI产品经理" \
  --max-notes 20
```

Rank normalized notes by explicit relevance signals, remove duplicates, and retain source provenance, including note URL or note ID, source keyword, and collection date when available. Classify each item as one of: firsthand interview report, role discussion, company discussion, generic advice, promotional content, or uncertain. Assess credibility from the traceable source type and stated uncertainty; do not promote an anecdote because it is highly relevant. Extract only claims traceable to a note URL or note ID. Treat anecdotes as leads rather than verified company policy, and keep conflicts or uncertain claims visible rather than resolving them into facts.

## Stage 2: image evidence

Inspect only entries named by `image_review_candidates`, and only when their local image files or supported image attachments are actually available. Record every image actually inspected, extract questions and experiences with an uncertainty label, and merge image and text findings with deduplication. If the images are unavailable, state that text analysis is complete and that image-contained evidence remains unreviewed; do not infer image content from filenames, URLs, captions, or note metadata.

## Research output contract

Return these sections:

1. Search scope and date, including the selected files and unselected exclusions.
2. Source inventory with note URL or note ID, source type, collection date, relevance, credibility, and duplicate handling.
3. Recurring question themes and company/role-specific signals.
4. Conflicting or uncertain reports, including whether relevant images were inspected or remain unreviewed.
5. Targeted simulation questions and answer-preparation implications, clearly separated from candidate facts and performance judgment.
6. An evidence table whose claims link to a note URL or note ID, plus limitations and coverage gaps.

External reports can change preparation priority or suggest likely themes. They cannot establish a company policy, candidate biography, candidate answer quality, or real-interview performance; use supplied resume and explicitly selected real evidence for those claims.
