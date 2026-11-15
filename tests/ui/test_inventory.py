from selenium.webdriver.support.ui import Select

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


def test_product_sorting(driver):
    helpers.login(driver)

    expected_first = {
        "Name (A to Z)": "Sauce Labs Backpack",
        "Name (Z to A)": "Test.allTheThings() T-Shirt (Red)",
        "Price (low to high)": "Sauce Labs Onesie",
        "Price (high to low)": "Sauce Labs Fleece Jacket",
    }
    for option, first_product in expected_first.items():
        dropdown = Select(helpers.element_visible(driver, helpers.SORT_DROPDOWN))
        dropdown.select_by_visible_text(option)
        helpers.wait_first_product_name(driver, first_product)
        names = [e.text for e in driver.find_elements(*helpers.PRODUCT_NAME)]
        assert names[0] == first_product, (
            f"{option}: expected {first_product!r} first, found {names[0]!r}"
        )


def test_product_detail_page_matches_catalog(driver):
    helpers.login(driver)
    catalog_name, catalog_price = helpers.first_product_details(driver)

    helpers.js_click(driver, helpers.FIRST_PRODUCT_NAME)
    helpers.wait(driver).until(helpers.EC.url_contains("inventory-item.html"))

    detail_name = helpers.element_visible(driver, helpers.PRODUCT_NAME).text
    detail_price = helpers.element_visible(driver, helpers.PRODUCT_PRICE).text
    assert detail_name == catalog_name, (
        f"Detail name {detail_name!r} differs from catalog {catalog_name!r}"
    )
    assert detail_price == catalog_price, (
        f"Detail price {detail_price!r} differs from catalog {catalog_price!r}"
    )

    helpers.js_click(driver, helpers.DETAIL_ADD_BUTTON)
    assert helpers.cart_badge_value(driver) == "1", (
        "Expected badge '1' after adding from the detail page"
    )
    driver.back()
    helpers.wait(driver).until(helpers.EC.url_contains("inventory.html"))
    assert helpers.cart_badge_value(driver) == "1", (
        "Cart badge must persist after navigating back from the detail page"
    )
