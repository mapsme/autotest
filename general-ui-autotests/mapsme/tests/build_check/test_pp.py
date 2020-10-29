import logging
import re
from time import sleep

import pytest
from PIL import Image
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.pageobjects.discovery_page import DiscoveryPage
from mapsmefr.pageobjects.guides_catalog import GuidesCatalog
from mapsmefr.steps.locators import LocalizedButtons, Locator, LocalizedMapsNames, LocalizedCategories, \
    LocalizedSettings
from mapsmefr.utils.tools import get_settings
from selenium.common.exceptions import WebDriverException


@pytest.mark.regress1
@pytest.mark.pp
class TestPlacePageMapsme:

    @pytest.fixture
    def main(self, testitem, press_back_to_main):
        pass

    @pytest.mark.name("[Place Page] Проверка описания достопримечательности на PP")
    def test_poi_description(self, main, steps):
        steps.search("Владимиру Великому")
        steps.choose_first_search_result(category=LocalizedCategories.MEMORIAL.get())
        steps.assert_pp(LocalizedButtons.VLADIMIR_VELIKI.get())
        steps.assert_category_on_pp(LocalizedCategories.MEMORIAL.get())
        steps.scroll_down()
        steps.assert_poi_description(LocalizedButtons.VLADIMIR_MEMORIAL_DESCRIPTION.get())

        steps.press_back_until_main_page()
        steps.search("Проспект Мира 78")
        steps.choose_first_search_result()
        steps.scroll_down()
        steps.assert_poi_description(LocalizedButtons.VLADIMIR_MEMORIAL_DESCRIPTION.get(), no=True)

    @pytest.mark.name("[Place Page] Проверка порядка кнопок на PP")
    def test_pp_buttons(self, main, steps, b_steps):
        panel = BottomPanel()
        # if get_settings("System", "platform") == "Android":
        #    pytest.fail("Кнопка download не в экшен баре, а на PP")
        steps.delete_map(LocalizedMapsNames.GREAT_BRITAIN, None, LocalizedMapsNames.LONDON)
        steps.search("Big Ben")
        steps.choose_first_search_result(category=LocalizedCategories.SIGHTS.get())
        steps.assert_buttons_order(LocalizedButtons.BOOKMARK.get(), LocalizedButtons.FROM.get(),
                                   LocalizedButtons.TO.get(), LocalizedButtons.SHARE_BOOKMARK.get())

        b_steps.search_booking_hotel(LocalizedButtons.AEROPOLIS_NAME.get())
        steps.assert_buttons_order(LocalizedButtons.BOOK.get(), LocalizedButtons.BOOKMARK.get(),
                                   LocalizedButtons.TO.get(), LocalizedButtons.MORE.get())
        panel.more().click()
        steps.assert_buttons_more_order(LocalizedButtons.FROM.get(), LocalizedButtons.SHARE_BOOKMARK.get())
        steps.press_back_until_main_page()

        b_steps.search_osm_hotel("Аэрополис")
        steps.assert_buttons_order(LocalizedButtons.BOOKING_COM.get(), LocalizedButtons.BOOKMARK.get(),
                                   LocalizedButtons.TO.get(), LocalizedButtons.MORE.get())
        panel.more().click()
        steps.assert_buttons_more_order(LocalizedButtons.CALL.get(), LocalizedButtons.FROM.get(),
                                        LocalizedButtons.SHARE_BOOKMARK.get())

        steps.press_back_until_main_page()
        b_steps.search_osm_hotel("ЦСКА", category=LocalizedCategories.HOTEL.get())

        steps.assert_buttons_order(LocalizedButtons.BOOKING_COM.get(), LocalizedButtons.BOOKMARK.get(),
                                   LocalizedButtons.TO.get(), LocalizedButtons.MORE.get())
        panel.more().click()
        steps.assert_buttons_more_order(LocalizedButtons.FROM.get(),
                                        LocalizedButtons.SHARE_BOOKMARK.get())

        steps.press_back_until_main_page()
        steps.search(LocalizedCategories.SIGHTS.get())
        steps.choose_first_search_result(category=LocalizedCategories.MUSEUM.get())
        steps.assert_buttons_order(LocalizedButtons.CALL.get(), LocalizedButtons.BOOKMARK.get(),
                                   LocalizedButtons.TO.get(), LocalizedButtons.MORE.get())
        panel.more().click()
        steps.assert_buttons_more_order(LocalizedButtons.FROM.get(),
                                        LocalizedButtons.SHARE_BOOKMARK.get())

        steps.press_back_until_main_page()
        steps.search("Проспект Мира 78")
        steps.choose_first_search_result()
        steps.assert_buttons_order(LocalizedButtons.FROM.get(), LocalizedButtons.BOOKMARK.get(),
                                   LocalizedButtons.TO.get(), LocalizedButtons.SHARE_BOOKMARK.get())

    @pytest.mark.name("[Place Page] Проверка описания и рекламы на топонимах")
    def test_pp_toponyms(self, main, steps):
        steps.search(LocalizedMapsNames.MOSCOW.get())
        steps.choose_first_search_result(category=LocalizedCategories.CAPITAL.get())
        steps.assert_catalog_promo()
        assert not steps.try_get(Locator.AD_BANNER.get())
        steps.scroll_down()
        assert steps.try_get_by_text(LocalizedButtons.DETAILS.get())

        sleep(5)
        steps.try_get_by_text(LocalizedButtons.DETAILS.get()).click()
        assert GuidesCatalog().navigation_bar_title()

        """steps.press_back_until_main_page()
        steps.search("Воронеж")
        steps.choose_first_search_result(category=LocalizedCategories.CITY.get())
        steps.scroll_down()
        steps.assert_catalog_promo(no=True)
        assert steps.try_get(Locator.AD_BANNER.get())"""

    @pytest.mark.name("[Place Page] Проверка отображения гидов и рекламы на PP достопримечательностей")
    def test_pp_sight_guides(self, main, steps, bookmark_steps):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delete_bookmark(LocalizedButtons.MY_BOOKMARKS.get(), LocalizedButtons.TRETYAKOV.get())
        steps.search("Московский Кремль")
        steps.choose_first_search_result()
        steps.scroll_down()

        steps.assert_catalog_promo()
        assert steps.try_get_by_text(LocalizedButtons.GUIDES_BY_TITLE.get())
        # steps.assert_poi_description(LocalizedButtons.VLADIMIR_MEMORIAL_DESCRIPTION.get())
        assert steps.try_get_by_text(LocalizedButtons.DETAILS.get())

        steps.press_back_until_main_page()
        steps.search(LocalizedButtons.TRETYAKOV.get())
        steps.choose_first_search_result()
        steps.scroll_down()
        steps.assert_promo_card()
        assert not steps.try_get(Locator.AD_BANNER.get())

        BottomPanel().bookmark().click()
        steps.press_back_until_main_page()
        steps.search(LocalizedButtons.TRETYAKOV.get())
        steps.choose_first_search_result()
        sleep(2)
        steps.scroll_down()
        steps.assert_promo_card(no=True)
        #assert steps.try_get(Locator.POI_DESCRIPTION.get())

        steps.press_back_until_main_page()
        steps.search("Дон Кихот")
        sleep(2)
        steps.choose_first_search_result(category=LocalizedCategories.MEMORIAL.get())
        steps.scroll_down()
        steps.assert_promo_card(no=True)
        # assert not steps.try_get(Locator.CATALOG_PROMO_PP.get())

    # assert not steps.try_get(Locator.PROMO_POI_CARD.get())
    # assert not steps.try_get(Locator.PROMO_POI_DESCRIPTION.get())
    # assert not steps.try_get(Locator.PROMO_POI_CTA_BUTTON.get())
    #assert not steps.try_get(Locator.POI_DESCRIPTION.get())

    @pytest.mark.name("[Place Page][Ads] Проверка рекламы на PP")
    def test_ad_banner(self, main, steps, settings_steps):
        steps.search(LocalizedMapsNames.CHELYABINSK.get())
        steps.driver.hide_keyboard()
        sleep(2)
        steps.choose_first_search_result(category=LocalizedCategories.CITY.get())
        steps.assert_catalog_promo(no=True)
        assert steps.try_get(Locator.AD_BANNER.get())
        assert steps.try_get(Locator.AD_CLOSE.get())
        steps.click_ad_close()
        self.assert_ads_popup(steps)
        steps.scroll_down()
        steps.click_ad_close()
        self.assert_ads_popup(steps)
        steps.try_get(Locator.AD_REMOVE.get()).click()

        self.assert_ads_popup(steps)

        steps.press_back_until_main_page()
        settings_steps.open_settings()
        remove_ads = settings_steps.scroll_to_setting(LocalizedSettings.REMOVE_ADS.get())
        remove_ads.click()
        self.assert_ads_popup(steps)

    def assert_ads_popup(self, steps):
        if get_settings("System", "platform") == "Android":
            self.assert_ads_popup_android(steps)
        else:
            self.assert_ads_popup_ios(steps)

    def assert_ads_popup_ios(self, steps):
        assert steps.try_get_by_text(LocalizedButtons.REMOVE_ADS_TITLE.get())
        assert steps.try_get_by_text(LocalizedButtons.MORE_OPRIONS.get())
        assert steps.try_get_by_text(LocalizedButtons.WHY_SUPPORT.get())
        steps.try_get_by_text(LocalizedButtons.MORE_OPRIONS.get()).click()

        yearly_pay = steps.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeOther' and ./*[@name='{}']]/*[@type='XCUIElementTypeButton']"
            .format(LocalizedButtons.WHY_SUPPORT.get()))[1].text.replace(" ", "")
        yearly_saving = steps.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeOther' and ./*[@name='{}']]/*[@type='XCUIElementTypeStaticText']"
                .format(LocalizedButtons.WHY_SUPPORT.get()))[1].text.replace(" ", "")
        monthly = steps.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeOther' and ./*[@name='{}']]//*[@type='XCUIElementTypeButton']"
            .format(LocalizedButtons.MORE_OPRIONS.get().upper()))[1].text.replace(" ", "")
        weekly = steps.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeOther' and ./*[@name='{}']]//*[@type='XCUIElementTypeButton']"
            .format(LocalizedButtons.MORE_OPRIONS.get().upper()))[2].text.replace(" ", "")
        yearly_pr = re.findall('\d+[\.,]?\d+', yearly_pay)
        yearly_sv = re.findall('\d+[\.,]?\d+', yearly_saving)
        monthly_all = re.findall('\d+[\.,]?\d+', monthly)
        weekly_all = re.findall('\d+[\.,]?\d+', weekly)
        assert float(yearly_sv[0].replace(",", ".")) == round(
            float(weekly_all[0].replace(",", ".")) * 52 - float(yearly_pr[0].replace(",", ".")), 2)
        assert float(monthly_all[1].replace(",", ".")) == round(
            float(weekly_all[0].replace(",", ".")) * 52 - float(monthly_all[0].replace(",", ".")) * 12, 2)
        assert len(weekly_all) == 1
        steps.try_get_by_text(LocalizedButtons.WHY_SUPPORT.get()).click()
        assert steps.try_get_by_text(LocalizedButtons.MORE_OPRIONS.get())
        assert steps.try_get_by_text(LocalizedButtons.WHY_SUPPORT.get())
        assert steps.try_get_by_text(LocalizedButtons.WE_WILL_REMOVE_ADS.get())
        assert steps.try_get_by_text(LocalizedButtons.YOU_HELP_US_TO_IMPROVE.get())
        assert steps.try_get_by_text(LocalizedButtons.HELP_IMPROVE_OSM.get())

        steps.try_get("ic ads remove close").click()

    def assert_ads_popup_android(self, steps):
        assert steps.try_get_by_text(LocalizedButtons.REMOVE_ADS_TITLE.get())
        assert steps.try_get("pay_button_container")
        assert steps.try_get("yearly_button")
        assert steps.try_get("price")
        assert steps.try_get_by_text(LocalizedButtons.MORE_OPRIONS.get())
        assert steps.try_get_by_text(LocalizedButtons.WHY_SUPPORT.get())
        steps.try_get("options").click()
        assert steps.try_get("monthly_button")
        assert steps.try_get("weekly_button")

        yearly_price = steps.try_get("price").text
        yearly_saving = steps.try_get("saving").text
        monthly = steps.try_get("monthly_button").text
        weekly = steps.try_get("weekly_button").text
        yearly_pr = re.findall('\d+[\.,]?\d+', yearly_price)
        yearly_sav = re.findall('\d+[\.,]?\d+', yearly_saving)
        monthly_all = re.findall('\d+[\.,]?\d+', monthly)
        weekly_all = re.findall('\d+[\.,]?\d+', weekly)
        assert float(yearly_sav[0].replace(",", ".")) == round(
            float(weekly_all[0].replace(",", ".")) * 52 - float(yearly_pr[0].replace(",", ".")), 2)
        assert float(monthly_all[1].replace(",", ".")) == round(
            float(weekly_all[0].replace(",", ".")) * 52 - float(monthly_all[0].replace(",", ".")) * 12, 2)
        assert len(weekly_all) == 1
        steps.try_get("explanation").click()
        assert steps.try_get("yearly_button")
        assert steps.try_get("price")
        assert steps.try_get_by_text(LocalizedButtons.MORE_OPRIONS.get())
        assert steps.try_get_by_text(LocalizedButtons.WHY_SUPPORT.get())
        assert steps.try_get_by_text(LocalizedButtons.WE_WILL_REMOVE_ADS.get())
        assert steps.try_get_by_text(LocalizedButtons.YOU_HELP_US_TO_IMPROVE.get())
        assert steps.try_get_by_text(LocalizedButtons.HELP_IMPROVE_OSM.get())

        try:
            TouchAction(steps.driver).tap(x=50, y=100).perform()
        except:
            pass
