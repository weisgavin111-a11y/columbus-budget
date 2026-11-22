# Columbus Ledger

Plain-English explainers and charts of City of Columbus finances, built from the city's own public reports and tied out like an audit schedule.

## Quick start
```bash
python3 scripts/validate.py   # tie out every dataset
python3 scripts/build.py      # writes dist/index.html
```
Open `dist/index.html` in a browser. Deploy `dist/` to GitHub Pages.

## How Claude runs this project

| Piece | Claude capability | What it does |
|---|---|---|
| Building the site and scripts | Claude Code | Writes and maintains everything in this repo. `CLAUDE.md` holds the standing rules. |
| `extract-report` skill | Skills | Turns a city PDF into a validated JSON dataset |
| `civic-explainer` skill | Skills | Keeps all copy neutral, plain-English, and sourced |
| `/new-report`, `/check-sources` | Slash commands | One-line entry points for the recurring workflows |
| Multi-year backfill | Subagents | One agent per fiscal year extracts in parallel; you review each tie-out |
| Source watcher | Scheduled task | Monthly: checks columbus.gov for new quarterly reviews, budget sections, ACFR/PAFR and drafts the update for review |
| Budget-season mode | Scheduled task | Mid-Nov to Feb: weekly check for council amendments while the budget is debated |
| Packaging | Plugin | Bundles the skills and commands so the same pipeline can be pointed at another Ohio city or school district |
| Monthly source check | Scheduled task | Prompt and schedule in `automation/monthly-source-check.md` |
| Reader dashboards | Artifacts | Shareable previews of new pages before they go live |

## Roadmap
1. **Done:** 2025 general fund results page.
2. **Done:** 2027 proposed budget page (2025 actual vs 2026 projected vs 2027 proposed, 10-year forecast, rainy-day fund). Next: track council amendments through adoption.
3. **Ten-year trends:** backfill year-end reviews 2016–2025 with subagents. Income tax growth, public safety share, reserves over time.
4. **Quarterly pulse:** each quarterly review becomes a "how is this year tracking?" page.
5. **ACFR deep dives (GAAP):** pensions, debt, the AAA rating, plainly explained.
6. **Expand:** Columbus City Schools, Franklin County, then other Ohio cities via the plugin.

## Open items
- 2025 figures differ between the 2027 budget book and the FY25 year-end review (beginning cash by $300,000, cancelled orders by $106,687).
- 2025 ending balance: $3,385 difference between resources minus spending and the reported balance (see `data/2025/general_fund_actuals.json`). Trace it in the year-end review's detail tables.
