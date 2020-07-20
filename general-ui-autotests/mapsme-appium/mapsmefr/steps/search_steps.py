from mapsmefr.steps.base_steps import AndroidSteps, IosSteps, screenshotwrap
from mapsmefr.steps.locators import LocalizedCategories, Locator
from mapsmefr.utils.driver import WebDriverManager


class SearchSteps:

    def __init__(self):
        self.driver = WebDriverManager.get_instance().driver

    @staticmethod
    def get():
        if WebDriverManager.get_instance().device.platform == "Android":
            return AndroidSearchSteps()
        else:
            return IosSearchSteps()


class AndroidSearchSteps(SearchSteps, AndroidSteps):

    @screenshotwrap("Проверить, что в списке отображаются популярные достопримечательности", two_screenshots=False)
    def assert_popular_sights_list(self):
        sights = [LocalizedCategories.ATTRACTION.get(), LocalizedCategories.MUSEUM.get(),
                  LocalizedCategories.PARK.get(), LocalizedCategories.CHURCH.get(),
                  LocalizedCategories.ZOO.get(), LocalizedCategories.MONUMENT.get(),
                  LocalizedCategories.MEMORIAL.get()]
        for _ in range(3):
            results = [x.text for x in self.driver.find_elements_by_id("description")]
            populars = [x for x in self.driver.find_elements_by_id(Locator.POPULAR.get())]
            assert len(populars) > 0
            for res in results:
                assert res.split()[0] in sights

            self.scroll_down()


class IosSearchSteps(SearchSteps, IosSteps):

    @screenshotwrap("Проверить, что в списке отображаются популярные достопримечательности", two_screenshots=False)
    def assert_popular_sights_list(self):
        sights = [LocalizedCategories.ATTRACTION.get(), LocalizedCategories.MUSEUM.get(),
                  LocalizedCategories.PARK.get(), LocalizedCategories.CHURCH.get(),
                  LocalizedCategories.ZOO.get(), LocalizedCategories.MONUMENT.get(),
                  LocalizedCategories.MEMORIAL.get()]
        results = self.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeTable']/*[@type='XCUIElementTypeCell']")
        populars = [x for x in self.driver.find_elements_by_id(Locator.POPULAR.get())]
        assert len(populars) > 0
        for res in results:
            el = res.find_element_by_xpath("./*[@name='searchType']")
            assert el.text.split()[0] in sights

    def get_first_search_name(self):
        return self.try_get(Locator.TITLE.get()).text
