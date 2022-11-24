from playwright.sync_api import Page
import pytest


def test_show_detail_history_call(page: Page):
    page.goto("/login")
    page.locator('#email_login').fill('admin@gmail.com')
    page.locator('#password_login').fill('123456')
    page.locator('button#buttom_login').click()
    page.goto("/history-calls")
    page.locator('button#show_detail_history_call').first.click()
    rows = page.locator('div#detail_history_call div table tbody tr')
    count = rows.count()
    print(count)
    for i in range(count):
        print(rows.nth(i).text_content())        
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 100
