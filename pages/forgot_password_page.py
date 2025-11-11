import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ForgotPasswordPage(BasePage):
    root = (By.XPATH, "//h2[text()='Восстановление пароля']")
    email_input = (By.NAME, "name")
    restore_button = (
        By.XPATH,
        "//button[contains(@class,'button') and contains(.,'Восстановить')]",
    )

    @allure.step("Ожидать загрузки страницы восстановления пароля")
    def wait_loaded(self):
        self.find_visible(self.root)

    @allure.step("Ввести почту для восстановления пароля: {email}")
    def set_email(self, email: str):
        field = self.find_visible(self.email_input)
        field.clear()
        field.send_keys(email)

    @allure.step("Отправить форму восстановления пароля")
    def submit_restore(self):
        self.click(self.restore_button)
