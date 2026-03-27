#!/usr/bin/env python3
"""Build a clean, deduplicated thesis.bib file."""

import re
import os

BASE_DIR = "/home/lukas/research/thesis"

def parse_bib_entries(content):
    """Parse bib content into individual entries."""
    entries = {}
    seen_keys_lower = set()  # Track lowercase versions to catch case variants
    current_entry = []
    current_key = None
    brace_count = 0
    in_entry = False

    for line in content.split('\n'):
        match = re.match(r'^@(\w+)\s*\{\s*([^,]+)\s*,', line)
        if match:
            # Save previous entry
            if in_entry and current_key and current_entry:
                key_lower = current_key.lower()
                if key_lower not in seen_keys_lower:
                    entries[current_key] = '\n'.join(current_entry)
                    seen_keys_lower.add(key_lower)

            current_entry = [line]
            current_key = match.group(2).strip()
            in_entry = True
            brace_count = line.count('{') - line.count('}')
        elif in_entry:
            current_entry.append(line)
            brace_count += line.count('{') - line.count('}')

            if brace_count <= 0:
                key_lower = current_key.lower() if current_key else None
                if current_key and key_lower not in seen_keys_lower:
                    entries[current_key] = '\n'.join(current_entry)
                    seen_keys_lower.add(key_lower)
                current_entry = []
                current_key = None
                in_entry = False

    # Handle last entry
    if current_entry and current_key:
        key_lower = current_key.lower()
        if key_lower not in seen_keys_lower:
            entries[current_key] = '\n'.join(current_entry)

    return entries

def main():
    # Read base bib
    with open(os.path.join(BASE_DIR, "bib", "thesis_base.bib"), 'r', encoding='utf-8', errors='replace') as f:
        base_content = f.read()

    base_entries = parse_bib_entries(base_content)
    print(f"Base entries: {len(base_entries)}")

    # Read missing entries
    with open(os.path.join(BASE_DIR, "bib", "missing_entries.bib"), 'r', encoding='utf-8', errors='replace') as f:
        missing_content = f.read()

    missing_entries = parse_bib_entries(missing_content)
    print(f"Missing entries file: {len(missing_entries)}")

    # Add only truly missing entries (case-insensitive check)
    base_keys_lower = {k.lower() for k in base_entries.keys()}
    added = 0
    for key, entry in missing_entries.items():
        if key.lower() not in base_keys_lower:
            base_entries[key] = entry
            base_keys_lower.add(key.lower())
            added += 1

    print(f"Added {added} truly missing entries")
    print(f"Total unique entries: {len(base_entries)}")

    # Write clean bib file
    with open(os.path.join(BASE_DIR, "bib", "thesis.bib"), 'w', encoding='utf-8') as f:
        f.write("% Thesis bibliography - deduplicated\n\n")
        for key in sorted(base_entries.keys()):
            f.write(base_entries[key])
            f.write("\n\n")

    print("Written to bib/thesis.bib")

if __name__ == "__main__":
    main()
