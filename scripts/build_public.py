#!/usr/bin/env python3
"""Generate in isolated staging, then atomically publish only explicitly approved files."""
from pathlib import Path
from hashlib import sha256
import json
import os
import shutil
import subprocess
import sys
import tempfile
from public_files import ROOT, dependency_files, load, safe_file


def main():
    output = ROOT / 'dist'
    if output.is_symlink():
        raise ValueError('dist must not be a symlink')
    # A failed rebuild cannot leave an older package available for deployment.
    if output.exists():
        shutil.rmtree(output)
    config = load(ROOT / 'config/public-files.json')
    pages = config['body_pages'] + config['redirect_pages']
    approved = set(pages + config['assets'])
    withheld = set(load(ROOT / 'content/publication-withheld-images.json'))
    if len(config['body_pages']) != 81 or len(set(pages)) != len(pages):
        raise ValueError('Public page contract must contain 81 distinct body pages')
    if approved & withheld:
        raise ValueError('Withheld files cannot be approved')
    for name in approved:
        safe_file(ROOT, name)
    # Source scripts/content remain private build inputs, never deployed files.
    with tempfile.TemporaryDirectory(prefix='haeon-public-build-') as scratch:
        stage = Path(scratch)
        for directory in ('scripts', 'content', 'assets'):
            source = ROOT / directory
            if source.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
                raise ValueError(f'Symlink in build inputs: {directory}')
            shutil.copytree(source, stage / directory,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for name in pages:
            shutil.copy2(ROOT / name, stage / name)
        subprocess.run([sys.executable, str(stage / 'scripts/build_site.py')], cwd=stage, check=True)
        generated = load(stage / 'content/generated-pages.json')
        if set(generated) != set(config['body_pages']):
            raise ValueError('Generator body pages differ from explicit public allowlist')
        graph = dependency_files(stage, pages, withheld)
        if graph != approved:
            raise ValueError(f'Allowlist mismatch; unapproved={sorted(graph-approved)}, '
                             f'unused={sorted(approved-graph)}')
        # No generated copy changes are published silently during this safety-only release.
        for name in pages:
            if (stage / name).read_bytes() != (ROOT / name).read_bytes():
                raise ValueError(f'Generator/source drift in {name}; reconcile before publishing')
        with tempfile.TemporaryDirectory(prefix='.public-output-', dir=ROOT) as temporary:
            candidate = Path(temporary) / 'dist'
            candidate.mkdir()
            for name in sorted(approved):
                target = candidate / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(safe_file(stage, name), target)
            os.replace(candidate, output)
    try:
        subprocess.run([sys.executable, str(ROOT / 'scripts/check_public.py')], cwd=ROOT, check=True)
    except BaseException:
        shutil.rmtree(output)
        raise
    manifest = {p.relative_to(output).as_posix(): sha256(p.read_bytes()).hexdigest()
                for p in sorted(output.rglob('*')) if p.is_file()}
    evidence = ROOT / 'audit/2026-10-12/implementation'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'public-build-manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'PASS: public dist: 81 body pages, {len(config["redirect_pages"])} fallbacks, '
          f'{len(config["assets"])} reachable assets. No source/medical draft published.')


if __name__ == '__main__':
    main()
