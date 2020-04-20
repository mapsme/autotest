from datetime import datetime
from time import sleep

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedSettings
from mapsmefr.utils.tools import get_random_string, get_settings


@pytest.mark.bookmark
@pytest.mark.build_check
class TestBookmarkMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main, restart_if_failed):
        pass

    @pytest.yield_fixture
    def restart_if_failed(self, request, system_steps, steps):
        yield
        status = True if request.node.rep_setup.passed and request.node.rep_call.passed else False
        if not status:
            system_steps.restart_app()
            steps.close_first_time_frame()
            steps.press_back_until_main_page()

    @pytest.mark.name("[Bookmarks] Создание букмарки на здании")
    def test_bookmark_add(self, main, download_moscow_map, steps, bookmark_steps):
        panel = BottomPanel()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")

        steps.search("Проспект Мира 78")
        steps.choose_first_search_result()
        panel.bookmark().click()
        steps.scroll_down()
        steps.assert_element_presence(Locator.EDIT_BOOKMARK_BUTTON)

        steps.try_get(Locator.EDIT_BOOKMARK_BUTTON.get()).click()
        sleep(1)
        group = bookmark_steps.get_bookmark_group_name()
        steps.press_back_until_main_page()

        panel.bookmarks().click()

        bookmark_steps.click_bookmark_group(group)
        assert bookmark_steps.try_find_bookmark_with_scroll("проспект Мира, 78")

    @pytest.mark.name("[Bookmarks] Изменение букмарки")
    def test_bookmark_edit(self, main, download_moscow_map, steps, bookmark_steps):
        "(созданной ранее - меняем цвет, группу новую создаём, добавляем описание)"
        bookmark_steps.delete_all_groups()
        bookmark_name = "проспект Мира, 78"
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), bookmark_name)
        bookmark_steps.create_bookmark(bookmark_name)
        BottomPanel().bookmarks().click()
        new_group = get_random_string(10)
        new_name = get_random_string(10)
        new_description = get_random_string(20)
        bookmark_steps.create_group(new_group)
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        bookmark_steps.click_edit_bookmark(bookmark_name)
        bookmark_steps.change_bookmark_name(new_name)
        bookmark_steps.change_bookmark_group(new_group)
        bookmark_steps.change_bookmark_description(new_description)
        bookmark_steps.change_bookmark_color()
        steps.try_get_by_text(LocalizedButtons.SAVE.get()).click()

        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())

        assert bookmark_steps.try_find_bookmark_with_scroll(bookmark_name) is None
        assert bookmark_steps.try_find_bookmark_with_scroll(new_name) is None

        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(new_group)
        b = bookmark_steps.try_find_bookmark_with_scroll(new_name)
        sleep(1)
        b.click()
        steps.scroll_down(small=True)

        assert steps.try_get_by_text(new_description)

    @pytest.mark.name("[Bookmarks] Удаление букмарки через PP")
    def test_delete_bookmark_from_pp(self, main, download_moscow_map, steps, bookmark_steps):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        bookmark_name = "проспект Мира, 78"
        bookmark_steps.create_bookmark(bookmark_name)
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        bookmark = bookmark_steps.try_find_bookmark_with_scroll(bookmark_name)
        sleep(1)
        bookmark.click()
        BottomPanel().bookmark().click()
        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        assert bookmark_steps.try_find_bookmark_with_scroll(bookmark_name) is None

    @pytest.mark.name("[Bookmarks] Удаление букмарки через список")
    def test_delete_bookmark_from_list(self, main, download_moscow_map, steps, bookmark_steps):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        bookmark_name = "проспект Мира, 78"
        bookmark_steps.create_bookmark(bookmark_name)
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), bookmark_name)

        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        assert bookmark_steps.try_find_bookmark_with_scroll(bookmark_name) is None

    @pytest.mark.name("[Bookmarks] Создание группы на экране букмарок")
    def test_create_new_group(self, main, download_moscow_map, steps, bookmark_steps):
        bookmark_steps.delete_all_groups()
        group_name = get_random_string(10)
        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.create_group(group_name)
        bookmark_steps.click_bookmark_group(group_name)

    @pytest.mark.name("[Bookmarks] Изменение группы на экране букмарок")
    def test_edit_group(self, main, download_moscow_map, steps, bookmark_steps):
        bookmark_steps.delete_all_groups()
        group_name = get_random_string(10)
        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.create_group(group_name)
        bookmark_steps.click_edit_group(group_name)
        new_name = get_random_string(10)
        new_description = get_random_string(30)
        bookmark_steps.change_group_name(new_name)
        bookmark_steps.change_group_description(new_description)
        button = steps.try_get(Locator.DONE.get()) or steps.try_get(LocalizedButtons.SAVE.get())
        button.click()
        assert steps.try_get_by_text(group_name) is None
        bookmark_steps.click_bookmark_group(new_name)
        sleep(2)
        more = steps.try_get(Locator.MORE_BUTTON.get())
        if more:
            more.click()
        assert steps.try_get_by_text(new_description)

    @pytest.mark.name("[Bookmarks] Удаление группы на экране букмарок (кроме последней)")
    def test_delete_all_groups(self, main, download_moscow_map, steps, bookmark_steps):
        bookmark_steps.delete_all_groups()
        first_group_name = get_random_string(10)
        second_group_name = get_random_string(10)
        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        bookmark_steps.create_group(first_group_name)
        bookmark_steps.create_group(second_group_name)
        bookmark_steps.delete_all_groups()
        steps.press_back_until_main_page()
        BottomPanel().bookmarks().click()
        assert steps.try_get_by_text(first_group_name) is None
        assert steps.try_get_by_text(second_group_name) is None
        bookmark_steps.click_more_group(LocalizedButtons.MY_BOOKMARKS.get())
        assert steps.try_get_by_text(LocalizedButtons.DELETE.get()) is None

    @pytest.fixture()
    def authorize(self, bookmark_steps):
        bookmark_steps.athorize()

    @pytest.fixture()
    def turn_off_backup(self, driver, settings_steps):
        settings_steps.open_settings()
        settings_steps.switch_settings(LocalizedSettings.BOOKMARK_BACKUP.get(), False)

    @pytest.mark.releaseonly
    @pytest.mark.name("[Bookmarks] Бэкап, локальное удаление с последующим восстановлением группы для проверки")
    def test_backup_bookmarks(self, main, download_moscow_map, steps, bookmark_steps, system_steps, authorize,
                              turn_off_backup):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        group_name = get_random_string(10)
        BottomPanel().bookmarks().click()
        bookmark_steps.create_group(group_name)
        bookmarks = ["проспект Мира, 78", "метро Динамо", "Якитория", "Белорусская"]
        for b in bookmarks:
            bookmark_steps.create_bookmark(b)
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(group_name)
        sleep(1)
        bookmark_steps.click_edit_bookmark(bookmarks[0])
        bookmark_steps.change_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        steps.try_get_by_text(LocalizedButtons.SAVE.get()).click()
        steps.press_back_until_main_page()

        BottomPanel().bookmarks().click()
        button = steps.try_get(Locator.BACKUP_BUTTON.get()) or steps.try_get(LocalizedButtons.ENABLE_BACKUP.get())
        button.click()
        system_steps.restart_app()

        steps.close_first_time_frame()
        BottomPanel().bookmarks().click()
        assert steps.try_get_by_text(LocalizedButtons.LAST_BACKUP.get().format(datetime.now().strftime("%d.%m.%Y")),
                                     strict=False) or \
               steps.try_get_by_text(LocalizedButtons.LAST_BACKUP.get().format(datetime.now().strftime("%d/%m/%y")),
                                     strict=False) or \
               steps.try_get_by_text(
                   LocalizedButtons.LAST_BACKUP.get().format(datetime.now().strftime("%m/%d/%y").split("0")[0]
                                                             if datetime.now().strftime("%m/%d/%y").startswith(
                       "0") else datetime.now().strftime("%m/%d/%y")),
                   strict=False)
        group_size = bookmark_steps.get_group_size(group_name)
        my_group_size = bookmark_steps.get_group_size(LocalizedButtons.MY_BOOKMARKS.get())

        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), "проспект Мира, 78")
        BottomPanel().bookmarks().click()
        sleep(1)

        steps.try_get(Locator.RESTORE_BUTTON.get()).click()
        sleep(1)
        steps.try_get_by_text(LocalizedButtons.RESTORE.get()).click()

        group = bookmark_steps.try_get(group_name)
        if group:
            assert group_size == bookmark_steps.get_group_size(group_name)
        else:
            assert my_group_size == bookmark_steps.get_group_size(LocalizedButtons.MY_BOOKMARKS.get())

    @pytest.mark.name("[Bookmarks] Шаринг букмарки через почту с последующим её же импортом")
    def test_share_bookmark(self, main, download_moscow_map, steps, bookmark_steps, system_steps):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delele_all_bookmarks_in_group(LocalizedButtons.MY_BOOKMARKS.get())
        steps.press_back_until_main_page()
        bookmark_name = "проспект Мира, 78"
        new_name = get_random_string(10)
        bookmark_steps.create_bookmark(bookmark_name)
        BottomPanel().bookmarks().click()
        bookmark_steps.click_bookmark_group(LocalizedButtons.MY_BOOKMARKS.get())
        bookmark_steps.click_edit_bookmark(bookmark_name)
        bookmark_steps.change_bookmark_name(new_name)
        steps.try_get_by_text(LocalizedButtons.SAVE.get()).click()

        bookmark_steps.share_bookmark(new_name)
        loc = steps.driver.get_window_size()
        try:
            TouchAction(steps.driver).tap(x=loc["width"] / 2, y=loc["height"] / 2).perform()
        except:
            pass
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), new_name)

        system_steps.start_mail_app()
        sleep(5)
        bookmark_steps.import_bookmark_from_mail(new_name)

        steps.assert_pp(bookmark_name)

        assert steps.try_get(Locator.ZOOM_OUT.get()), "Отсутсвуют кнопки зума!"
        assert steps.try_get(Locator.ZOOM_IN.get())

    @pytest.mark.name("[Bookmarks] Шарринг группы через почту с последующим импортом её же")
    def test_share_group(self, main, download_moscow_map, steps, bookmark_steps, system_steps):
        bookmark_steps.delete_all_groups()
        group_name = get_random_string(10)
        BottomPanel().bookmarks().click()
        bookmark_steps.create_group(group_name)
        bookmarks = ["метро Динамо", "Якитория", "Белорусская"]
        for b in bookmarks:
            bookmark_steps.create_bookmark(b)
        BottomPanel().bookmarks().click()
        bookmark_steps.share_group(group_name)
        loc = steps.driver.get_window_size()
        try:
            TouchAction(steps.driver).tap(x=loc["width"] / 2, y=loc["height"] / 2).perform()
        except:
            pass
        bookmark_steps.delete_all_groups()

        system_steps.start_mail_app()
        bookmark_steps.import_group_from_mail(group_name)
        BottomPanel().bookmarks().click()
        assert "3" in bookmark_steps.get_group_size(group_name)