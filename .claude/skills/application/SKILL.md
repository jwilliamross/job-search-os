---
name: application
description: Start a new application from a job posting. Use when the user pastes or links a posting, says "apply to this", or asks to set up an application. Creates the application folder from the template, saves the posting verbatim, writes the fit analysis, adds the tracker row, and lists what still needs the user.
---

# Application setup

## Steps

1. **Capture the posting.** If given a URL, fetch it. (LinkedIn blocks most sandboxes;
   an external page fetcher usually works on public job pages, otherwise ask the user to
   paste the text.) Save the full text, unedited, plus the URL and capture date, to
   `applications/<folder>/posting.md`. Folder name: `YYYY-MM-<firm-slug>-<role-slug>`.
2. **Create the folder** by copying `applications/_template/` and filling the README
   table (firm, role, req ID, team, location, term, deadline, portal, contacts).
3. **Fit analysis** in `notes.md`: one row per requirement in the posting, in the
   posting's own words, matched to a specific item from `profile/PROFILE.md`. Mark each
   strong / ok / gap. Be honest about gaps; they shape the letter.
4. **Firm research**, three to five checkable facts with sources: what the team does,
   recent work, anything the hiring team has written or said publicly, anyone the user
   might know (check `profile/network/` and earlier `applications/*/outreach.md`).
5. **Decide** and record in `notes.md`: lead differentiator, whether personal context is
   used, whether the prompt appendix fits (see the `prompt-showcase` skill).
6. **Tracker row** in `applications/TRACKER.md`, status `researching`, with the deadline.
7. **Deadline safety:** if the deadline is within 7 days, say so first.
8. Commit with message `app: <firm> <role> setup`.

## Reply to the user

The deadline and how much time there is; the three strongest matches and the biggest gap;
what is needed from them for this one; whether to proceed to the cover letter now.
