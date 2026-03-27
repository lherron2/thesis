#!/usr/bin/env python3
"""Add chapter prefixes to all labels and refs to avoid conflicts."""

import re
import os

BASE_DIR = "/home/lukas/research/thesis/src"

CHAPTERS = [
    ("ch2_diffusion_review.tex", "ch2:"),
    ("ch3_ddpm_remd.tex", "ch3:"),
    ("ch4_thermodynamic_maps.tex", "ch4:"),
    ("ch5_diffdock_glide.tex", "ch5:"),
    ("ch6_rnaanneal.tex", "ch6:"),
]

def add_prefix_to_labels(content, prefix):
    """Add prefix to all \label{} and \ref{} commands."""

    # Find all labels in this file
    labels = set(re.findall(r'\\label\{([^}]+)\}', content))

    # For each label, prefix it and update all refs
    for label in labels:
        new_label = f"{prefix}{label}"

        # Replace \label{label}
        content = re.sub(
            rf'\\label\{{{re.escape(label)}\}}',
            f'\\\\label{{{new_label}}}',
            content
        )

        # Replace \ref{label}
        content = re.sub(
            rf'\\ref\{{{re.escape(label)}\}}',
            f'\\\\ref{{{new_label}}}',
            content
        )

        # Replace \eqref{label}
        content = re.sub(
            rf'\\eqref\{{{re.escape(label)}\}}',
            f'\\\\eqref{{{new_label}}}',
            content
        )

        # Replace \autoref{label}
        content = re.sub(
            rf'\\autoref\{{{re.escape(label)}\}}',
            f'\\\\autoref{{{new_label}}}',
            content
        )

    return content, len(labels)

def main():
    for filename, prefix in CHAPTERS:
        filepath = os.path.join(BASE_DIR, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, label_count = add_prefix_to_labels(content, prefix)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"{filename}: prefixed {label_count} labels with '{prefix}'")

if __name__ == "__main__":
    main()
