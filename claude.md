# CLAUDE.md — Thesis Editing

PhD dissertation for Lukas Herron, Biophysics, University of Maryland College Park (Tiwary Lab). Adapts 5 published papers into chapters with new intro and outlook chapters. Compiled LaTeX source exists (127 pages, 260 merged refs). The job is structural editing, not rewriting.

## Chapter Map

| Final Ch | Title | Source |
|----------|-------|--------|
| 1 | Generative Modeling in the Biomolecular Sciences | New (placeholder) |
| 2 | A Comparison of Probabilistic Generative Frameworks for Molecular Simulations | Current Ch 1 |
| 3 | From Data to Noise to Data: Mixing Physics Across Temperatures with Generative AI | Current Ch 2 |
| 4 | Inferring Phase Transitions and Critical Exponents from Limited Observations with Thermodynamic Maps | Current Ch 3 |
| 5 | DiffDock-Glide: A Hybrid Physics-Based and Data-Driven Approach to Molecular Docking | Current Ch 4 |
| 6 | Ab Initio Prediction of RNA Structure Ensembles with RNAnneal | Current Ch 5 |
| 7 | Outlook | New (placeholder) |

## Before Working on Anything

- **Before working on a chapter**, read `docs/CHN_FIXES.md` for that chapter.
- **Before doing any formatting work**, read `docs/UMD_FORMAT.md` for UMD ETD requirements.

## Global Rules

### Source Control
- Commit before and after every logical unit of work. Descriptive messages.
- Never make uncommitted bulk changes. If a find-and-replace touches multiple chapters, commit chapter by chapter.
- Compile after every commit. Fix compilation errors before moving on.

### Editing
- **Preserve all content.** No deletions unless explicitly flagged in a fix list.
- **Do not change technical content.** No rephrasing scientific claims, altering equations, or modifying figure captions beyond formatting.
- **Leave "we" language as-is.** Co-authored papers.
- **When ambiguous, leave a `% TODO:` comment and move on.** Do not guess.

### Compilation
```bash
latexmk -pdf thesis.tex
# or: pdflatex thesis.tex && bibtex thesis && pdflatex thesis.tex && pdflatex thesis.tex
```
After build, verify:
```bash
pdftotext thesis.pdf - | grep '??' | head -20
pdftotext thesis.pdf - | grep 'author?' | head -5
grep -i 'undefined\|rerun' thesis.log | head -20
```

### Figures (global)
- Place every figure inline, immediately after the paragraph that first references it. `[htbp]` float specifier.
- Remove any `\clearpage` or `\FloatBarrier` that forces figures to the chapter end.
- Sizing defaults: single-panel `0.65\textwidth`, two-panel stacked `0.7\textwidth`, two-panel side-by-side `0.85\textwidth`, three+ panels `\textwidth`.

### Section Hierarchy (global)
- Numbered: `\section{}`, `\subsection{}`
- Unnumbered: Data/Code Availability, Acknowledgements → `\section*{}`
- Chapter appendices: `\begin{subappendices}...\end{subappendices}` (requires `\usepackage[title]{appendix}`)

### SI Handling (global)
- No "Supplementary Information" in a dissertation. Fold SI inline or into chapter appendices.
- Rewrite all references to "Supplementary", "SI Appendix", "Fig. S*", "Table S*".

### Journal Boilerplate (global)
- Remove: `\maketitle`, author blocks, affiliations, "Correspondence:", journal-specific commands.
- Each adapted chapter gets a footnote: `\chapter{Title}\footnote{Adapted from: [citation].}`

## Execution Order

1. Preamble and front matter stubs
2. Chapter renumbering
3. Section hierarchy fixes (per chapter)
4. Broken references (Ch 2 `(author?)`, Ch 6 32×`??`)
5. SI integration (Ch 3, Ch 4, Ch 6)
6. Figure placement and sizing
7. Journal boilerplate cleanup
8. Full compilation and verification
9. Placeholder chapters (Ch 1, Ch 7)
10. UMD format compliance check
