#!/usr/bin/env python3
"""Local public-output HTTP fixture. Models only reviewed literal routes, not Vercel edge."""
import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs
from public_files import ROOT, load


def make_handler(output, config, preview=True):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(output), **kwargs)

        def route(self):
            parsed = urlsplit(self.path)
            query = parse_qs(parsed.query, keep_blank_values=True)
            for rule in config.get('redirects', []):
                if parsed.path != rule['source']:
                    continue
                if not all(c['type'] == 'query' and query.get(c['key']) == [c['value']]
                           for c in rule.get('has', [])):
                    continue
                target = rule['destination'] + ('?' + parsed.query if parsed.query else '')
                self.send_response(308 if rule.get('permanent', True) else 307)
                self.send_header('Location', target)
                self.send_header('Content-Length', '0')
                self.end_headers()
                return True
            for rule in config.get('rewrites', []):
                if parsed.path == rule['source']:
                    self.path = rule['destination'] + ('?' + parsed.query if parsed.query else '')
                    break
            return False

        def do_GET(self):
            if not self.route():
                super().do_GET()

        def do_HEAD(self):
            if not self.route():
                super().do_HEAD()

        def end_headers(self):
            if preview:
                self.send_header('X-Robots-Tag', 'noindex, nofollow')
            super().end_headers()

        def list_directory(self, path):
            self.send_error(404, 'Directory listing disabled')
            return None

        def log_message(self, *args):
            pass
    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8873)
    parser.add_argument('--candidate', action='store_true')
    args = parser.parse_args()
    path = 'config/vercel-p1-routing.candidate.json' if args.candidate else 'vercel.json'
    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(ROOT / 'dist', load(ROOT / path)))
    print(f'Local preview fixture http://127.0.0.1:{args.port}; serving dist only', flush=True)
    server.serve_forever()
