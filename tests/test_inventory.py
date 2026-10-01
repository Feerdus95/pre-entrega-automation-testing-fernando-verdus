from utils import helpers


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
