# CLAUDE.md — Thesis Assembly Instructions

## Project

PhD thesis for Lukas Herron, UMD Biophysics (Tiwary Lab). The thesis adapts 5 published/submitted papers into chapters, with original intro and outlook chapters bookending them.

## Thesis Structure

```
Ch 1: Intro — Generative Modeling in the Biomolecular Sciences (written from scratch)
Ch 2: Diffusion Models — review paper for theoretical chemistry audience
Ch 3: DDPM-REMD — diffusion models for post-processing REMD simulations (Yihang Wang, PNAS)
Ch 4: Thermodynamic Maps — physics-inspired inductive biases in diffusion models (Lukas, PNAS)
Ch 5: DiffDock-Glide — chemistry-inspired inductive biases in DiffDock (w/ Schrödinger, preprint)
Ch 6: RNAnneal — ab initio RNA 3D structure prediction, preprint
Ch 7: Outlook — SPIB integration, expTM, LaTF
```

## Directory Layout

```
thesis/
├── CLAUDE.md              # this file
├── thesis.tex             # root document (create if missing)
├── preamble.tex           # shared macros/packages (generate during preprocessing)
├── src/                   # thesis chapter .tex files (output target)
├── papers/                # raw paper sources (read-only after setup)
├── figures/               # consolidated figures, renamed by chapter
├── bib/                   # merged bibliography
└── archives/              # original .zip/.tar.gz files dropped here
```

## Phase 1: Unpack and Organize

### Step 1 — Unzip archives

Look in `archives/` for compressed files. Unzip each into the correct `papers/` subdirectory based on filename or contents. Use best judgment to match archives to these paper directories:

- `papers/diffusion-review/`
- `papers/ddpm-remd/`
- `papers/thermodynamic-maps/`
- `papers/diffdock-glide/`
- `papers/rnaanneal/`

If the mapping is ambiguous, check the `.tex` files inside for title/author clues. Ask if still unclear.

```bash
mkdir -p papers/{diffdock-glide,rnaanneal,...}
mkdir -p figures bib src archives
```

### Step 2 — Figure extraction

For each `papers/<name>/` directory:

1. Find all image files: `.pdf`, `.png`, `.eps`, `.svg`, `.jpg`, `.tif`
2. Copy (not move) them into `figures/` with chapter-prefixed names:
   - `papers/diffusion-review/fig1.pdf` → `figures/ch2_fig1.pdf`
   - `papers/ddpm-remd/figure_2a.png` → `figures/ch3_figure_2a.png`
   - Prefix mapping: diffusion-review=ch2, ddpm-remd=ch3, thermodynamic-maps=ch4, diffdock-glide=ch5, rnaanneal=ch6
3. Check for figures in subdirectories (e.g., `figs/`, `figures/`, `images/`, `SI/`)
4. Generate `figures/MANIFEST.md` — a table mapping original path → new path for every figure

### Step 3 — Create directories if missing

Ensure `src/`, `bib/`, `figures/` all exist.

---

## Phase 2: Preprocessing

### Step 4 — Expand and flatten LaTeX

For each paper, produce a self-contained expanded file:

```bash
cd papers/<name>/
# if latexpand is available:
latexpand --expand-bbl main.tex > expanded.tex
# fallback: manually inline \input{} and \include{} files
```

Find the correct root `.tex` file (the one with `\documentclass`). It may not be called `main.tex`.

### Step 5 — Extract body content

From each `expanded.tex`, extract everything between `\begin{document}` and `\end{document}`. Strip:

- `\maketitle`
- `\author{}`, `\affiliation{}`, `\date{}`, `\title{}` commands
- `\begin{abstract}...\end{abstract}` — save this separately as `papers/<name>/abstract.txt`
- Acknowledgments sections
- Journal-specific commands (e.g., `\journalname`, `\received`, `\revised`)
- Any `\bibliography{}` or `\printbibliography` call (bib will be handled globally)

Save the cleaned body to `src/ch<N>_<name>.tex` (e.g., `src/ch4_thermodynamic_maps.tex`).

### Step 6 — Macro inventory

Scan all papers for:

- `\newcommand` / `\renewcommand`
- `\DeclareMathOperator`
- `\def`
- `\newenvironment`

Collect into `preamble.tex`. Deduplicate. If two papers define the same macro differently, flag it with a comment:

```latex
% CONFLICT: defined differently in ddpm-remd and thermodynamic-maps
% ddpm-remd version:
% \newcommand{\vb}[1]{\mathbf{#1}}
% thermodynamic-maps version:
% \newcommand{\vb}[1]{\boldsymbol{#1}}
\newcommand{\vb}[1]{\mathbf{#1}}  % RESOLVE: picked ddpm-remd, verify
```

### Step 7 — Bibliography merge

```bash
# if bibtool is available:
bibtool -s -d papers/*/*.bib -o bib/thesis.bib
# fallback: concatenate and manually flag duplicates
cat papers/*/*.bib > bib/thesis_raw.bib
```

Then scan for likely duplicates: entries with matching DOIs, or titles with >80% overlap but different cite keys. Write findings to `bib/DUPLICATES.md`.

### Step 8 — Update figure paths in chapter files

In each `src/ch<N>_*.tex`, replace original figure paths with the new `figures/ch<N>_*` paths using the manifest from Step 2.

### Step 9 — Compilation test

Create a minimal `thesis.tex` root document if one doesn't exist:

```latex
\documentclass[12pt]{report}
\input{preamble}
\begin{document}
\include{src/ch2_diffusion_review}
\include{src/ch3_ddpm_remd}
\include{src/ch4_thermodynamic_maps}
\include{src/ch5_diffdock_glide}
\include{src/ch6_rnaanneal}
\bibliographystyle{unsrt}
\bibliography{bib/thesis}
\end{document}
```

Try to compile with `pdflatex thesis.tex` (or `latexmk -pdf thesis.tex`). Collect errors. Fix missing packages, undefined macros, broken figure refs. Iterate until it compiles without errors. Warnings are fine at this stage.

---

## General Rules

- **Never modify files in `papers/`.** That directory is the read-only source of truth.
- **Commit after each step.** Use messages like `phase1-step2: extract figures with chapter prefixes`.
- **If something is ambiguous, ask.** Don't guess at which paper maps to which chapter or how to resolve a macro conflict.
- **Preserve all content.** At this stage we are organizing and flattening, not rewriting. Editorial adaptation happens later.
- **Log everything.** If a step produces warnings or requires judgment calls, append notes to a `PROCESSING_LOG.md` at the repo root.
