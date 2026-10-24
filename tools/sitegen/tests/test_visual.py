"""Kiểm tra trong trình duyệt thật: tràn ngang, lỗi console, tài nguyên lỗi, axe-core WCAG A/AA.

Dùng Chromium của Playwright. Nếu máy có sẵn một bản Chromium khác bản mà gói Playwright
mong đợi, đặt PLAYWRIGHT_CHROMIUM_EXECUTABLE hoặc để test tự tìm trong ms-playwright.
Ảnh chụp lưu ở tests/_artifacts/ (không commit).
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

from .conftest import AS_OF_V1, page_paths  # noqa: E402

pytestmark = pytest.mark.visual
AXE = Path(__file__).parent / "vendor" / "axe.min.js"
ARTIFACTS = Path(__file__).parent / "_artifacts"
WIDTHS = (390, 1440)


def chromium_executable() -> str | None:
    env = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    if env:
        return env
    found = sorted(Path.home().glob("AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe"))
    return str(found[-1]) if found else None


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        try:
            b = p.chromium.launch(executable_path=chromium_executable())
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"Không mở được Chromium: {exc}")
        yield b
        b.close()


@pytest.fixture(scope="module")
def results(browser, server, built):
    ARTIFACTS.mkdir(exist_ok=True)
    data = {}
    axe_source = AXE.read_text(encoding="utf-8")
    for width in WIDTHS:
        ctx = browser.new_context(viewport={"width": width, "height": 900}, reduced_motion="reduce")
        page = ctx.new_page()
        for path in page_paths(built[AS_OF_V1]) + ["/404.html"]:
            console: list[str] = []
            failed: list[str] = []

            def on_console(msg, sink=console):
                if msg.type == "error":
                    sink.append(msg.text)

            def on_failed(req, sink=failed):
                sink.append(req.url)

            page.on("console", on_console)
            page.on("requestfailed", on_failed)
            response = page.goto(server + path, wait_until="networkidle")
            overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            fonts_ok = page.evaluate(
                "document.fonts.ready.then(() => "
                "[...document.fonts].filter(f => f.status === 'error').length)"
            )
            page.add_script_tag(content=axe_source)
            axe = page.evaluate(
                "axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa']}})"
                ".then(r => r.violations.map(v => v.id + ' x' + v.nodes.length + ': '"
                " + v.nodes.slice(0, 2).map(n => n.target.join(' ')).join(' | ')))"
            )
            name = (path.strip("/").replace("/", "_") or "home") + f"-{width}.png"
            page.screenshot(path=str(ARTIFACTS / name), full_page=True)
            data[(width, path)] = {
                "status": response.status if response else None,
                "overflow": overflow,
                "console": list(console),
                "failed": list(failed),
                "fonts_error": fonts_ok,
                "axe": axe,
            }
            page.remove_listener("console", on_console)
            page.remove_listener("requestfailed", on_failed)
        ctx.close()
    return data


def test_no_horizontal_overflow(results):
    bad = {k: v["overflow"] for k, v in results.items() if v["overflow"] > 0}
    assert bad == {}


def test_no_console_errors_or_failed_requests(results):
    bad = {k: (v["console"], v["failed"]) for k, v in results.items() if v["console"] or v["failed"]}
    assert bad == {}


def test_fonts_load(results):
    assert all(v["fonts_error"] == 0 for v in results.values())


def test_axe_wcag_aa(results):
    bad = {k: v["axe"] for k, v in results.items() if v["axe"]}
    assert bad == {}


def test_status_codes(results):
    for (width, path), v in results.items():
        assert v["status"] == 200, (width, path)
