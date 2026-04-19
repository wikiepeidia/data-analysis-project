# YouTube Trending Content Analysis

## What This Is

This is a report-first data analysis project for an academic assignment built around the Trending YouTube Video Statistics dataset. The project analyzes multi-country trending video data to identify what helps videos trend, compare performance across content categories, and recommend practical actions for a new channel trying to optimize views. Checkpoint notebooks support exploration and verification, but the final submission target is a proper Vietnamese PDF for the teacher.

## Core Value

Produce a defensible, evidence-based analysis that answers the teacher's required questions with clear findings, visuals, and actionable recommendations.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Clean and standardize the multi-country YouTube trending datasets into an analysis-ready form.
- [ ] Identify timing, title/tag, and content-category factors associated with trending performance.
- [ ] Deliver a teacher-ready Vietnamese PDF, backed by reproducible checkpoint notebooks and evidence-based recommendations for a new channel.

### Out of Scope

- Interactive web app or frontend dashboard — the assignment is report-first and does not require a product UI.
- Slide deck production — presentation materials are secondary to the final Vietnamese PDF report.

## Context

- The assignment brief offers five project themes; this project is the YouTube content-trend analysis option.
- The dataset scope is all available country CSV files in the repository, not a single-market subset.
- The deliverable should be a proper Vietnamese PDF for the teacher, with notebooks kept as checkpoints rather than the final artifact.
- The analysis must answer the teacher's required questions, especially how a new channel can optimize views using data-backed posting windows, tags, and content insights.
- Sentiment analysis should use a stronger NLP approach if the available text fields and data quality allow it, while still keeping the project grounded in the assignment's core questions.

## Constraints

- **Deliverable**: Teacher-ready Vietnamese PDF first — the repository should optimize for an academic report artifact, not an application.
- **Formatting path**: Prefer a Markdown-friendly or Quarto-style report workflow and avoid a LaTeX-heavy export path unless there is no simpler option.
- **Dataset**: Use all country files in the provided YouTube dataset — cross-market coverage is part of the chosen scope.
- **Assignment**: Must answer the brief's required questions — findings and recommendations are not optional.
- **Method**: Stronger NLP is preferred for sentiment analysis — but it must remain feasible within the dataset's available text and the assignment timeline.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Analyze the YouTube project option | This is the selected assignment theme from the provided brief | — Pending |
| Use all country datasets | Broader coverage supports stronger comparisons and more defensible recommendations | — Pending |
| Deliver a Vietnamese PDF report from a Markdown-friendly workflow | The user wants a proper teacher submission and wants to avoid LaTeX-heavy friction where possible | Markdown or Quarto source; notebooks are checkpoints only |
| Aim for stronger NLP sentiment analysis | The brief includes sentiment analysis and the user wants a more ambitious treatment where feasible | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check -> still the right priority?
3. Audit Out of Scope -> reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-19 after initialization*