import base64
import logging
import re
from datetime import datetime
from pathlib import Path

import pytest
from pytest_html import extras

from utils.api_client import ApiClient
from utils.driver import create_driver

ROOT = Path(__file__).parent
SCREENSHOTS_DIR = ROOT / "reports" / "screenshots"
LOG_FILE = ROOT / "reports" / "logs" / "test_execution.log"


@pytest.fixture(scope="session", autouse=True)
def execution_logging():
    # One log per run (mode "w"): the versioned file always reflects the last execution
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("saucedemo")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    yield
    logger.removeHandler(handler)
    handler.close()


def pytest_runtest_logstart(nodeid, location):
    logging.getLogger("saucedemo").info("START %s", nodeid)


@pytest.fixture
def driver():
    # Fresh browser per test so no test can inherit another test's state
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.fixture
def api_client():
    client = ApiClient()
    yield client
    client.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    logger = logging.getLogger("saucedemo")
    if report.when == "call":
        logger.info("RESULT %s: %s", report.nodeid, report.outcome.upper())
        if report.failed:
            logger.error("FAILURE DETAILS %s: %s", report.nodeid, str(report.longrepr))
            drv = item.funcargs.get("driver")
            if drv:
                _attach_screenshot(item, report, drv, logger)


def _attach_screenshot(item, report, drv, logger):
    try:
        url = drv.current_url
        png = drv.get_screenshot_as_png()
    except Exception as exc:  # noqa: BLE001
        # Broad on purpose: a dead browser raises WebDriverException or urllib3
        # connection errors, and any of them escaping here would replace the
        # test's real failure with an INTERNALERROR. Logged, never swallowed silently.
        logger.error("Screenshot failed for %s: %s: %s", report.nodeid, type(exc).__name__, exc)
        return
    safe_name = re.sub(r"[^A-Za-z0-9_-]", "-", item.name).rstrip("-")
    path = SCREENSHOTS_DIR / f"{safe_name}_{datetime.now():%Y%m%d_%H%M%S}.png"
    try:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        path.write_bytes(png)
        logger.info("Screenshot saved: %s (page: %s)", path, url)
    except OSError as exc:
        logger.error("Screenshot could not be written to %s: %s", path, exc)
    report.extras = getattr(report, "extras", []) + [
        extras.url(url, name="Page at failure"),
        extras.png(base64.b64encode(png).decode("ascii"), name=path.name),
    ]
