from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage


def test_inventory_catalog(driver):
    LoginPage(driver).login()
    inventory = InventoryPage(driver)

    assert driver.title == "Swag Labs", f"Expected page title 'Swag Labs', found: '{driver.title}'"

    products = inventory.products()
    assert len(products) > 0, "Expected at least one product visible in the inventory"

    for label, visible in [
        ("main navigation menu", inventory.header.is_menu_visible()),
        ("shopping cart", inventory.header.is_cart_link_visible()),
        ("product sort control", inventory.is_sort_control_visible()),
    ]:
        assert visible, f"Expected {label} to be visible"

    first_name, first_price = inventory.first_product_details()
    assert first_name.strip(), f"Expected non-empty product name, found: '{first_name}'"
    assert first_price.strip(), f"Expected non-empty product price, found: '{first_price}'"


def test_product_sorting(driver):
    LoginPage(driver).login()
    inventory = InventoryPage(driver)

    expected_first = {
        "Name (A to Z)": "Sauce Labs Backpack",
        "Name (Z to A)": "Test.allTheThings() T-Shirt (Red)",
        "Price (low to high)": "Sauce Labs Onesie",
        "Price (high to low)": "Sauce Labs Fleece Jacket",
    }
    for option, first_product in expected_first.items():
        inventory.sort_by(option)
        inventory.wait_first_product_name(first_product)
        names = inventory.product_names()
        assert names[0] == first_product, (
            f"{option}: expected {first_product!r} first, found {names[0]!r}"
        )


def test_product_detail_page_matches_catalog(driver):
    LoginPage(driver).login()
    inventory = InventoryPage(driver)
    catalog_name, catalog_price = inventory.first_product_details()

    inventory.open_first_product_detail()
    detail = ProductDetailPage(driver)

    detail_name = detail.name()
    detail_price = detail.price()
    assert detail_name == catalog_name, (
        f"Detail name {detail_name!r} differs from catalog {catalog_name!r}"
    )
    assert detail_price == catalog_price, (
        f"Detail price {detail_price!r} differs from catalog {catalog_price!r}"
    )

    detail.add_to_cart()
    assert detail.header.cart_badge_value() == "1", (
        "Expected badge '1' after adding from the detail page"
    )
    driver.back()
    inventory.wait_until_loaded()
    assert inventory.header.cart_badge_value() == "1", (
        "Cart badge must persist after navigating back from the detail page"
    )
