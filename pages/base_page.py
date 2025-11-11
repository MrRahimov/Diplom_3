import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу: {url}")
    def open_url(self, url: str):
        self.driver.get(url)

    @allure.step("Найти видимый элемент: {locator}")
    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Найти элементы: {locator}")
    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        self.find_visible(locator).click()

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator):
        return self.find_visible(locator).text

    @allure.step("Ожидать исчезновения элемента: {locator}")
    def wait_invisible(self, locator, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        return True

    @allure.step("Клик по элементу через JS: {locator}")
    def click_js(self, locator):
        element = self.find_visible(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Прокрутить до элемента: {locator}")
    def scroll_to_element(self, locator):
        element = self.find_visible(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element,
        )
        return element

    @allure.step("Перетащить элемент JS из {source_locator} в {target_locator}")
    def drag_and_drop_js(self, source_locator, target_locator):
        source = self.find_visible(source_locator)
        target = self.find_visible(target_locator)
        self.driver.execute_script(
            """
            const src = arguments[0];
            const dst = arguments[1];
            const dt = new DataTransfer();
            const fire = (el, type) => el.dispatchEvent(
                new DragEvent(type, {bubbles:true, cancelable:true, dataTransfer: dt})
            );
            fire(src, 'dragstart');
            fire(dst, 'dragenter');
            fire(dst, 'dragover');
            fire(dst, 'drop');
            fire(src, 'dragend');
            """,
            source,
            target,
        )

    @allure.step("Нажать ESC")
    def press_esc(self):
        self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    @allure.step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()

    @allure.step("Выполнить JS: {script}")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    @allure.step("Вернуться на предыдущую страницу")
    def go_back(self):
        self.driver.back()

    @property
    def current_url(self):
        return self.driver.current_url
