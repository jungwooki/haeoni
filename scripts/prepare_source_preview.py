#!/usr/bin/env python3
"""Create a minimal source-build snapshot; no Git mutation, remote call or patient data."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import shutil
import subprocess
import sys
from public_files import ROOT, load, safe_file

# Only generator inputs, not archived source trees, review drafts, audit logs or EMR.
CONTENT_INPUTS = [
    'about-original.json', 'asset-path-migrations.json', 'care-guides.json',
    'clinic-photo-inventory.json', 'digestive-pages.json', 'doctors-original.json',
    'family-pages.json', 'family-routes.json', 'gallery.json', 'internal-pages.json',
    'inventory.json', 'legacy-redirects.json', 'moving-photos.json',
    'publication-copy-edits.json', 'publication-overrides.json',
    'publication-withheld-images.json', 'tonics.json', 'visual-guides.json',
]
PYTHON_INPUTS = [
    'asset_catalog.py', 'build_public.py', 'build_site.py', 'care_editorial.py',
    'care_guides.py', 'check_public.py', 'child_reading.py', 'clinical_visuals.py',
    'clinic_photos.py', 'family_pages.py', 'fees.py', 'floating_menu.py',
    'home_hero.py', 'internal_pages.py', 'internal_reading.py', 'page_routes.py',
    'pain_care.py', 'public_files.py', 'publication_review.py', 'site_assets.py', 'tonic_care.py',
]
CANARIES = ['audit/source-build-canary.txt', 'skills/source-build-canary.txt',
            'reviews/internal-report-canary.md']


def prepare(destination):
    if destination.exists():
        raise ValueError('Use a new temporary destination; original files are never removed')
    destination.mkdir(parents=True)
    policy = load(ROOT / 'config/public-files.json')
    files = policy['body_pages'] + policy['redirect_pages'] + policy['assets']
    withheld = set(load(ROOT / 'content/publication-withheld-images.json'))
    # Canonical deduplication reads a few source images which are not rendered.
    # Keep these explicit private build dependencies; never add them to public-files.json.
    build_images = set()
    for source_name in ('internal-pages.json', 'family-pages.json', 'digestive-pages.json'):
        for article in load(ROOT / 'content' / source_name):
            for section in article['sections']:
                for item in section['items']:
                    if item['type'] == 'image' and item['path'] not in withheld:
                        build_images.add(item['path'])
    files += sorted(build_images - set(files))
    files += ['scripts/' + name for name in PYTHON_INPUTS]
    files += ['content/' + name for name in CONTENT_INPUTS]
    files += ['content/privacy-original.txt', 'content/legacy/index.html',
              'config/public-files.json', 'config/public-regression.json', 'vercel.json']
    for name in files:
        source = safe_file(ROOT, name)
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for name in CANARIES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('Synthetic non-medical build-input canary. Must not be publicly served.\n')
    config = load(destination / 'vercel.json')
    if config != load(ROOT / 'vercel.json'):
        raise ValueError('Source preview must use exactly the local Vercel configuration')
    if any((destination / name).exists() for name in withheld):
        raise ValueError('Withheld images must not be uploaded as source')
    # The same command Vercel runs. No prebuilt dist is supplied in the upload manifest.
    subprocess.run([sys.executable, 'scripts/build_site.py', '--public'],
                   cwd=destination, check=True)
    manifest = {name: {'sha256': sha256((destination / name).read_bytes()).hexdigest(),
                       'bytes': (destination / name).stat().st_size}
                for name in sorted(files + CANARIES)}
    if any(name.startswith('dist/') for name in manifest):
        raise ValueError('Prebuilt output cannot be part of a source-build upload')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    manifest = prepare(args.destination.resolve())
    evidence = ROOT / 'audit/2026-10-12/source-build'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'source-input-manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (evidence / 'snapshot-path.txt').write_text(str(args.destination.resolve()) + '\n')
    print(f'PASS: {len(manifest)} explicit source inputs; no prebuilt dist, withheld images, EMR or medical drafts uploaded')
