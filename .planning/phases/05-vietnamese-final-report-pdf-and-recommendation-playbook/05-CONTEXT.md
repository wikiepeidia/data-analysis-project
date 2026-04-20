# Phase 5: Vietnamese Final Report PDF & Recommendation Playbook - Context

**Gathered:** 2026-04-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Turn the completed Phase 1-4 analysis artifacts into a reproducible, teacher-ready Vietnamese report package. This phase must produce a final Vietnamese report source, a recommendation playbook for a new channel, a browser-friendly HTML export path, and a real PDF artifact without introducing LaTeX-heavy tooling. This phase does not reopen upstream analysis logic, invent unsupported category labels, or hide the multilingual text limitations already established in Phase 4.

</domain>

<decisions>
## Implementation Decisions

### Evidence and Scope

- **D-01:** Use the saved Phase 1-4 checkpoints and processed parquet artifacts as the only evidence base for the final report.
- **D-02:** Keep the report framed around association inside the trending corpus rather than causal claims about how any upload becomes trending.
- **D-03:** Keep unresolved category labels as raw `category_id` values unless a verified in-repo mapping source appears during implementation.
- **D-04:** Treat missing video duration as a required limitation section item rather than a late enrichment opportunity.

### Deliverable Structure

- **D-05:** Produce a Vietnamese report source that is easy to diff and rerun, plus a separate recommendation playbook artifact.
- **D-06:** Generate a styled HTML report as the PDF export surface instead of relying on notebook output or manual copy-paste.
- **D-07:** Keep report styling in a separate CSS asset rather than embedding everything directly in one HTML file.
- **D-08:** Include a reproducible command path so the final report package can be rebuilt from the repo root.

### PDF Export Workflow

- **D-09:** Use browser-based headless PDF export rather than a LaTeX-heavy toolchain.
- **D-10:** The current machine has Microsoft Edge available at `/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`, so Phase 5 can generate a real PDF artifact locally.
- **D-11:** Do not depend on Quarto for execution because it is not currently available on `PATH`.
- **D-12:** Keep the export pipeline inside Python plus a browser subprocess so the workflow stays reproducible from the existing environment.

### Narrative Guardrails

- **D-13:** The Vietnamese report must answer the teacher's required question: how a new channel can optimize views using data-backed timing, metadata, category, and text-tone findings.
- **D-14:** Phase 4 findings must stay labeled as metadata tone, not audience emotion or universal semantic sentiment.
- **D-15:** Markets with high `likely_mojibake` shares must be called out explicitly when text findings are summarized.
- **D-16:** The recommendation playbook should emphasize creator-controlled actions and distinguish them from post-trending outcome context.

### the agent's Discretion

- Exact directory names for report outputs, as long as the source, HTML, and PDF artifacts remain easy to discover.
- Exact report section order, as long as methods, findings, recommendations, limitations, and rerun/export steps are all present.
- Exact chart choices and table cuts, as long as they stay grounded in saved artifacts and support the teacher-facing narrative.

</decisions>

<canonical_refs>

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Assignment and scope

- `project.md` - Original assignment brief and teacher-facing questions.
- `.planning/PROJECT.md` - Project scope, Markdown-checkpoint workflow, and report-first constraints.
- `.planning/REQUIREMENTS.md` - Final-delivery requirements `REPT-01` to `REPT-04`.
- `.planning/ROADMAP.md` - Phase 5 goal, success criteria, and completion state for Phases 1-4.
- `.planning/STATE.md` - Current continuity notes and Phase 5 readiness.

### Upstream evidence artifacts

- `checkpoints/01_canonical_dataset.md` - Dataset contract, proxy framing, and missing-duration limitation.
- `checkpoints/02_feature_layer.md` - Timing, metadata, and engagement semantics.
- `checkpoints/03_cross_country_category_analysis.md` - Country-aware timing, metadata, and category findings.
- `checkpoints/04_multilingual_text_tone_analysis.md` - Text-tone findings and multilingual handling limits.

### Runtime/tooling context

- `requirements.txt` - Current declared Python dependencies.
- `copilot-instructions.md` - Repo conventions and report-first workflow guidance.

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- `src/youtube_trends/canonical_dataset.py`, `performance_frame.py`, `feature_layer.py`, `comparative_analysis.py`, and `text_tone_analysis.py` already provide reproducible upstream artifact writers.
- `data/processed/phase3_analysis/*.parquet` and `data/processed/phase4_analysis/*.parquet` already contain the summary surfaces needed for final report tables and charts.
- The current Python environment already has `markdown` and `matplotlib` available.

### Established Patterns

- Each completed phase exposes a `python -m youtube_trends.<module>` entrypoint that regenerates its artifacts.
- Markdown checkpoints are the durable narrative artifacts for methodology and findings.
- Pytest contract tests are used to lock key headings, wording, and rerun instructions.

### Integration Points

- Phase 5 should reuse the completed checkpoints as report inputs rather than re-deriving narrative claims by hand.
- The final report module should fit the existing `src/youtube_trends` package pattern and expose a single rebuild command.
- Planning state, roadmap progress, and requirements tracking must be updated after the report artifacts and verification pass.

</code_context>

<specifics>
## Specific Ideas

The strongest Phase 5 outcome is a lightweight report pipeline that writes:

- one Vietnamese report source
- one recommendation playbook source
- one styled HTML export artifact
- one teacher-ready PDF artifact

That keeps the submission reproducible while staying consistent with the repo's text-first workflow.

</specifics>

<deferred>
## Deferred Ideas

- Human-readable category label mapping remains deferred unless a verified source is added.
- Any further multilingual semantic modeling remains out of scope; Phase 4 limitations are final for this milestone.

</deferred>

---

*Phase: 05-vietnamese-final-report-pdf-and-recommendation-playbook*
*Context gathered: 2026-04-20*
