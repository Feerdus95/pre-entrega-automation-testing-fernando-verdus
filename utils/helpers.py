import logging

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
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
PAGE_TITLE = (By.CSS_SELECTOR, ".title")
PRODUCTS = (By.CSS_SELECTOR, ".inventory_item")
PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_item_price")
FIRST_PRODUCT_ADD = (By.CSS_SELECTOR, ".btn_primary")  # used relative to a product element
CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
CART_LINK = (By.CSS_SELECTOR, "#shopping_cart_container a")
CART_ITEM_NAMES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")

INVENTORY_ELEMENT = (By.ID, "inventory_container")
NAV_MENU = (By.CSS_SELECTOR, ".bm-burger-button")
SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")


def wait(driver: WebDriver):
    return WebDriverWait(driver, TIMEOUT)


def inventory_products(driver: WebDriver):
    wait(driver).until(EC.visibility_of_all_elements_located(PRODUCTS))
    return driver.find_elements(*PRODUCTS)


def login(driver: WebDriver, username: str = USERNAME, password: str = PASSWORD) -> None:
    logger.info("Opening login page: %s", BASE_URL)
    driver.get(BASE_URL)
    wait(driver).until(EC.visibility_of_element_located(USER_INPUT)).send_keys(username)
    wait(driver).until(EC.visibility_of_element_located(PASSWORD_INPUT)).send_keys(password)
    wait(driver).until(EC.element_to_be_clickable(LOGIN_BUTTON)).click()
    # Wait for the application to complete authentication before validating inventory
    wait(driver).until(EC.url_contains("/inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_ELEMENT))
    logger.info("Login succeeded for user '%s' (password not logged)", username)


def add_first_product(driver: WebDriver) -> str:
    first = inventory_products(driver)[0]
    name = first.find_element(*PRODUCT_NAME).text
    first.find_element(*FIRST_PRODUCT_ADD).click()
    logger.info("Added first product to cart: %s", name)
    return name


def cart_badge_value(driver: WebDriver) -> str:
    return wait(driver).until(EC.visibility_of_element_located(CART_BADGE)).text


def open_cart(driver: WebDriver) -> None:
    wait(driver).until(EC.element_to_be_clickable(CART_LINK)).click()
    wait(driver).until(EC.url_contains("/cart.html"))
    wait(driver).until(EC.visibility_of_element_located(CART_ITEM_NAMES))
    logger.info("Cart page opened: %s", driver.current_url)


def cart_item_names(driver: WebDriver):
    return [item.text for item in driver.find_elements(*CART_ITEM_NAMES)]
