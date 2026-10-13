#!/usr/bin/env python3
"""HTTP and adversarial publication regressions, independent of external EMR."""
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
from hashlib import sha256
import json
import tempfile
import threading
import unittest
from public_files import ROOT, dependency_files, load, safe_file
from check_public import check
from serve_public import make_handler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


class PublicHTTP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load(ROOT / 'config/public-files.json')
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0),
                                        make_handler(ROOT / 'dist', load(ROOT / 'vercel.json')))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def get(self, path, follow=True, method='GET'):
        opener = build_opener() if follow else build_opener(NoRedirect())
        try:
            response = opener.open(Request(self.base + path, method=method), timeout=10)
        except HTTPError as response:
            return response.code, response.headers, response.read()
        with response:
            return response.status, response.headers, response.read()

    def test_01_exact_public_contract(self):
        result = check()
        self.assertEqual(result['body_pages'], 81)
        self.assertFalse(result['external_emr_used'])

    def test_02_every_page_and_asset_served_unchanged(self):
        for name in self.config['body_pages'] + self.config['redirect_pages'] + self.config['assets']:
            with self.subTest(path=name):
                status, headers, data = self.get('/' + name)
                self.assertEqual(status, 200)
                self.assertEqual(data, (ROOT / name).read_bytes())
                self.assertEqual(headers.get('X-Robots-Tag'), 'noindex, nofollow')

    def test_03_private_paths_are_real_404(self):
        paths = list(load(ROOT / 'content/publication-withheld-images.json'))
        paths += ['content/legacy/index.html', 'content/care-review.json', 'content/family-pages.json',
                  'scripts/build_site.py', 'audit/2026-10-12/live-http.json', 'skills/technical-seo/SKILL.md',
                  'AGENTS.md', 'HAEON_SEARCH_MASTER.md', 'SEO_AUDIT_PRECHANGE_2026-10-12.md',
                  'CARE_PUBLICATION_REVIEW.md', 'assets/README.md', '.git/config', 'vercel.json',
                  'config/public-files.json', 'content/', 'assets/', '%63ontent/legacy/index.html']
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.get('/' + path, False)[0], 404)
                self.assertEqual(self.get('/' + path, False, 'HEAD')[0], 404)

    def test_04_policy_redirects_preserve_policy_bytes(self):
        for source in ['/', '/index.html']:
            for mode, page in [('privacy', 'privacy.html'), ('policy', 'terms.html')]:
                path = source + '?mode=' + mode + '&utm_source=regression'
                status, headers, _ = self.get(path, False)
                self.assertEqual(status, 307)
                self.assertEqual(headers['Location'], '/' + page + '?mode=' + mode + '&utm_source=regression')
                status, _, data = self.get(path)
                self.assertEqual(status, 200)
                self.assertEqual(data, (ROOT / page).read_bytes())
        for query in ['', '?mode=unknown', '?utm_source=regression']:
            self.assertEqual(self.get('/' + query)[2], (ROOT / 'index.html').read_bytes())

    def test_05_legacy_routes_not_silently_enabled(self):
        for item in load(ROOT / 'content/inventory.json'):
            if item['url'].startswith('/'):
                self.assertEqual(self.get(item['url'], False)[0], 404, item['url'])
        self.assertEqual(self.get('/does-not-exist', False)[0], 404)

    def test_06_p1_candidate_has_only_four_rewrites(self):
        candidate = load(ROOT / 'config/vercel-p1-routing.candidate.json')
        self.assertEqual({x['source'] for x in candidate['rewrites']},
                         {'/kids10', '/rhini1', '/woman1', '/pain1'})
        server = ThreadingHTTPServer(('127.0.0.1', 0), make_handler(ROOT / 'dist', candidate))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f'http://127.0.0.1:{server.server_port}'
            for name in ['kids10', 'rhini1', 'woman1', 'pain1']:
                with urlopen(base + '/' + name) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.read(), (ROOT / (name + '.html')).read_bytes())
                # Python 3.9 urllib does not follow 308 automatically; inspect each hop explicitly.
                try:
                    build_opener(NoRedirect()).open(base + '/' + name + '/?utm_source=test')
                    self.fail('Trailing-slash request must redirect')
                except HTTPError as redirect:
                    self.assertEqual(redirect.code, 308)
                    self.assertEqual(redirect.headers['Location'], '/' + name + '?utm_source=test')
                    with urlopen(base + redirect.headers['Location']) as response:
                        self.assertEqual(response.read(), (ROOT / (name + '.html')).read_bytes())
            for path in ['/93', '/165', '/152', '/does-not-exist']:
                with self.assertRaises(HTTPError) as raised:
                    urlopen(base + path)
                self.assertEqual(raised.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


class DependencySafety(unittest.TestCase):
    def test_missing_dependency_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'index.html').write_text('<img src="assets/missing.png">')
            with self.assertRaisesRegex(ValueError, 'Missing'):
                dependency_files(root, ['index.html'], set())

    def test_withheld_reference_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'index.html').write_text('<img src="assets/private.png">')
            with self.assertRaisesRegex(ValueError, 'Withheld'):
                dependency_files(root, ['index.html'], {'assets/private.png'})

    def test_symlink_and_traversal_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'target.txt').write_text('fixture, no patient information')
            (root / 'link.png').symlink_to(root / 'target.txt')
            for path in ['link.png', '../target.txt', '.git/config']:
                with self.assertRaises(ValueError):
                    safe_file(root, path)

    def test_css_font_and_srcset_dependency_closure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'assets/css').mkdir(parents=True)
            (root / 'assets/fonts').mkdir()
            (root / 'index.html').write_text('<link href="assets/css/a.css"><img srcset="assets/a.png 1x, assets/b.png 2x">')
            (root / 'assets/css/a.css').write_text('@import "b.css"; @font-face{src:url(../fonts/font.woff2)}')
            (root / 'assets/css/b.css').write_text('p{color:black}')
            for name in ['assets/fonts/font.woff2', 'assets/a.png', 'assets/b.png']:
                (root / name).write_bytes(b'test fixture')
            self.assertEqual(len(dependency_files(root, ['index.html'], set())), 6)

    def test_non_public_source_reference_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'index.html').write_text('<a href="content/source.html">internal</a>')
            with self.assertRaisesRegex(ValueError, 'Non-public'):
                dependency_files(root, ['index.html'], set())


if __name__ == '__main__':
    unittest.main(verbosity=2)
