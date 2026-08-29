# Task 2–3 forward-test matrix

These are human or independent-agent acceptance cases. They test the coaching behavior by running the Skill; they are not source-matching assertions.

## 1. Missing company

**Given** a targeted preparation request includes a role title and resume but no company.
**When** the Skill is invoked.
**Then** it asks for the company and stops before role analysis, research, questions, or coaching output.

## 2. Missing role

**Given** a question-bank request includes a company and resume but no role title.
**When** the Skill is invoked.
**Then** it asks for the role title and stops before generating targeted questions.

## 3. Missing resume

**Given** a simulation request includes a company and role title but no resume.
**When** the Skill is invoked.
**Then** it asks for the resume and stops before beginning a simulation.

## 4. Role title only

**Given** a user asks to prepare for an AI Product Manager interview and gives only that title.
**When** the Skill is invoked.
**Then** the stop condition requests both the company and resume; it does not proceed with illustrative first-person experience or metrics.

## 5. No JD with complete inputs

**Given** company, role title, and resume are supplied but no JD.
**When** the user requests targeted preparation.
**Then** the output contains a source ledger with links; publication or update date when available (otherwise explicitly `Unknown`); access date; freshness or staleness risk; and separate fact/inference fields. Only evidence that reliably supports currentness and the company/role claim permits the subsequent requirement-to-evidence map. A live current first-party careers or ATS page may qualify when its publication/update date is `Unknown`; the output does not fabricate a JD or present an old posting as current.

## 5a. No JD with stale or unreliable sources only

**Given** company, role title, and resume are supplied but no JD, and the available sources are stale, social-only, otherwise unreliable, or have an unknown publication/update date whose currentness cannot be established through source authority, live availability or current-listing state, access date, corroboration, and staleness risk.
**When** the user requests targeted preparation.
**Then** the ledger labels the company/role-specific gap `Unknown`, records the access date and freshness/staleness risk for every source, and stops before company-specific requirement mapping, question-bank creation, or simulation. It asks for a JD or official link, or offers a clearly labeled generic role-practice path only after the user chooses it.

## 6. Standard question bank and exact question count

**Given** complete required inputs and a request for the Standard variant with ten one-shot questions.
**When** the Skill generates the question bank.
**Then** the output contains exactly ten primary question items, while listed follow-ups remain outside that primary count. Each item includes question type, difficulty, a separate practice priority, likelihood, competency, evidence trigger, answer direction, compact reference answer, likely follow-ups, and red flags.

## 7. Sprint question bank

**Given** complete required inputs and a request for the Sprint variant.
**When** the Skill generates the question bank.
**Then** every item contains a question, exactly three answer points, must-use evidence, a concise reference answer, and its most dangerous follow-up; it does not add Standard-only fields or a fourth answer point.

## 8. Resume metric gap

**Given** a supplied resume says a project improved engagement but provides no baseline, measurement method, or result.
**When** the Skill maps project evidence or drafts a reference answer.
**Then** it asks a factual follow-up for the missing measurement instead of assigning an improvement number or claiming an unsupported outcome.

## 9. Simulation is not a real interview

**Given** a coaching simulation has occurred and the user later designates a separate transcript as a real interview.
**When** the later request is reviewed.
**Then** the simulation is excluded from performance evidence and may appear only in a separately requested comparison section.

## 10. Early interviewer-style adaptation

**Given** a strict simulation has an agreed four-question block and reaches four substantive question-and-answer exchanges.
**When** that agreed strict block has ended.
**Then** it labels the disclosed interviewer-pattern result provisional and includes observable-question evidence, confidence, a competing interpretation, and an adjustment strategy with a revision condition for conflicting later behavior. It does not disclose the diagnosis before the block ends.

## 10a. Long strict block remains feedback-free while adapting internally

**Given** a strict simulation has an agreed six-question block, and after exchanges three through five the observable question behavior supports a provisional interviewer-style hypothesis.
**When** the block is still in progress.
**Then** the Skill applies that hypothesis internally only to choose realistic follow-ups; it gives no hints, corrections, answer feedback, interviewer-style diagnosis, evidence summary, confidence, competing interpretation, or adjustment advice. Once the sixth exchange ends the block, it may disclose that card and feedback.

