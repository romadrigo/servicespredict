from playwright.sync_api import Page
import pytest




# def test_search_prediction_without_filter_select(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/predictions")
#     page.locator('button#prediction_search').click()
#     assert page.inner_text('.v-toast__text') == 'Debe seleccionar una entidad financiera'

# def test_search_prediction_with_filter_select(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/predictions")
#     page.locator(".v-input__append-inner").first.click()
#     page.locator(".v-list-item:has-text('RODRIBANKSD')").last.click()
#     page.locator('button#prediction_search').click()
#     assert page.inner_text('.v-toast__text') == 'Success'


# def test_search_prediction_with_entity_without_prediction(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/predictions")
#     page.locator(".v-input__append-inner").first.click()
#     page.locator(".v-list-item:has-text('RODRIBANKS')").first.click()
#     page.locator('button#prediction_search').click()
#     assert page.inner_text('.v-toast__text') == 'Predicciones no encontrados ..'

# def test_export_prediction(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/predictions")
#     page.locator(".v-input__append-inner").first.click()
#     page.locator(".v-list-item:has-text('RODRIBANKSD')").first.click()
#     page.locator('button#prediction_search').click()
#     page.locator('button#prediction_export').click()
#     assert page.inner_text('.v-toast__text') == 'Archivo de predicción exportado con éxito'
