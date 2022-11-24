# from playwright.sync_api import Page
# import pytest

# def test_title(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/company_register")
#     assert page.title() == 'Registro de organización'


# def test_razon_social_exists(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/company_register")

#     page.locator('#name_register').fill('Rodrigo Group')
#     page.locator('#number_register').fill('10705004480705001234')
#     page.locator('button#register_company').click()
#     assert page.inner_text('.v-toast__text') == 'La organización ya fue creada anteriormente'

# def test_ruc_exists(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/company_register")

#     page.locator('#name_register').fill('Rodrigo Inject')
#     page.locator('#number_register').fill('10705004480705004485')
#     page.locator('button#register_company').click()
#     assert page.inner_text('.v-toast__text') == 'La organización ya fue creada anteriormente'

# def test_correct_data_for_new_company(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/company_register")

#     page.locator('#name_register').fill('LATAN CALL')
#     page.locator('#number_register').fill('10705004480705001244')
#     page.locator('button#register_company').click()
#     assert page.inner_text('.v-toast__text') == 'Success'

