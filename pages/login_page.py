from selenium.webdriver.common.by import By

from pages.inventory_page import InventoryPage
from utils.helpers import BASE_URL, PASSWORD, USERNAME, element_visible, error_text, is_visible, js_click, logger


class LoginPage:
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver):
        self.driver = driver

    def open(self) -> None:
        logger.info("Opening login page: %s", BASE_URL)
        self.driver.get(BASE_URL)

    def submit(self, username: str, password: str) -> None:
        element_visible(self.driver, self.USERNAME_INPUT).send_keys(username)
        element_visible(self.driver, self.PASSWORD_INPUT).send_keys(password)
        js_click(self.driver, self.LOGIN_BUTTON)

    def login(self, username: str = USERNAME, password: str = PASSWORD) -> None:
        self.open()
        self.submit(username, password)
        # Wait for the application to complete authentication before validating inventory
        InventoryPage(self.driver).wait_until_loaded()
        logger.info("Login succeeded for user '%s' (password not logged)", username)

    def error_message(self) -> str:
        return error_text(self.driver)

    def is_displayed(self) -> bool:
        return is_visible(self.driver, self.LOGIN_BUTTON)
