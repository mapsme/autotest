import logging
from time import time, sleep

from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.steps.base_steps import AndroidSteps, IosSteps, check_not_crash, BaseSteps, screenshotwrap
from mapsmefr.steps.locators import Locator, LocalizedButtons, LocalizedSettings
from mapsmefr.utils.driver import WebDriverManager
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException


class BookmarkSteps(BaseSteps):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get():
        if WebDriverManager.get_instance().device.platform == "Android":
            return AndroidBookmarkSteps()
        else:
            return IosBookmarkSteps()

    def create_bookmark(self, address):
        self.press_back_until_main_page()
        self.search(address)
        self.choose_first_search_result()
        self.click_bookmark()
        self.press_back_until_main_page()

    @screenshotwrap("Нажать на значок метки")
    def click_bookmark(self):
        BottomPanel().bookmark().click()

    @screenshotwrap("Перейти в метки")
    def click_bookmarks(self):
        BottomPanel().bookmarks().click()

    @screenshotwrap("Проверить наличие букмарки")
    def assert_bookmark(self, bookmark_name):
        assert self.try_find_bookmark_with_scroll(bookmark_name)

    @screenshotwrap("Проверить отсутствие букмарки")
    def assert_no_bookmark(self, bookmark_name):
        assert self.try_find_bookmark_with_scroll(bookmark_name) is None

    def try_find_bookmark_with_scroll(self, bookmark_name):
        pass


