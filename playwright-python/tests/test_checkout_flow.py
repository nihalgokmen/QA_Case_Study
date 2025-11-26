import pytest
from playwright.sync_api import Page

@pytest.mark.checkout
def test_add_to_cart_and_checkout(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.wait_for_selector('[data-test="username"]', timeout=15000)
    page.fill('[data-test="username"]', 'standard_user')
    page.fill('[data-test="password"]', 'secret_sauce')
    page.click('[data-test="login-button"]')
    page.wait_for_selector('.inventory_list', timeout=15000)

    add_buttons = page.locator('button[id^="add-to-cart"]')
    assert add_buttons.count() > 0
    add_buttons.nth(0).click()

    page.click('.shopping_cart_link')
    page.wait_for_selector('.cart_list', timeout=15000)

    page.click('[data-test="checkout"]')
    page.wait_for_selector('[data-test="firstName"]', timeout=15000)
    page.fill('[data-test="firstName"]', 'John')
    page.fill('[data-test="lastName"]', 'Doe')
    page.fill('[data-test="postalCode"]', '12345')
    page.click('[data-test="continue"]')

    page.wait_for_selector('.summary_info', timeout=15000)
    assert page.locator('.summary_info').is_visible()


@pytest.mark.checkout
def test_checkout_cancel_returns_to_cart(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.wait_for_selector('[data-test="username"]', timeout=15000)
    page.fill('[data-test="username"]', 'standard_user')
    page.fill('[data-test="password"]', 'secret_sauce')
    page.click('[data-test="login-button"]')
    page.wait_for_selector('.inventory_list', timeout=15000)

    page.locator('button[id^="add-to-cart"]').nth(0).click()
    page.click('.shopping_cart_link')
    page.wait_for_selector('.cart_list', timeout=15000)

    page.click('[data-test="checkout"]')
    page.wait_for_selector('[data-test="cancel"]', timeout=15000)
    page.click('[data-test="cancel"]')

    assert page.url.endswith('/cart.html')
