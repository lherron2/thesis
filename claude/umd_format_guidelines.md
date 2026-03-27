# UMD_FORMAT.md — UMD ETD Formatting Requirements

Source: 2025 UMD Electronic Thesis and Dissertation Style Guide. These requirements are non-negotiable. The Office of the Registrar's requirements supersede all other style manuals.

---

## Page Layout

- **Margins:** 1" all sides. Applies to everything — figures, headers/footers, footnotes, full-page images.
- **Page numbers:** At least 3/4" from edge of page.
- **LaTeX:**
  ```latex
  \usepackage[margin=1in]{geometry}
  ```

## Fonts

- All fonts must be **embedded**. pdflatex embeds by default. Verify: `pdffonts thesis.pdf | grep -v 'yes'`.
- Equivalent in scale to **10pt Arial** or **12pt Times New Roman**.
- No script, italic, or ornamental fonts as body text. Italics allowed only for non-English words and quotations.
- Applies to all text including captions, footnotes, citations.
- Figure captions: may be 2pt smaller than body text, but no smaller than 10pt.

## Line Spacing

- **Double-space:** abstract, dedication, acknowledgements, TOC, body text.
- **May single-space:** block quotations, captions, table contents, lists, graphs, charts.
- **Single-space:** footnotes/endnotes, bibliography entries, appendix lists.
- **LaTeX:**
  ```latex
  \usepackage{setspace}
  \doublespacing
  ```

## Color

- Document viewed electronically in color. Microfilm is grayscale only.
- All figures must be interpretable in grayscale. Color-coded data needs non-color differentiators.

---

## Front Matter (required order, exact)

```
1.  Abstract                    — REQUIRED, non-numbered page
2.  Title Page                  — REQUIRED, non-numbered page
3.  Copyright Page              — highly recommended, non-numbered page
4.  Preface or Foreword         — optional, lowercase Roman starting at ii
5.  Dedication                  — optional, lowercase Roman
6.  Acknowledgements            — optional, lowercase Roman
7.  Table of Contents           — REQUIRED, lowercase Roman
8.  List of Tables              — required if ≥1 table, lowercase Roman
9.  List of Figures             — required if ≥1 figure, lowercase Roman
10. List of Abbreviations       — optional, lowercase Roman
```

### LaTeX skeleton:
```latex
\pagenumbering{gobble}          % no page numbers
\include{front/abstract}
\include{front/titlepage}
\include{front/copyright}

\pagenumbering{roman}           % lowercase Roman starting at ii
\setcounter{page}{2}
\include{front/acknowledgements}
\tableofcontents
\listoftables
\listoffigures

\pagenumbering{arabic}          % Arabic starting at 1
\include{chapters/ch1_intro}
...
```

### Abstract Page
- "ABSTRACT" centered, <2" from top of page.
- Contains: title (ALL CAPS), author name, degree (spelled out), year, advisor title/name/department.
- Double-spaced body. No page number.
- Title must be identical on abstract page and title page.

### Title Page
- Title in ALL CAPS. No italics unless foreign/botanical terms. No abbreviations. Formulas/symbols as words.
- Author name as in university records.
- Degree statement in inverted pyramid:
  ```
  Dissertation submitted to the Faculty of the Graduate School of the
  University of Maryland, College Park, in partial fulfillment
  of the requirements for the degree of
  Doctor of Philosophy
  2026
  ```
- Advisory Committee: Chair first, then alphabetical. Use professorial title or "Dr."

### Copyright Page
- Centered: ©Copyright by / [full name] / [year]

### Table of Contents
- TOC numbering must match text numbering.
- Software-generated is acceptable.
- May single-space between subheadings. Dot leaders optional.

---

## Body

- Arabic numeral 1, numbered consecutively to the end.
- Double-spaced. Each chapter on a fresh page.
- Chapter title: up to 3pt larger than base font, no more than 3" from top of page.

## Illustrations and Figures

- Numbered consecutively. Listed in List of Figures (required if ≥1 figure).
- **Placement:** Same page or following page as first mention. NOT before the first reference.
- Must respect 1" margins.
- Must have captions, preferably on same page. If figure is full-page, caption on preceding page.
- Landscape pages: page numbering may be suppressed.
- Captions consistent with body text; may be 2pt smaller but ≥10pt.

## Tables

- Numbered consecutively. Listed in List of Tables (required if ≥1 table).
- Same placement rules as figures.

---

## Back Matter

```
11. Appendices                  — optional, Arabic (consecutive with body)
12. Glossary                    — optional, Arabic
13. References / Bibliography   — REQUIRED, Arabic (consecutive with body)
14. Index                       — optional, Arabic
15. Curriculum Vitae            — optional, non-numbered
```

### Appendices
- Labeled consecutively: A, B, C or I, II, III.
- No cover pages. Include in TOC.
- Arabic page numbering, consecutive with body.

### References
- Comprehensive reference list at end of dissertation is **required**, even if refs appear in footnotes.
- Must be placed at the end, regardless of style manual recommendations.
- Footnote/endnote style must be consistent throughout — do not mix bottom-of-page with end-of-chapter.

### Supplementary Materials
- Do NOT embed media in the PDF.
- Upload as supplementary files during ProQuest submission.

---

## Preamble Checklist

Verify these are present. Add any missing:

```latex
\documentclass[12pt]{report}          % or UMD thesis class
\usepackage[margin=1in]{geometry}     % 1" margins
\usepackage{setspace}                 % double spacing
\doublespacing
\usepackage[title]{appendix}          % chapter-scoped appendices
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}
```

Check for a UMD LaTeX template at:
https://gradschool.umd.edu/students/academic-progress/thesis-and-dissertation-filing

If one exists, prefer it over manual setup — it handles pagination, front matter, and margins correctly.
