from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import element_visible, is_visible, js_click, logger, wait


class Header:
    """Header shared by every authenticated page; pages hold one by composition."""

    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    # The clickable burger wrapper: react-burger-menu only opens on native mouse
    # events, so this element (not the inner icon) must receive the click.
    MENU_BUTTON = (By.CSS_SELECTOR, ".bm-burger-button")
    LOGOUT_LINK = (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')

    def __init__(self, driver):
        self.driver = driver

    def title(self) -> str:
        return element_visible(self.driver, self.TITLE).text

    def cart_badge_value(self) -> str:
        return element_visible(self.driver, self.CART_BADGE).text

    def is_menu_visible(self) -> bool:
        return is_visible(self.driver, self.MENU_BUTTON)

    def is_cart_link_visible(self) -> bool:
        return is_visible(self.driver, self.CART_LINK)

    def open_cart(self) -> None:
        js_click(self.driver, self.CART_LINK)
        wait(self.driver).until(EC.url_contains("/cart.html"))
        logger.info("Cart page opened: %s", self.driver.current_url)

    def logout(self) -> None:
        # Imported here: the login page leads to the inventory, which holds this header
        from pages.login_page import LoginPage

        # Native click here on purpose: the burger menu ignores JS-dispatched clicks.
        wait(self.driver).until(EC.element_to_be_clickable(self.MENU_BUTTON)).click()
        js_click(self.driver, self.LOGOUT_LINK)
        element_visible(self.driver, LoginPage.LOGIN_BUTTON)
        logger.info("Logged out")
