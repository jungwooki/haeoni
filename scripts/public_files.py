"""Public dependency graph. No EMR, network, generator imports or directory publishing."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSET_SUFFIXES = {'.css', '.js', '.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg',
                  '.ico', '.avif', '.woff', '.woff2', '.ttf', '.otf', '.mp4', '.webm', '.pdf'}


def load(path):
    return json.loads(Path(path).read_text())


def safe_file(root, name):
    """Reject traversal, hidden components, symlinks and missing/empty inputs."""
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or any(p.startswith('.') for p in path.parts):
        raise ValueError(f'Unsafe public path: {name}')
    file = root / name
    if any((root / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)):
        raise ValueError(f'Symlink is not publishable: {name}')
    if not file.is_file() or not file.stat().st_size:
        raise ValueError(f'Missing/empty public dependency: {name}')
    if not file.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Escaping dependency: {name}')
    return file


def local_path(owner, url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    raw = unquote(parsed.path)
    if '\\' in raw or '..' in PurePosixPath(raw).parts:
        # CSS ../ paths are permitted only after resolution inside assets.
        import posixpath
        path = posixpath.normpath(str(PurePosixPath(owner).parent / raw))
    else:
        path = str(PurePosixPath(raw.lstrip('/')) if raw.startswith('/')
                   else PurePosixPath(owner).parent / raw)
    return path


def css_refs(text):
    refs = [m[1] for m in re.findall(r'url\(\s*([\'"]?)(.*?)\1\s*\)', text)]
    refs += re.findall(r'@import\s+[\'"]([^\'"]+)[\'"]', text)
    return refs


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs = set(css_refs(text))
        self.links = []
        self.ids = []
        self.h1 = 0
        self.titles = []
        self.descriptions = []
        self.canonicals = []
        self.robots = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'title':
            self.titles.append(True)
        for key in ('src', 'href', 'poster'):
            if a.get(key):
                self.refs.add(a[key])
        if a.get('srcset') and not a['srcset'].startswith('data:'):
            self.refs.update(x.strip().split()[0] for x in a['srcset'].split(',') if x.strip())
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'meta' and a.get('name', '').lower() == 'description':
            self.descriptions.append(a.get('content', ''))
        if tag == 'meta' and a.get('name', '').lower() in ('robots', 'googlebot'):
            self.robots.append(a.get('content', ''))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href', ''))


def dependency_files(root, pages, withheld):
    """Only reachable assets; CSS imports, fonts, srcset and inline CSS included."""
    found = set(pages)
    queue = list(pages)
    while queue:
        owner = queue.pop()
        file = safe_file(root, owner)
        suffix = file.suffix.lower()
        if suffix in ('.html', '.svg'):
            refs = Document(file.read_text()).refs
        elif suffix == '.css':
            refs = css_refs(file.read_text())
        elif suffix == '.js':
            # Static module references; dynamically constructed assets require explicit review.
            text = file.read_text()
            refs = re.findall(r'(?:from\s*|import\s*\(|import\s*)[\'"]([^\'"]+)[\'"]', text)
            refs += re.findall(r'[\'"]((?:/?assets/|\./|\.\./)[^\'"\s]+\.(?:png|jpg|svg|webp|json|js|woff2?))[\'"]', text)
        else:
            refs = []
        for url in refs:
            target = local_path(owner, url)
            if target is None:
                continue
            if target in withheld:
                raise ValueError(f'Withheld asset referenced by {owner}: {target}')
            if target in pages:
                continue
            if not target.startswith('assets/') or Path(target).suffix.lower() not in ASSET_SUFFIXES:
                raise ValueError(f'Non-public local reference in {owner}: {url}')
            safe_file(root, target)
            if target not in found:
                found.add(target)
                queue.append(target)
    return found
