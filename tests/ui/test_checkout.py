from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _add_one_product_and_open_checkout(driver) -> CheckoutPage:
    LoginPage(driver).login()
    inventory = InventoryPage(driver)
    inventory.add_first_product()
    inventory.header.open_cart()
    CartPage(driver).go_to_checkout()
    return CheckoutPage(driver)


def test_checkout_completes_order(driver):
    checkout = _add_one_product_and_open_checkout(driver)
    checkout.fill_buyer_info()
    checkout.continue_to_overview()

    assert checkout.item_quantity() == "1", (
        "Expected one item in the checkout summary"
    )
    assert checkout.subtotal() == "Item total: $29.99"
    assert checkout.tax() == "Tax: $2.40"
    assert checkout.total() == "Total: $32.39"

    checkout.finish_order()
    assert checkout.complete_header() == (
        "Thank you for your order!"
    )


def test_checkout_requires_postal_code(driver):
    checkout = _add_one_product_and_open_checkout(driver)
    checkout.fill_buyer_info(postal="")
    checkout.click_continue()

    banner = checkout.error_message()
    assert "Postal Code is required" in banner, f"Found: {banner!r}"
    assert "checkout-step-two" not in driver.current_url, (
        "Checkout must not advance without a postal code"
    )


def test_checkout_cancel_returns_to_cart(driver):
    checkout = _add_one_product_and_open_checkout(driver)
    checkout.cancel()

    assert checkout.header.cart_badge_value() == "1", (
        "Cancelling checkout must leave the cart untouched"
    )
