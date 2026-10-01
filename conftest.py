from pathlib import Path

import pytest

from utils.driver import create_driver

SCREENSHOTS_DIR = Path(__file__).parent / "reports" / "screenshots"


@pytest.fixture
def driver():
    # Fresh browser per test so no test can inherit another test's state
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Capture evidence while the browser from the failed test is still open
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            path = SCREENSHOTS_DIR / f"{item.name}.png"
            drv.save_screenshot(str(path))
