import re
import time
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class FeedPage(BasePage):
    feed_tab = (By.CSS_SELECTOR, 'a[href="/feed"]')
    overlay = (By.CSS_SELECTOR, "[class*='Modal_modal_overlay']")

    count_all_time_ru = (
        By.XPATH,
        "//*[contains(., 'Выполнено за всё время')]/ancestor::*[self::section or self::div][1]",
    )
    count_today_ru = (
        By.XPATH,
        "//*[contains(., 'Выполнено за сегодня')]/ancestor::*[self::section or self::div][1]",
    )
    count_all_time_en = (
        By.XPATH,
        "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'all time')]/ancestor::*[self::section or self::div][1]",
    )
    count_today_en = (
        By.XPATH,
        "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'today')]/ancestor::*[self::section or self::div][1]",
    )

    create_order_button = (
        By.XPATH,
        "//button[contains(@class,'button_button_type_primary') and .//*[text()='Оформить заказ']]",
    )
    in_progress_column = (
        By.XPATH,
        "//ul[contains(@class,'OrderFeed_orderListReady') or contains(@class,'OrderFeed_orderListInProgress')]",
    )

    order_items = (
        By.XPATH,
        "//ul[contains(@class,'OrderFeed_list') or contains(@class,'OrderFeed_orderList')]/li",
    )
    order_detail_modal = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal') and .//*[contains(text(),'#')]]",
    )

    @allure.step("Закрыть оверлей, если он есть")
    def _dismiss_overlay_hard(self):
        try:
            self.wait_invisible(self.overlay, timeout=1)
            return
        except TimeoutException:
            pass
        try:
            self.execute_script(
                """
                const nodes = document.querySelectorAll('[class*="Modal_modal_overlay"]');
                nodes.forEach(n => n.remove());
                """
            )
        except Exception:
            pass

    @allure.step("Открыть ленту заказов")
    def open_feed(self, timeout: int = 3):
        self._dismiss_overlay_hard()
        self.click_js(self.feed_tab)
        if not self._any_counter_block(timeout=timeout):
            raise TimeoutException(
                "Сводные счётчики в Ленте не появились за отведённое время"
            )

    def _any_counter_block(self, timeout: int = 3) -> bool:
        locs = (
            self.count_all_time_ru,
            self.count_all_time_en,
            self.count_today_ru,
            self.count_today_en,
        )
        end = time.time() + timeout
        while time.time() < end:
            for loc in locs:
                try:
                    self.find_visible(loc)
                    return True
                except TimeoutException:
                    continue
        return False

    def _extract_number(self, text: str) -> int:
        m = re.search(r"(\d[\d\s]{2,})", text)
        if m:
            return int(m.group(1).replace(" ", ""))
        digits = "".join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else 0

    def _block_text(self, locs) -> str:
        for loc in locs:
            try:
                return self.get_text(loc)
            except TimeoutException:
                continue
        return ""

    @allure.step("Получить значение счётчика 'за всё время'")
    def num_all_time(self) -> int:
        txt = self._block_text((self.count_all_time_ru, self.count_all_time_en))
        return self._extract_number(txt) if txt else 0

    @allure.step("Получить значение счётчика 'за сегодня'")
    def num_today(self) -> int:
        txt = self._block_text((self.count_today_ru, self.count_today_en))
        return self._extract_number(txt) if txt else 0

    @allure.step("Есть кнопка оформления заказа")
    def has_create_order_button(self) -> bool:
        return len(self.find_all(self.create_order_button)) > 0

    @allure.step("Нажать первую кнопку оформления заказа")
    def click_first_create_order(self):
        buttons = self.find_all(self.create_order_button)
        if buttons:
            buttons[0].click()

    @allure.step("Есть заказы в работе")
    def has_orders_in_progress(self) -> bool:
        return len(self.find_all(self.in_progress_column)) > 0

    @allure.step("Ожидать увеличения счётчика 'за всё время'")
    def wait_all_time_counter_increased(self, before: int, timeout: int = 10) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            if self.num_all_time() > before:
                return True
            self.refresh()
        return False

    @allure.step("Ожидать увеличения счётчика 'за сегодня'")
    def wait_today_counter_increased(self, before: int, timeout: int = 10) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            if self.num_today() > before:
                return True
            self.refresh()
        return False

    @allure.step("Открыть детали первого заказа в ленте")
    def open_first_order_details(self):
        orders = self.find_all(self.order_items)
        if not orders:
            raise TimeoutException("Нет заказов в ленте")
        orders[0].click()

    @allure.step("Проверить, что модалка с деталями заказа открыта")
    def is_order_details_open(self) -> bool:
        try:
            self.find_visible(self.order_detail_modal)
            return True
        except TimeoutException:
            return False
