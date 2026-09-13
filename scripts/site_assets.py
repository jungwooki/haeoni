"""Shared asset lookup and compatibility for immutable source archives."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = json.loads((ROOT / 'content/asset-path-migrations.json').read_text())
_OLD_PATHS = re.compile('|'.join(re.escape(p) for p in sorted(MIGRATIONS, key=len, reverse=True)))


def migrate_archived_asset_paths(html):
    """Adapt captured HTML in memory; never rewrite the historical source file."""
    return _OLD_PATHS.sub(lambda match: MIGRATIONS[match.group()], html)


def asset_url(asset_id):
    """Resolve an extensionless ID, e.g. images/people/doctor-lee, to a local URL."""
    if asset_id.startswith('/') or '..' in asset_id.split('/'):
        raise ValueError(f'Invalid asset ID: {asset_id}')
    parent, _, name = asset_id.rpartition('/')
    matches = [p for p in (ROOT / 'assets' / parent).glob(name + '.*') if p.is_file()]
    if len(matches) != 1:
        raise ValueError(f'Expected one asset for {asset_id}, found {len(matches)}')
    return matches[0].relative_to(ROOT).as_posix()
