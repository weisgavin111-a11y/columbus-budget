---
description: Add a new city financial report to Columbus Ledger, from PDF to published page
argument-hint: <report URL>
---

Add the report at $ARGUMENTS to Columbus Ledger.

1. Use the extract-report skill to turn it into a dataset under data/.
2. Run `python3 scripts/validate.py` and show me the output. Stop if anything FAILs that isn't recorded in known_differences.
3. Draft or update the page sections using the civic-explainer skill. Show me the new copy before editing the site.
4. Run `python3 scripts/build.py` and summarize what changed on the page.
