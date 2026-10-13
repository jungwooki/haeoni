#!/usr/bin/env python3
"""Optional original guide comparison. Never used by public builds; no default EMR path."""
import argparse
from pathlib import Path
from public_files import ROOT, load

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, required=True,
                        help='Operator-authorized guide JSON directory; no patient records')
    args = parser.parse_args()
    for kind, items in load(ROOT / 'content/care-guides.json').items():
        if not isinstance(items, list):
            continue
        source = load(args.source_dir / f'{kind}.json')['data']
        mapped = [sid for item in items for sid in item['source_ids'] if not sid.startswith('USER_')]
        if sorted(mapped) != sorted(x['id'] for x in source):
            raise SystemExit(f'FAIL: {kind} source coverage')
    print('PASS: explicitly supplied original guide IDs match public mappings')
