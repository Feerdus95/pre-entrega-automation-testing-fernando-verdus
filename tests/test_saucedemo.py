from utils import helpers


def test_successful_login(driver):
    helpers.login(driver)

    assert "/inventory.html" in driver.current_url, (
        f"Expected to land on inventory page, current URL: {driver.current_url}"
    )
    title = helpers.wait(driver).until(
        helpers.EC.visibility_of_element_located(helpers.PAGE_TITLE)
    ).text
    assert title == "Products", f"Expected 'Products' heading, found: '{title}'"
    assert driver.title == "Swag Labs", f"Expected page title 'Swag Labs', found: '{driver.title}'"
