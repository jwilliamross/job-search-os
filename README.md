# job-search-os

A job-application system for [Claude Code](https://claude.com/claude-code). You give it a
posting; it researches the firm, builds a table of the posting's requirements against your
evidence, drafts a one-page cover letter in your own voice, gates the draft for AI tells,
renders a clean PDF, drafts outreach notes, and tracks the pipeline in the repo.

Built by James Ross, a second-year Commerce student, for his own internship search after
a cycle of generic AI letters produced zero human interviews. The difference in this
version is discipline: a fact sheet every claim must trace to, hand-written voice samples
the model has to match, and a deterministic checker that blocks the sentences recruiters
recognise as AI.

## What is in it

```
CLAUDE.md                    rules and workflow Claude reads first
profile/                     your facts, voice guide, targets, stories, interview questions
samples/own-writing/         three to six pieces you wrote yourself (voice reference)
applications/_template/      posting.md, notes.md (fit table), cover-letter.md, outreach.md
applications/TRACKER.md      the pipeline
.claude/skills/              application, cover-letter, humanizer, job-search, outreach, prompt-showcase
scripts/voice_check.py       hard/soft AI-tell gate (dashes, not-X-but-Y, stock words, triads, closers...)
scripts/render_letter.py     letter markdown to PDF with headless Chromium
scripts/humanizer-metrics/   vendored 0-100 scorer (burstiness signal only; see calibration note)
scripts/search_jobs.py       python-jobspy scraper for LinkedIn / Indeed / Glassdoor
```

## Setup

1. Clone, open in Claude Code.
2. Answer `profile/interview/QUESTIONS.md` (voice memo transcript is fine). Ask Claude to
   fill `profile/PROFILE.md`, `VOICE.md`, `TARGETS.md`, and `stories.md` from it.
3. Put three to six things you wrote yourself in `samples/own-writing/`.
4. `pip install python-jobspy` if you want the scraper. Node 18+ for the metrics CLI.
   Chromium for PDFs (Playwright's `playwright install chromium` is enough).
5. Paste a posting. Say "apply to this."

## The pipeline for one letter

posting → fit table (their words vs. your evidence) → firm research (site, founder posts,
podcasts) → draft in your voice → `voice_check.py` (zero hard hits) → `humanizer` skill with
your samples → readability polish → `render_letter.py` → PDF → tracker row → commit.

## Honesty notes

- The numeric AI scorer rates some genuinely human writing as more "AI" than a rejected AI
  draft. It is kept for its sentence-variety signal only. The structural checker and the
  humanizer rules are the real gate.
- The system never applies on your behalf and never invents a fact. If it does not know a
  number, it leaves `[NEED: ...]` in the draft.

## Credits

- [blader/humanizer](https://github.com/blader/humanizer) (MIT), vendored as the primary humanizer skill.
- [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) (MIT), CLI scorer and 55-pattern checklist.
- [humanizer-tools/slop-humanizer](https://github.com/humanizer-tools/slop-humanizer) (MIT), banned-phrase checklist.
- [python-jobspy](https://github.com/speedyapply/JobSpy) for scraping.

## License

MIT. See `LICENSE`. Vendored components keep their own MIT notices.
