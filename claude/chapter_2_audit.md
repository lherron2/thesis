CH2_FIXES.md — Task Brief for Claude Code
Current Chapter 1 → Thesis Chapter 2: "A Comparison of Probabilistic Generative Frameworks for Molecular Simulations"
This document describes all fixes needed for what is currently Chapter 1 in the compiled thesis (pages 3–18 of the PDF). In the final thesis numbering this becomes Chapter 2. The LaTeX source file for this chapter should be identified by searching for \chapter or \section{Introduction} containing text about "generative artificial intelligence" and "Neural Spline Flows" and "Conditional Flow Matching" and "DDPM".
Work on the actual .tex source files, not the PDF. Compile after each major fix to verify.

1. Chapter Renumbering
This chapter is currently numbered Chapter 1. It must become Chapter 2 in the final thesis. Chapter 1 will be a new introductory chapter written later.
Action: Renumber the \chapter command and all internal \label / \ref keys from ch1 or 1 to ch2 or 2. Update all cross-references throughout the thesis that point to this chapter. If the thesis uses \chapter{} with automatic numbering, this may just require reordering the \include statements in the root thesis.tex.

2. Section Hierarchy Cleanup
The current section structure is:
1.1  Introduction
1.2  Theoretical background
1.3  Probabilistic Generative Frameworks
  1.3.1  Normalizable Architectures
  1.3.2  Neural Ordinary Differential Equations
  1.3.3  Diffusion Models
  1.3.4  Schrödinger Bridges
1.4  Experiments
  1.4.1  Gaussian Mixture
  1.4.2  Aib9 Dihedral Torsion Angles
1.5  Conclusion
1.6  Data and Code Availability
1.7  Acknowledgements
1.8  Appendix
  1.8.1  Architectural Details
  1.8.2  Data Details
Issues to fix:
a) Unnumbered subsection headers within 1.4 Experiments.
In the rendered PDF (page 9), there are two bold subsection-style headers — "Gaussian Mixture Experiments" and "Aib₉ Experiments" — that appear above the numbered subsections 1.4.1 and 1.4.2. These are likely \paragraph{} or \textbf{} rather than \subsection{}. They create a confusing doubled structure: the unnumbered header says "Gaussian Mixture Experiments" and then immediately below it, \subsection{Gaussian Mixture} appears.
Action: Remove the unnumbered "Gaussian Mixture Experiments" and "Aib₉ Experiments" headers entirely. The numbered subsections 1.4.1 and 1.4.2 already serve this purpose. If the unnumbered headers contain text not in the numbered subsections, fold that text into the numbered subsection body.
b) Sections 1.6 (Data and Code Availability) and 1.7 (Acknowledgements) should not be numbered \sections.
In a thesis chapter, these are typically unnumbered.
Action: Change \section{Data and Code Availability} to \section*{Data and Code Availability} (or move to end matter). Same for Acknowledgements. Alternatively, if the thesis template has a standard way to handle per-chapter acknowledgements, use that.
c) Section 1.8 Appendix should become a proper chapter appendix.
The "Appendix" section (1.8) with subsections for Architectural Details and Data Details is currently formatted as a regular section. In a thesis, this should use the chapter appendix mechanism.
Action: Replace \section{Appendix} with the appropriate LaTeX appendix command for within-chapter appendices. Common approaches:
latex\appendix  % or use a chapter-level appendix environment
\section{Architectural Details}  % becomes A.1 or 2.A.1
\section{Data Details}           % becomes A.2 or 2.A.2
Check what the thesis \documentclass supports. If using report or book class, \appendix switches all subsequent \section commands to lettered numbering. If the appendix should be scoped to just this chapter, consider using the appendix package with \begin{subappendices}...\end{subappendices}.

3. Broken Reference: (author?)
Location: Section 1.3.4 (Schrödinger Bridges), visible on PDF page 9.
The rendered text reads:

"p(x) and q(x') that minimizes the KL divergence to a reference path distribution. (author?)"

This is a broken \cite{} command — the bibliography key is not resolving.
Action: Search the .tex source for the \cite command in the Schrödinger Bridges section near the sentence about KL divergence and reference path distributions. The citation likely refers to Vargas et al. (2021) "Solving Schrödinger Bridges via Maximum Likelihood" or De Bortoli et al. (2021) "Diffusion Schrödinger Bridge". Identify the correct bib key from thesis.bib and fix the \cite{}. If the bib entry is missing, add it.

