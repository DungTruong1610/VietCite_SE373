"""Fixture chung: build site vào thư mục tạm (không đụng tới fixtures/ trong repo)."""

from __future__ import annotations

import functools
import http.server
import shutil
import threading
from collections.abc import Iterator
from datetime import date
from pathlib import Path

import pytest

from sitegen.build import build, repo_root

BRAND = "tallyo"
AS_OF_V1 = date(2026, 10, 24)
AS_OF_V2 = date(2026, 11, 10)
REPO_BRAND = repo_root() / "fixtures" / "brands" / BRAND


def copy_brand(root: Path) -> Path:
    target = root / "fixtures" / "brands" / BRAND
    target.mkdir(parents=True)
    for part in ("content", "theme"):
        shutil.copytree(REPO_BRAND / part, target / part)
    return target


@pytest.fixture(scope="session", autouse=True)
def _default_urls(monkeypatch_session):
    """Test luôn dùng URL mặc định trong facts.yaml, không phụ thuộc biến môi trường của máy."""
    monkeypatch_session.delenv("TALLYO_SITE_URL", raising=False)
    monkeypatch_session.delenv("WP_BASE_URL", raising=False)


@pytest.fixture(scope="session")
def monkeypatch_session() -> Iterator[pytest.MonkeyPatch]:
    mp = pytest.MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(scope="session")
def built(tmp_path_factory, _default_urls) -> dict[date, Path]:
    root = tmp_path_factory.mktemp("site-a")
    copy_brand(root)
    return {d: build(BRAND, d, root=root) for d in (AS_OF_V1, AS_OF_V2)}


@pytest.fixture(scope="session")
def built_again(tmp_path_factory, _default_urls) -> dict[date, Path]:
    root = tmp_path_factory.mktemp("site-b")
    copy_brand(root)
    return {d: build(BRAND, d, root=root) for d in (AS_OF_V1, AS_OF_V2)}


def page_paths(out: Path) -> list[str]:
    paths = []
    for f in sorted(out.rglob("index.html")):
        rel = f.parent.relative_to(out).as_posix()
        paths.append("/" if rel == "." else f"/{rel}/")
    return paths


@pytest.fixture(scope="session")
def server(built) -> Iterator[str]:
    """Phục vụ bản v1 qua HTTP để test giống trình duyệt và crawler thật."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(built[AS_OF_V1]))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    httpd.RequestHandlerClass.log_message = lambda *a, **k: None
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
