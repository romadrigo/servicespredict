from playwright.sync_api import Page
import pytest


# def test_title(page: Page):
#     page.goto("/recover_password")
#     assert page.title() == 'Recuperar Contraseña'

# def test_recover_with_incorrect_email(page: Page):
#     page.goto("/recover_password")
#     page.locator('#email_recover').fill('rodrigo_test@gmail.com')
#     page.locator('button#recover').click()
#     assert page.inner_text('.v-toast__text') == 'El correo electrónico no esta registrado.'

# def test_recover_with_correct_email(page: Page):
#     page.goto("/recover_password")
#     page.locator('#email_recover').fill('rrodrigourbina@hotmail.com')
#     page.locator('button#recover').click()
#     assert page.inner_text('.v-toast__text') == 'Revisar su correo electrónico por favor'


# def test_restart_password_title(page: Page):
#     page.goto("/restart_password/10BH1IQB5SOP10")
#     assert page.title() == 'Restablecer contraseña'


def test_restart_password_incorrect_token(page: Page):
    page.goto("/restart_password/10BH1IQB5SOP101")
    assert page.inner_text('.v-toast__text') == 'Token no encontrado'


def test_restart_password_incorrect_confirm_password(page: Page):
    page.goto("/restart_password/10FQSSZS47S210")
    page.locator('#password_update').fill('123456')
    page.locator('#confirm_password_update').fill('12345')
    page.locator('button#restart_password').click()
    assert page.inner_text('.v-toast__text') == 'Las contraseñas no coiciden'

def test_restart_password_incorrect_long_confirm(page: Page):
    page.goto("/restart_password/10FQSSZS47S210")
    page.locator('#password_update').fill('12345')
    page.locator('#confirm_password_update').fill('12345')
    page.locator('button#restart_password').click()
    assert page.inner_text('.v-toast__text') == 'La contraseña debe tener al menos 6 digitos'

def test_restart_password_correct(page: Page):
    page.goto("/restart_password/10FQSSZS47S210")
    page.locator('#password_update').fill('123456')
    page.locator('#confirm_password_update').fill('123456')
    page.locator('button#restart_password').click()
    assert page.inner_text('.v-toast__text') == 'success'

