# Columbus Ledger

A neutral, plain-English explainer of City of Columbus finances, built from the city's own public reports.

## Rules that never bend
1. **Every number traces to a public document.** Each dataset in `data/` carries a `source` block (title, publisher, URL, retrieved date). No figure appears on the site without one.
2. **Tie out before publishing.** `python3 scripts/validate.py` must pass. Lines must sum to reported totals within rounding. Unexplained differences go in `known_differences` and show on the site as OPEN, never hidden.
3. **Neutral tone.** Describe what the reports say. No verdicts on whether spending is good or bad, no endorsing or criticizing officials or candidates. Columbus has a mayoral race in 2027; be extra careful around anything that reads as campaign material. Follow `.claude/skills/civic-explainer`.
4. **Say which basis.** Budgetary-basis numbers (budget books, quarterly and year-end reviews) and GAAP numbers (ACFR) differ. Label every dataset with its basis and never mix them in one chart.
5. **Independence.** The owner is a Big 4 audit associate. Don't add content about entities the owner's firm audits, and keep the site personal (not affiliated with any employer). Check before adding a new entity.

## Layout
- `data/<year>/*.json` — extracted, validated datasets (one per source document)
- `scripts/validate.py` — tie-out checks; exits non-zero on failure
- `scripts/build.py` — inlines data into `site/index.html` → `docs/index.html` (GitHub Pages serves this folder)
- `site/` — page templates (plain HTML/CSS/JS, no framework)
- `.claude/skills/` — how Claude extracts reports and writes explainers
- `.claude/commands/` — slash commands for the recurring workflows

## Workflow
`/new-report <url>` → extract to JSON (extract-report skill) → validate → write explainer copy (civic-explainer skill) → build → review diff → publish.
