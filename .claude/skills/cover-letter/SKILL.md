---
name: cover-letter
description: Draft a cover letter in the user's own voice for a specific posting. Use when the user asks for a cover letter, a letter of interest, a "why us" answer, or an application essay. Produces a one-page letter, checked against the profile for facts, gated by voice_check.py and the humanizer skill, then rendered to PDF.
---

# Cover letter

## Inputs to gather first

1. The posting, verbatim, at `applications/<folder>/posting.md` (run `application` first).
2. `profile/PROFILE.md` (facts; nothing tagged `[VERIFY]` may be used).
3. `profile/VOICE.md` (the user's voice rules) and the writing samples in
   `samples/own-writing/` (read at least two before drafting; feed them to the humanizer
   as the voice sample).
4. `applications/<folder>/notes.md` for the fit table and the firm-specific fact.

## Shape of the letter

Body 250-380 words, one page. Four moves:

1. **Frame, then the writer.** One sentence of context that is true and specific to this
   firm or team (a line from the posting, a deal, a product, something the hiring team
   wrote), then the writer in one sentence: who they are and what they are applying for.
   No "I am writing to express my interest."
2. **The posting's own words, answered.** Take the two or three requirements the posting
   emphasizes and answer each with one concrete thing the writer did, with a number or a
   name. Prose, not a bulleted list.
3. **The through-line.** One short cause-and-result sequence that shows the writer's
   pattern (the same trait proven two or three times, briefly). Interests the posting
   names as assets get one clause each, never the lead.
4. **Close on the firm.** Quote or paraphrase the one specific thing the hiring team wrote
   and say what the writer did with it. Then the writer's usual sign-off.

## Rules (learned the hard way; keep them)

- No em-dashes. No bold sub-headers. No numbered reasons. At most one not-X-but-Y.
- Keep the writer's contractions and directness. Formal balanced sentences read as AI.
- Do not volunteer negatives or gaps ("I have no X yet", "X is the gap").
- Do not oversell traits the posting merely lists as assets; one modest clause each.
- Say "helped" where the writer was one contributor. Never claim they executed what they
  proposed.
- Never state availability dates in the letter; handle scheduling after an offer.
- Never frame a past job as the high point or compare its stakes to the target firm's.
  Frame what was earned to get it and what was done there.
- No superlatives about the firm's writing ("the clearest thing I've ever read").
- No "which has meant X-ing, Y-ing, and Z-ing." Give the sentence a subject.
- Every number and name must trace to the profile or the user's own words. Unknown detail
  gets `[NEED: ...]`, never a guess.
- Personal, family, financial, or health context stays out unless the user says otherwise.

## Process (mandatory order; do not skip a gate)

1. Fill the fit table in `notes.md` if it is empty. Research the firm.
2. Draft to `applications/<folder>/cover-letter.md` in the format
   `scripts/render_letter.py` expects (name line, contact line, date, address, `Re:`,
   salutation, paragraphs, sign-off, optional "Prompts used" appendix).
3. Gate 1: `python3 scripts/voice_check.py <file>`. Zero HARD hits. Fix soft hits unless
   there is a reason to keep one, and say the reason.
4. Gate 2: run the `humanizer` skill with the samples in `samples/own-writing/` as the
   voice sample. Apply the rewrite. If it still reads flat, read
   `.claude/skills/humanizer/references/slop-humanizer-SKILL.md` and go again.
5. Gate 3: polish for readability. Split any sentence with three or more clauses. Keep
   sentence lengths varied. Then read it aloud as the writer: would they say each
   sentence to a former boss?
6. Optional signal: `node scripts/humanizer-metrics/index.js score <file>`. Use the
   burstiness line only; the total score does not separate real human writing from AI.
7. Word count. Render: `python3 scripts/render_letter.py <file>`. Check the page count.
8. Deliver the PDF (and a Doc if the user wants one), record links in the application
   README, update `applications/TRACKER.md`, commit.
