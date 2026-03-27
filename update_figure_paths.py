#!/usr/bin/env python3
"""Update figure paths in chapter files based on the manifest."""

import re
import os

BASE_DIR = "/home/lukas/research/thesis"

# Chapter prefix mapping
CHAPTER_PREFIXES = {
    2: "ch2_",
    3: "ch3_",
    4: "ch4_",
    5: "ch5_",
    6: "ch6_",
}

def update_chapter(chapter_num, chapter_file):
    """Update figure paths in a chapter file."""
    filepath = os.path.join(BASE_DIR, "src", chapter_file)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    prefix = CHAPTER_PREFIXES[chapter_num]

    # Find all includegraphics commands and update paths
    # Match patterns like: \includegraphics[...]{path}
    def replace_path(match):
        options = match.group(1) if match.group(1) else ""
        old_path = match.group(2)

        # Extract just the filename
        filename = os.path.basename(old_path)

        # Handle paths with ./ prefix or subdirectories
        if '/' in old_path:
            filename = old_path.split('/')[-1]

        # Create new path
        new_path = f"figures/{prefix}{filename}"

        # Check if the new file exists
        new_filepath = os.path.join(BASE_DIR, new_path)
        if not os.path.exists(new_filepath):
            # Try without chapter prefix (some figs might be named differently)
            print(f"  Warning: {new_filepath} not found")

        return f"\\includegraphics{options}{{{new_path}}}"

    pattern = r'\\includegraphics(\[[^\]]*\])?\{([^}]+)\}'
    new_content, count = re.subn(pattern, replace_path, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated {chapter_file}: {count} figure references")

def main():
    chapters = [
        (2, "ch2_diffusion_review.tex"),
        (3, "ch3_ddpm_remd.tex"),
        (4, "ch4_thermodynamic_maps.tex"),
        (5, "ch5_diffdock_glide.tex"),
        (6, "ch6_rnaanneal.tex"),
    ]

    for chapter_num, chapter_file in chapters:
        update_chapter(chapter_num, chapter_file)

    print("\nDone!")

if __name__ == "__main__":
    main()
