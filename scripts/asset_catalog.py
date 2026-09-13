"""Generate a deterministic inventory of site assets and their published usage.

Run after building HTML. No packages or network access required.
"""
from collections import defaultdict
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'content/asset-catalog.json'


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('src', 'href', 'poster'):
            if attrs.get(key):
                self.urls.add(attrs[key])
        if attrs.get('srcset'):
            self.urls.update(item.strip().split()[0] for item in attrs['srcset'].split(',') if item.strip())
        self.urls.update(css_urls(attrs.get('style', '')))


def css_urls(text):
    return [m[1] for m in re.findall(r'url\(\s*([\'\"]?)(.*?)\1\s*\)', text)]


def source_records(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from source_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from source_records(child)


def create_catalog():
    files = sorted(p for p in (ROOT / 'assets').rglob('*') if p.is_file() and p.suffix != '.md')
    paths = {p.relative_to(ROOT).as_posix(): p for p in files}
    used_by = defaultdict(set)
    metadata = defaultdict(lambda: {'sources': set(), 'metadata_files': set(), 'alt_texts': set()})
    missing = []
    for page in sorted(ROOT.glob('*.html')):
        parser = References()
        text = page.read_text()
        parser.feed(text)
        for url in parser.urls | set(css_urls(text)):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            path = unquote(parsed.path).lstrip('/')
            if path.startswith('assets/'):
                if path not in paths:
                    missing.append((page.name, path))
                used_by[path].add(page.name)
    for path, file in paths.items():
        if file.suffix != '.css':
            continue
        for url in css_urls(file.read_text()):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = ROOT / parsed.path.lstrip('/') if parsed.path.startswith('/') else file.parent / unquote(parsed.path)
            target = target.resolve().relative_to(ROOT).as_posix()
            if target not in paths:
                missing.append((path, target))
            used_by[target].add(path)
    if missing:
        raise ValueError(f'Broken asset references: {missing}')
    for source in sorted((ROOT / 'content').glob('*.json')):
        if source == CATALOG or source.name in ('asset-path-migrations.json', 'site-audit-layout.json'):
            continue
        for item in source_records(json.loads(source.read_text())):
            path = item.get('path')
            if not isinstance(path, str) or path not in paths:
                continue
            meta = metadata[path]
            meta['metadata_files'].add(source.relative_to(ROOT).as_posix())
            for key in ('source', 'source_url', 'source_page', 'url'):
                if isinstance(item.get(key), str) and item[key].startswith(('http://', 'https://')):
                    meta['sources'].add(item[key])
            if item.get('alt'):
                meta['alt_texts'].add(item['alt'])
            for key in ('width', 'height'):
                if item.get(key):
                    meta[key] = item[key]
    withheld = set(json.loads((ROOT / 'content/publication-withheld-images.json').read_text()))
    entries = []
    duplicates = defaultdict(list)
    ids = set()
    for path, file in paths.items():
        asset_id = file.relative_to(ROOT / 'assets').with_suffix('').as_posix()
        if asset_id in ids:
            raise ValueError(f'Duplicate asset ID: {asset_id}')
        ids.add(asset_id)
        digest = sha256(file.read_bytes()).hexdigest()
        duplicates[digest].append(path)
        entry = {'id': asset_id, 'path': path, 'kind': 'style' if file.suffix == '.css' else 'script' if file.suffix == '.js' else 'image',
                 'bytes': file.stat().st_size, 'sha256': digest,
                 'status': 'withheld' if path in withheld else 'published' if used_by[path] else 'unreferenced',
                 'used_by': sorted(used_by[path])}
        entry.update({key: sorted(value) if isinstance(value, set) else value for key, value in metadata[path].items()})
        entries.append(entry)
    return {'schema_version': 1, 'assets': entries,
            'duplicate_groups': [group for group in duplicates.values() if len(group) > 1]}


def write_catalog():
    catalog = create_catalog()
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    print(f'Cataloged {len(catalog["assets"])} assets; {len(catalog["duplicate_groups"])} duplicate groups (files retained).')


if __name__ == '__main__':
    write_catalog()
