import pytest
from playwright.sync_api import Page

@pytest.mark.checkout
def test_add_to_cart_and_checkout(page: Page):
    # Login first
    page.goto("https://www.saucedemo.com/")
    page.wait_for_selector('[data-test="username"]', timeout=15000)
    page.fill('[data-test="username"]', 'standard_user')
    page.fill('[data-test="password"]', 'secret_sauce')
    page.click('[data-test="login-button"]')
    page.wait_for_selector('.inventory_list', timeout=15000)

    # Add first product to cart
    add_buttons = page.locator('button[id^="add-to-cart"]')
    assert add_buttons.count() > 0
    add_buttons.nth(0).click()

    # Go to cart
    page.click('.shopping_cart_link')
    page.wait_for_selector('.cart_list', timeout=15000)

    # Start checkout
    page.click('[data-test="checkout"]')
    page.wait_for_selector('[data-test="firstName"]', timeout=15000)
    page.fill('[data-test="firstName"]', 'John')
    page.fill('[data-test="lastName"]', 'Doe')
    page.fill('[data-test="postalCode"]', '12345')
    page.click('[data-test="continue"]')

    # Summary displayed
    page.wait_for_selector('.summary_info', timeout=15000)
    assert page.locator('.summary_info').is_visible()


@pytest.mark.checkout
def test_checkout_cancel_returns_to_cart(page: Page):
    # Login and add product
    page.goto("https://www.saucedemo.com/")
    page.wait_for_selector('[data-test="username"]', timeout=15000)
    page.fill('[data-test="username"]', 'standard_user')
    page.fill('[data-test="password"]', 'secret_sauce')
    page.click('[data-test="login-button"]')
    page.wait_for_selector('.inventory_list', timeout=15000)

    # Add first product
    page.locator('button[id^="add-to-cart"]').nth(0).click()
    page.click('.shopping_cart_link')
    page.wait_for_selector('.cart_list', timeout=15000)

    # Go to checkout then cancel
    page.click('[data-test="checkout"]')
    page.wait_for_selector('[data-test="cancel"]', timeout=15000)
    page.click('[data-test="cancel"]')

    # Back to cart page
    assert page.url.endswith('/cart.html')