class AndroidBookmarkSteps(BookmarkSteps, AndroidSteps):

    def athorize(self):
        self.press_back_until_main_page()
        self.click_bookmarks()
        backup_button = self.try_get(Locator.BACKUP_BUTTON.get())
        if backup_button:
            backup_button.click()
            self.try_get(Locator.TERM_OF_USE_CHECKBOX.get()).click()
            self.try_get(Locator.POLICY_CHECKBOX.get()).click()
            self.try_get(Locator.GOOGLE_BUTTON.get()).click()
            self.try_get_by_text(get_settings("Tests", "test_user")).click()
            next_button = self.try_get_by_text(LocalizedButtons.NEXT.get())
            if next_button:
                next_button.click()
                self.try_get_by_xpath("//*[@class='android.widget.EditText']").send_keys(
                    get_settings("Tests", "test_pass"))
                self.try_get_by_text(LocalizedButtons.NEXT.get()).click()
                self.try_get(Locator.GOOGLE_BUTTON.get()).click()
                self.try_get_by_text(get_settings("Tests", "test_user")).click()
        self.press_back_until_main_page()

    @check_not_crash
    def delete_bookmark(self, group_name, bookmark_name):
        self._wait_in_progress()
        self.press_back_until_main_page()
        self.click_bookmarks()
        self.click_bookmark_group(group_name)
        self.click_delete_bookmark(bookmark_name)
        self.press_back_until_main_page()

    @screenshotwrap("Удалить метку")
    def click_delete_bookmark(self, name):
        bookmark = self.try_find_bookmark_with_scroll(name)
        if bookmark:
            TouchAction(self.driver).long_press(bookmark).perform()
            self.try_get_by_text(text=LocalizedButtons.DELETE.get()).click()

    def delele_all_bookmarks_in_group(self, group_name):
        self._wait_in_progress()
        self.press_back_until_main_page()
        self.click_bookmarks()
        self.click_bookmark_group(group_name)

        bookmarks = self.driver.find_elements_by_id(Locator.BOOKMARK_NAME.get())

        while len(bookmarks) > 0:
            self.click_more_bookmark(bookmarks[0].text)
            self.try_get_by_text(LocalizedButtons.DELETE.get()).click()
            bookmarks = self.driver.find_elements_by_id(Locator.BOOKMARK_NAME.get())

        self.press_back_until_main_page()

    @check_not_crash
    @screenshotwrap("Выбрать группу меток в списке")
    def click_bookmark_group(self, group_name):
        self.try_get_by_xpath("//*[@text='{}']".format(group_name)).click()

    def try_find_bookmark_with_scroll(self, name):
        bookmark = self.try_get_by_xpath("//*[@text='{}']".format(name))
        if not bookmark:
            old_page_elements = [x.text for x in self.driver.find_elements_by_id(Locator.NAME.get())]
            self.scroll_down()
            bookmark = self.try_get_by_xpath("//*[@text='{}']".format(name))
            new_page_elements = [x.text for x in self.driver.find_elements_by_id(Locator.NAME.get())]
            timeout = time() + 60 * 2
            while not bookmark and old_page_elements != new_page_elements:
                old_page_elements = new_page_elements
                self.scroll_down()
                country, _ = self.try_get_by_text(locator=Locator.NAME, text=name)
                new_page_elements = [x.text for x in self.driver.find_elements_by_id(Locator.NAME.get())]
                if time() > timeout:
                    break
        return bookmark

    def get_bookmark_group_name(self):
        return self.try_get(Locator.BOOKMARK_SET.get()).text

    def check_if_bookmark_exist(self, address):
        self.press_back_until_main_page()
        self.search(address)
        self.choose_first_search_result()
        edit = self.try_get(Locator.EDIT_BOOKMARK_BUTTON.get())
        return True if edit else False

    @screenshotwrap("Создать новую группу меток")
    def create_group(self, name):
        self.try_get_by_text(LocalizedButtons.ADD_BOOKMARK_GROUP.get()).click()
        self.try_get(Locator.CREATE_NEW_LIST_INPUT.get()).click()
        self.try_get(Locator.CREATE_NEW_LIST_INPUT.get()).clear()
        self.try_get(Locator.CREATE_NEW_LIST_INPUT.get()).send_keys(name)
        self.try_get_by_text(LocalizedButtons.CREATE.get()).click()

    def delete_all_groups(self):
        self.press_back_until_main_page()
        self.click_bookmarks()
        groups = self.driver.find_elements_by_xpath(
            "//*[@class='android.widget.RelativeLayout' and not(./*[@text='{}'])]/*[@resource-id='{}']"
                .format(LocalizedButtons.MY_BOOKMARKS.get(), "{}:id/more".format(get_settings("Android", "package"))))
        while len(groups) > 0:
            groups[0].click()
            self.try_get_by_text(LocalizedButtons.DELETE.get()).click()
            groups = self.driver.find_elements_by_xpath(
                "//*[@class='android.widget.RelativeLayout' and not(./*[@text='{}'])]/*[@resource-id='{}']"
                    .format(LocalizedButtons.MY_BOOKMARKS.get(),
                            "{}:id/more".format(get_settings("Android", "package"))))

        self.press_back_until_main_page()

    @screenshotwrap("Нажать редактировать метку")
    def click_edit_bookmark(self, name):
        self.click_more_bookmark(name)
        self.try_get_by_text(LocalizedButtons.EDIT.get()).click()

    def click_more_bookmark(self, name):
        self.try_find_bookmark_with_scroll(name)  # for scrolling purposes
        sleep(1)
        self.try_get_by_xpath("//*[@class='android.widget.RelativeLayout' and .//*[@text='{}']]/*[@resource-id='{}']"
                              .format(name, "{}:id/more".format(get_settings("Android", "package")))).click()

    @screenshotwrap("Изменить название метки")
    def change_bookmark_name(self, new_name):
        self.try_get(Locator.EDIT_BOOKMARK_NAME.get()).click()
        self.try_get(Locator.EDIT_BOOKMARK_NAME.get()).clear()
        self.try_get(Locator.EDIT_BOOKMARK_NAME.get()).send_keys(new_name)

    @screenshotwrap("Изменить группу метки")
    def change_bookmark_group(self, group_name):
        self.try_get(Locator.BOOKMARK_SET.get()).click()
        self.try_get_by_text(group_name).click()

    @screenshotwrap("Изменить описание метки")
    def change_bookmark_description(self, text):
        self.try_get(Locator.EDIT_BOOKMARK_DESCRIPTION.get()).click()
        self.try_get(Locator.EDIT_BOOKMARK_DESCRIPTION.get()).clear()
        self.try_get(Locator.EDIT_BOOKMARK_DESCRIPTION.get()).send_keys(text)

    @screenshotwrap("Изменить цвет метки")
    def change_bookmark_color(self):
        self.try_get("iv__bookmark_color").click()
        assert self.try_get_by_text(LocalizedButtons.BOOKMARK_COLOR.get())
        self.driver.find_elements_by_id("iv__color")[3].click()

    @screenshotwrap("Изменить название группы меток")
    def change_group_name(self, new_name):
        self.try_get(Locator.EDIT_BOOKMARK_GROUP_NAME.get()).click()
        self.try_get(Locator.EDIT_BOOKMARK_GROUP_NAME.get()).clear()
        self.try_get(Locator.EDIT_BOOKMARK_GROUP_NAME.get()).send_keys(new_name)

    @screenshotwrap("Изменить описание группы меток")
    def change_group_description(self, text):
        self.try_get(Locator.EDIT_BOOKMARK_GROUP_DESCRIPTION.get()).click()
        self.try_get(Locator.EDIT_BOOKMARK_GROUP_DESCRIPTION.get()).clear()
        self.try_get(Locator.EDIT_BOOKMARK_GROUP_DESCRIPTION.get()).send_keys(text)

    @screenshotwrap("Нажать редактировать группу меток")
    def click_edit_group(self, name):
        self.click_more_group(name)
        self.try_get_by_text(LocalizedButtons.EDIT_BOOKMARK_GROUP.get()).click()

    @screenshotwrap("Нажать Больше у группы меток")
    def click_more_group(self, name):
        self.driver.find_element_by_xpath(
            "//*[@class='android.widget.RelativeLayout' and ./*[@text='{}']]/*[@resource-id='{}']"
                .format(name, "{}:id/more".format(get_settings("Android", "package")))).click()

    def get_group_size(self, group_name):
        return self.driver.find_element_by_xpath(
            "//*[@class='android.widget.RelativeLayout' and ./*[@text='{}']]//*[@resource-id='{}']"
                .format(group_name, "{}:id/size".format(get_settings("Android", "package")))).text

    def share_group(self, group_name):
        self.click_more_group(group_name)
        self.try_get_by_text(LocalizedButtons.SHARE_BOOKMARK_GROUP.get()).click()
        if not self.try_get_by_text("Gmail"):
            self.try_get_by_text("More").click()
        self.try_get_by_text("Gmail").click()
        self.try_get("com.google.android.gm:id/to").clear()
        self.try_get("com.google.android.gm:id/to").send_keys("k.kravchuk@mapswithme.com")
        self.try_get("com.google.android.gm:id/send").click()

    def share_bookmark(self, name):
        self.click_more_bookmark(name)
        self.try_get_by_text(LocalizedButtons.SHARE_BOOKMARK.get()).click()
        if not self.try_get_by_text("Gmail"):
            self.try_get_by_text("More").click()
        self.try_get_by_text("Gmail").click()
        self.try_get("com.google.android.gm:id/to").clear()
        self.try_get("com.google.android.gm:id/to").send_keys("k.kravchuk@mapswithme.com")
        self.try_get("com.google.android.gm:id/send").click()

    def import_group_from_mail(self, group_name):
        self.try_get_by_xpath("//*[@content-desc='{}']".format(LocalizedButtons.GMAIL_OPEN_NAV.get())).click()
        self.try_get_by_text(LocalizedButtons.GMAIL_SENT.get()).click()
        self.try_get_by_text(LocalizedButtons.GMAIL_BOOKMARKS_GROUP.get(), strict=False).click()
        self.try_get_by_xpath("//*[contains(@content-desc, '{}.kmz')]".format(group_name)).click()
        sleep(10)
        assert get_settings("Android", "package") in self.driver.execute_script("mobile: shell", {
            'command': "dumpsys window windows | grep -E 'mObscuringWindow|mHoldScreenWindow|mCurrentFocus''"})
        self.close_first_time_frame()

    def import_bookmark_from_mail(self, new_name):
        self.try_get_by_xpath("//*[@content-desc='{}']".format(LocalizedButtons.GMAIL_OPEN_NAV.get())).click()
        self.try_get_by_text(LocalizedButtons.GMAIL_SENT.get()).click()
        b = self.try_get_by_xpath("//*[contains(@content-desc, '{}')]".format(LocalizedButtons.GMAIL_BOOKMARK.get())) or \
            self.try_get_by_text(LocalizedButtons.GMAIL_BOOKMARK.get(), strict=False)
        b.click()
        sleep(10)
        self.try_get_by_xpath("//*[starts-with(@text, 'http://ge0') and contains(@text, {})]".format(new_name)).click()
        if self.try_get_by_text(LocalizedButtons.OPEN_WITH.get(), strict=False):
            (self.try_get_by_text("MAPS.ME") or self.try_get_by_text("maps.me beta")).click()
            if self.try_get_by_text(LocalizedSettings.ALWAYS.get()):
                self.try_get_by_text(LocalizedSettings.ALWAYS.get()).click()
        sleep(10)
        assert get_settings("Android", "package") in self.driver.execute_script("mobile: shell", {
            'command': "dumpsys window windows | grep -E 'mObscuringWindow|mHoldScreenWindow|mCurrentFocus'"})


