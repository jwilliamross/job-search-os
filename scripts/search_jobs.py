#!/usr/bin/env python3
"""Scrape postings that match the QUERIES and LOCATIONS below with python-jobspy.

Usage:
    python3 scripts/search_jobs.py                 # default queries and cities
    python3 scripts/search_jobs.py --hours 168     # only postings from the last week
    python3 scripts/search_jobs.py --out scratch/jobs.csv

Writes a CSV (default scratch/jobs-<date>.csv) and prints a short summary. Review the CSV
by hand; scraped titles are noisy. The job-search skill then writes the shortlist.
"""
import argparse
import datetime as dt
import os
import sys

try:
    from jobspy import scrape_jobs
    import pandas as pd
except ImportError:
    sys.exit("pip install python-jobspy pandas")

QUERIES = [
    "investment banking summer analyst 2027",
    "investment banking intern",
    "private equity intern",
    "private equity analyst student",
    "energy trading intern",
    "commodity trading summer student",
    "corporate development intern",
    "finance summer student",
    "consulting summer analyst 2027",
    "business analyst intern",
    "treasury intern",
    "investor relations intern",
]
LOCATIONS = ["Toronto, ON", "Vancouver, BC", "Canada"]  # edit me
SITES = ["linkedin", "indeed", "glassdoor"]
TITLE_KEYWORDS = [
    "intern", "student", "analyst", "co-op", "coop", "summer", "trainee",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24 * 30, help="max posting age in hours")
    ap.add_argument("--results", type=int, default=25, help="results per query per site")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    frames = []
    for loc in LOCATIONS:
        for q in QUERIES:
            try:
                df = scrape_jobs(
                    site_name=SITES,
                    search_term=q,
                    location=loc,
                    results_wanted=args.results,
                    hours_old=args.hours,
                    country_indeed="Canada",
                )
                df["query"] = q
                df["query_location"] = loc
                frames.append(df)
                print(f"{loc:14s} | {q:45s} | {len(df):3d}")
            except Exception as e:  # scraping is flaky; keep going
                print(f"{loc:14s} | {q:45s} | error: {e}")
    if not frames:
        sys.exit("no results")
    all_jobs = pd.concat(frames, ignore_index=True)
    all_jobs = all_jobs.drop_duplicates(subset=["job_url"])
    mask = all_jobs["title"].str.lower().str.contains("|".join(TITLE_KEYWORDS), na=False)
    all_jobs = all_jobs[mask]
    cols = [c for c in ["title", "company", "location", "date_posted", "job_type",
                        "site", "job_url", "query", "query_location"] if c in all_jobs]
    out = args.out or f"scratch/jobs-{dt.date.today()}.csv"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    all_jobs[cols].sort_values("date_posted", ascending=False).to_csv(out, index=False)
    print(f"\n{len(all_jobs)} postings written to {out}")


if __name__ == "__main__":
    main()
