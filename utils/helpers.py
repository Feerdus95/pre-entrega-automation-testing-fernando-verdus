import logging

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
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
ERROR_BANNER = (By.CSS_SELECTOR, '[data-test="error"]')
LOGOUT_LINK = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')
PAGE_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
PRODUCTS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
# Live DOM has per-product add buttons (add-to-cart-<slug>), not a plain "add-to-cart";
# document-scoped: first inventory item's add button.
FIRST_PRODUCT_ADD = (By.CSS_SELECTOR, '[data-test="inventory-item"] [data-test^="add-to-cart"]')
FIRST_PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item"] [data-test="inventory-item-name"]')
DETAIL_ADD_BUTTON = (By.CSS_SELECTOR, '[data-test="add-to-cart"]')
CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
# Cart rows reuse the inventory-item markup: live DOM has no "cart-item-name",
# the name element carries data-test="inventory-item-name".
CART_ITEM_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')
FIRST_NAME_INPUT = (By.CSS_SELECTOR, '[data-test="firstName"]')
LAST_NAME_INPUT = (By.CSS_SELECTOR, '[data-test="lastName"]')
POSTAL_CODE_INPUT = (By.CSS_SELECTOR, '[data-test="postalCode"]')
CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
CANCEL_BUTTON = (By.CSS_SELECTOR, '[data-test="cancel"]')
FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')
ITEM_QUANTITY = (By.CSS_SELECTOR, '[data-test="item-quantity"]')
SUBTOTAL_LABEL = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
TAX_LABEL = (By.CSS_SELECTOR, '[data-test="tax-label"]')
TOTAL_LABEL = (By.CSS_SELECTOR, '[data-test="total-label"]')
COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

INVENTORY_ELEMENT = (By.ID, "inventory_container")
# The clickable burger wrapper: react-burger-menu only opens on native mouse
# events, so this element (not the inner icon) must receive the click.
NAV_MENU = (By.CSS_SELECTOR, ".bm-burger-button")
SORT_DROPDOWN = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')


def wait(driver: WebDriver):
    return WebDriverWait(driver, TIMEOUT)


def inventory_products(driver: WebDriver):
    wait(driver).until(EC.visibility_of_all_elements_located(PRODUCTS))
    return driver.find_elements(*PRODUCTS)


def wait_first_product_name(driver: WebDriver, expected: str) -> None:
    # Sorting reorders the same React nodes, so wait on the resulting order
    # rather than on element staleness; re-reads dodge stale references.
    def is_first(drv: WebDriver) -> bool:
        try:
            return drv.find_elements(*PRODUCT_NAME)[0].text == expected
        except (StaleElementReferenceException, IndexError):
            return False

    wait(driver).until(
        is_first, message=f"{expected!r} never became the first product"
    )


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


def go_to_checkout(driver: WebDriver) -> None:
    js_click(driver, CHECKOUT_BUTTON)
    wait(driver).until(EC.url_contains("checkout-step-one"))


def fill_buyer_info(driver: WebDriver, first: str = "Fernando", last: str = "Verdus", postal: str = "1000") -> None:
    driver.find_element(*FIRST_NAME_INPUT).send_keys(first)
    driver.find_element(*LAST_NAME_INPUT).send_keys(last)
    driver.find_element(*POSTAL_CODE_INPUT).send_keys(postal)


def logout(driver: WebDriver) -> None:
    # Native click here on purpose: the burger menu ignores JS-dispatched clicks.
    wait(driver).until(EC.element_to_be_clickable(NAV_MENU)).click()
    js_click(driver, LOGOUT_LINK)
    wait(driver).until(EC.visibility_of_element_located(LOGIN_BUTTON))
    logger.info("Logged out")
