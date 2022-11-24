from playwright.sync_api import Page
import pytest

def test_title(page: Page):
    page.goto("/history-calls")
    assert page.title() == 'Historial de llamadas'

def test_submit_search_history_call_with_dates_correct(page: Page):
    page.goto("/history-calls")
    assert page.title() == 'Historial de llamadas'
    page.locator('#init_date_search_submit').fill('2022-09-27')
    page.locator('#end_date_search_submit').fill('2022-09-28')
    page.locator('button#history_calls_search').click()
    rows = page.locator('table tbody tr')
    count = rows.count()
    for i in range(count):
        print(rows.nth(i).text_content())
    rows.evaluate_all("list => list.map(element => element.textContent)")
    assert rows.count() == 2

def test_submit_search_history_call_with_dates_incorrect(page: Page):
    page.goto("/history-calls")
    assert page.title() == 'Historial de llamadas'    
    page.locator('#init_date_search_submit').fill('2022-09-29')
    page.locator('#end_date_search_submit').fill('2022-09-30')
    page.locator('button#history_calls_search').click()
    assert page.inner_text('.v-toast__text') == 'Historial de llamadas no encontrados ..'


def test_upload_without_file(page: Page):
    page.goto("/history-calls")
    assert page.title() == 'Historial de llamadas'
    page.locator('button#history_calls_modal_up').click()
    page.locator('button#history_calls_import').click()
    assert page.inner_text('.v-toast__text') == 'No se encontro ningún archivo'


def test_upload_with_file(page: Page):
    page.goto("/history-calls")
    assert page.title() == 'Historial de llamadas'
    page.locator('button#history_calls_modal_up').click()
    page.locator('input#upload_file_history_call').set_input_files('DataTest.xlsx')
    page.locator('button#history_calls_import').click()
    assert page.inner_text('.v-toast__text') == 'Historial de llamadas guardado con éxito.'



