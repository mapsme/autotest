import logging

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

    def assert_popular_sights_list(self):
        pass

    def get_first_search_name(self):
        pass


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

    def assert_food_list(self):
        sights = [LocalizedCategories.RESTAURANT.get(), LocalizedCategories.CAFE.get(),
                  LocalizedCategories.MARKETPLACE.get(), LocalizedCategories.BAR.get(),
                  LocalizedCategories.PUB.get(), LocalizedCategories.FASTFOOD.get(),
                  LocalizedCategories.GROCERY.get(), LocalizedCategories.LIQUOR_STORE.get()]
        for _ in range(3):
            results = [x.text for x in self.driver.find_elements_by_id("description")]
            for res in results:
                assert res.split(" •")[0] in sights

            self.scroll_down()

    def assert_shops_list(self):
        sights = [LocalizedCategories.MALL.get(), LocalizedCategories.CAFE.get(),
                  LocalizedCategories.MARKETPLACE.get(), LocalizedCategories.GROCERY.get(),
                  LocalizedCategories.SHOP.get(), LocalizedCategories.CLOTHES_SHOP.get(),
                  LocalizedCategories.BEAUTY_SHOP.get(), LocalizedCategories.JEWELRY.get(),
                  LocalizedCategories.FLORISTS.get(), LocalizedCategories.CAR_SHOP.get(),
                  LocalizedCategories.TICKET_SHOP.get(), LocalizedCategories.OPTICIAN.get(),
                  LocalizedCategories.BOOKSTORE.get(), LocalizedCategories.LIQUOR_STORE.get(),
                  LocalizedCategories.GIFT_SHOP.get(), LocalizedCategories.VEG_AND_FRUITS.get(),
                  LocalizedCategories.ELECTRONICS.get()
                  ]
        for _ in range(3):
            results = [x.text for x in self.driver.find_elements_by_id("description")]
            for res in results:
                assert res.split(" •")[0] in sights

            self.scroll_down()

    def assert_title_contains(self, title, limit=5):
        for _ in range(3):
            results = [x.text for x in self.driver.find_elements_by_id("title")][:limit]
            for res in results:
                assert title.lower() in res.lower()
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

    def assert_food_list(self):
        food = [LocalizedCategories.RESTAURANT.get(), LocalizedCategories.CAFE.get(),
                LocalizedCategories.MARKETPLACE.get(), LocalizedCategories.BAR.get(),
                LocalizedCategories.PUB.get(), LocalizedCategories.FASTFOOD.get(),
                LocalizedCategories.GROCERY.get(), LocalizedCategories.LIQUOR_STORE.get()]
        results = self.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeTable']/*[@type='XCUIElementTypeCell']")
        for res in results:
            el = res.find_element_by_xpath("./*[@name='searchType']")
            text = el.text
            logging.info(text)
            assert text in food

    def assert_shops_list(self):
        shops = [LocalizedCategories.MALL.get(), LocalizedCategories.CAFE.get(),
                 LocalizedCategories.MARKETPLACE.get(), LocalizedCategories.GROCERY.get(),
                 LocalizedCategories.SHOP.get(), LocalizedCategories.CLOTHES_SHOP.get(),
                 LocalizedCategories.BEAUTY_SHOP.get(), LocalizedCategories.JEWELRY.get(),
                 LocalizedCategories.FLORISTS.get(), LocalizedCategories.CAR_SHOP.get(),
                 LocalizedCategories.TICKET_SHOP.get(), LocalizedCategories.OPTICIAN.get(),
                 LocalizedCategories.BOOKSTORE.get(), LocalizedCategories.LIQUOR_STORE.get(),
                 LocalizedCategories.GIFT_SHOP.get(), LocalizedCategories.VEG_AND_FRUITS.get(),
                 LocalizedCategories.ELECTRONICS.get()]
        results = self.driver.find_elements_by_xpath(
            "//*[@type='XCUIElementTypeTable']/*[@type='XCUIElementTypeCell']")
        for res in results:
            el = res.find_element_by_xpath("./*[@name='searchType']")
            text = el.text
            logging.info(text)
            assert text in shops


    def assert_title_contains(self, title, limit=5):
        results = WebDriverManager.get_instance().driver.find_elements_by_id(Locator.TITLE.get())[:limit]
        for res in results:
            assert title.lower() in res.text.lower(), "Search result should contain {}".format(title)
