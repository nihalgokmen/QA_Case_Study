import os
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

Path("screenshots").mkdir(exist_ok=True)
Path("videos").mkdir(exist_ok=True)
Path("traces").mkdir(exist_ok=True)

@pytest.fixture(scope="session")
def _playwright():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(_playwright):
    headless = True if (Path.cwd().joinpath('CI').exists() or (os.environ.get('CI')=='true')) else False
    browser = _playwright.chromium.launch(headless=headless)
    yield browser
    browser.close()

@pytest.fixture
def page(browser, request):
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()

    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        name = request.node.name
        try:
            page.screenshot(path=f"screenshots/{name}.png", full_page=True)
        except Exception:
            pass
        try:
            trace_path = f"traces/{name}.zip"
            context.tracing.stop(path=trace_path)
        except Exception:
            pass
    else:
        try:
            context.tracing.stop()
        except Exception:
            pass

    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
