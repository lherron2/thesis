#!/usr/bin/env python3
"""Find potential duplicate bibliography entries."""

import re
from collections import defaultdict

def parse_bib(filename):
    """Parse bib file and extract entries."""
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    entries = []
    # Match bib entries
    pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*)'
    matches = re.findall(pattern, content, re.DOTALL)

    for entry_type, cite_key, fields in matches:
        entry = {
            'type': entry_type,
            'key': cite_key.strip(),
            'fields': {}
        }

        # Extract title
        title_match = re.search(r'title\s*=\s*[\{"](.+?)[\}"]', fields, re.IGNORECASE | re.DOTALL)
        if title_match:
            entry['fields']['title'] = title_match.group(1).strip()

        # Extract DOI
        doi_match = re.search(r'doi\s*=\s*[\{"](.+?)[\}"]', fields, re.IGNORECASE)
        if doi_match:
            entry['fields']['doi'] = doi_match.group(1).strip()

        entries.append(entry)

    return entries

def normalize_title(title):
    """Normalize title for comparison."""
    # Remove braces, special chars, lowercase
    title = re.sub(r'[{}\\]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title.lower().strip()

def find_duplicates(entries):
    """Find potential duplicates by DOI and title similarity."""
    duplicates = []

    # Group by DOI
    doi_groups = defaultdict(list)
    for entry in entries:
        doi = entry['fields'].get('doi', '').lower()
        if doi:
            doi_groups[doi].append(entry)

    for doi, group in doi_groups.items():
        if len(group) > 1:
            keys = [e['key'] for e in group]
            duplicates.append(('DOI', doi, keys))

    # Group by normalized title
    title_groups = defaultdict(list)
    for entry in entries:
        title = entry['fields'].get('title', '')
        if title:
            norm_title = normalize_title(title)
            if len(norm_title) > 20:  # Only consider substantive titles
                title_groups[norm_title].append(entry)

    for title, group in title_groups.items():
        if len(group) > 1:
            keys = [e['key'] for e in group]
            # Skip if already reported by DOI
            duplicates.append(('Title', title[:80], keys))

    return duplicates

def main():
    entries = parse_bib('/home/lukas/research/thesis/bib/thesis.bib')
    print(f"Total entries: {len(entries)}")

    duplicates = find_duplicates(entries)

    with open('/home/lukas/research/thesis/bib/DUPLICATES.md', 'w') as f:
        f.write("# Potential Duplicate Bibliography Entries\n\n")
        f.write(f"Total entries scanned: {len(entries)}\n\n")

        if duplicates:
            f.write("## Duplicates Found\n\n")
            for match_type, value, keys in duplicates:
                f.write(f"### {match_type}: `{value}`\n")
                f.write(f"- Keys: {', '.join(keys)}\n\n")
        else:
            f.write("No duplicates found.\n")

    print(f"Found {len(duplicates)} potential duplicate groups")
    print("Written to bib/DUPLICATES.md")

if __name__ == "__main__":
    main()
