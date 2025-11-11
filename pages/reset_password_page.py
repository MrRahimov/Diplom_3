import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class ResetPasswordPage(BasePage):
    root = (
        By.XPATH,
        "//h2[contains(text(),'Восстановление пароля') or "
        "contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'reset password')]",
    )
    password_input = (
        By.XPATH,
        "//input[@type='password' or @name='Пароль' or @name='password']",
    )
    toggle_password_button = (
        By.XPATH,
        "("
        "//input[@type='password' or @name='Пароль' or @name='password']"
        "/following-sibling::*[1]"
        ")[1]",
    )

    @allure.step("Ожидать загрузки страницы ввода нового пароля")
    def wait_loaded(self):
        try:
            self.find_visible(self.password_input)
        except TimeoutException:
            self.find_visible(self.root)

    @allure.step("Клик по кнопке показать/скрыть пароль")
    def toggle_password_visibility(self):
        self.click(self.toggle_password_button)

    @allure.step("Поле пароля активно")
    def is_password_field_active(self) -> bool:
        field = self.find_visible(self.password_input)
        return field == self.driver.switch_to.active_element
