from utils import helpers


def _add_one_product_and_open_checkout(driver):
    helpers.login(driver)
    helpers.add_first_product(driver)
    helpers.open_cart(driver)
    helpers.go_to_checkout(driver)


def test_checkout_completes_order(driver):
    _add_one_product_and_open_checkout(driver)
    helpers.fill_buyer_info(driver)
    helpers.js_click(driver, helpers.CONTINUE_BUTTON)
    helpers.wait(driver).until(helpers.EC.url_contains("checkout-step-two"))

    assert helpers.element_visible(driver, helpers.ITEM_QUANTITY).text == "1", (
        "Expected one item in the checkout summary"
    )
    assert helpers.element_visible(driver, helpers.SUBTOTAL_LABEL).text == "Item total: $29.99"
    assert helpers.element_visible(driver, helpers.TAX_LABEL).text == "Tax: $2.40"
    assert helpers.element_visible(driver, helpers.TOTAL_LABEL).text == "Total: $32.39"

    helpers.js_click(driver, helpers.FINISH_BUTTON)
    helpers.wait(driver).until(helpers.EC.url_contains("checkout-complete"))
    assert helpers.element_visible(driver, helpers.COMPLETE_HEADER).text == (
        "Thank you for your order!"
    )


def test_checkout_requires_postal_code(driver):
    _add_one_product_and_open_checkout(driver)
    helpers.fill_buyer_info(driver, postal="")
    helpers.js_click(driver, helpers.CONTINUE_BUTTON)

    banner = helpers.element_visible(driver, helpers.ERROR_BANNER)
    assert "Postal Code is required" in banner.text, f"Found: {banner.text!r}"
    assert "checkout-step-two" not in driver.current_url, (
        "Checkout must not advance without a postal code"
    )


def test_checkout_cancel_returns_to_cart(driver):
    _add_one_product_and_open_checkout(driver)
    helpers.js_click(driver, helpers.CANCEL_BUTTON)

    helpers.wait(driver).until(helpers.EC.url_contains("/cart.html"))
    assert helpers.cart_badge_value(driver) == "1", (
        "Cancelling checkout must leave the cart untouched"
    )
