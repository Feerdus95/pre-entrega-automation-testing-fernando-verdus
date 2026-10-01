import pytest

from utils.driver import create_driver


@pytest.fixture
def driver():
    # Fresh browser per test so no test can inherit another test's state
    drv = create_driver()
    yield drv
    drv.quit()
