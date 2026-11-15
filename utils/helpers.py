import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger("saucedemo")

BASE_URL = "https://www.saucedemo.com/"
# Public demo credentials provided by SauceDemo
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
TIMEOUT = 10

# Shared by the login and checkout forms
ERROR_BANNER = (By.CSS_SELECTOR, '[data-test="error"]')


def wait(driver: WebDriver):
    return WebDriverWait(driver, TIMEOUT)


def element_visible(driver: WebDriver, locator: tuple) -> WebElement:
    """Wait for an element to be visible and return it (centralized TIMEOUT via wait())."""
    return wait(driver).until(
        EC.visibility_of_element_located(locator),
        message=f"Element {locator} not visible after {TIMEOUT}s",
    )


def is_visible(driver: WebDriver, locator: tuple) -> bool:
    """Same wait as element_visible, but answers instead of raising, for assertions."""
    try:
        element_visible(driver, locator)
        return True
    except TimeoutException:
        return False


def error_text(driver: WebDriver) -> str:
    # The error banner shares one markup across login and checkout forms
    return element_visible(driver, ERROR_BANNER).text


def js_click(driver: WebDriver, locator: tuple) -> None:
    # Native clicks are occasionally dropped before React's synthetic-event
    # system is listening (screenshot evidence: UI stays unchanged, no error).
    # A dispatched DOM click event is always captured.
    element = wait(driver).until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].click()", element)
