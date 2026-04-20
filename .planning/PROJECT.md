# YouTube Trending Content Analysis

## What This Is

This is a report-first data analysis project for an academic assignment built around the Trending YouTube Video Statistics dataset. The project analyzes multi-country trending video data to identify what helps videos trend, compare performance across content categories, and recommend practical actions for a new channel trying to optimize views. Markdown checkpoints support exploration, verification, and low-token AI review, while the final submission target is a proper Vietnamese PDF for the teacher.

## Core Value

Produce a defensible, evidence-based analysis that answers the teacher's required questions with clear findings, visuals, and actionable recommendations.

## Requirements

### Validated

- [x] Clean and standardize the multi-country YouTube trending datasets into an analysis-ready form.
- [x] Identify timing, title/tag, content-category, and bounded metadata-tone patterns associated with trending performance.
- [x] Deliver a teacher-ready Vietnamese PDF, backed by reproducible Markdown checkpoints and evidence-based recommendations for a new channel.

### Active

- [ ] None inside this milestone - the v1 deliverable set is complete.

### Out of Scope

- Interactive web app or frontend dashboard — the assignment is report-first and does not require a product UI.
- Slide deck production — presentation materials are secondary to the final Vietnamese PDF report.

## Context

- The assignment brief offers five project themes; this project is the YouTube content-trend analysis option.
- The dataset scope is all available country CSV files in the repository, not a single-market subset.
- The deliverable should be a proper Vietnamese PDF for the teacher, with Markdown checkpoints kept as supporting artifacts rather than the final artifact.
- The analysis must answer the teacher's required questions, especially how a new channel can optimize views using data-backed posting windows, tags, and content insights.
- Text-tone analysis should stay grounded in the assignment's core questions and respect corpus quality limits instead of forcing one semantic sentiment model across corrupted multilingual text.

## Constraints

- **Deliverable**: Teacher-ready Vietnamese PDF first — the repository should optimize for an academic report artifact, not an application.
- **Formatting path**: Prefer a Markdown-friendly or Quarto-style report workflow and avoid a LaTeX-heavy export path unless there is no simpler option.
- **Dataset**: Use all country files in the provided YouTube dataset — cross-market coverage is part of the chosen scope.
- **Assignment**: Must answer the brief's required questions — findings and recommendations are not optional.
- **Method**: Use the strongest NLP approach the saved text quality can support, but prefer bounded structural metadata tone over invalid semantic sentiment claims when the corpus is corrupted.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Analyze the YouTube project option | This is the selected assignment theme from the provided brief | Scope locked at initialization |
| Use all country datasets | Broader coverage supports stronger comparisons and more defensible recommendations | All 10 country datasets retained through Phases 1-4 |
| Deliver a Vietnamese PDF report from a Markdown-friendly workflow | The user wants a proper teacher submission and wants to avoid LaTeX-heavy friction where possible | Markdown or Quarto source; Markdown checkpoints are the only checkpoint artifact |
| Use bounded multilingual text tone instead of universal semantic sentiment | The saved corpus has heavy mojibake in several markets, so structural metadata tone is more defensible than pretending semantic sentiment is reliable everywhere | Phase 4 uses Unicode-aware structural tone plus explicit readable-text and corruption limits |
| Export the final PDF through Edge headless from generated HTML | The machine already has Edge installed, and browser export avoids LaTeX-heavy setup while still producing a real PDF artifact | Phase 5 writes Markdown, HTML, PDF, and playbook artifacts reproducibly |

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
*Last updated: 2026-04-20 after Phase 5 completion*
