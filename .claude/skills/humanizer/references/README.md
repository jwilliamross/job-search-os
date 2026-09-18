Second-opinion checklists, vendored 2026-09-18:
- aboudjem-humanizer-SKILL.md: 55 patterns, five voices (MIT, Aboudjem/humanizer-skill). Its
  CLI scorer lives at scripts/humanizer-metrics/.
- slop-humanizer-SKILL.md: synthesis of eight humanizer repos (humanizer-tools/slop-humanizer),
  strongest on banned phrases and "throat-clearing openers".
The primary skill (../SKILL.md, blader/humanizer) stays the one that runs; read these when a
draft still reads as AI after the primary pass, and pull their banned-phrase lists into
scripts/voice_check.py as they prove useful.
