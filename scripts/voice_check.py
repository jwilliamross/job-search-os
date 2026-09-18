#!/usr/bin/env python3
"""Deterministic AI-tell and voice check for a cover letter draft.

Usage: python3 scripts/voice_check.py applications/<folder>/cover-letter.md
Exit code 1 if any HARD tell is found. Prints every hit with the sentence.

Hard tells (block the draft): em/en dashes, not-X-but-Y and its variants, "I am writing to",
stock AI words, staged openers, "I hope this", triads by reflex in three or more sentences,
the same word opening three consecutive sentences.
Soft tells (warn): semicolons > 3, sentences over 42 words, three or more sentences in a row
of near-identical length, hedges stacked, parallel "X, testing it, and Y" gerund lists,
paragraph-final one-liners, "which has meant".
Voice stats: contraction count, average sentence length, share of sentences with a number.
"""
import re, sys

HARD = {
    "dash": r"[—–]|\s--\s",
    "not_x_but_y": r"\bnot (just|only|merely|simply)?\s*\w[^.;]{0,60}?\bbut\b|\bit'?s not [^.;]{0,50}, it'?s\b|\brather than\b|\bthis (does not|doesn't) mean\b",
    "i_am_writing": r"\bI am writing to\b|\bI'm writing to\b|\bexpress my (strong )?interest\b",
    "stock_words": r"\b(delve|tapestry|testament|underscore|showcase|pivotal|crucial|robust|leverage|leveraging|passionate|passion for|seamless(ly)?|dynamic|synergy|fast-paced|results-driven|proven track record|eager to|thrilled|excited to|unique blend|honed|spearheaded|utilize[sd]?|impactful|cutting-edge|in today's|landscape|journey|elevate|empower|foster(ing)?|vibrant|meticulous(ly)?|deep dive|aligns? with|resonate[sd]?)\b",
    "staged_opener": r"^(Honestly|Look|Here'?s the thing|The thing is|Let'?s be honest|Real talk)\b",
    "chat_residue": r"\bI hope this (helps|finds you well)\b|\bThank you for (your time and )?consideration\b|\blook forward to (the opportunity|discussing)\b",
    "win_win": r"\bwin-win\b|\bhit the ground running\b|\bthink outside the box\b|\bgo above and beyond\b|\bwear many hats\b",
}
SOFT = {
    "which_has_meant": r"\bwhich has meant\b|\bwhich means\b",
    "gerund_triad": r"\b\w+ing\b[^.]{0,40},\s*\w+ing\b[^.]{0,40},\s*and\s+\w+ing\b",
    "hedge_stack": r"\b(perhaps|arguably|potentially|somewhat|fairly|quite|rather)\b[^.]*\b(perhaps|arguably|potentially|somewhat|fairly|quite|rather)\b",
    "adjective_stack": r"\b(strong|excellent|exceptional|outstanding|significant|extensive|proven)\b[^.]*\b(strong|excellent|exceptional|outstanding|significant|extensive|proven)\b",
    "clearest_ever": r"\bthe (clearest|best|most \w+) [^.]{0,40} I('ve| have) (ever )?(read|seen|heard)\b",
}

def sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", text) if s.strip()]

def main(path):
    raw = open(path, encoding="utf-8").read()
    body = raw.split("Prompts used")[0]  # check the letter, not the appendix
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    hard_hits, soft_hits = [], []
    sents = []
    for p in paras:
        ss = sentences(p)
        sents.extend(ss)
        for s in ss:
            if s.rstrip().endswith(",") and len(s.split()) <= 7:
                continue  # sign-off line ("Look forward to hearing from you,")
            for name, rx in HARD.items():
                if re.search(rx, s, re.I): hard_hits.append((name, s))
            for name, rx in SOFT.items():
                if re.search(rx, s, re.I): soft_hits.append((name, s))
            if len(s.split()) > 42: soft_hits.append(("long_sentence", s))
        if len(ss) >= 3 and len(ss[-1].split()) <= 8: soft_hits.append(("one_line_closer", ss[-1]))
    # triads by reflex: count ", X, and Y" lists
    triads = [s for s in sents if re.search(r"\b\w+, \w+(\s\w+)?, and \w+", s)]
    if len(triads) >= 3: hard_hits.append(("triads_x%d" % len(triads), " | ".join(t[:50] for t in triads)))
    # repeated openings
    opens = [re.match(r"\W*(\w+)", s).group(1).lower() for s in sents if re.match(r"\W*(\w+)", s)]
    for i in range(len(opens) - 2):
        if opens[i] == opens[i+1] == opens[i+2] and opens[i] not in ("i",):
            hard_hits.append(("repeated_opening", opens[i])); break
    semis = body.count(";")
    if semis > 3: soft_hits.append(("semicolons", str(semis)))
    words = sum(len(s.split()) for s in sents)
    contractions = len(re.findall(r"\b\w+'(m|re|ve|ll|d|s|t)\b", body))
    numbered = sum(1 for s in sents if re.search(r"\d", s))
    print(f"words={words} sentences={len(sents)} avg_len={words/max(1,len(sents)):.1f} "
          f"contractions={contractions} sentences_with_numbers={numbered}/{len(sents)} semicolons={semis}")
    for n, s in hard_hits: print(f"HARD [{n}] {s}")
    for n, s in soft_hits: print(f"soft [{n}] {s}")
    if not hard_hits and not soft_hits: print("clean")
    sys.exit(1 if hard_hits else 0)

if __name__ == "__main__":
    main(sys.argv[1])
