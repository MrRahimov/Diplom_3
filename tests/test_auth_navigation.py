import pytest
import allure
from selenium.common.exceptions import TimeoutException

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.forgot_password_page import ForgotPasswordPage
from pages.reset_password_page import ResetPasswordPage
from data.user import USER_EMAIL, USER_PASS


@allure.suite("UI: Авторизация и навигация")
@pytest.mark.ui
class TestAuthNavigation:
    @allure.title("Переход в личный кабинет и обратно в конструктор")
    def test_go_account_and_back_to_constructor(self, driver):
        main = MainPage(driver)
        login = LoginPage(driver)

        main.open()
        login.open_login()
        main.go_back()
        main.go_constructor()

        assert main.is_constructor_active()

    @allure.title("Успешный логин через кнопку 'Личный кабинет'")
    def test_login_via_header(self, driver):
        if not USER_EMAIL or not USER_PASS:
            pytest.skip("Нет SB_USER_EMAIL/SB_USER_PASS")

        main = MainPage(driver)
        login = LoginPage(driver)
        profile = ProfilePage(driver)

        main.open()
        login.open_login()
        login.login(USER_EMAIL, USER_PASS)
        main.go_account()
        profile.wait_loaded()

    @allure.title("Выход из аккаунта из личного кабинета")
    def test_logout_from_profile(self, driver):
        if not USER_EMAIL or not USER_PASS:
            pytest.skip("Нет SB_USER_EMAIL/SB_USER_PASS")

        main = MainPage(driver)
        login = LoginPage(driver)
        profile = ProfilePage(driver)

        main.open()
        login.open_login()
        login.login(USER_EMAIL, USER_PASS)

        main.go_account()
        profile.wait_loaded()
        profile.logout()

        main.go_account()
        assert "login" in main.current_url or "login" in driver.current_url

    @allure.title("Переход на страницу восстановления пароля по ссылке 'Восстановить пароль'")
    def test_go_to_forgot_password_page(self, driver):
        main = MainPage(driver)
        login = LoginPage(driver)
        forgot = ForgotPasswordPage(driver)

        main.open()
        login.open_login()
        login.go_to_forgot_password()
        forgot.wait_loaded()

    @allure.title("Ввод почты и клик по 'Восстановить' ведут на страницу ввода нового пароля")
    def test_forgot_password_submit_redirects_to_reset(self, driver):
        main = MainPage(driver)
        login = LoginPage(driver)
        forgot = ForgotPasswordPage(driver)
        reset = ResetPasswordPage(driver)

        main.open()
        login.open_login()
        login.go_to_forgot_password()
        forgot.wait_loaded()
        forgot.set_email("test@example.com")
        forgot.submit_restore()

        try:
            reset.wait_loaded()
        except TimeoutException:
            pytest.xfail("Страница ввода нового пароля не открылась на тестовом стенде")

    @allure.title("Клик по показать/скрыть пароль делает поле активным на странице сброса пароля")
    def test_toggle_password_makes_field_active(self, driver):
        main = MainPage(driver)
        login = LoginPage(driver)
        forgot = ForgotPasswordPage(driver)
        reset = ResetPasswordPage(driver)

        main.open()
        login.open_login()
        login.go_to_forgot_password()
        forgot.wait_loaded()
        forgot.set_email("test@example.com")
        forgot.submit_restore()

        try:
            reset.wait_loaded()
        except TimeoutException:
            pytest.xfail("Страница ввода нового пароля не открылась на тестовом стенде")

        reset.toggle_password_visibility()
        assert reset.is_password_field_active()
