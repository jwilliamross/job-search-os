# CLAUDE.md — job-search-os

This repo is a job-search operating system run with Claude Code. Claude finds roles,
writes application materials in the user's own voice, gates every draft for AI tells,
renders the PDF, and tracks the pipeline. Read this file first in every session.

## Repo map

| Path | What lives there |
|---|---|
| `profile/` | `PROFILE.md` (facts, the source of truth), `VOICE.md`, `TARGETS.md`, `stories.md`, `interview/QUESTIONS.md`, `network/` (LinkedIn export, gitignored) |
| `samples/own-writing/` | Pieces the user wrote entirely themselves. Voice reference only |
| `applications/` | One folder per application from `_template/`, plus `TRACKER.md` |
| `prompts/` | Showcase prompts and resume change-list prompts |
| `scripts/` | `voice_check.py` (AI-tell gate), `render_letter.py` (letter to PDF), `humanizer-metrics/` (vendored scorer), `search_jobs.py` |
| `.claude/skills/` | `application`, `cover-letter`, `humanizer`, `job-search`, `outreach`, `prompt-showcase` |

## Hard rules

1. **Never fabricate.** Every claim in a resume or letter traces to `profile/PROFILE.md` or
   to something the user said in the session. Missing fact: leave `[NEED: ...]` and ask.
2. **`[VERIFY]` items are unconfirmed.** Never put them in an outbound document.
3. **Write in the user's voice.** Follow `profile/VOICE.md`; read `samples/own-writing/`
   before drafting; run `scripts/voice_check.py` and the `humanizer` skill on every draft.
4. **No secrets in the repo.** No keys, passwords, government IDs, banking details.
5. **One application, one folder**, and a row in `applications/TRACKER.md`.
6. **Echo everything back to the repo.** New facts, preferences, and decisions the user
   states in chat get written into `profile/` or the application folder and committed.
7. **Commit early, commit often.**

## Letter rules (see `.claude/skills/cover-letter/SKILL.md` for the full list)

One page, 250-380 words, the posting's own requirements answered with numbers, no
em-dashes, no bold headers, no numbered reasons, no availability dates, no volunteered
gaps, contractions kept, one modest clause per "nice to have" trait, one specific thing
the hiring team wrote, the user's own sign-off.

## Standard workflow for a new application

1. `application` skill: posting saved verbatim, folder, fit table, tracker row.
2. `cover-letter` skill: draft, `voice_check.py` (zero hard hits), `humanizer`, polish
   pass, `render_letter.py`, deliver PDF, commit.
3. `prompt-showcase` if the posting asks for prompts or the firm is AI-curious.
4. Resume: copy the working resume into the folder; reorder and re-emphasize only.
5. `outreach`: two or three people, drafted notes.
6. Commit.
