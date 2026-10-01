from utils import helpers


def test_successful_login(driver):
    helpers.login(driver)

    assert "/inventory.html" in driver.current_url, (
        f"Expected to land on inventory page, current URL: {driver.current_url}"
    )
    title = helpers.element_visible(driver, helpers.PAGE_TITLE).text
    assert title == "Products", f"Expected 'Products' heading, found: '{title}'"
    assert driver.title == "Swag Labs", f"Expected page title 'Swag Labs', found: '{driver.title}'"


def test_inventory_catalog(driver):
    helpers.login(driver)

    assert driver.title == "Swag Labs", f"Expected page title 'Swag Labs', found: '{driver.title}'"

    products = helpers.inventory_products(driver)
    assert len(products) > 0, "Expected at least one product visible in the inventory"

    for label, locator in [
        ("main navigation menu", helpers.NAV_MENU),
        ("shopping cart", helpers.CART_LINK),
        ("product sort control", helpers.SORT_DROPDOWN),
    ]:
        assert helpers.element_visible(driver, locator), f"Expected {label} to be visible"

    first_name, first_price = helpers.first_product_details(driver)
    assert first_name.strip(), f"Expected non-empty product name, found: '{first_name}'"
    assert first_price.strip(), f"Expected non-empty product price, found: '{first_price}'"


def test_add_first_product_to_cart(driver):
    helpers.login(driver)

    added_name = helpers.add_first_product(driver)
    assert helpers.cart_badge_value(driver) == "1", (
        f"Expected cart badge '1' after adding a product"
    )

    helpers.open_cart(driver)
    assert "/cart.html" in driver.current_url, (
        f"Expected cart page URL, current URL: {driver.current_url}"
    )
    names = helpers.cart_item_names(driver)
    assert added_name in names, (
        f"Expected '{added_name}' in the cart, found: {names}"
    )
