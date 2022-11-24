from playwright.sync_api import Page
import pytest

def test_title(page: Page):
    page.goto("/login")
    assert page.title() == 'Iniciar Sesión'


def test_incorrect_credentials(page: Page):
    page.goto("/login")
    page.locator('#email_login').fill('jperez@gmail.com')
    page.locator('#password_login').fill('123123123123')
    page.locator('button#buttom_login').click()
    assert page.inner_text('.v-toast__text') == 'Credenciales incorrectos'

def test_correct_credentials(page: Page):
    page.goto("/login")
    page.locator('#email_login').fill('admin@gmail.com')
    page.locator('#password_login').fill('123456')
    page.locator('button#buttom_login').click()
    assert page.title() == 'Dashboard'
