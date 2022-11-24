# from playwright.sync_api import Page
# import pytest

# def test_title(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()
#     page.goto("/user_register")
#     assert page.title() == 'Registro de usuario'


# def test_email_exists(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()

#     page.goto("/user_register")
#     page.locator('#name_register').fill('John Doe')
#     page.locator(".v-input__append-inner").first.click()
#     page.locator(".v-list-item:has-text('Usuario')").last.click()
#     page.locator(".v-input__append-inner").last.click()
#     page.locator(".v-list-item:has-text('Rodrigo Group')").last.click()
#     page.locator('#email_register').fill('admin@gmail.com')
#     page.locator('#password_register').fill('123456')
#     page.locator('#confirm_password_register').fill('123456')
#     page.locator('button#register').click()
#     assert page.inner_text('.v-toast__text') == 'El correo electrónico ya esta en uso'

# def test_incorrect_password_confirm(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()

#     page.goto("/user_register")
#     page.locator('#name_register').fill('John Doe')
#     page.locator(".v-input__append-inner").first.click()
#     page.locator(".v-list-item:has-text('Usuario')").last.click()
#     page.locator(".v-input__append-inner").last.click()
#     page.locator(".v-list-item:has-text('Rodrigo Group')").last.click()
#     page.locator('#email_register').fill('test@gmail.com')
#     page.locator('#password_register').fill('123456')
#     page.locator('#confirm_password_register').fill('12345')
#     page.locator('button#register').click()
#     assert page.inner_text('.v-toast__text') == 'Las contraseñas no coiciden'


# def test_correct_data_new_user(page: Page):
#     page.goto("/login")
#     page.locator('#email_login').fill('admin@gmail.com')
#     page.locator('#password_login').fill('123456')
#     page.locator('button#buttom_login').click()

#     page.goto("/user_register")
#     page.locator('#name_register').fill('John Doe')
#     page.locator(".v-input__append-inner").first.click()
#     page.locator(".v-list-item:has-text('Usuario')").last.click()
#     page.locator(".v-input__append-inner").last.click()
#     page.locator(".v-list-item:has-text('Rodrigo Group')").last.click()
#     page.locator('#email_register').fill('johndoe@gmail.com')
#     page.locator('#password_register').fill('123456')
#     page.locator('#confirm_password_register').fill('123456')
#     page.locator('button#register').click()
#     assert page.inner_text('.v-toast__text') == 'Success'

