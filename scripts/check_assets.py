"""Check asset inventory, reusable IDs, archive migration and live references."""
import json
from asset_catalog import CATALOG, ROOT, create_catalog
from site_assets import MIGRATIONS, asset_url, migrate_archived_asset_paths


def main():
    saved = json.loads(CATALOG.read_text())
    actual = create_catalog()
    assert saved == actual, 'Asset catalog is stale; run scripts/build_site.py'
    for asset in actual['assets']:
        assert asset_url(asset['id']) == asset['path'], asset['id']
        if asset['status'] == 'withheld':
            assert not asset['used_by'], ('Withheld asset is published', asset['path'])
    for old, target in MIGRATIONS.items():
        assert (ROOT / target).is_file(), target
        assert not (ROOT / old).exists(), ('Asset left in old location', old)
        assert migrate_archived_asset_paths(old) == target, old
        assert migrate_archived_asset_paths(target) == target, target
    for page in ROOT.glob('*.html'):
        html = page.read_text()
        assert migrate_archived_asset_paths(html) == html, ('Old asset path in published HTML', page.name)
    print(f'PASS: {len(actual["assets"])} asset IDs, hashes, catalog metadata, live references, withheld images and archive path migration.')


if __name__ == '__main__':
    main()
