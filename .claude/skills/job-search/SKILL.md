---
name: job-search
description: Find and shortlist postings that fit the user's targets in profile/TARGETS.md. Use when the user asks to find jobs, check deadlines, scan postings, or refresh the pipeline. Produces a ranked shortlist and updates the tracker.
---

# Job search

## Targets

Read `profile/TARGETS.md` first: role types in priority order, geography, term dates,
pay floor, eligibility (year of study). Read eligibility lines in postings carefully and
flag mismatches rather than silently skipping.

## Sources, in order of yield

1. Company career pages (most reliable for dates). Keep the firm list in `profile/TARGETS.md`.
2. The user's school career portal (their login; ask for exports or screenshots).
3. LinkedIn Jobs, Indeed, Glassdoor via `scripts/search_jobs.py` (python-jobspy). Edit the
   `QUERIES` and `LOCATIONS` lists at the top of the script. Expect noise.
4. Aggregators and industry boards relevant to the user's field.
5. Web search for `"<role>" <year> site:<firm>` when a page is hard to find.

## Process

1. Pull the current pipeline from `applications/TRACKER.md` so nothing is duplicated.
2. For every candidate: firm, role, team, location, term, deadline (or "rolling"),
   eligibility line, URL, one-line fit note.
3. Rank by fit (weight 3), deadline urgency (2), the user's edge at that firm (2),
   eligibility risk (-2).
4. Write `applications/SHORTLIST-<YYYY-MM-DD>.md` and add the top rows to the tracker.
5. Tell the user: the five to start this week, anything closing within 10 days, and any
   eligibility questions to ask a recruiter rather than assume.

## Never

- Never mark a deadline confirmed unless it was read from the posting itself.
- Never apply on the user's behalf. Claude drafts, the user submits.
