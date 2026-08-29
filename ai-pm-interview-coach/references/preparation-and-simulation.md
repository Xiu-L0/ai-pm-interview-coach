# Preparation, question bank, and simulation

Apply this workflow only for targeted preparation, a one-shot question bank, or an interactive simulation. Keep all work within the evidence and modality boundaries in the input contract.

## Start conditions and research

Before analysis, confirm the company, role title, and resume are all present. They are mandatory. Ask for every missing item and stop; do not begin generic targeted coaching in the meantime. If the user supplies only a role title, explicitly request both the company and the resume, then stop. A JD is optional: use one the user supplied, but never fabricate one.

When company, role, and resume are present but the JD is absent, research the named company and role. Prefer official company information and current recruiting pages, then reputable job pages, product and business context, and recent role-adjacent information. For every source-ledger row, record link; publication or update date when available (otherwise explicitly `Unknown`); access date; freshness or staleness risk; fact; and derived inference in separate fields. Treat social interview reports as preparation signals, not role facts, and never present an old posting as current.

Continue with company/role-specific preparation only when the evidence reliably supports both currentness and the company/role claim being mapped. Evaluate source authority, live availability or current-listing state, publication or update date when available, access date, corroboration, and staleness risk together. A missing publication or update date remains explicitly `Unknown` and contributes freshness risk, but does not by itself require a stop; for example, a live first-party careers or ATS listing can qualify when its authority and current-listing state reliably establish currentness. Stop only when the available evidence cannot reliably support current company/role-specific claims: label the gap `Unknown`, stop before the requirement-to-evidence map, company-specific question bank, or company-specific simulation, and ask the user for a JD or official link. A clearly labeled generic role-practice path is available only after the user explicitly chooses it; do not blend it into targeted preparation.

## Evidence map and story extraction

Create a requirement-to-evidence map before drafting the questions:

| Likely requirement | Evidence source | Resume proof | Gap/risk | Interview priority |
| --- | --- | --- | --- | --- |

For a supplied JD, decompose explicit responsibilities, expected outcomes, core competencies, hidden constraints, likely interviewer verification methods, and business or industry assumptions. Tie every hidden inference to the specific JD wording that supports it.

Extract each relevant project story as: context, goal, ownership, decision, AI/product method, trade-off, result, metric credibility, failure/reflection, and likely drill-down. A missing fact, metric, ownership detail, or result becomes an explicit factual question for the candidate. Never invent candidate experience, ownership, results, metrics, or numbers.

## Question-bank construction

Set coverage from the requirement-to-evidence map, especially job requirements and resume risks. Cover as relevant: resume, project depth, AI product judgment, strategy, metrics, experimentation, technical collaboration, execution, conflict, failure, pressure, scenario, motivation, company/role fit, and candidate questions.

For a requested count **N**, return exactly **N** primary questions. Follow-up prompts are supplementary and do not count toward N.

Offer two question-bank variants. Use Standard unless the user explicitly requests Sprint.

### Standard

Each Standard one-shot item includes:

1. Question
2. Question type, difficulty, and **priority** (what to practice first; priority is separate from difficulty)
3. Why it is likely and the competency tested
4. Resume/JD trigger and candidate project evidence to use
5. Answer direction and a compact reference answer
6. Likely follow-ups and red flags

The reference answer is a response blueprint, not invented biography: use only supplied candidate facts, mark missing facts as placeholders to verify, and do not state unverified ownership, results, or numbers as the candidate's own.

### Sprint

Each Sprint one-shot item includes: question; exactly three answer points; must-use evidence; a concise reference answer; and the most dangerous follow-up. Keep Sprint concise without adding Standard-only fields or extra answer points.

## Interactive simulation

Offer only these explicit modes:

- **Strict simulation:** give no hints, corrections, answer feedback, or disclosed interviewer-style diagnosis during the agreed question block; disclose feedback only after that block ends.
- **Coaching simulation (live coaching):** give feedback immediately after each answer.
- **Focused pressure drill:** concentrate on a selected weakness or question type.

Ask one primary question at a time, wait for the user's answer, and select follow-ups based on weak, missing, or contradictory evidence. A simulated interviewer style is always a training setup, never a factual portrait of a target interviewer.

After the first three to five substantive exchanges—or after the first few minutes when reliable time evidence exists—form a provisional interviewer-style hypothesis from observable question behavior. In strict simulation, apply it internally to continue realistic questioning, but explicitly give no hints and disclose no diagnosis, evidence, confidence, competing interpretation, or adjustment until the agreed block ends. At the end of that block, disclose the provisional card with its evidence, confidence, competing interpretation, adjustment strategy, and revision condition. In separately selected live coaching, disclose it immediately when it is formed. Do not carry simulation behavior into a later real-interview evaluation as performance evidence.

## Answer pattern

Default to: conclusion first; only relevant context; personal ownership; key decision and trade-off; measurable result; reflection. Use another structure when the scenario calls for it, while preserving evidence-backed ownership and factual precision.
