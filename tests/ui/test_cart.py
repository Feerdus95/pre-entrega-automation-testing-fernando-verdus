from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_add_first_product_to_cart(driver):
    LoginPage(driver).login()
    inventory = InventoryPage(driver)

    added_name = inventory.add_first_product()
    assert inventory.header.cart_badge_value() == "1", (
        f"Expected cart badge '1' after adding a product"
    )

    inventory.header.open_cart()
    assert "/cart.html" in driver.current_url, (
        f"Expected cart page URL, current URL: {driver.current_url}"
    )
    names = CartPage(driver).item_names()
    assert added_name in names, (
        f"Expected '{added_name}' in the cart, found: {names}"
    )
