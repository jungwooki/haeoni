#!/usr/bin/env python3
"""Independent public safety/SEO regression gate; Python standard library only, no EMR."""
from pathlib import Path
from hashlib import sha256
from urllib.parse import urlsplit, unquote
import json
import re
from public_files import ROOT, Document, dependency_files, load, safe_file


def check(root=ROOT, output=None):
    output = output or root / 'dist'
    policy = load(root / 'config/public-files.json')
    pages = policy['body_pages'] + policy['redirect_pages']
    expected = set(pages + policy['assets'])
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError(f'Output mismatch: extra={sorted(actual-expected)}, missing={sorted(expected-actual)}')
    withheld = set(load(root / 'content/publication-withheld-images.json'))
    if actual & withheld:
        raise ValueError('Withheld file leaked')
    if dependency_files(output, pages, withheld) != actual:
        raise ValueError('Output contains unreachable/invalid files')
    baseline = load(root / 'config/public-regression.json')
    for name in actual:
        copied = safe_file(output, name)
        digest = sha256(copied.read_bytes()).hexdigest()
        if digest != sha256(safe_file(root, name).read_bytes()).hexdigest():
            raise ValueError(f'Source/output mismatch: {name}')
        if digest != baseline['sha256'][name]:
            raise ValueError(f'Unreviewed public content/design change: {name}')
    docs = {n: Document((output / n).read_text()) for n in pages}
    canonical_missing = 0
    for name in policy['body_pages']:
        doc = docs[name]
        if doc.h1 != 1 or len(doc.ids) != len(set(doc.ids)):
            raise ValueError(f'H1/duplicate anchor error: {name}')
        if not doc.titles or not doc.descriptions or not doc.descriptions[0]:
            raise ValueError(f'Missing SEO title/description: {name}')
        if any('noindex' in s.lower() for s in doc.robots):
            raise ValueError(f'Unexpected body noindex: {name}')
        if not doc.canonicals:
            canonical_missing += 1
        else:
            canonical = doc.canonicals[0]
            target = urlsplit(canonical)
            own = '/' if name == 'index.html' else '/' + name
            if len(doc.canonicals) != 1 or target.scheme != 'https' or target.netloc != 'haeoni.com' or target.path != own:
                raise ValueError(f'Incorrect page canonical: {name}')
        text = (output / name).read_text()
        for required in baseline['required_references']:
            if required not in doc.refs:
                raise ValueError(f'Contact/menu regression: {name}: {required}')
        if 'class="floating-contact"' not in text or 'name="viewport"' not in text:
            raise ValueError(f'Mobile menu/viewport regression: {name}')
        for url in doc.links:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            dest = unquote(parsed.path).lstrip('/') or name
            if dest not in docs:
                raise ValueError(f'Broken local page link: {name}: {url}')
            if parsed.fragment and parsed.fragment not in docs[dest].ids:
                raise ValueError(f'Broken anchor: {name}: {url}')
    for name in policy['redirect_pages']:
        if 'http-equiv="refresh"' not in (output / name).read_text():
            raise ValueError(f'Legacy fallback lost: {name}')
    vercel = load(root / 'vercel.json')
    if vercel.get('outputDirectory') != 'dist' or vercel.get('buildCommand') != 'python3 scripts/build_site.py --public':
        raise ValueError('Vercel must use isolated public build/dist')
    if vercel.get('cleanUrls') is not False or vercel.get('rewrites') or vercel.get('routes'):
        raise ValueError('Unapproved routing change in active Vercel config')
    expected_routes = {(source, mode, target) for source in ('/', '/index.html')
                       for mode, target in (('privacy', '/privacy.html'), ('policy', '/terms.html'))}
    observed = set()
    for rule in vercel.get('redirects', []):
        if rule.get('permanent') is not False or len(rule.get('has', [])) != 1:
            raise ValueError('Unexpected policy redirect')
        condition = rule['has'][0]
        if condition.get('type') != 'query' or condition.get('key') != 'mode':
            raise ValueError('Unexpected redirect condition')
        observed.add((rule['source'], condition['value'], rule['destination']))
    if observed != expected_routes or len(vercel['redirects']) != 4:
        raise ValueError('Policy route mismatch or unapproved legacy redirects')
    headers = vercel.get('headers', [])
    if len(headers) != 1 or headers[0].get('headers') != [{'key': 'X-Robots-Tag', 'value': 'noindex, nofollow'}]:
        raise ValueError('Preview noindex contract missing')
    if headers[0].get('has') != [{'type': 'host', 'value': '(?<preview>.+\\.vercel\\.app)'}]:
        raise ValueError('Preview header must not block custom production hosts')
    result = {'status': 'PASS', 'body_pages': len(policy['body_pages']),
              'redirect_fallbacks': len(policy['redirect_pages']), 'assets': len(policy['assets']),
              'public_files': len(actual), 'canonical_missing_known_p1': canonical_missing,
              'medical_candidates_published': False, 'external_emr_used': False}
    print(json.dumps(result, ensure_ascii=False))
    return result


if __name__ == '__main__':
    check()
