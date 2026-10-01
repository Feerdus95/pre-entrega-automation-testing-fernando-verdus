from utils import helpers


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