4. Supplementary / Appendix References
Chapter 1 has internal references to its own appendix that use the pattern Section 1.8.2:Appendix. These appear in:

The Experiments section (around "see Section 1.8.2:Appendix for details of the molecular dynamics data generation procedure and Aib₉ simulation details")
The Aib₉ subsection (around "as a function of simulation time (see Section 1.8.2:Appendix for details...")

Action: These references should work correctly once the appendix is properly structured. Verify that \ref{} labels point to the right targets after the appendix restructuring in Step 2c. The rendered text should read something clean like "see Appendix 2.A" or "see Section 2.8.2" — not "Section 1.8.2:Appendix" with a colon in it.
Search the source for the literal string :Appendix — this may be a hardcoded string rather than a proper \ref{}, which would explain the odd formatting.

5. Figure Placement and Sizing
All six figures (1.1 through 1.6) are currently banished to the end of the chapter (PDF pages 16–19), after the appendix. This is the journal preprint style (figures at the end). For a thesis, figures should appear inline near where they are first referenced.
Specific figure issues:
a) Figure 1.3 (Free energy difference estimation, PDF page 17):
The plot is small and centered on a mostly empty page — roughly 40% of the page width with large whitespace above and below. The figure should be sized to \textwidth or at least 0.7\textwidth.
Action: Find \includegraphics for Figure 1.3 and set width to 0.6\textwidth or 0.65\textwidth. The plot is a single-panel scatter plot that reads fine at moderate size.
b) Figure 1.4 (Speed and model size, PDF page 18):
Two-panel figure (a, b) stacked vertically. Currently undersized — panels are roughly 50% of text width. Should use more of the available width.
Action: Set width to 0.7\textwidth for the stacked layout, or consider 0.9\textwidth if panels are side-by-side.
c) Figure 1.5 (Aib₉ results, PDF page 19):
Six-panel figure (a–f) with a complex 2×3 grid layout. This is the most information-dense figure. Currently occupies roughly the top half of the page — sizing seems acceptable but verify it's readable at print resolution.
Action: Set width to \textwidth. This figure needs the full page width given 6 panels.
d) Figure 1.6 (Hyperparameter tuning, PDF page 19):
Three-panel figure (a–c) in a row. Currently on the same page as Figure 1.5 — cramped.
Action: Set width to \textwidth. Consider forcing a page break before this figure if it collides with Figure 1.5.
e) Figures 1.1 and 1.2 (PDF page 16):
These share a page. Figure 1.1 is a two-panel stacked figure that takes the top 60% of the page. Figure 1.2 is below it. Sizing looks reasonable but both could be slightly larger.
Action: Set Figure 1.1 to 0.7\textwidth and Figure 1.2 to 0.6\textwidth.
Global figure action:
Move all figures inline. Remove any \clearpage or float barriers that force figures to the chapter end. Set float placement to [htbp] for each figure environment. Place each \begin{figure} block immediately after the paragraph that first references it in the text. The ordering should be:

Figure 1.1 → after first reference in Section 1.4.1 (Gaussian Mixture)
Figure 1.2 → after its first reference in Section 1.4.1
Figure 1.3 → after its first reference in Section 1.4.1 (free energy difference results)
Figure 1.4 → after its first reference in Section 1.4.1 (speed/capacity results)
Figure 1.5 → after first reference in Section 1.4.2 (Aib₉)
Figure 1.6 → in Section 1.8.1 (Architectural Details / Appendix) where hyperparameter tuning is discussed


6. Table Check
Table 1.1 (Aib₉ MD parameters) is on PDF page 15, inside Section 1.8.2 (Data Details). This placement is correct — it belongs in the appendix. Verify it has [htbp] float placement and a proper \label.

7. Journal Boilerplate to Remove or Adapt
a) "We" language: Thesis chapters adapted from multi-author papers sometimes need pronoun adjustment. Check with the advisor (Pratyush). If first-person plural is acceptable, leave it. If the committee prefers first-person singular for the candidate's thesis, change "we" → "I" throughout, but only where the candidate is the primary contributor. For a co-authored paper, "we" is often acceptable.
b) Data and Code Availability section (1.6): This is a journal requirement. In a thesis it can be shortened or moved to an unnumbered section at the chapter end. The GitHub links should be preserved.
c) Acknowledgements section (1.7): Keep but make unnumbered (\section*{}). Standard in a thesis to acknowledge per-chapter.

