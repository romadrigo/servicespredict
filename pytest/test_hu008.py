from playwright.sync_api import Page
import pytest

def test_title(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'

def test_up_modal_prediction(page: Page):
    page.goto("/predictions")
    page.locator('button#prediction_modal_up').click()
    assert page.inner_text('#title_modal_prediction') == 'Predicción de disponibilidad'

def test_submit_modal_prediction_with_only_number(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator('button#prediction_modal_up').click()
    assert page.inner_text('#title_modal_prediction') == 'Predicción de disponibilidad'
    page.locator('#phone_prediction_submit').fill('997365939')
    page.locator('button#prediction_submit').click()
    assert page.inner_text('.v-toast__text') == 'Success'
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 2
    row_locator  = page.locator('table tbody tr')
    assert row_locator.filter(has_text="09:00")

def test_submit_modal_prediction_with_number_financial_entity(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator('button#prediction_modal_up').click()
    assert page.inner_text('#title_modal_prediction') == 'Predicción de disponibilidad'
    page.locator(".v-input__append-inner").last.click()
    page.locator(".v-list-item:has-text('ABANCA')").last.click()
    page.locator('#phone_prediction_submit').fill('997365939')
    page.locator('button#prediction_submit').click()
    assert page.inner_text('.v-toast__text') == 'Success'
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 1
    row_locator  = page.locator('table tbody tr')
    assert row_locator.filter(has_text="09:00")

def test_submit_modal_prediction_without_inputs(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator('button#prediction_modal_up').click()
    assert page.inner_text('#title_modal_prediction') == 'Predicción de disponibilidad'
    page.locator('button#prediction_submit').click()
    assert page.inner_text('.v-toast__text') == 'Debe seleccionar al menos un filtro'