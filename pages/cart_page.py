from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.header import Header
from pages.inventory_page import InventoryPage
from utils.helpers import element_visible, js_click, wait


class CartPage:
    # Cart rows reuse the inventory-item markup: live DOM has no "cart-item-name",
    # the name element carries data-test="inventory-item-name".
    ITEM_NAMES = InventoryPage.PRODUCT_NAME
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def __init__(self, driver):
        self.driver = driver
        self.header = Header(driver)

    def item_names(self) -> list[str]:
        element_visible(self.driver, self.ITEM_NAMES)
        return [item.text for item in self.driver.find_elements(*self.ITEM_NAMES)]

    def go_to_checkout(self) -> None:
        js_click(self.driver, self.CHECKOUT_BUTTON)
        wait(self.driver).until(EC.url_contains("checkout-step-one"))
