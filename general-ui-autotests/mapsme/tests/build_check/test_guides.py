from time import sleep

import pytest
from appium.webdriver.common.touch_action import TouchAction
from mapsmefr.pageobjects.base import BottomPanel
from mapsmefr.pageobjects.booking_filter_page import SearchFilter
from mapsmefr.pageobjects.discovery_page import DiscoveryPage
from mapsmefr.pageobjects.guides_catalog import GuidesCatalog
from mapsmefr.pageobjects.subscription_banner import SubscriptionBanner
from mapsmefr.steps.base_steps import BookingSteps
from mapsmefr.steps.locators import LocalizedCategories, Locator, LocalizedButtons, LocalizedMapsNames
from mapsmefr.steps.locators import PlatformDependantAttributes as attributes
from mapsmefr.steps.routing_steps import RoutingSteps


@pytest.mark.regress1
@pytest.mark.guides
@pytest.mark.webview
class TestGuidesMapsme:

    @pytest.fixture
    def main(self, emulate_location_moscow, testitem, press_back_to_main, switch_to_native):
        pass

    @pytest.mark.name("[Subscription] Проверка баннера подписки в каталоге")
    def test_subscription_banner(self, main, steps, bookmark_steps):
        BottomPanel().bookmarks().click()
        steps.try_get_by_text(LocalizedButtons.GUIDES.get()).click()
        bookmark_steps.click_download_guides()
        guides_page = GuidesCatalog()
        guides_page.try_subscription().click()
        banner = SubscriptionBanner()
        assert banner.title()
        assert banner.city_outdoor()
        assert banner.monthly()
        assert banner.yearly()
        banner.yearly().click()
        assert steps.try_get(Locator.TERM_OF_USE_CHECKBOX.get())
        assert steps.try_get(Locator.POLICY_CHECKBOX.get())
        if steps.try_get(LocalizedButtons.SIGN_IN_WITH.get()):
            TouchAction(steps.driver).tap(x=100, y=100).perform()
        assert banner.close()
        banner.close().click()
        assert not banner.title()

    @pytest.mark.skip
    @pytest.mark.name("[Subscription] Проверка баннера подписки в поиске")
    def test_search_banner(self, main, steps, bookmark_steps):
        BottomPanel().bookmarks().click()
        steps.try_get_by_text(LocalizedButtons.GUIDES.get()).click()
        bookmark_steps.click_download_guides()
        guides_page = GuidesCatalog()
        sleep(2)
        guides_page.filter_by_tag().send_keys(LocalizedMapsNames.MOSCOW.get())
        sleep(2)
        guides_page.search_result_dropdown(LocalizedMapsNames.MOSCOW.get()).click()
        sleep(2)
        guides_page.clear_search().click()
        sleep(2)

        guides_page.filter_by_tag().send_keys(LocalizedMapsNames.LONDON.get())
        sleep(2)
        guides_page.search_result_dropdown(LocalizedMapsNames.LONDON.get()).click()
        sleep(2)
        guides_page.clear_search().click()
        sleep(2)

        guides_page.filter_by_tag().send_keys(LocalizedMapsNames.BERLIN.get())
        sleep(2)
        guides_page.search_result_dropdown(LocalizedMapsNames.BERLIN.get()).click()
        sleep(2)
        guides_page.clear_search().click()
        sleep(2)

        assert guides_page.subscribe_result_banner()
