"""CLI: python -m sitegen build|check|serve --brand tallyo [--as-of YYYY-MM-DD | --all]."""

from __future__ import annotations

import argparse
import functools
import http.server
import sys
from datetime import date

from .build import brand_dir, build, make_site, output_dir
from .checks import check_site
from .content import load_facts


def _as_of_list(args) -> list[date]:
    facts = load_facts(brand_dir(args.brand))
    if args.as_of:
        return [date.fromisoformat(args.as_of)]
    builds = [b.as_of for b in facts.builds]
    return builds if args.all else builds[:1]


def cmd_build(args) -> int:
    for as_of in _as_of_list(args):
        out = build(args.brand, as_of)
        print(f"built {out}")
    return 0


def cmd_check(args) -> int:
    worst = 0
    for as_of in _as_of_list(args):
        site = make_site(args.brand, as_of)
        out = output_dir(site.brand_dir, as_of)
        if not out.exists():
            print(f"Chưa build {out}. Chạy: python -m sitegen build --brand {args.brand}")
            return 2
        issues = check_site(out, site.facts, site.base_url, strict=args.strict)
        errors = [i for i in issues if i.severity == "error"]
        for issue in issues:
            print(issue)
        pages = len(list(out.rglob("*.html")))
        print(f"{as_of}: {pages} trang HTML, {len(errors)} lỗi, {len(issues) - len(errors)} cảnh báo")
        worst = max(worst, 1 if errors else 0)
    return worst


def cmd_serve(args) -> int:
    as_of = _as_of_list(args)[0]
    out = output_dir(brand_dir(args.brand), as_of)
    if not out.exists():
        build(args.brand, as_of)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def send_error(self, code, message=None, explain=None):
            page_404 = out / "404.html"
            if code == 404 and page_404.exists():
                body = page_404.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            super().send_error(code, message, explain)

    handler = functools.partial(Handler, directory=str(out))
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as httpd:
        print(f"Phục vụ {out} tại http://localhost:{args.port}/  (Ctrl+C để dừng)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sitegen", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, fn in (("build", cmd_build), ("check", cmd_check), ("serve", cmd_serve)):
        p = sub.add_parser(name)
        p.add_argument("--brand", default="tallyo")
        p.add_argument("--as-of", help="Ngày build YYYY-MM-DD (mặc định: bản đầu trong facts.builds)")
        p.add_argument("--all", action="store_true", help="Mọi bản trong facts.builds")
        if name == "check":
            p.add_argument("--strict", action="store_true", help="Văn bản pháp luật chưa xác minh là lỗi")
        if name == "serve":
            p.add_argument("--port", type=int, default=8081)
        p.set_defaults(func=fn)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