## 11. Ambiguous real-interview designation

**Given** a user invokes the Skill and attaches two transcripts but does not identify either as an actual interview.
**When** they ask for a review.
**Then** the Skill asks which exact artifact is the real interview and stops before assigning any performance or hiring signal.

## 12. Transcript available, raw audio unavailable

**Given** a user explicitly designates a speaker-labeled timestamped transcript as a real interview and also mentions an MP3 that cannot be processed.
**When** the Skill reviews the interview.
**Then** it names the designated transcript, discloses text-only analysis and unavailable audio processing, may analyze timestamps and visible interruptions, and does not claim tone, vocal hesitation, audible pauses, or speaking rate.

## 13. Adaptive per-question analysis

**Given** a designated interview contains a project-depth question and an AI-product scenario question.
**When** the Skill performs question-level review.
**Then** each question receives the mandatory core analysis, while the project question adds ownership and metric-credibility analysis and the scenario question adds AI necessity, evaluation, risk, and trade-off analysis only where supported by the evidence.

## 14. Evidence-grounded direct feedback

**Given** a designated transcript contains one answer that leads with an owned decision and evidence, and another that evades a repeated question about a metric.
**When** the Skill synthesizes feedback.
**Then** it gives direct positive and negative judgments with turn-specific evidence, identifies the metric evasion as a hiring-relevant risk, and does not add flattery, humiliation, or personality labels.

## 15. Long-transcript reconciliation

**Given** a designated long transcript must be processed in several bounded sections and contains substantive questions near both the beginning and end.
**When** the Skill produces the final review.
**Then** it builds a chronological question index, accounts for the final substantive question in the completed analysis, and discloses any segment it could not reconcile instead of claiming complete coverage.

## 16. Original-transcript conflict

**Given** an old review says the candidate never gave a metric, while the user-designated original transcript contains a timestamped metric statement.
**When** the Skill evaluates that claim.
**Then** it treats the transcript as direct performance evidence, exposes the discrepancy with the relevant turn, and adjusts the old review’s conclusion rather than silently repeating it.

## 17. Text-only interviewer tone

**Given** the only real-interview evidence is plain text with no successfully analyzed audio.
**When** the Skill infers interviewer style.
**Then** it may discuss observable question depth, follow-up pattern, and requests for evidence, but marks tone, vocal affect, intonation, and audible pauses as Unknown.

## 18. Explicit non-vocal style evidence level

**Given** a designated text transcript shows the interviewer repeatedly asks for ownership and quantitative evidence, with no audio analysis.
**When** the Skill concludes that the interviewer likely prefers concise, evidence-led answers.
**Then** the conclusion explicitly labels `Evidence level: Inferred`, cites the observed question pattern, includes a competing interpretation and confidence, recommends a candidate adjustment, and warns against overfitting the inference.

## 19. Explicitly limited longitudinal scope

**Given** a user selects exactly two designated real-interview transcripts for a longitudinal review and identifies their interview dates.
**When** the Skill compares them.
**Then** it lists only those two files in its evidence register, maps each to the provided identity, stage, and date, extracts them independently before comparing normalized dimensions, and cites interview-specific evidence for any pattern; it does not inspect or include other available artifacts.

## 20. Folder boundary does not expand scope

**Given** a user mentions a folder while asking to prepare for a later round, but does not select files inside it or authorize any adjacent or parent directory.
**When** the Skill needs earlier-round evidence.
**Then** it asks the user to identify the exact artifacts or an explicit folder scope, and it does not search the mentioned folder, its parent, or neighboring folders for a presumed first-round transcript.

## 21. Second-round preparation from a designated first-round transcript

**Given** a user supplies company, role, resume, current stage, and designates a first-round real transcript plus an old first-round review.
**When** the Skill prepares the second round.
**Then** it uses the transcript as direct evidence, treats the review as supporting judgment, exposes any material conflict, identifies unresolved doubts and repeated probes, provides a re-prioritized question set and fact-grounded answer repairs, and treats the next interviewer’s style as a fresh hypothesis rather than copying the first interviewer’s style.

## 22. Repeated weakness with controlled evidence

