from time import sleep

import pytest
import requests
from mapsmefr.steps.locators import LocalizedMapsNames, LocalizedCategories, LocalizedButtons, Locator
from mapsmefr.utils.tools import get_settings
import xml.etree.ElementTree as ET


@pytest.mark.build_check
@pytest.mark.edit
class TestEditMapsme:

    @pytest.fixture
    def main(self, testitem, emulate_location_moscow, press_back_to_main):
        pass

    @pytest.mark.name("Редактирование ресторана без отправки правок в OSM")
    def test_edit_restaurant(self, main, steps):
        steps.search("Burger King")
        steps.choose_first_search_result()
        steps.driver.implicitly_wait(3)
        edit_button = steps.scroll_down_to_element(locator=Locator.EDIT_PLACE_BUTTON, scroll_time=15)
        edit_button.click()
        cuis_button = steps.scroll_down_to_element(locator=Locator.CUISINE, scroll_time=15)
        cuis_button.click()
        steps.try_get(Locator.SEARCH_FIELD.get()).send_keys("arab")
        assert len(steps.driver.find_elements_by_id(Locator.CUISINE.get())) == 1
        assert steps.try_get(Locator.CUISINE.get()).text == "Арабская кухня"

    @pytest.mark.name("Редактирование этажности здания с отправкой правок в OSM")
    def test_edit_building_with_osm(self, main, download_moscow_map, steps, settings_steps, osm_changes_reset):
        steps.search("Проспект Мира 78")
        steps.choose_first_search_result()

        steps.driver.implicitly_wait(3)
        edit_button = steps.scroll_down_to_element(locator=Locator.EDIT_PLACE_BUTTON, scroll_time=15)
        edit_button.click()

        steps.edit_level_field("11")

        steps.try_get(Locator.SAVE_BUTTON.get()).click()
        steps.try_get_by_text(LocalizedButtons.CANCELLATION.get()).click()
        steps.try_get(Locator.SAVE_BUTTON.get()).click()
        steps.find_and_click_send()
        settings_steps.login_osm()
        sleep(3)
        steps.driver.background_app(5)
        tags = self.get_osm_response()
        assert tags["building:levels"] == "11"

    def get_osm_response(self):
        resp = requests.get("https://api.openstreetmap.org/api/0.6/way/261952031")
        xml = ET.XML(resp.text)
        assert xml.findall("way")[0].get("user") == get_settings("Tests", "osm_user")
        return {tag.get("k"): tag.get("v") for tag in xml.findall("way")[0].findall("tag")}

    @pytest.yield_fixture
    def osm_changes_reset(self):
        yield
        resp = requests.get("https://api.openstreetmap.org/api/0.6/way/261952031")
        xml = ET.XML(resp.text)
        changeset_text = "<osm> <changeset> <tag k=\"created_by\" v=\"MAPS.ME android 9.6.1-Google\"/> <tag k=\"comment\" v=\"Updated a building\"/> <tag k=\"bundle_id\" v=\"com.mapswithme.maps.pro\"/> </changeset></osm>"
        changeset_id = requests.put("https://api.openstreetmap.org/api/0.6/changeset/create",
                                    data=changeset_text,
                                    auth=(get_settings("Tests", "osm_user"), get_settings("Tests", "osm_pass"))).text
        need_tag = [tag for tag in xml.findall("way")[0].findall("tag") if tag.get("k") == "building:levels"][0]
        need_tag.attrib["v"] = '9'
        xml.findall("way")[0].attrib["changeset"] = changeset_id
        str_xml = ET.tostring(xml).decode()
        requests.put("https://api.openstreetmap.org/api/0.6/way/261952031", data=str_xml,
                     auth=(get_settings("Tests", "osm_user"), get_settings("Tests", "osm_pass")))
