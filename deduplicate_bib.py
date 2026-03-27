#!/usr/bin/env python3
"""Deduplicate bibliography entries and update citations."""

import re
import os

BASE_DIR = "/home/lukas/research/thesis"

# Map duplicate keys to canonical key (first key is canonical)
CANONICAL_KEYS = {
    # DiffDock variants
    "corso2022diffdock": "diffdock",
    "Diffdock": "diffdock",

    # Score-based generative
    "sgm-sde": "score-based-generative",
    "song2020sgm": "score-based-generative",
    "song2020score": "score-based-generative",

    # Neural ODE
    "CNF": "NeuralODE",

    # Flow matching
    "flow-matching": "CFM",

    # Stochastic NF
    "stochastic-normalizing-flows": "StochasticNF",
    "SNF": "StochasticNF",

    # Sinkhorn
    "sinkhornot": "sinkhorn-ot",

    # Non-equilibrium learning
    "learning-non-eq-thermo": "nonequilibrium-learning",
    "sohl2015deep": "nonequilibrium-learning",

    # TFEP
    "tfep-2002": "TFEP",
    "wirnsberger-TFEP": "tfep-2020",

    # DDPM-REMD / thermomaps
    "ddpm-wang-2022": "ddpm-remd",
    "thermomaps-2023": "herron2024inferring",

    # NF-REMD
    "NF-REMD": "lrex-2022",

    # DIG
    "dig-2024": "distributional-graphormer",

    # Latent diffusion
    "rombach2022high": "latent-diffusion",

    # RF-AA
    "krishna2024rfaa": "RF-AA",

    # AlphaFold
    "jumper2021af2": "alphafold-2",
    "abramson2024af3": "alphafold-3",
    "abramson2024accurate": "alphafold-3",

    # U-Net
    "ronneberger2015u": "unet",

    # NF Review
    "NFreview": "kobyzev2020normalizing",

    # RNA FF
    "tan2018rna": "DE-Shaw-RNA-ff",

    # G-vectors
    "bottaro2014role": "gvecs-bussi",

    # Equivariant diffusion
    "hoogeboom2022equivariant": "equivariant-diffusion-model",

    # Unified perspectives
    "three-interpretations": "luo-unified-perspectives",

    # Chai-1
    "Chai-1-Technical-Report": "chai2024chai",

    # BEDROC
    "truchon2007evaluating": "truchon2007bedroc",

    # expTM
    "lee2025exponentially": "exptm",

    # Leonard survey
    "leonard2013survey": "leonard-2014",
}

def update_citations_in_file(filepath):
    """Update citation keys in a tex file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = 0
    for old_key, new_key in CANONICAL_KEYS.items():
        # Match \cite{...old_key...}
        pattern = rf'(\\cite\{{[^}}]*){re.escape(old_key)}([^}}]*\}})'
        new_content = re.sub(pattern, rf'\1{new_key}\2', content)
        if new_content != content:
            changes += 1
            content = new_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return changes

def remove_duplicate_entries(bibfile):
    """Remove duplicate bib entries, keeping first occurrence."""
    with open(bibfile, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track seen keys
    seen_keys = set()
    output_lines = []
    current_entry = []
    current_key = None
    in_entry = False
    brace_count = 0

    for line in content.split('\n'):
        # Check for entry start
        match = re.match(r'^@(\w+)\s*\{\s*([^,]+)\s*,', line)
        if match:
            if in_entry and current_entry:
                # Save previous entry if key not seen
                if current_key and current_key not in seen_keys:
                    output_lines.extend(current_entry)
                    seen_keys.add(current_key)

            current_entry = [line]
            current_key = match.group(2).strip()
            in_entry = True
            brace_count = line.count('{') - line.count('}')
        elif in_entry:
            current_entry.append(line)
            brace_count += line.count('{') - line.count('}')

            if brace_count <= 0:
                # Entry complete
                if current_key and current_key not in seen_keys:
                    output_lines.extend(current_entry)
                    seen_keys.add(current_key)
                current_entry = []
                current_key = None
                in_entry = False
        else:
            output_lines.append(line)

    # Handle last entry
    if current_entry and current_key and current_key not in seen_keys:
        output_lines.extend(current_entry)

    with open(bibfile, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    return len(seen_keys)

def main():
    # Update citations in all chapter files
    src_dir = os.path.join(BASE_DIR, "src")
    total_changes = 0
    for filename in os.listdir(src_dir):
        if filename.endswith('.tex'):
            filepath = os.path.join(src_dir, filename)
            changes = update_citations_in_file(filepath)
            if changes > 0:
                print(f"{filename}: {changes} citation key updates")
                total_changes += changes

    print(f"\nTotal citation key updates: {total_changes}")

    # Remove duplicate entries from bib file
    bibfile = os.path.join(BASE_DIR, "bib", "thesis.bib")
    unique_entries = remove_duplicate_entries(bibfile)
    print(f"\nBib file now has {unique_entries} unique entries")

if __name__ == "__main__":
    main()