8. Compilation and Verification
After all fixes:

Run pdflatex (or latexmk -pdf) and bibtex/biber twice to resolve all references.
Verify no ?? appears anywhere in Chapter 2 output.
Verify no (author?) appears.
Verify all 6 figures render inline near their first reference.
Verify the TOC shows clean section numbering with no doubled entries.
Verify the chapter appendix sections are lettered (e.g., 2.A, 2.B) or otherwise distinguished from main sections.
Check that cross-references from other chapters pointing to this chapter (if any) still resolve.


Execution Order

Renumber (Step 1) — mechanical, low risk
Fix broken cite (Step 3) — quick, isolated
Section hierarchy (Step 2) — structural, compile after
SI/Appendix refs (Step 4) — depends on Step 2c
Move and resize figures (Step 5) — highest-impact visual change
Journal boilerplate (Step 7) — editorial
Compile and verify (Step 8) — final pass

Commit after each step.

Appendix: SI Handling Strategy (applies to all chapters)
Each chapter has a different SI situation. Here is the unified strategy:
Chapter 2 (this chapter — Diffusion Review)

SI material: Self-contained appendix (Sections 1.8.1 and 1.8.2) already included in the chapter.
SI references in text: Uses Section 1.8.2:Appendix — clean up the colon syntax as described in Step 4.
Action: Convert to chapter-level appendix. No external SI to import.

Chapter 3 (DDPM-REMD, Yihang PNAS)

SI material: References Supplementary Fig. S2, S2b, S4-S5, S9, and Table S1. This supplementary content is NOT currently in the compiled thesis — these are dangling references to the journal SI.
Action: Either (a) import the SI figures/tables into a chapter appendix and rewire refs, or (b) fold the key SI figures inline into the chapter body where they add value, and drop the rest. Option (b) is recommended — REMD free energy comparisons (Fig S2) and dihedral angle definitions (Table S1) are useful inline. Decorative supplementary figures can be dropped.

Chapter 4 (Thermodynamic Maps, Lukas PNAS)

SI material: References SI Appendix A, C, D, and G — substantial supplementary appendices with derivations and methodological details.
Action: Import all SI appendices as chapter-level appendices (2.A through 2.D or similar). These contain derivations and theoretical details that strengthen a thesis chapter. Rewire all SI Appendix X references to Appendix 4.X.

Chapter 5 (DiffDock-Glide)

SI material: No supplementary references found in the text. Clean.
Action: None needed.

Chapter 6 (RNAnneal)

SI material: The compiled thesis already includes RNAnneal's Supplementary Information (starting around page 81 — algorithms, tables, supplementary figures). However, the main text has 32 broken ?? references — these are \ref{} or \nameref{} calls pointing to SI labels that aren't resolving. Many follow the pattern (see ??) and refer to methods subsections, algorithm boxes, and definitions in the SI.
Action: The SI is already present in the document, so the fix is to repair the broken \label/\ref pairs. Go through each ?? in the RNAnneal chapter, identify what it's trying to reference (usually an Algorithm, Table, Figure, or equation in the SI section), and fix the label. The SI also references Fig. S5.5, Fig. S5.14 which may need label fixes.

Naming Convention for Chapter Appendices
Use a consistent pattern across all chapters:
latex% At the end of each chapter, before the next \chapter:
\begin{subappendices}
\section{First appendix section title}  % renders as e.g. 2.A
\label{app:ch2-arch-details}
...
\section{Second appendix section title} % renders as e.g. 2.B
\label{app:ch2-data-details}
...
\end{subappendices}
This requires the appendix package (\usepackage{appendix}) in the preamble. The subappendices environment scopes the appendix numbering to the chapter so it doesn't affect subsequent chapters.
Updating SI References in Text
When converting Supplementary Fig. SX references:

If the figure is folded inline → just use Figure N.M with the chapter figure number
If the figure goes to a chapter appendix → use Figure N.A.M or Appendix N.A, Figure M
If the figure is dropped entirely → delete the parenthetical reference or rewrite the sentence

When converting SI Appendix X references:

SI Appendix A → Appendix 4.A (or whatever the chapter number is)
Search-and-replace per chapter after establishing the appendix structure
