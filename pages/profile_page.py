import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProfilePage(BasePage):
    profile_root = (By.XPATH, "//h2[text()='Профиль']")
    orders_tab = (By.XPATH, "//a[contains(@href,'/account/orders')]")
    logout_button = (By.XPATH, "//button[text()='Выход']")
    orders_list = (
        By.XPATH,
        "//ul[contains(@class,'OrderHistory_profile__list') or contains(@class,'Profile_ordersList')]//li",
    )

    @allure.step("Ожидать загрузки страницы профиля")
    def wait_loaded(self):
        self.find_visible(self.profile_root)

    @allure.step("Перейти в историю заказов")
    def go_to_order_history(self):
        self.click(self.orders_tab)

    @allure.step("Проверить, что в истории есть заказы")
    def has_orders(self) -> bool:
        return len(self.find_all(self.orders_list)) > 0

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.click(self.logout_button)
