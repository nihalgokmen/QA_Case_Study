import pytest
from playwright.sync_api import Page

@pytest.mark.login
def test_login_success(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.wait_for_selector('[data-test="username"]', timeout=15000)
    page.fill('[data-test="username"]', 'standard_user')
    page.fill('[data-test="password"]', 'secret_sauce')
    page.click('[data-test="login-button"]')
    page.wait_for_selector('.inventory_list', timeout=15000)
    assert "inventory.html" in page.url

@pytest.mark.login
def test_login_failure(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.wait_for_selector('[data-test="username"]', timeout=15000)
    page.fill('[data-test="username"]', 'wrong_user')
    page.fill('[data-test="password"]', 'wrong_password')
    page.click('[data-test="login-button"]')
    
    err = page.locator('[data-test="error"]')
    err.wait_for(state="visible", timeout=10000)
    assert err.is_visible()
