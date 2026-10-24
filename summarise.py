# SPDX-License-Identifier: Apache-2.0
"""Recompute every figure in README.md from register.csv, reports.csv and second_annotator.csv.

Standard library only. Run from this folder:  python summarise.py
"""
import collections
import csv
import hashlib
import json
import sys


def read(name):
    with open(name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def table(title, rows, key, order=None):
    counts = collections.Counter(r[key] for r in rows)
    print(f"\n{title} (n = {len(rows)})")
    for value in order or sorted(counts, key=lambda v: (-counts[v], v)):
        print(f"  {value:<16} {counts.get(value, 0):>4}")


def withheld_sha256(row_id, what_was_checked, problem, evidence_quote, note):
    """The recipe used for the withheld_sha256 column, for checking released text later."""
    data = {"row_id": row_id, "what_was_checked": what_was_checked, "problem": problem,
            "evidence_quote": evidence_quote, "note": note}
    text = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    rows = read("register.csv")
    reports = read("reports.csv")
    second = read("second_annotator.csv")
    counted = [r for r in rows if r["counted"] == "yes"]
    serious = [r for r in counted if r["severity"] == "HIGH"]

    print(f"review reports:            {len({r['report_id'] for r in rows})}")
    print(f"rows in the register:      {len(rows)}")
    print(f"distinct problems counted: {len(counted)}")
    print(f"serious problems (HIGH):   {len(serious)}")
    print(f"dates of the reviews:      {min(r['date'] for r in rows)} to {max(r['date'] for r in rows)}")

    table("Rows not counted, by reason", [r for r in rows if r["counted"] != "yes"], "counted")
    table("Serious problems by stage", serious, "stage", ["PRE_FREEZE", "PRE_PUBLISH", "POST_PUBLISH"])
    table("Serious problems by category", serious, "category")
    table("Serious problems by kind of work", serious, "work_type", ["research", "text"])
    table("Outcome of the serious problems", serious, "outcome", ["FIXED", "REJECTED", "UNCLEAR"])
    table("All counted problems by severity", counted, "severity", ["HIGH", "MED", "LOW"])
    table("All counted problems by outcome", counted, "outcome", ["FIXED", "REJECTED", "UNCLEAR"])
    table("All counted problems by reviewer", counted, "reviewer")
    post = sorted({r["report_id"] for r in serious if r["stage"] == "POST_PUBLISH"})
    print(f"\nreports with serious problems found after publication: {post}")

    withheld = [r for r in rows if r["text_withheld"]]
    table("Rows whose text is withheld, by reason", withheld, "text_withheld")
    print(f"  serious rows among them: {sum(r in serious for r in withheld)}")
    public = [r for r in reports if r["public_copy"]]
    print(f"\nreports with a public copy: {len(public)} of {len(reports)}, "
          f"covering {sum(int(r['rows']) for r in public)} of {len(rows)} rows")

    print(f"\nsecond annotator: {len(second)} rows "
          f"({sum(s['sample'].startswith('all serious') for s in second)} serious, "
          f"{sum(s['sample'].startswith('random') for s in second)} random others)")
    for key in ("quote_confirmed", "error_of_the_work", "severity_agreed", "category_agreed"):
        print(f"  {key:<20} yes in {sum(s[key] == 'yes' for s in second)} of {len(second)}")
    high = [s for s in second if s["serious_outcome_confirmed"]]
    print(f"  serious_outcome_confirmed yes in {sum(s['serious_outcome_confirmed'] == 'yes' for s in high)} "
          f"of {len(high)}")
    print("  changes adopted:", {s["row_id"]: s["change_adopted"] for s in second if s["change_adopted"]})
    return 0


if __name__ == "__main__":
    sys.exit(main())
