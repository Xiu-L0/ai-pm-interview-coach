# Input contract

Use this matrix before mode-specific work. Required inputs are blocking unless the user explicitly changes to a different mode or requests a non-targeted general answer.

| Mode | Required | Optional | Blocking behavior |
| --- | --- | --- | --- |
| Preparation / simulation / question bank | company, role title, resume | JD, interview stage, interviewer role, user-selected historical files, research request | Ask for every missing required item; do not continue. |
| Single real-interview review | user-designated real transcript or recording | company, role, resume, JD, prior-round files | If real evidence is not explicitly designated, ask which artifact is the real interview. |
| Later-round preparation | company, role, resume, current stage, explicitly selected prior real-interview evidence | JD, interviewer role, selected historical reviews | Ask for missing required items. |
| Longitudinal review | two or more explicitly selected real-interview transcripts or reviews | resumes, JDs, date range | State the supplied scope; never expand it automatically. |

## Missing-JD fallback

When preparation, simulation, or a question bank has the required company, role, and resume but no JD, research the named company and role on the web. For every source-ledger row, record the source link, publication or update date when available (otherwise explicitly `Unknown`), access date, freshness or staleness risk, facts, and derived inferences separately. Do not fabricate a JD, present an old posting as current, or treat social interview reports as role facts.

Proceed with company/role-specific requirement mapping, question-bank generation, or simulation only when at least one reliable current source supports those company/role-specific claims. If no such source is available, label the gap `Unknown`, stop the company-specific route, and ask for a JD or official link. Offer a clearly labeled generic role-practice path only after the user chooses it.

## Evidence terms

- **Real interview evidence:** a transcript or recording that the user explicitly designates as an actual interview.
- **Simulation evidence:** material created during practice, mock interviews, or training; it is never real-performance evidence by default.
- **Supporting context:** user-selected material that informs interpretation but is not direct evidence of the performance or role fact at issue.
- **Derived inference:** a clearly labeled conclusion drawn from supplied evidence rather than a user-confirmed fact.

## Source precedence and conflicts

Apply precedence to the fact being evaluated; sources are not globally interchangeable.

- For performance facts, a current real-interview transcript outranks an old review.
- For role facts, the current JD and official company sources outrank social posts.
- Social interview reports affect preparation probability only; they do not establish role or performance facts.
- User-confirmed facts override a conflicting inference.

Show conflicts, their sources, and their effect on the conclusion. Do not silently resolve them.

## Optional MediaCrawler and Xiaohongshu boundary

Use MediaCrawler or Xiaohongshu only after the user explicitly requests a bounded search. Do not install MediaCrawler, log in, extract or reuse cookies, bypass controls, or start a crawl because a tool or checkout exists. Process metadata and text first; inspect images only when the image inputs are actually available.
