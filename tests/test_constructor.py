import pytest
import allure
from pages.main_page import MainPage


@allure.suite("UI: Конструктор")
@pytest.mark.ui
class TestConstructor:
    @allure.title("Переход в конструктор из шапки")
    def test_go_to_constructor(self, driver):
        page = MainPage(driver)
        page.open()
        page.go_constructor()
        assert page.is_constructor_active()

    @allure.title("Открытие модального окна ингредиента")
    def test_ingredient_modal_opens(self, driver):
        page = MainPage(driver)
        page.open()
        page.open_first_ingredient()
        assert page.is_ingredient_modal_open()

    @allure.title("Закрытие модального окна ингредиента")
    def test_ingredient_modal_closes(self, driver):
        page = MainPage(driver)
        page.open()
        page.open_first_ingredient()
        page.close_modal()
        assert page.wait_ingredient_modal_closed()

    @allure.title("Счётчик ингредиента увеличивается при добавлении в конструктор")
    def test_counter_increases_when_add_ingredient(self, driver):
        page = MainPage(driver)
        page.open()

        before = page.get_first_ingredient_counter()
        page.add_first_ingredient_to_constructor()
        after = page.get_first_ingredient_counter()

        assert after - before in (1, 2)
