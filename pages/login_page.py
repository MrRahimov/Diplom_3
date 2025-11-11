import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    login_btn_header = (By.XPATH, "//p[text()='Личный Кабинет']/ancestor::a")
    email_input = (By.NAME, "name")
    pass_input = (By.NAME, "Пароль")
    submit_btn = (By.XPATH, "//button[.//span[text()='Войти']]")
    forgot_password_link = (
        By.LINK_TEXT,
        "Восстановить пароль",
    )

    @allure.step("Открыть страницу логина через хедер")
    def open_login(self):
        self.click(self.login_btn_header)

    @allure.step("Логин с email и паролем")
    def login(self, email, password):
        self.find_visible(self.email_input).clear()
        self.find_visible(self.email_input).send_keys(email)
        self.find_visible(self.pass_input).clear()
        self.find_visible(self.pass_input).send_keys(password)
        self.click(self.submit_btn)

    @allure.step("Перейти на страницу восстановления пароля")
    def go_to_forgot_password(self):
        self.click(self.forgot_password_link)
