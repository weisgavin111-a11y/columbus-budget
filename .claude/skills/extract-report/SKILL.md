---
name: extract-report
description: Extract figures from a City of Columbus financial report (year-end or quarterly review, budget book section, ACFR, PAFR) into a validated Columbus Ledger dataset. Use when adding or refreshing anything in data/.
---

# Extracting a city financial report

## Known sources
| Report | Publisher | Basis | Cadence | Where |
|---|---|---|---|---|
| Year-end financial review | Finance and Management | Budgetary | Annually, ~Q1 | columbus.gov Finance document library, "year-end-reviews" |
| Quarterly financial reviews | Finance and Management | Budgetary | Quarterly | document library, "quarterly-financial-reports" |
| Proposed operating budget | Finance and Management | Budgetary | Mid-November | columbus.gov/<year>budget, split into numbered section PDFs |
| City Auditor revenue estimate | City Auditor | Budgetary | Before budget | City Auditor news |
| ACFR | City Auditor | GAAP | Annually, ~April | City Auditor Annual Financial Reports; also ohioauditor.gov AuditSearch |
| PAFR (popular report) | City Auditor | GAAP summary | Annually | City Auditor PAFR Reports |

## Steps
1. Download the PDF and extract text with `pdftotext -layout` (or pdfplumber for tables). Budget books are split into section PDFs; get the one you need instead of the 30 MB full book.
2. Find the summary table, then copy every line item and the reported total exactly as printed, in whole dollars. Don't recalculate totals; record what the city reports.
3. Write `data/<fiscal_year>/<dataset>.json` following the shape of `data/2025/general_fund_actuals.json`: entity, fund, fiscal_year, basis, a source block with URL and retrieved date, line items, reported totals, and `known_differences`.
4. Run `python3 scripts/validate.py`. If a check fails:
   - Re-read the table. Most failures are a skipped or doubled line.
   - If the city's own table doesn't foot, record it in `known_differences`. Don't change the numbers.
5. Note the page or table name for each block so a reviewer can find it fast.

## Agent fan-out
For a multi-year backfill, spawn one subagent per fiscal year, each running these steps for its year and returning only the JSON path and validator output. Review each validator result before merging.
