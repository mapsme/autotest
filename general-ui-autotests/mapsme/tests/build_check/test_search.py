import pytest
from PIL import Image
from mapsmefr.steps.locators import LocalizedMapsNames, LocalizedCategories, LocalizedButtons, Locator


@pytest.mark.regress1
class TestSearchMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main, clean_bookmarks):
        pass

    @pytest.fixture(scope="class")
    def clean_bookmarks(self, bookmark_steps, steps):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delele_all_bookmarks_in_group(LocalizedButtons.MY_BOOKMARKS.get())
        steps.press_back_until_main_page()

    @pytest.mark.name("[Search] Поиск адреса 'Проспект Мира 78' с картой Москвы")
    @pytest.mark.base
    @pytest.mark.build_check
    def test_search_with_map(self, main, download_moscow_map, steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653559"""
        steps.search("Проспект Мира 78")
        steps.choose_first_search_result()
        steps.assert_pp("проспект Мира, 78")

    @pytest.mark.name("[Search] Поиск названия города 'Лондон' без карт")
    @pytest.mark.build_check
    def test_search_without_map(self, main, steps):
        steps.search(LocalizedMapsNames.LONDON.get())
        steps.choose_first_search_result(category=LocalizedCategories.CAPITAL.get())
        steps.assert_pp(LocalizedMapsNames.LONDON.get())
        steps.assert_category_on_pp(LocalizedCategories.CAPITAL.get())

    @pytest.mark.name("[Search] Поиск по координатам (38.662, -9.08) и переход к точке с загрузкой карты")
    @pytest.mark.build_check
    def test_search_coordinates(self, main, steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653560"""
        steps.delete_map(LocalizedMapsNames.PORTUGAL, None, LocalizedMapsNames.PORTO)
        steps.search("41.145819, -8.614019")
        steps.choose_first_search_result()

        steps.wait_map_download(LocalizedMapsNames.PORTUGAL.get())

        steps.assert_pp(LocalizedMapsNames.UNKNOWN_PLACE.get())
        steps.assert_category_on_pp("41.145819, -8.614019")

        steps.press_back_until_main_page()

    @pytest.mark.name("[Search] Проверка результатов поиска при запросе food")
    def test_search_food(self, main, steps, search_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653519"""
        steps.search("food")
        search_steps.assert_food_list()

    @pytest.mark.name("[Search] Проверка результатов поиска при запросе shop")
    def test_search_shop(self, main, steps, search_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653520"""
        steps.search("shop")
        search_steps.assert_shops_list()

    @pytest.mark.name("[Search] Поиск по названию (Лондон)")
    def test_search_by_name(self, main, steps, search_steps):
        """https://testrail.corp.mail.ru/index.php?/tests/view/36653558"""
        steps.search(LocalizedMapsNames.LONDON.get())
        search_steps.assert_title_contains(LocalizedMapsNames.LONDON.get(), 5)

    """def test_search_on_map(self, main, steps, search_steps):
        steps.click_search_button()
        steps.choose_category_in_list(LocalizedCategories.WHERE_TO_EAT.get())
        steps.try_get(LocalizedButtons.SEARCH_IN_THE_MAP.get()).click()
        filename = "where_to_eat.png"
        steps.driver.get_screenshot_as_file(filename)
        pass"""

    def get_coords_proportions(self, filename):
        img = Image.open(filename)
        img = img.convert("RGB")

        width, height = img.size

        rg = None
        n = 1

        for i in range(width):
            for j in range(height):
                x = img.getpixel((i, j))
                if rg != x:
                    rg = x

                if rg[1] < 60 and rg[2] < 60 and rg[0] > 200:
                    if i > 200 and j > 100:
                        if n == number:
                            return i / width, j / height
                        n = n + 1