class IosBookmarkSteps(BookmarkSteps, IosSteps):

    def athorize(self):
        self.press_back_until_main_page()
        self.click_bookmarks()
        backup_button = self.try_get(LocalizedButtons.SIGN_IN.get())
        if backup_button:
            backup_button.click()
            self.try_get_by_xpath("//*[@type='XCUIElementTypeOther' and ./*[@name='radioBtnOff']]").click()
            sleep(1)
            self.try_get_by_xpath("//*[@type='XCUIElementTypeOther' and ./*[@name='radioBtnOff']]").click()
            sleep(1)
            self.try_get_by_text("Google").click()
            self.try_get_by_text(LocalizedButtons.CONTINUE_SIGN_IN.get()).click()
            self.try_get_by_text(get_settings("Tests", "test_user")).click()
            self.try_get_by_xpath("//*[@type='XCUIElementTypeSecureTextField']").send_keys(
                get_settings("Tests", "test_pass"))
            self.try_get_by_text(LocalizedButtons.NEXT.get()).click()
        self.press_back_until_main_page()

    @check_not_crash
    def delete_bookmark(self, group_name, bookmark_name):
        self.press_back_until_main_page()
        self.click_bookmarks()
        self.click_bookmark_group(group_name)
        self.click_delete_bookmark(bookmark_name)
        self.press_back_until_main_page()

    @screenshotwrap("Удалить метку")
    def click_delete_bookmark(self, name):
        bookmark = self.try_find_bookmark_with_scroll(name)
        if bookmark:
            self.try_get(LocalizedButtons.EDIT.get()).click()
            sleep(1)
            self.try_get_by_xpath(
                "//*[@type='XCUIElementTypeCell' and ./*[@name='{}']]/*[@type='XCUIElementTypeButton']".format(
                    name)).click()
            sleep(1)
            self.try_get(LocalizedButtons.DELETE.get()).click()

    def delele_all_bookmarks_in_group(self, group_name):
        self.press_back_until_main_page()
        self.click_bookmarks()
        self.click_bookmark_group(group_name)

        if self.try_get(LocalizedButtons.EDIT.get()):
            self.try_get(LocalizedButtons.EDIT.get()).click()

        while self.try_get_by_text(LocalizedButtons.DELETE.get(), strict=False):
            self.try_get_by_text(LocalizedButtons.DELETE.get(), strict=False).click()
            self.try_get_by_text(LocalizedButtons.DELETE.get()).click()

    @check_not_crash
    @screenshotwrap("Выбрать группу меток в списке")
    def click_bookmark_group(self, group_name):
        self.try_get(group_name).click()

    def try_find_bookmark_with_scroll(self, name):
        bookmark = self.try_get(name)
        if not bookmark:
            old_page_elements = [x.text for x in
                                 self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeStaticText']")]
            self.scroll_down()
            bookmark = self.try_get(name)
            new_page_elements = [x.text for x in
                                 self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeStaticText']")]
            timeout = time() + 60 * 2
            while not bookmark and old_page_elements != new_page_elements:
                old_page_elements = new_page_elements
                self.scroll_down()
                bookmark = self.try_get(name)
                new_page_elements = [x.text for x in
                                     self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeStaticText']")]
                if time() > timeout:
                    break
        return bookmark

    def get_bookmark_group_name(self):
        return self.try_get_by_xpath("//*[@type='XCUIElementTypeCell'][3]/*[@type='XCUIElementTypeStaticText']").text

    def delete_all_groups(self):
        self.press_back_until_main_page()
        self.click_bookmarks()
        groups = self.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeCell' and not(./*[@type='XCUIElementTypeStaticText' and @name='{}'])]/*[@name='{}']"
                .format(LocalizedButtons.MY_BOOKMARKS.get(), Locator.MORE_BUTTON.get()))
        while len(groups) > 0:
            groups[0].click()
            self.try_get_by_text(LocalizedButtons.DELETE.get(), strict=False).click()
            groups = self.driver.find_elements_by_xpath(
                "//*[@type='XCUIElementTypeCell' and not(./*[@type='XCUIElementTypeStaticText' and @name='{}'])]/*[@name='{}']"
                    .format(LocalizedButtons.MY_BOOKMARKS.get(), Locator.MORE_BUTTON.get()))
        self.press_back_until_main_page()

    @screenshotwrap("Создать новую группу меток")
    def create_group(self, name):
        sleep(1)
        self.try_get_by_text(LocalizedButtons.ADD_BOOKMARK_GROUP.get()).click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").clear()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").send_keys(name)
        self.try_get_by_text(LocalizedButtons.CREATE.get()).click()

    @screenshotwrap("Нажать редактировать метку")
    def click_edit_bookmark(self, name):
        sleep(1)
        self.try_find_bookmark_with_scroll(name).click()
        sleep(1)
        self.scroll_down(from_el=self.try_get(Locator.PP_ANCHOR.get()))
        self.try_get(Locator.EDIT_BOOKMARK_BUTTON.get()).click()
        sleep(1)

    @screenshotwrap("Изменить название метки")
    def change_bookmark_name(self, new_name):
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").clear()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").send_keys(new_name)

    @screenshotwrap("Изменить группу метки")
    def change_bookmark_group(self, group_name):
        self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']/*[@type='XCUIElementTypeStaticText']")[
            1].click()
        self.try_get_by_text(group_name).click()

    @screenshotwrap("Изменить описание метки")
    def change_bookmark_description(self, text):
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextView']").click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextView']").clear()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextView']").send_keys(text)

    @screenshotwrap("Изменить цвет метки")
    def change_bookmark_color(self):
        self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']/*[@type='XCUIElementTypeStaticText']")[
            0].click()
        sleep(1)
        self.try_get_by_text(LocalizedButtons.BLUE.get()).click()

    @screenshotwrap("Нажать Больше у группы меток")
    def click_more_group(self, name):
        self.driver.find_element_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@type='XCUIElementTypeStaticText' and @name='{}']]/*[@name='{}']"
                .format(name, Locator.MORE_BUTTON.get())).click()

    @screenshotwrap("Нажать редактировать группу меток")
    def click_edit_group(self, name):
        self.click_more_group(name)
        self.try_get_by_text(LocalizedButtons.EDIT_BOOKMARK_GROUP.get()).click()

    @screenshotwrap("Изменить название группы меток")
    def change_group_name(self, new_name):
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").clear()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextField']").send_keys(new_name)

    @screenshotwrap("Изменить описание группы меток")
    def change_group_description(self, text):
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextView']").click()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextView']").clear()
        self.try_get_by_xpath("//*[@type='XCUIElementTypeTextView']").send_keys(text)

    def get_group_size(self, group_name):
        return self.driver.find_element_by_xpath(
            "//*[@type='XCUIElementTypeCell' and ./*[@type='XCUIElementTypeStaticText' and @name='{}']]/*[@type='XCUIElementTypeStaticText'][2]"
                .format(group_name, Locator.MORE_BUTTON.get())).text

    def share_group(self, group_name):
        sleep(3)
        self.click_more_group(group_name)
        self.try_get_by_text(LocalizedButtons.SHARE_BOOKMARK_GROUP.get()).click()
        self.try_get_by_text(LocalizedButtons.MAIL.get()).click()
        sleep(3)
        self.try_get("toField").clear()
        sleep(3)
        self.try_get("toField").send_keys("k.kravchuk@mapswithme.com")
        self.try_get_by_text(LocalizedButtons.RETURN.get()).click()
        if self.try_get("Mail.sendButton"):
            self.try_get("Mail.sendButton").click()
        if self.try_get(LocalizedButtons.SEND.get()):
            self.try_get(LocalizedButtons.SEND.get()).click()

    def share_bookmark(self, name):
        sleep(3)
        self.try_get_by_text(Locator.SHARE_BOOKMARK.get()).click()
        self.try_get_by_text(LocalizedButtons.MAIL.get()).click()
        sleep(3)
        self.try_get("toField").clear()
        sleep(3)
        self.try_get("toField").send_keys("k.kravchuk@mapswithme.com")
        self.try_get_by_text(LocalizedButtons.RETURN.get()).click()
        if self.try_get("Mail.sendButton"):
            self.try_get("Mail.sendButton").click()
        if self.try_get(LocalizedButtons.SEND.get()):
            self.try_get(LocalizedButtons.SEND.get()).click()

    def import_group_from_mail(self, group_name):
        self.try_get(LocalizedButtons.MAILBOXES.get()).click()
        self.try_get(LocalizedButtons.GMAIL_SENT.get()).click()
        sleep(4)
        self.try_get_by_text(LocalizedButtons.MAIL_BOOKMARK.get(), strict=False).click()
        sleep(5)
        self.try_get_by_text("{}.kmz".format(group_name), strict=False).click()
        sleep(1)
        self.try_get_by_text(LocalizedButtons.SHARE_BOOKMARK.get()).click()

        coord_y = self.try_get(LocalizedButtons.MAIL.get()).location["y"]
        self.slide_left(coord_y, 3)
        self.driver.find_elements_by_id(LocalizedButtons.ACTIVITY.get())[3].click()

        sleep(10)
        alerts = self.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeAlert']")
        if len(alerts) > 0:
            self.driver.execute_script('mobile: alert', {'action': 'dismiss'})
            sleep(1)
        if self.try_get_by_text(LocalizedButtons.OK.get()):
            self.try_get_by_text(LocalizedButtons.OK.get()).click()
        self.close_first_time_frame()
        self.press_back_until_main_page()

    def import_bookmark_from_mail(self, name):
        self.try_get(LocalizedButtons.MAILBOXES.get()).click()
        self.try_get(LocalizedButtons.GMAIL_SENT.get()).click()
        sleep(4)
        self.try_get_by_text(LocalizedButtons.GMAIL_BOOKMARK.get(), strict=False).click()
        sleep(5)
        self.try_get_by_xpath("//*[@type='XCUIElementTypeLink' and starts-with(@name, 'ge0')]").click()
        sleep(1)
        if self.try_get_by_text(LocalizedButtons.OPEN.get()):
            self.try_get_by_text(LocalizedButtons.OPEN.get()).click()

    def slide_left(self, coord_y, times):
        for _ in range(times):
            coords_x_from = self.driver.get_window_size()['width'] * 0.8
            coords_x_to = self.driver.get_window_size()['width'] * 0.2
            actions = TouchAction(
                self.driver)  # да, тут нужно создавать объет заново, потому что после первого эксепшона все летит к чертям
            try:
                actions.press(None, coords_x_from, coord_y) \
                    .wait(4000).move_to(None, coords_x_to,
                                        coord_y).release().perform().release().perform()
            except WebDriverException:
                pass

        sleep(5)
