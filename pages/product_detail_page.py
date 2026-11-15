from selenium.webdriver.common.by import By

from pages.header import Header
from pages.inventory_page import InventoryPage
from utils.helpers import element_visible, js_click


class ProductDetailPage:
    # Name and price reuse the inventory product markup
    NAME = InventoryPage.PRODUCT_NAME
    PRICE = InventoryPage.PRODUCT_PRICE
    ADD_BUTTON = (By.CSS_SELECTOR, '[data-test="add-to-cart"]')

    def __init__(self, driver):
        self.driver = driver
        self.header = Header(driver)

    def name(self) -> str:
        return element_visible(self.driver, self.NAME).text

    def price(self) -> str:
        return element_visible(self.driver, self.PRICE).text

    def add_to_cart(self) -> None:
        js_click(self.driver, self.ADD_BUTTON)
