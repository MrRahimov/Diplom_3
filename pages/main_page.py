import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage

BASE_URL = "https://stellarburgers.education-services.ru/"


class MainPage(BasePage):
    url = BASE_URL

    login_button_on_main = (
        By.XPATH,
        "//button//*[text()='Войти в аккаунт']/..",
    )
    account_button = (By.XPATH, "//p[text()='Личный Кабинет']/ancestor::a")
    constructor_tab = (By.XPATH, "//span[text()='Конструктор']/ancestor::a")
    constructor_header = (By.XPATH, "//*[text()='Соберите бургер']")
    logo_constructor = (
        By.XPATH,
        "//div[contains(@class,'AppHeader_header')]/a[contains(@href,'/')]",
    )
    feed_tab = (By.XPATH, "//p[text()='Лента Заказов']/ancestor::a")

    ingredient_card = (By.CSS_SELECTOR, 'a[href^="/ingredient/"]')
    constructor_drop = (
        By.XPATH,
        "//section[contains(@class,'BurgerConstructor')]",
    )
    ingredient_modal = (
        By.XPATH,
        "//section[contains(@class,'Modal') and .//h2]",
    )
    close_modal_btn = (
        By.XPATH,
        "//section[contains(@class,'Modal')]//button[contains(@class,'close')]",
    )
    ingredient_counter_on_card = (
        By.CSS_SELECTOR,
        'a[href^="/ingredient/"] p[class*="counter__num"]',
    )

    @allure.step("Открыть главную страницу")
    def open(self):
        self.open_url(self.url)

    @allure.step("Открыть форму логина")
    def open_login(self):
        if self.find_all(self.login_button_on_main):
            self.click(self.login_button_on_main)
        else:
            self.click(self.account_button)

    @allure.step("Перейти в конструктор")
    def go_constructor(self):
        if self.find_all(self.constructor_tab):
            self.click(self.constructor_tab)
        else:
            self.click(self.logo_constructor)

    @allure.step("Конструктор открыт")
    def is_constructor_active(self):
        try:
            self.find_visible(self.constructor_header)
            return True
        except Exception:
            return False

    @allure.step("Перейти в ленту заказов")
    def go_feed(self):
        self.click(self.feed_tab)

    @allure.step("Перейти в личный кабинет")
    def go_account(self):
        self.click(self.account_button)

    @allure.step("Открыть первый ингредиент в модалке")
    def open_first_ingredient(self):
        self.scroll_to_element(self.ingredient_card)
        self.click_js(self.ingredient_card)

    @allure.step("Закрыть модалку ингредиента")
    def close_modal(self):
        self.click_js(self.close_modal_btn)

    @allure.step("Добавить первый ингредиент в конструктор")
    def add_first_ingredient_to_constructor(self):
        self.drag_and_drop_js(self.ingredient_card, self.constructor_drop)

    @allure.step("Модальное окно ингредиента открыто")
    def is_ingredient_modal_open(self) -> bool:
        try:
            self.find_visible(self.ingredient_modal)
            return True
        except Exception:
            return False

    @allure.step("Ожидать закрытия модального окна ингредиента")
    def wait_ingredient_modal_closed(self) -> bool:
        self.wait_invisible(self.ingredient_modal)
        return True

    @allure.step("Получить значение счётчика первого ингредиента")
    def get_first_ingredient_counter(self) -> int:
        counters = self.find_all(self.ingredient_counter_on_card)
        if counters:
            text = counters[0].text or "0"
            try:
                return int(text)
            except ValueError:
                return 0
        return 0