**Given** two comparable selected real interviews contain separate timestamped follow-ups because the candidate cannot define the denominator for an outcome metric.
**When** the Skill performs longitudinal review.
**Then** it classifies metric credibility as a repeated or stable weakness, cites evidence from both interviews, distinguishes the observation from any causal explanation, and prioritizes a measurable drill by hiring impact, frequency, and ease of improvement.

## 23. Insufficient evidence for a trend

**Given** one selected interview is an HR motivation screen and the other is a technical project deep dive, with unknown stages and difficulty.
**When** the Skill compares answer concision or pressure response.
**Then** it records the unknown metadata and control mismatch, classifies the trend as insufficient evidence or conditional rather than improvement or regression, and does not use filename order or a prior simulation to manufacture a trend.

## 24. MediaCrawler is missing

**Given** a user explicitly asks for Xiaohongshu research but supplies neither a current-request checkout path nor `AI_PM_MEDIACRAWLER_PATH`.
**When** the Skill checks availability.
**Then** it reports `missing`, does not scan for a checkout or run a crawler, and offers ordinary web research with its non-export and image-coverage limits labeled.

## 25. Configured checkout is invalid

**Given** the user supplies a current-request checkout path and the checker returns `invalid`.
**When** the Skill evaluates the configuration.
**Then** it reports the observed invalid status, does not infer readiness from the directory, install or repair MediaCrawler, and offers the coverage-labeled ordinary-web fallback.

## 26. Ready checkout has unverified login

**Given** the checker returns `ready` for an explicitly supplied checkout, but the user has not verified login or live-site access.
**When** the Skill is asked about availability.
**Then** it states that `ready` verifies only checkout markers and `uv`, not browser, login, cookie, or live-access readiness, and it does not auto-login, inspect cookies, or run a crawler without a separate explicit search request.

## 27. Image-heavy note without local images

**Given** normalized results identify a note in `image_review_candidates`, but no local image files or supported image attachments are supplied.
**When** the Skill analyzes Xiaohongshu research.
**Then** it completes text and metadata analysis, lists the unreviewed image evidence as a limitation, and does not infer questions or experiences from image URLs, filenames, or captions.

## 28. Normalized notes become simulation preparation

**Given** user-selected normalized notes contain traceable, relevant interview reports with recurring themes.
**When** the Skill prepares a simulation.
**Then** it cites note URLs or note IDs in the research evidence table and produces targeted simulation questions and answer-preparation implications, while treating reports as likely themes rather than company policy, candidate facts, or candidate-performance scoring.

## 29. Setup advice is preview-only

**Given** a user asks how to configure MediaCrawler but does not explicitly request a Xiaohongshu search.
**When** the Skill provides setup guidance.
**Then** it shows the user-reviewed bounded command only as a preview after the checker guidance and does not execute a crawler command, login, or cookie action.

## 30. Explicit bounded MediaCrawler search

**Given** a current request explicitly asks the Skill to search Xiaohongshu with MediaCrawler and the local checker has returned `ready` for a current-request checkout or `AI_PM_MEDIACRAWLER_PATH`.
**When** the Skill proceeds.
**Then** before the command it creates a task-specific temporary artifact directory with `mktemp -d` outside the Skill repository and worktree, prints and discloses its exact path, and may run exactly one bounded command with the documented search, count, concurrency, JSONL, and output-path limits. It does not expand scope, install software, use any other crawler command, stage or commit artifacts, or silently promote them.

## 31. Login or risk-control failure stops safely

**Given** the one authorized bounded command reports QR/login, verification, access-control, risk-control, or rate-limit failure.
**When** the Skill reports the result.
**Then** it states the observed failure, stops the crawler workflow, and neither bypasses the control nor retries indefinitely; it may offer the coverage-labeled ordinary-web fallback.

## 32. Normalizer artifacts stay temporary unless explicitly promoted

**Given** the user selects a MediaCrawler JSONL export for analysis but does not request an output destination.
**When** the Skill normalizes the export.
**Then** before normalization it creates, prints, and discloses an exact task-specific `mktemp -d` artifact path outside the Skill repository and worktree, writes the normalized artifact there, and returns analysis in conversation. It neither stages nor commits the artifact and retains or promotes it only after the user explicitly names a safe destination that is not the Skill repository or worktree.
