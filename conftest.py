import logging
from pathlib import Path

import pytest

from utils.driver import create_driver

ROOT = Path(__file__).parent
SCREENSHOTS_DIR = ROOT / "reports" / "screenshots"
LOG_FILE = ROOT / "reports" / "logs" / "test_execution.log"


@pytest.fixture(scope="session", autouse=True)
def execution_logging():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
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
                SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
                path = SCREENSHOTS_DIR / f"{item.name}.png"
                drv.save_screenshot(str(path))
                logger.info("Screenshot saved: %s", path)
