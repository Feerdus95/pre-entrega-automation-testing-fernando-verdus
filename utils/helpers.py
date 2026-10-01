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

USER_INPUT = (By.ID, "user-name")
PASSWORD_INPUT = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
PAGE_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
PRODUCTS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
# Live DOM has per-product add buttons (add-to-cart-<slug>), not a plain "add-to-cart";
# document-scoped: first inventory item's add button.
FIRST_PRODUCT_ADD = (By.CSS_SELECTOR, '[data-test="inventory-item"] [data-test^="add-to-cart"]')
CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
# Cart rows reuse the inventory-item markup: live DOM has no "cart-item-name",
# the name element carries data-test="inventory-item-name".
CART_ITEM_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')

INVENTORY_ELEMENT = (By.ID, "inventory_container")
# Live DOM burger button is data-test="open-menu" (no "bm-burger-button" attribute).
NAV_MENU = (By.CSS_SELECTOR, '[data-test="open-menu"]')
SORT_DROPDOWN = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')


def wait(driver: WebDriver):
    return WebDriverWait(driver, TIMEOUT)


def inventory_products(driver: WebDriver):
    wait(driver).until(EC.visibility_of_all_elements_located(PRODUCTS))
    return driver.find_elements(*PRODUCTS)


def element_visible(driver: WebDriver, locator: tuple) -> WebElement:
    """Wait for an element to be visible and return it (centralized TIMEOUT via wait())."""
    return wait(driver).until(EC.visibility_of_element_located(locator))


def js_click(driver: WebDriver, locator: tuple) -> None:
    # Native clicks are occasionally dropped before React's synthetic-event
    # system is listening (screenshot evidence: UI stays unchanged, no error).
    # A dispatched DOM click event is always captured.
    element = wait(driver).until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].click()", element)


def first_product_details(driver: WebDriver) -> tuple[str, str]:
    """Read the name and price of the first inventory product."""
    first = inventory_products(driver)[0]
    name = first.find_element(*PRODUCT_NAME).text
    price = first.find_element(*PRODUCT_PRICE).text
    logger.info("First product: %s - %s", name, price)
    return name, price


def login(driver: WebDriver, username: str = USERNAME, password: str = PASSWORD) -> None:
    logger.info("Opening login page: %s", BASE_URL)
    driver.get(BASE_URL)
    wait(driver).until(EC.visibility_of_element_located(USER_INPUT)).send_keys(username)
    wait(driver).until(EC.visibility_of_element_located(PASSWORD_INPUT)).send_keys(password)
    js_click(driver, LOGIN_BUTTON)
    # Wait for the application to complete authentication before validating inventory
    wait(driver).until(EC.url_contains("/inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_ELEMENT))
    logger.info("Login succeeded for user '%s' (password not logged)", username)


def add_first_product(driver: WebDriver) -> str:
    first = inventory_products(driver)[0]
    name = first.find_element(*PRODUCT_NAME).text
    # React can drop the first synthetic click before handlers are mounted
    # (observed suite flake): retry only while the badge is absent, so a
    # landed click never produces a double add.
    for attempt in range(1, 4):
        js_click(driver, FIRST_PRODUCT_ADD)
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CART_BADGE))
            break
        except TimeoutException:
            logger.warning("Cart badge absent after add click %d, retrying", attempt)
    logger.info("Added first product to cart: %s", name)
    return name


def cart_badge_value(driver: WebDriver) -> str:
    return wait(driver).until(EC.visibility_of_element_located(CART_BADGE)).text


def open_cart(driver: WebDriver) -> None:
    js_click(driver, CART_LINK)
    wait(driver).until(EC.url_contains("/cart.html"))
    wait(driver).until(EC.visibility_of_element_located(CART_ITEM_NAMES))
    logger.info("Cart page opened: %s", driver.current_url)


def cart_item_names(driver: WebDriver):
    return [item.text for item in driver.find_elements(*CART_ITEM_NAMES)]
