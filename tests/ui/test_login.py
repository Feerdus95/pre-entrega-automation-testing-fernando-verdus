import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import load_json

LOGIN_DATA = load_json("login_data.json")


@pytest.mark.parametrize(
    "username,password",
    [pytest.param(c["username"], c["password"], id=c["id"]) for c in LOGIN_DATA["valid"]],
)
def test_successful_login(driver, username, password):
    LoginPage(driver).login(username, password)

    assert "/inventory.html" in driver.current_url, (
        f"Expected to land on inventory page, current URL: {driver.current_url}"
    )
    title = InventoryPage(driver).header.title()
    assert title == "Products", f"Expected 'Products' heading, found: '{title}'"
    assert driver.title == "Swag Labs", f"Expected page title 'Swag Labs', found: '{driver.title}'"


@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        pytest.param(c["username"], c["password"], c["expected_error"], id=c["id"])
        for c in LOGIN_DATA["invalid"]
    ],
)
def test_login_failure_shows_error_banner(driver, username, password, expected_error):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.submit(username, password)

    banner = login_page.error_message()
    assert expected_error in banner, f"Expected {expected_error!r} in banner: {banner!r}"
    assert "/inventory.html" not in driver.current_url, (
        f"Failed login must not reach the inventory, URL: {driver.current_url}"
    )


def test_back_button_after_logout_does_not_restore_session(driver):
    LoginPage(driver).login()
    InventoryPage(driver).header.logout()

    driver.back()
    assert InventoryPage(driver).rendered_product_count() == 0, (
        "Back button must not show inventory products after logout"
    )
    assert LoginPage(driver).is_displayed(), (
        "Expected the login form after logging out and navigating back"
    )
