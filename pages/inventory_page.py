from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.header import Header
from utils.helpers import element_visible, is_visible, js_click, logger, wait


class InventoryPage:
    CONTAINER = (By.ID, "inventory_container")
    PRODUCTS = (By.CSS_SELECTOR, '[data-test="inventory-item"]')
    # Product markup is reused by the detail and cart pages
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    # Live DOM has per-product add buttons (add-to-cart-<slug>), not a plain "add-to-cart";
    # document-scoped: first inventory item's add button.
    FIRST_PRODUCT_ADD = (By.CSS_SELECTOR, '[data-test="inventory-item"] [data-test^="add-to-cart"]')
    FIRST_PRODUCT_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item"] [data-test="inventory-item-name"]')
    SORT_DROPDOWN = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')

    def __init__(self, driver):
        self.driver = driver
        self.header = Header(driver)

    def wait_until_loaded(self) -> None:
        wait(self.driver).until(EC.url_contains("/inventory.html"))
        element_visible(self.driver, self.CONTAINER)

    def products(self):
        wait(self.driver).until(EC.visibility_of_all_elements_located(self.PRODUCTS))
        return self.driver.find_elements(*self.PRODUCTS)

    def rendered_product_count(self) -> int:
        # Immediate count, no wait: used to prove the inventory is NOT shown
        return len(self.driver.find_elements(*self.PRODUCTS))

    def product_names(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(*self.PRODUCT_NAME)]

    def is_sort_control_visible(self) -> bool:
        return is_visible(self.driver, self.SORT_DROPDOWN)

    def first_product_details(self) -> tuple[str, str]:
        """Read the name and price of the first inventory product."""
        first = self.products()[0]
        name = first.find_element(*self.PRODUCT_NAME).text
        price = first.find_element(*self.PRODUCT_PRICE).text
        logger.info("First product: %s - %s", name, price)
        return name, price

    def add_first_product(self) -> str:
        first = self.products()[0]
        name = first.find_element(*self.PRODUCT_NAME).text
        # React can drop the first synthetic click before handlers are mounted
        # (observed suite flake): retry only while the badge is absent, so a
        # landed click never produces a double add.
        for attempt in range(1, 4):
            js_click(self.driver, self.FIRST_PRODUCT_ADD)
            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(Header.CART_BADGE))
                break
            except TimeoutException:
                logger.warning("Cart badge absent after add click %d, retrying", attempt)
        logger.info("Added first product to cart: %s", name)
        return name

    def sort_by(self, option: str) -> None:
        Select(element_visible(self.driver, self.SORT_DROPDOWN)).select_by_visible_text(option)

    def wait_first_product_name(self, expected: str) -> None:
        # Sorting reorders the same React nodes, so wait on the resulting order
        # rather than on element staleness; re-reads dodge stale references.
        def is_first(drv) -> bool:
            try:
                return drv.find_elements(*self.PRODUCT_NAME)[0].text == expected
            except (StaleElementReferenceException, IndexError):
                return False

        wait(self.driver).until(
            is_first, message=f"{expected!r} never became the first product"
        )

    def open_first_product_detail(self) -> None:
        js_click(self.driver, self.FIRST_PRODUCT_NAME)
        wait(self.driver).until(EC.url_contains("inventory-item.html"))
