# Optional MediaCrawler integration

MediaCrawler is optional and is not bundled with this Skill. It must be separately installed and configured on each computer. The portable Skill travels through GitHub; machine-specific checkout paths do not. Use only a checkout path supplied in the current request or `AI_PM_MEDIACRAWLER_PATH`; never scan for a likely checkout or treat the existence of a directory as readiness.

## Availability and authorization

Before suggesting or running a search, run the local checker against the user-supplied checkout:

```bash
python3 ai-pm-interview-coach/scripts/check_mediacrawler.py --path /absolute/path/to/MediaCrawler --json
```

When configuration comes only from `AI_PM_MEDIACRAWLER_PATH`, omit `--path` and keep `--json`. The checker statuses are `missing`, `invalid`, `uv-missing`, and `ready`. Only `ready` permits preparing the bounded command; it confirms the supplied checkout markers and local `uv` only. It does not verify dependencies, browser availability, login state, cookies, or live-site access.

Never install MediaCrawler, auto-login, access or reuse cookies, bypass anti-bot, access, risk, or rate controls, or run a crawler merely because the checkout is available. A setup-only request receives the command below as a preview for user review and does not authorize execution. Only a current request that explicitly asks this Skill to search Xiaohongshu with MediaCrawler, together with a `ready` checker result, authorizes one bounded command.

Before an authorized run, create a task-specific temporary artifact directory outside the Skill repository and worktree. Print and disclose its exact path before using it; use this task-specific variable name, not `HOME` or `CODEX_HOME`:

```bash
task_mediacrawler_artifact_dir="$(mktemp -d /tmp/ai-pm-mediacrawler.XXXXXX)"
printf 'MediaCrawler temporary artifact directory: %s\n' "$task_mediacrawler_artifact_dir"
```

The temporary directory is the default output location. Do not stage, commit, or silently promote scraped artifacts. Retain or copy an artifact only after the user explicitly requests it and names a safe destination; never use the Skill repository or worktree as that destination.

```bash
cd /absolute/path/to/MediaCrawler
uv run main.py \
  --platform xhs \
  --lt qrcode \
  --type search \
  --keywords "公司名,岗位名,AI产品经理,面试,面经" \
  --get_comment false \
  --get_sub_comment false \
  --crawler_max_notes_count 20 \
  --max_concurrency_num 1 \
  --save_data_option jsonl \
  --save_data_path "$task_mediacrawler_artifact_dir"
```

Expected content output is `$task_mediacrawler_artifact_dir/xhs/jsonl/search_contents_YYYY-MM-DD.jsonl`; expected images are `$task_mediacrawler_artifact_dir/xhs/images/<note_id>/<filename>`. Do not infer that either exists before the user supplies or selects it for analysis.

## Ownership, sources, and safe stop

The user is responsible for QR login, site terms, account risk, local browser state, and MediaCrawler's current non-commercial learning license. Refer the user to the official [MediaCrawler repository](https://github.com/NanmiCoder/MediaCrawler), [quick-start section](https://github.com/NanmiCoder/MediaCrawler#-快速开始), [pyproject](https://github.com/NanmiCoder/MediaCrawler/blob/main/pyproject.toml), and [license](https://github.com/NanmiCoder/MediaCrawler/blob/main/LICENSE).

If QR/login, verification, access control, risk control, or rate limiting prevents the bounded run, stop safely. Report only the observed status or error; do not bypass the control and do not retry indefinitely. If MediaCrawler is missing, invalid, or otherwise unavailable, use ordinary web research instead and label that its coverage differs: it is not a local MediaCrawler Xiaohongshu export and may not include locally inspectable note images.
