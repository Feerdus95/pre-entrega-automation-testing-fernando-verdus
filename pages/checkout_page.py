from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.header import Header
from utils.helpers import element_visible, error_text, js_click, wait


class CheckoutPage:
    """The three checkout steps: buyer info, overview and completion."""

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

    def __init__(self, driver):
        self.driver = driver
        self.header = Header(driver)

    def fill_buyer_info(self, first: str = "Fernando", last: str = "Verdus", postal: str = "1000") -> None:
        element_visible(self.driver, self.FIRST_NAME_INPUT).send_keys(first)
        element_visible(self.driver, self.LAST_NAME_INPUT).send_keys(last)
        element_visible(self.driver, self.POSTAL_CODE_INPUT).send_keys(postal)

    def click_continue(self) -> None:
        js_click(self.driver, self.CONTINUE_BUTTON)

    def continue_to_overview(self) -> None:
        self.click_continue()
        wait(self.driver).until(EC.url_contains("checkout-step-two"))

    def item_quantity(self) -> str:
        return element_visible(self.driver, self.ITEM_QUANTITY).text

    def subtotal(self) -> str:
        return element_visible(self.driver, self.SUBTOTAL_LABEL).text

    def tax(self) -> str:
        return element_visible(self.driver, self.TAX_LABEL).text

    def total(self) -> str:
        return element_visible(self.driver, self.TOTAL_LABEL).text

    def finish_order(self) -> None:
        js_click(self.driver, self.FINISH_BUTTON)
        wait(self.driver).until(EC.url_contains("checkout-complete"))

    def complete_header(self) -> str:
        return element_visible(self.driver, self.COMPLETE_HEADER).text

    def cancel(self) -> None:
        js_click(self.driver, self.CANCEL_BUTTON)
        wait(self.driver).until(EC.url_contains("/cart.html"))

    def error_message(self) -> str:
        return error_text(self.driver)
