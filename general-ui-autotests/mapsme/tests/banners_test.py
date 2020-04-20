import json
import logging
import random
from os.path import realpath, dirname, join
from time import time, sleep

from mapsmefr.steps.locators import LocalizedMapsNames, LocalizedCategories, Locator, LocalizedButtons
from mapsmefr.utils.tools import is_element_scrolled
from selenium.common.exceptions import NoSuchElementException


class TestBanners:

    def test_banner_android(self, main, download_moscow_map, steps, search_steps):
        cities = [LocalizedMapsNames.MOSCOW, LocalizedMapsNames.LONDON, LocalizedMapsNames.PARIS,
                  LocalizedMapsNames.BERLIN, LocalizedMapsNames.NEWYORK]

        categories = [LocalizedCategories.WHERE_TO_EAT, LocalizedCategories.BUS_STOP, LocalizedCategories.SHOPPING]

        times = 30
        visited = []
        res = []

        try:
            for city in cities:
                steps.search(city.get())
                steps.choose_first_search_result()
                try:
                    steps.download_map_from_pp()
                except NoSuchElementException:
                    pass
                steps.press_back_until_main_page()

                for category in categories:
                    for _ in range(times):
                        try:
                            search_steps.search(category.get())
                            clicked = False
                            while not clicked:
                                for place in steps.driver.find_elements_by_id(Locator.TITLE.get()):
                                    if place.text in visited:
                                        continue
                                    visited.append(place.text)
                                    place.click()
                                    clicked = True
                                    break
                                steps.scroll_down(small=True)
                            banner = None
                            coordinates = None
                            try:
                                banner = steps.try_get("banner")
                                coordinates = steps.try_get("tv__place_latlon")
                                steps.scroll_down(from_el=steps.try_get(Locator.PP_ANCHOR.get()), small=True)

                                timeout = time() + 90
                                while not coordinates:
                                    steps.scroll_down(small=True)
                                    coordinates = steps.try_get("tv__place_latlon")
                                    if time() > timeout:
                                        break
                            except Exception as e:
                                logging.info(str(e))
                                steps.press_back_until_main_page()

                            res.append({"city": city.get(), "category": category.get(), "place": visited[-1],
                                        "banner": 1 if banner else 0,
                                        "coordinates": coordinates.text if coordinates else ""})

                            steps.press_back_until_main_page()
                        except Exception as e:
                            logging.info(str(e))
                            steps.press_back_until_main_page()
        except:
            pass

        with open("result.json", "a") as f:
            f.write(str(json.dumps(res)))

    def test_banner_android_92(self, main, download_moscow_map, steps, search_steps):
        res = []
        with open(join(dirname(realpath(__file__)), "result_android.json"), "r") as f:
            info = json.loads(f.read().replace("\'s", "\\\"s").replace("\'", "\""))

        current_city = info[0]["city"]
        try:
            for inf in info:
                if inf["city"] != current_city:
                    current_city = inf["city"]
                    steps.search(inf["city"])
                    steps.choose_first_search_result()
                    try:
                        steps.download_map_from_pp()
                    except NoSuchElementException:
                        pass
                    steps.press_back_until_main_page()

                steps.search(inf["coordinates"])
                steps.choose_first_search_result()

                try:
                    if steps.try_get("onmap_downloader"):
                        steps.try_get(Locator.DOWNLOAD_MAP_BUTTON.get()).click()
                        sleep(15)
                except:
                    pass

                banner = None
                try:
                    banner = steps.try_get("banner")

                except Exception as e:
                    logging.info(str(e))
                    steps.press_back_until_main_page()
                inf["banner92"] = 1 if banner else 0
                res.append(inf)
                steps.press_back_until_main_page()
        except:
            pass

        with open("result.json", "a") as f:
            f.write(str(json.dumps(res)))

    def test_banner_ios(self, main, steps, search_steps):
        cities = [LocalizedMapsNames.MOSCOW, LocalizedMapsNames.LONDON, LocalizedMapsNames.PARIS,
                  LocalizedMapsNames.BERLIN, LocalizedMapsNames.NEWYORK]
        categories = [LocalizedCategories.WHERE_TO_EAT, LocalizedCategories.BUS_STOP, LocalizedCategories.SHOPPING]

        times = 29
        visited = []

        res = []

        try:

            for city in cities:
                steps.search(city.get())
                steps.choose_first_search_result()
                try:
                    steps.download_map_from_pp()
                except NoSuchElementException:
                    pass
                steps.press_back_until_main_page()

                for category in categories:
                    for _ in range(times):
                        try:
                            search_steps.search(category.get())
                            try:
                                steps.try_get(LocalizedButtons.SEARCH.get()).click()
                            except:
                                pass
                            try:
                                steps.driver.hide_keyboard()
                            except:
                                pass
                            for place in steps.driver.find_elements_by_xpath("//*[@type='XCUIElementTypeCell']"):
                                title = place.find_element_by_xpath("./*[@name='searchTitle']").text
                                if title in visited:
                                    continue
                                y = place.location['y']
                                height = steps.driver.get_window_size()['height']
                                min_y = 120
                                logging.info("y: {}".format(y))
                                logging.info("height: {}".format(height))
                                logging.info("scrolled: {}".format(y < height - min_y))
                                logging.info(
                                    "{} scrolled: {}".format(title, is_element_scrolled(steps.driver, place)))
                                while not is_element_scrolled(steps.driver, place):
                                    logging.info(
                                        "{} scrolled: {}".format(title, is_element_scrolled(steps.driver, place)))
                                    steps.scroll_down(small=True)
                                    logging.info("y: {}".format(place.location_once_scrolled_into_view['y']))
                                    # logging.info(steps.driver.page_source)
                                visited.append(title)
                                sleep(1)
                                try:
                                    place.click()
                                except Exception as e:
                                    pass

                                break
                            banner = steps.try_get(LocalizedButtons.REMOVE_ADS.get())
                            coordinates = steps.try_get_by_xpath(
                                "//*[@type='XCUIElementTypeCell' and ./*[@name='ic_placepage_coordinate']]/*[@type='XCUIElementTypeStaticText']")
                            res.append({"city": city.get(), "category": category.get(), "place": visited[-1],
                                        "banner": 1 if banner else 0, "coordinates": coordinates.text})

                            steps.press_back_until_main_page()
                        except Exception as e:
                            logging.info(str(e))
                            try:
                                steps.driver.save_screenshot("{}.png".format(random.randint(1, 200)))
                            except Exception as e:
                                logging.info(str(e))
                            steps.press_back_until_main_page()
        except:
            pass

        with open("result.json", "a") as f:
            f.write(str(json.dumps(res)))
