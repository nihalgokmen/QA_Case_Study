import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

# create artifact dirs
Path("screenshots").mkdir(exist_ok=True)
Path("videos").mkdir(exist_ok=True)
Path("traces").mkdir(exist_ok=True)

@pytest.fixture(scope="session")
def _playwright():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(_playwright):
    # headless False during local debug; CI can set env var PLAYWRIGHT_HEADLESS=1
    headless = True if (Path.cwd().joinpath('CI').exists() or (os.environ.get('CI')=='true')) else False
    browser = _playwright.chromium.launch(headless=headless)
    yield browser
    browser.close()

@pytest.fixture
def page(browser, request):
    # create context with video recording
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()

    # start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    # test outcome handling
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        name = request.node.name
        # screenshot
        try:
            page.screenshot(path=f"screenshots/{name}.png", full_page=True)
        except Exception:
            pass
        # stop tracing to file
        try:
            trace_path = f"traces/{name}.zip"
            context.tracing.stop(path=trace_path)
        except Exception:
            pass
    else:
        # stop tracing without saving
        try:
            context.tracing.stop()
        except Exception:
            pass

    context.close()

# register hook so request.node.rep_call is available
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
