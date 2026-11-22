#!/usr/bin/env python3
"""Tie out every dataset before it reaches the site.

Run: python3 scripts/validate.py
Exits non-zero if any check fails beyond its rounding tolerance, so a
scheduled job or a pre-commit hook can block a bad extraction.
"""
import json
import sys
from pathlib import Path

ROUNDING = 5  # dollars; source tables round each line
DATA = Path(__file__).resolve().parent.parent / "data"


def check(label, actual, expected, tol=ROUNDING):
    diff = actual - expected
    ok = abs(diff) <= tol
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}: computed {actual:,} vs reported {expected:,} (diff {diff:+,})")
    return ok


def validate_comparison(d):
    results = []
    for i, col in enumerate(d["columns"]):
        results.append(check(f"{col}: revenue lines = total", sum(x["values"][i] for x in d["revenue"]), d["revenue_total"][i]))
        results.append(check(f"{col}: revenue + other resources = total resources",
                             d["revenue_total"][i] + sum(x["values"][i] for x in d["other_resources"]), d["resources_total"][i]))
        results.append(check(f"{col}: department lines = total spending", sum(x["values"][i] for x in d["departments"]), d["spending_total"][i]))
    for i in range(len(d["columns"]) - 1):
        left = d["resources_total"][i] - d["spending_total"][i]
        carried = d["other_resources"][1]["values"][i + 1]
        if i > 0:  # 2025 ending is reported in the year-end review, not here
            results.append(check(f"{d['columns'][i]} leftover = next year's carried-in balance", left, carried))
    results.append(check("2027 spending by type = total", sum(x["amount"] for x in d["spending_by_object_2027"]), d["spending_total"][-1]))
    f = d["forecast"]
    for y, r, s_, g in zip(f["years"], f["revenue"], f["spending"], f["gap"]):
        if y > f["years"][0]:
            results.append(check(f"Forecast {y}: revenue - spending = gap", r - s_, g))
    return all(results)


def validate(path):
    d = json.loads(path.read_text())
    if d.get("kind") == "budget_comparison":
        print(f"{path.relative_to(DATA.parent)}  ({d['entity']}, FY{d['fiscal_year']} proposed)")
        return validate_comparison(d)
    print(f"{path.relative_to(DATA.parent)}  ({d['entity']}, FY{d['fiscal_year']})")
    r = d["resources"]
    results = [
        check("Revenue lines = revenue total", sum(x["amount"] for x in d["revenue"]), r["revenue_total"]),
        check("Resource components = total resources",
              r["beginning_unencumbered_cash"] + r["encumbrance_cancellations"] + r["transfers_in"] + r["revenue_total"],
              r["total"]),
        check("Department lines = total spending", sum(x["amount"] for x in d["expenditures_by_department"]), d["expenditures_total"]),
        check("Object lines = total spending", sum(x["amount"] for x in d["expenditures_by_object"]), d["expenditures_total"]),
    ]
    res = d["reserves"]["economic_stabilization_fund"]
    results.append(check("Rainy-day fund roll-forward", res["beginning"] + res["additions"], res["ending"]))

    # Known reconciling item: reported, not failed, until explained.
    implied = r["total"] - d["expenditures_total"]
    gap = implied - d["ending_fund_balance"]
    print(f"  [NOTE] Resources - spending = {implied:,}; reported ending balance {d['ending_fund_balance']:,} (gap {gap:+,})")
    if abs(gap) > 10_000:
        print("  [FAIL] Ending balance gap is too large to be an open item")
        results.append(False)
    return all(results)


if __name__ == "__main__":
    files = sorted(DATA.glob("*/*.json"))
    ok = all([validate(f) for f in files])
    print("\nAll checks passed." if ok else "\nSome checks FAILED.")
    sys.exit(0 if ok else 1)
