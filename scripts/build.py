#!/usr/bin/env python3
"""Build the static site: inline the validated data into one HTML page.

Run: python3 scripts/validate.py && python3 scripts/build.py
Output: docs/index.html (served by GitHub Pages) (self-contained; deploy to GitHub Pages or publish as an artifact)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = {
    "y2025": json.loads((ROOT / "data/2025/general_fund_actuals.json").read_text()),
    "y2027": json.loads((ROOT / "data/2027/proposed_budget.json").read_text()),
}
template = (ROOT / "site/index.html").read_text()
html = template.replace("/*__DATA__*/null", json.dumps(data))
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs/index.html").write_text(html)
print(f"Built docs/index.html ({len(html):,} bytes)")
