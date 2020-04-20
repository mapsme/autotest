import pytest
from mapsmefr.steps.locators import LocalizedMapsNames, LocalizedCategories, LocalizedButtons


@pytest.mark.build_check
class TestSearchMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main, clean_bookmarks):
        pass

    @pytest.fixture(scope="class")
    def clean_bookmarks(self, bookmark_steps):
        bookmark_steps.delete_all_groups()
        bookmark_steps.delele_all_bookmarks_in_group(LocalizedButtons.MY_BOOKMARKS.get())

    @pytest.mark.name("[Search] Поиск адреса 'Проспект Мира 78' с картой Москвы")
    @pytest.mark.base
    def test_search_with_map(self, main, download_moscow_map, steps):
        steps.search("Проспект Мира 78")
        steps.choose_first_search_result()
        steps.assert_pp("проспект Мира, 78")

    @pytest.mark.name("[Search] Поиск названия города 'Лондон' без карт")
    def test_search_without_map(self, main, steps):
        steps.search(LocalizedMapsNames.LONDON.get())
        steps.choose_first_search_result(category=LocalizedCategories.CAPITAL.get())
        steps.assert_pp(LocalizedMapsNames.LONDON.get())
        steps.assert_category_on_pp(LocalizedCategories.CAPITAL.get())

    @pytest.mark.name("[Search] Поиск по координатам (38.662, -9.08) и переход к точке с загрузкой карты")
    def test_search_coordinates(self, main, steps):
        steps.delete_map(LocalizedMapsNames.PORTUGAL, None, LocalizedMapsNames.PORTO)
        steps.search("41.145819, -8.614019")
        steps.choose_first_search_result()

        steps.wait_map_download(LocalizedMapsNames.PORTUGAL.get())

        steps.assert_pp(LocalizedMapsNames.UNKNOWN_PLACE.get())
        steps.assert_category_on_pp("41.145819, -8.614019")

        steps.press_back_until_main_page()
