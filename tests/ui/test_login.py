from utils import helpers

import pytest


def test_successful_login(driver):
    helpers.login(driver)

    assert "/inventory.html" in driver.current_url, (
        f"Expected to land on inventory page, current URL: {driver.current_url}"
    )
    title = helpers.element_visible(driver, helpers.PAGE_TITLE).text
    assert title == "Products", f"Expected 'Products' heading, found: '{title}'"
    assert driver.title == "Swag Labs", f"Expected page title 'Swag Labs', found: '{driver.title}'"


@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        pytest.param("locked_out_user", "secret_sauce", "Sorry, this user has been locked out.", id="locked-out"),
        pytest.param("standard_user", "wrong_password", "do not match any user", id="wrong-password"),
        pytest.param("", "secret_sauce", "Username is required", id="empty-username"),
        pytest.param("standard_user", "", "Password is required", id="empty-password"),
    ],
)
def test_login_failure_shows_error_banner(driver, username, password, expected_error):
    driver.get(helpers.BASE_URL)
    helpers.element_visible(driver, helpers.USER_INPUT).send_keys(username)
    helpers.element_visible(driver, helpers.PASSWORD_INPUT).send_keys(password)
    helpers.js_click(driver, helpers.LOGIN_BUTTON)

    banner = helpers.element_visible(driver, helpers.ERROR_BANNER)
    assert expected_error in banner.text, f"Expected {expected_error!r} in banner: {banner.text!r}"
    assert "/inventory.html" not in driver.current_url, (
        f"Failed login must not reach the inventory, URL: {driver.current_url}"
    )


def test_back_button_after_logout_does_not_restore_session(driver):
    helpers.login(driver)
    helpers.logout(driver)

    driver.back()
    assert len(driver.find_elements(*helpers.PRODUCTS)) == 0, (
        "Back button must not show inventory products after logout"
    )
    assert helpers.element_visible(driver, helpers.LOGIN_BUTTON), (
        "Expected the login form after logging out and navigating back"
    )
