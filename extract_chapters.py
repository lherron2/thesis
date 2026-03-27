#!/usr/bin/env python3
"""Extract body content from paper .tex files for thesis chapters."""

import re
import os

# Paper configurations: (source_dir, source_file, chapter_num, output_name)
PAPERS = [
    ("papers/diffusion-review-jcp", "main.tex", 2, "diffusion_review"),
    ("papers/ddpm-rmsd-pnas", "main.tex", 3, "ddpm_remd"),
    ("papers/thermodynamic-maps-pnas", "Research_report.tex", 4, "thermodynamic_maps"),
    ("papers/diffdock-glide", "main.tex", 5, "diffdock_glide"),
    ("papers/rnanneal", "nature_draft0.tex", 6, "rnaanneal"),
]

BASE_DIR = "/home/lukas/research/thesis"

def extract_abstract(content):
    """Extract abstract content."""
    # Match \begin{abstract}...\end{abstract}
    match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def clean_body(content):
    """Extract and clean body content."""
    # Find content between \begin{document} and \end{document}
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
    if not doc_match:
        return ""

    body = doc_match.group(1)

    # Remove title, author, affiliation blocks
    patterns_to_remove = [
        r'\\title\{[^}]*\}',
        r'\\title\[[^\]]*\]\{[^}]*\}',
        r'\\author\[[^\]]*\]\{[^}]*\}',
        r'\\author\{[^}]*\}',
        r'\\affil\[[^\]]*\]\{[^}]*\}',
        r'\\affiliation\{[^}]*\}',
        r'\\thanks\{[^}]*\}',
        r'\\maketitle',
        r'\\thispagestyle\{[^}]*\}',
        r'\\leadauthor\{[^}]*\}',
        r'\\correspondingauthor\{[^}]*\}',
        r'\\authorcontributions\{[^}]*\}',
        r'\\authordeclaration\{[^}]*\}',
        r'\\significancestatement\{[^}]*\}',
        r'\\keywords\{[^}]*\}',
        r'\\dates\{[^}]*\}',
        r'\\doi\{[^}]*\}',
        r'\\firstpage\[[^\]]*\]\{[^}]*\}',
        r'\\firstpage\{[^}]*\}',
        r'\\dropcap\{([A-Z])\}',  # Keep the letter but remove \dropcap
        r'\\ifthenelse\{\\boolean\{shortarticle\}\}.*?\\}\\}\\}',
        r'\\begin\{abstract\}.*?\\end\{abstract\}',
        r'\\showmatmethods\{\}',
        r'\\showacknow\{\}',
    ]

    for pattern in patterns_to_remove:
        body = re.sub(pattern, '', body, flags=re.DOTALL)

    # Replace \dropcap{X} with just X
    body = re.sub(r'\\dropcap\{([A-Z])\}', r'\1', body)

    # Remove acknowledgments section
    body = re.sub(r'\\section\*?\{Acknowledgments?\}.*?(?=\\section|\Z)', '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'\\acknow\{.*?\}', '', body, flags=re.DOTALL)

    # Remove bibliography
    body = re.sub(r'\\bibliography\{[^}]*\}', '', body)
    body = re.sub(r'\\bibliographystyle\{[^}]*\}', '', body)
    body = re.sub(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', '', body, flags=re.DOTALL)

    # Clean up excessive newlines
    body = re.sub(r'\n{3,}', '\n\n', body)

    return body.strip()

def process_paper(paper_dir, source_file, chapter_num, output_name):
    """Process a single paper and extract chapter content."""
    source_path = os.path.join(BASE_DIR, paper_dir, source_file)

    print(f"Processing: {source_path}")

    with open(source_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Extract abstract
    abstract = extract_abstract(content)
    if abstract:
        abstract_path = os.path.join(BASE_DIR, paper_dir, "abstract.txt")
        with open(abstract_path, 'w', encoding='utf-8') as f:
            f.write(abstract)
        print(f"  Saved abstract to: {abstract_path}")

    # Clean body
    body = clean_body(content)

    # Add chapter header
    chapter_content = f"% Chapter {chapter_num}: {output_name.replace('_', ' ').title()}\n"
    chapter_content += f"% Source: {paper_dir}/{source_file}\n\n"
    chapter_content += body

    # Write to src/
    output_path = os.path.join(BASE_DIR, "src", f"ch{chapter_num}_{output_name}.tex")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(chapter_content)

    print(f"  Saved chapter to: {output_path}")
    print(f"  Body length: {len(body)} chars")

def main():
    for paper_dir, source_file, chapter_num, output_name in PAPERS:
        process_paper(paper_dir, source_file, chapter_num, output_name)
    print("\nDone!")

if __name__ == "__main__":
    main()
