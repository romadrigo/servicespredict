from playwright.sync_api import Page
import pytest

def test_title(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'


def test_submit_search_prediction_with_only_number(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator('#phone_search_submit').fill('997365939')
    page.locator('button#prediction_search').click()
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 2

def test_submit_search_prediction_with_number_financial_entity(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator(".v-input__append-inner").first.click()
    page.locator(".v-list-item:has-text('ABANCA')").first.click()
    page.locator('#phone_search_submit').fill('997365939')
    page.locator('button#prediction_search').click()
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 1

def test_submit_search_prediction_with_only_financial_entity(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator(".v-input__append-inner").first.click()
    page.locator(".v-list-item:has-text('ABANCA')").first.click()
    page.locator('button#prediction_search').click()
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 50

def test_submit_search_prediction_with_dates_correct(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator('#init_date_search_submit').fill('2022-10-01')
    page.locator('#end_date_search_submit').fill('2022-10-02')
    page.locator('button#prediction_search').click()
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 2

def test_submit_search_prediction_with_dates_incorrect(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'    
    page.locator('#init_date_search_submit').fill('2022-09-29')
    page.locator('#end_date_search_submit').fill('2022-09-30')
    page.locator('button#prediction_search').click()
    assert page.inner_text('.v-toast__text') == 'Predicciones no encontrados ..'

def test_submit_search_prediction_without_inputs(page: Page):
    page.goto("/predictions")
    assert page.title() == 'Analisis de clientes'
    page.locator('button#prediction_search').click()
    assert page.inner_text('.v-toast__text') == 'Debe seleccionar al menos un filtro'