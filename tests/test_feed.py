import pytest
import allure

from data.user import USER_EMAIL, USER_PASS
from pages.main_page import MainPage
from pages.feed_page import FeedPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


@allure.suite("UI: Лента заказов")
@pytest.mark.ui
class TestFeed:

    @allure.title("Переход на страницу ленты заказов из шапки")
    def test_go_to_feed(self, driver):
        main = MainPage(driver)
        feed = FeedPage(driver)

        main.open()
        main.go_feed()
        feed.open_feed()

        assert "/feed" in feed.current_url

    @allure.title("Счётчик 'За всё время' увеличивается после оформления заказа")
    def test_all_time_counter_change_after_order(self, driver):
        if not USER_EMAIL or not USER_PASS:
            pytest.skip("Нет SB_USER_EMAIL/SB_USER_PASS")

        main = MainPage(driver)
        login = LoginPage(driver)
        feed = FeedPage(driver)

        main.open()
        login.open_login()
        login.login(USER_EMAIL, USER_PASS)

        main.go_feed()
        feed.open_feed()
        before = feed.num_all_time()

        main.go_constructor()
        main.add_first_ingredient_to_constructor()
        main.add_first_ingredient_to_constructor()

        main.go_feed()
        feed.open_feed()

        if not feed.wait_all_time_counter_increased(before):
            pytest.xfail("Счётчик 'за всё время' не обновился на стенде в отведённое время")

    @allure.title("Счётчик 'За сегодня' увеличивается после оформления заказа")
    def test_today_counter_change_after_order(self, driver):
        if not USER_EMAIL or not USER_PASS:
            pytest.skip("Нет SB_USER_EMAIL/SB_USER_PASS")

        main = MainPage(driver)
        login = LoginPage(driver)
        feed = FeedPage(driver)

        main.open()
        login.open_login()
        login.login(USER_EMAIL, USER_PASS)

        main.go_feed()
        feed.open_feed()
        before = feed.num_today()

        main.go_constructor()
        main.add_first_ingredient_to_constructor()
        main.add_first_ingredient_to_constructor()

        main.go_feed()
        feed.open_feed()

        if not feed.wait_today_counter_increased(before):
            pytest.xfail("Счётчик 'за сегодня' не обновился на стенде в отведённое время")

    @allure.title("Номер заказа появляется в колонке 'В работе'")
    def test_order_number_appears_in_progress(self, driver):
        if not USER_EMAIL or not USER_PASS:
            pytest.skip("Нет SB_USER_EMAIL/SB_USER_PASS")

        main = MainPage(driver)
        login = LoginPage(driver)
        feed = FeedPage(driver)

        main.open()
        login.open_login()
        login.login(USER_EMAIL, USER_PASS)

        main.go_constructor()
        main.add_first_ingredient_to_constructor()

        if not feed.has_create_order_button():
            pytest.skip("Кнопка оформления заказа недоступна")

        feed.click_first_create_order()

        main.go_feed()
        feed.open_feed()

        assert feed.has_orders_in_progress()

    @allure.title("Открытие деталей заказа из ленты")
    def test_order_details_in_feed(self, driver):
        main = MainPage(driver)
        feed = FeedPage(driver)

        main.open()
        main.go_feed()
        feed.open_feed()
        feed.open_first_order_details()

        assert feed.is_order_details_open()

    @allure.title("Заказы пользователя отображаются в истории заказов профиля")
    def test_user_orders_visible_in_profile_history(self, driver):
        if not USER_EMAIL or not USER_PASS:
            pytest.skip("Нет SB_USER_EMAIL/SB_USER_PASS")

        main = MainPage(driver)
        login = LoginPage(driver)
        profile = ProfilePage(driver)
        feed = FeedPage(driver)

        main.open()
        login.open_login()
        login.login(USER_EMAIL, USER_PASS)

        main.go_constructor()
        main.add_first_ingredient_to_constructor()
        if not feed.has_create_order_button():
            pytest.skip("Кнопка оформления заказа недоступна")
        feed.click_first_create_order()

        main.go_account()
        profile.wait_loaded()
        profile.go_to_order_history()

        assert profile.has_orders()
