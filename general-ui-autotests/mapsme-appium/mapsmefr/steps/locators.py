
from enum import Enum

from mapsmefr.utils.tools import get_settings


class PlatformDependantAttributes(Enum):
    TEXT_VALUE = {"Android": "text", "IOS": "value"}

    def get(self):
        return self.value[get_settings("System", "platform")]


class Localized(Enum):

    def get(self):
        return self.value[get_settings("Android", "locale")]


class IOSOnlySystemLocators(Localized):
    NEW_NOTE = {"ru": "Новая заметка", "en": "New note"}
    NOTE_FIELD = {"ru": "заметка", "en": "note"}


class LocalizedButtons(Localized):
    ACCEPT = {"ru": "Принять", "en": "Accept"}
    START = {"ru": 'Начать', "en": "Start"}
    TO = {"ru": 'Сюда', "en": "Route to"}
    FROM = {"ru": 'Отсюда', "en": "Route from"}
    ADD_STOP = {"ru": "Заехать", "en": "Add stop"}
    BOOKMARK = {"ru": 'Метка', "en": "Bookmark"}
    REMOVE = {"ru": 'Удалить', "en": "Remove"}
    DELETE = {"ru": 'Удалить', "en": "Delete"}
    SHOW_ON_MAP = {"ru": "Показать на карте", "en": "Show on the map"}
    OK = {"ru": 'Ок', "en": "Ok"}
    MY_BOOKMARKS = {"ru": 'Мои Метки', "en": "My Places"}
    CANCEL = {"ru": "Отменить", "en": "Cancel"}
    CANCELLATION = {"ru": "Отмена", "en": "Cancel"}
    STOP = {"ru": "Стоп", "en": "Stop"}
    DONE = {"ru": "Готово", "en": "Done"}
    MORE = {"ru": "Ещё", "en": "More"}
    CALL = {"ru": "Позвонить", "en": "Call"}

    SYSTEM_ERROR = {"ru": "Системная ошибка", "en": "System error"}

    EDIT_BOOKMARK = {"ru": "Редактировать метку", "en": "Edit Bookmark"}
    ADD_BOOKMARK_GROUP = {"ru": "Создать новый список", "en": "Create new list"}
    EDIT_BOOKMARK_GROUP = {"ru": "Настройки списка", "en": "List Settings"}
    SHARE_BOOKMARK_GROUP = {"ru": "Экспортировать файл", "en": "Export file"}
    SHARE_BOOKMARK = {"ru": "Поделиться", "en": "Share"}
    CREATE = {"ru": "Создать", "en": "Create"}
    EDIT_PLACE = {"ru": "Редактировать место", "en": "Edit Place"}
    SAVE = {"ru": "Сохранить", "en": "Save"}
    EDIT = {"ru": "Редактировать", "en": "Edit"}
    EDIT_BK = {"ru": "Править", "en": "Edit"}

    ALERT_ALLOW_ALWAYS = {"ru": "Разрешать всегда", "en": "Always Allow"}
    ALERT_ALLOW = {"ru": "Allow", "en": "Allow"}
    DOWNLOAD_MAPS = {"ru": "Загрузить карты", "en": "Download Maps"}
    DELETE_MAP = {"ru": "Удалить карту", "en": "Delete Map"}
    SETTINGS = {"ru": "Настройки", "en": "Settings"}
    BACK = {"ru": "Назад", "en": "Back"}
    FIND_MAP = {"ru": "Найти карту", "en": "Find map"}

    SEARCH = {"ru": "Найти", "en": "Search"}
    DOWNLOAD_MAP_BUTTON = {"ru": "Загрузить карту", "en": "Download Map"}
    DOWNLOAD_ALL_BUTTON = {"en": "Download All", "ru": "Загрузить все"}
    DOWNLOAD_NOW_BUTTON = {"ru": "Загрузить", "en": "Download"}
    DOWNLOAD_FROM_PP_BUTTON = {"ru": "Загрузить", "en": "Download"}

    SEARCH_CATEGORIES_TAB = {"ru": "Категории", "en": "Categories"}
    SEARCH_HISTORY_TAB = {"ru": "История", "en": "History"}

    BOOKING_COM = {"en": "Booking.com", "ru": "Booking.com"}
    BOOK = {"en": "Book", "ru": "Забронировать"}

    MANAGE_ROUTE = {"ru": "Изменить маршрут", "en": "Manage Route"}

    ROUTE_PLANNING_FAILED = {"ru": "Ошибка построения маршрута", "en": "Route Planning Failed"}
    ROUTE_TOO_LONG = {"ru": "Пешеходный маршрут слишком длинный",
                      "en": "The pedestrian route is too long"}
    ROUTE_CLOSER = {"ru": "Выберите начальную или конечную точку маршрута ближе к станции метро",
                    "en": "Please choose a start or end point closer to a subway station"}
    ROUTE_TO_TRANSPORT_TOO_LONG = {"ru": "Добираться до транспорта пешком слишком долго",
                                   "en": "The pedestrian route to the transport boarding point is too long"}
    INSTALL_BUTTON = {"ru": "Установить", "en": "Install"}
    TAXI_NOT_FOUND = {"ru": "Не удалось найти такси поблизости", "en": "Couldn't find a taxi nearby"}
    TAXI_NOT_AVAILABLE = {"ru": "Заказ такси временно недоступен.", "en": "Taxi ordering is temporarily unavailable."}
    TAXI_IS_NOT_AVAILABLE_HERE = {"ru": "Такси не доступно в данном регионе", "en": "Taxi is not available here"}
    TAXI = {"en": "Taxi", "ru": "Такси"}

    HOTEL_FILTER = {"ru": "Фильтр", "en": "Filter"}
    SEARCH_HOTEL_FILTER = {"ru": "Поиск", "en": "Search"}

    SHOW_MORE = {"ru": "Показать еще", "en": "Show more"}
    AEROPOLIS_DESCRIPTION = {"ru": "Отель «Аэрополис» расположен в 10 минутах ходьбы от станции метро «Динамо»",
                             "en": "A 10-minute walk from Dinamo Metro Station"}
    GUIDE_DOWNLOADED = {"ru": "Путеводитель был успешно загружен", "en": "The guide has been downloaded successfully"}
    AEROPOLIS_NAME = {"ru": "Отель Аэрополис", "en": "Aeropolis Hotel"}

    PLAN = {"ru": "Построить", "en": "Plan"}

    HOTEL_BOOKING = {"ru": "Бронирование отелей", "en": "Book hotels"}
    ATTRACTIONS = {"ru": "Достопримечательности", "en": "Attractions"}
    EAT_AND_DRINK = {"ru": "Перекусить", "en": "Eat and drink"}
    GUIDES = {"ru": "Путеводители", "en": "Guides"}

    LEAVE_A_REVIEW = {"ru": "Написать отзыв", "en": "Leave a Review"}
    DETAILS = {"ru": "Подробнее", "en": "Details"}
    POPULAR = {"ru": "Популярно", "en": "Popular"}

    OPEN = {"ru": "Открыть", "en": "Open"}
    LIST = {"ru": "Список", "en": "List"}
    NOT_NOW = {"ru": "Не сейчас", "en": "Not Now"}

    SEE_ALL = {"ru": "ПОСМОТРЕТЬ ВСЕ", "en": "SEE ALL"}
    NEXT_KEYBOARD = {"ru": "Следующая клавиатура", "en": "Next keyboard"}
    CLEAR_TEXT = {"ru": "Очистить текст", "en": "Clear text"}
    REMOVE_ADS = {"ru": "Отключить рекламу", "en": "Remove ads"}
    VEZET = {"ru": "Яндекс.Такси", "en": "Yandex.Taxi"}
    NEXT = {"ru": "Далее", "en": "Next"}

    BOOKMARK_COLOR = {"ru": "Цвет метки", "en": "Bookmark Color"}
    LAST_BACKUP = {"ru": "Последнее резервное копирование было {}", "en": "Last backup was {}"}
    RESTORE = {"ru": "Восстановить", "en": "Restore"}

    BOOKMARKS = {"ru": "Метки", "en": "Bookmarks"}

    GMAIL_OPEN_NAV = {"ru": "Открыть панель навигации", "en": "Open navigation drawer"}
    GMAIL_SENT = {"ru": "Отправленные", "en": "Sent"}
    GMAIL_BOOKMARKS_GROUP = {"ru": "С вами поделились метками MAPS.ME", "en": "MAPS.ME bookmarks were shared with you"}
    GMAIL_BOOKMARK = {"ru": "Смотри мою метку на карте MAPS.ME", "en": "Hey, check out my pin in MAPS.ME!"}
    MAIL_BOOKMARK = {"ru": "В прикрепленном файле мои метки",
                     "en": "Attached are my bookmarks from MAPS.ME offline maps"}

    SIGN_IN = {"ru": "ВОЙТИ", "en": "SIGN IN"}
    ENABLE_BACKUP = {"ru": "РАЗРЕШИТЬ РЕЗЕРВНОЕ КОПИРОВАНИЕ", "en": "ENABLE BACKUP"}
    RESTORE_BOOKMARKS = {"ru": "Восстановить метки", "en": " Restore bookmarks"}
    OPEN_WITH = {"ru": "Открыть с помощью", "en": "Open with"}

    MAIL = {"ru": "Почта", "en": "Mail"}
    BLUE = {"ru": "Синий", "en": "Blue"}
    RETURN = {"ru": "Ввод", "en": "Return"}
    SEND = {"ru": "Отправить", "en": "Send"}
    MAILBOXES = {"ru": "Ящики", "en": "Mailboxes"}
    ACTIVITY = {"ru": "Активность", "en": "Activity"}
    CONTINUE = {"ru": "Продолжить", "en": "Continue"}
    CONTINUE_SIGN_IN = {"ru": "Дальше", "en": "Continue"}
    ORDER_TAXI = {"ru": "Заказать такси", "en": "Order a taxi"}

    AVOID_TOLL_ROADS = {"ru": "Избегать платных дорог", "en": "Avoid toll roads"}
    TOLL_ROAD = {"ru": "Платная дорога", "en": "Toll road"}
    AVOID_UNPAVED_ROADS = {"ru": "Избегать грунтовых дорог", "en": "Avoid unpaved roads"}
    UNPAVED_ROAD = {"ru": "Грунтовая дорога", "en": "Unpaved road"}
    AVOID_FERRY_ROADS = {"ru": "Избегать паромных переправ", "en": "Avoid ferry crossings"}
    FERRY_ROAD = {"ru": "Паромная переправа", "en": "Ferry crossing"}

    SHARING_OPTIONS = {'ru': 'Настройки доступа', "en": "Sharing options"}
    BOOKMARKS_SORT = {"en": "Sort", "ru": "Сортировать"}
    NEAR_ME = {"en": "Near me", "ru": "Рядом со мной"}

    A_WEEK_AGO = {"en": "A week ago", "ru": "Неделю назад"}
    CANCELL_ALL = {"en": 'Cancell all', "ru": "Отменить все"}
    CANCEL_DOWNLOAD = {"en": "Cancel Download", "ru": "Отменить загрузку"}

    TRETYAKOV = {"en": "Tretyakov Gallery", "ru": "Третьяковская галерея"}
    DON_KIKHOT = {"en": "Don Kikhot", "ru": "Дон Кихот"}
    GUIDES_BY_TITLE = {"en": "Guides by tag “City walk”", "ru": "Путеводители по тегу «Городские прогулки»"}
    REMOVE_ADS_TITLE = {"ru": "Отключите всю рекламу и поддержите MAPS.ME", "en": "Remove all ads and support MAPS.ME"}
    MORE_OPRIONS = {"en": "More options", "ru": "Другие варианты"}
    WHY_SUPPORT = {"ru": "Зачем поддерживать MAPS.ME?", "en": "Why support MAPS.ME?"}
    WE_WILL_REMOVE_ADS = {"ru": "Мы отключим для вас всю рекламу", "en": "We will remove all ads for you"}
    YOU_HELP_US_TO_IMPROVE = {"ru": "Вы помогаете нам улучшать MAPS.ME", "en": "You help us to improve MAPS.ME"}
    HELP_IMPROVE_OSM = {"ru": "Вы помогаете нам улучшать карты OpenStreetMaps.org",
                        "en": "You help us improve open maps OpenStreetMap.org"}
    DOWNLOAD_GUIDES = {"en": "SEARCH GUIDES", "ru": "НАЙТИ ПУТЕВОДИТЕЛИ"}
    GET_DIRECT_LINK = {"en": "Upload and get a direct link", "ru": "Загрузить и получить ссылку"}
    UPLOAD_AND_PUBLISH = {"en": "Upload and publish", "ru": "Загрузить и опубликовать"}
    EDIT_ONLINE = {"en": "EDIT ONLINE", "ru": "РЕДАКТИРОВАТЬ ОНЛАЙН"}
    TERMS_OF_USE = {"en": "I agree to the Terms of Use", "ru": "Я согласен с Условиями использования"}
    PRIVACY_POLICY = {"en": "I agree to the Privacy Policy", "ru": "Я согласен с Политикой конфиденциальности"}
    SIGN_IN_WITH = {"en": "Sign in with", "ru": "Авторизуйтесь с помощью"}
    SORT = {"en": "Sort…", "ru": "Сортировать..."}
    SEARCH_IN_THE_LIST = {"en": "Search in the list", "ru": "Искать в списке"}
    SEARCH_IN_THE_MAP = {"en": "Search in the map", "ru": "Посмотреть на карте"}
    CATEGORY = {"en": "Category"}
    OSM = {"en": "OpenStreetMap", "ru": "OpenStreetMap"}
    LOG_IN_BTN = {"en": "Log In"}
    VLADIMIR_VELIKI = {"ru": "Владимиру Великому", "en": "Vladimir Velikiy"}
    VLADIMIR_MEMORIAL_DESCRIPTION = {"ru": "Памятник великому князю Киевскому Владимиру",
                                     "en": "The Monument to Vladimir the Great"}
    VIEW = {"en": "View", "ru": "Посмотреть"}
    THIS_PLACE_IN_GUIDES = {"en": "THIS PLACE IN THE GUIDES CATALOG", "ru": "ЭТО МЕСТО В КАТАЛОГЕ ПУТЕВОДИТЕЛЕЙ"}
    DEFINE_ROADS = {"en": "DEFINE ROADS TO AVOID", "ru": "НАСТРОИТЬ ПУТИ ОБЪЕЗДА"}
    RESET = {"en": "Reset", "ru": "Сбросить"}
    SUBWAY = {"ru": "Метро", "en": "Subway"}
    SUBWAY_UNAVAILABLE = {"ru": "Карта метро недоступна", "en": "Subway map is unavailable"}


class BookingButtons(Localized):
    MORE_ON_BOOKING_BUTTON = {"ru": "Больше на Booking.com", "en": "More on Booking.com"}
    MORE_REVIEWS_ON_BOOKING_BUTTON = {"ru": "Больше отзывов на Booking.com", "en": "More reviews on Booking.com"}
    DETAILS_ON_BOOKING_BUTTON = {"ru": "Подробней на Booking.com", "en": "Details on Booking.com"}
    # BOOK_BUTTON = {"ru": "", "en": "Book"}
    CHECK_IN = {"ru": "ЗАЕЗД", "en": "CHECK IN"}
    CHECK_OUT = {"ru": "ОТЪЕЗД", "en": "CHECK OUT"}
    RATING_ANY = {"ru": "Любой", "en": "Any"}
    RATING_GOOD = {"ru": "7.0+ Хорошо", "en": "7.0+ Good"}
    RATING_VERY_GOOD = {"ru": "8.0+ Очень хорошо", "en": "8.0+ Very Good"}
    RATING_EXCELLENT = {"ru": "9.0+ Отлично", "en": "9.0+ Excellent"}
    AVAILABLE = {"ru": "Есть места", "en": "Available"}

    HOTEL = {"ru": "Гостиница", "en": "Hotel"}
    APARTMENTS = {"ru": "Апартаменты", "en": "Apartments"}
    CAMPING = {"ru": "Кемпинг", "en": "Camping"}
    CHALET = {"ru": "Шале", "en": "Chalet"}
    GUEST_HOUSE = {"ru": "Гостевой дом", "en": "Guest House"}
    HOSTEL = {"ru": "Хостел", "en": "Hostel"}
    MOTEL = {"ru": "Мотель", "en": "Motel"}
    RESORT = {"ru": "Дом отдыха", "en": "Resort"}

    RATING = {"ru": "Рейтинг", "en": "Rating"}
    BOOKING_MENU_BTN = {"ru": "Подобрать отель на карте", "en": "Pick a hotel on the map"}



class Locator(Enum):
    PACKAGE_NAME = "com.mapswithme.maps.pro:id/{}"

    ACCEPT_POLICY_BUTTON = {"Android": "btn__continue", "IOS": "welcome_storyboard.button_next"}
    IOS_NEXT_BUTTON = {"Android": "btn__continue", "IOS": "welcome_storyboard.button_next2"}
    AGREE_PRIVACY = {"Android": "privacy_policy_welcome_checkbox", "IOS": "welcome_storyboard.agree_privacy.check"}
    AGREE_TERMS = {"Android": "term_of_use_welcome_checkbox", "IOS": "welcome_storyboard.agree_terms.check"}

    FIRST_TIME_INFO_FRAME = {"Android": "material_target_prompt_view", "IOS": "tips_bookmarks_got_it"}
    MENU_BUTTON = {"Android": 'menu', "IOS": "menuButton"}
    SEARCH_BUTTON = {"Android": 'search', "IOS": "searchButton"}
    SEARCH_BUTTON_ROUTING = {"Android": "btn_search", "IOS": "searchButton"}
    SEARCH_FIELD = {"Android": "query", "IOS": "queryField"}
    DOWNLOAD_MAPS = {"Android": 'download_maps', "IOS": None}
    SETTINGS = {"Android": "settings", "IOS": None}
    DOWNLOAD_ICON = {"Android": 'downloader_status', "IOS": "ic download"}
    DOWNLOADED_ICON = {"Android": None, "IOS": "ic check"}
    FOLDER_ICON = {'IOS': "ic folder"}
    DOWNLOAD_NOW_BUTTON = {"Android": None, "IOS": "downloadNowButton"}
    DOWNLOAD_NOT_NOW = {"Android": None, "IOS": "notNowButton"}
    IN_PROGRESS = {"Android": 'downloader_progress_wheel', "IOS": "ic close spinner"}
    IN_PROGRESS_WHEEL = {"Android": "wheel_progress", "IOS": "ic close spinner"}
    SEARCH_PROGRESS = {"Android": 'progress', "IOS": "In progress"}
    NAME = {"Android": 'name', "IOS": None}
    FOUND_NAME = {"Android": "found_name"}
    TITLE = {"Android": 'title', "IOS": "searchTitle"}
    TV_TITLE = {"Android": 'tv__title', "IOS": None}
    PP = {"Android": "placepage", "IOS": None}
    PP_ANCHOR = {"Android": "pull_icon", "IOS": "ic_anchor_up"}
    PP_BUTTONS = {"Android": 'pp__details_frame', "IOS": None}
    TIME = {"Android": "time", "IOS": None}
    DISTANCE = {"Android": "distance", "IOS": None}
    EDIT_BOOKMARK_BUTTON = {"Android": 'tv__bookmark_edit', "IOS": LocalizedButtons.EDIT_BOOKMARK}
    BOOKMARK_SET = {"Android": 'tv__bookmark_set', "IOS": None}
    BOOKMARK_NAME = {"Android": 'tv__bookmark_name', "IOS": None}
    BOOKMARKS_BUTTON = {"Android": 'bookmarks', "IOS": "bookmarksButton"}
    EDIT_PLACE_BUTTON = {"Android": 'tv__editor', "IOS": LocalizedButtons.EDIT_PLACE}
    SAVE_BUTTON = {"Android": 'save', "IOS": LocalizedButtons.SAVE}
    ALERT_TITLE = 'alertTitle'
    CANCEL_BUTTON = {"Android": None, "IOS": "cancelButton"}
    ACCEPT_BUTTON = {"Android": "accept_btn", "IOS": "acceptButton"}
    SEND = {"Android": None, "IOS": "OKButton"}
    DISCOVERY = {"Android": "discovery", "IOS": "discoveryButton"}
    POPULAR = {"Android": "popular_rating_view", "IOS": LocalizedButtons.POPULAR}

    SWITCH = {"Android": "switchWidget", "IOS": None}
    DOWNLOAD_MAP_BUTTON = {"Android": "downloader_button", "IOS": LocalizedButtons.DOWNLOAD_MAP_BUTTON}

    # edit place form

    LEVELS_LAYOUT = {"Android": 'block_levels', "IOS": None}

    START = {"Android": None, "IOS": "goButton"}

    DELETE_MAP = {"Android": None, "IOS": LocalizedButtons.DELETE_MAP}

    CREATE_NEW_LIST_INPUT = {"Android": "et__input", "IOS": None}

    GET_POSITION_LIGHT = {"Android": "my_position", "IOS": "btn get position light"}
    SHOW_ON_MAP = {"Android": "show_on_map", "IOS": "viewOnMapButton"}
    ZOOM_IN = {"Android": "nav_zoom_in", "IOS": "btn zoom in light"}
    ZOOM_OUT = {"Android": "nav_zoom_out", "IOS": "btn zoom out light"}

    TOGGLE = {"Android": "toggle", "IOS": None}
    STOP = {"Android": "stop", "IOS": LocalizedButtons.STOP.get()}
    DONE = {"Android": "done", "IOS": LocalizedButtons.DONE}
    MORE_BUTTON = {"Android": "more_btn", "IOS": "ic24PxMore"}
    MAP_LAYERS = {"Android": "subway", "IOS": "layers_button"}

    # edit bookmark?

    EDIT_BOOKMARK_NAME = {"Android": "et__bookmark_name", "IOS": None}
    EDIT_BOOKMARK_SET = {"Android": "tv__set_name", "IOS": None}
    EDIT_BOOKMARK_SET_RADIOBUTTON = {"Android": "rb__selected", "IOS": None}
    EDIT_BOOKMARK_DESCRIPTION = {"Android": "et__description", "IOS": None}
    EDIT_BOOKMARK_GROUP_NAME = {"Android": "edit_category_name_view", "IOS": None}
    EDIT_BOOKMARK_GROUP_DESCRIPTION = {"Android": "edit_description", "IOS": None}
    BACKUP_BUTTON = {"Android": "backup_button", "IOS": LocalizedButtons.SIGN_IN}
    RESTORE_BUTTON = {"Android": "restore_button", "IOS": LocalizedButtons.RESTORE_BOOKMARKS}
    TERM_OF_USE_CHECKBOX = {"Android": "termOfUseCheck", "IOS": LocalizedButtons.TERMS_OF_USE}
    POLICY_CHECKBOX = {"Android": "privacyPolicyCheck", "IOS": LocalizedButtons.PRIVACY_POLICY}
    GOOGLE_BUTTON = {"Android": "google_button", "IOS": None}
    SHARE_BOOKMARK = {"Android": None, "IOS": "ic menu share"}


    # ROUTING

    ROUTING_CHOOSE_POINT = {"IOS": "routePlaningButtomPanel", "Android": "btn__search_point"}
    ROUTING_BIKE = {"IOS": "ic bike", "Android": "bicycle"}
    ROUTING_METRO = {"IOS": "ic train", "Android": "transit"}
    ROUTING_WALK = {"IOS": "ic pedestrian", "Android": "pedestrian"}
    ROUTING_CAR = {"IOS": "ic car", "Android": "vehicle"}
    ROUTING_TAXI = {"IOS": "ic taxi", "Android": "taxi"}

    TAXI_VEZET = {"IOS": LocalizedButtons.VEZET, "Android": "taxi_panel"}
    ROUTE_STOP_A = {"IOS": "ic_route_manager_stop_a"}
    ROUTE_STOP_B = {"IOS": "ic_route_manager_stop_b"}
    ROUTE_MY_POSITION = {"IOS": "ic_route_manager_my_position"}
    ROUTE_START = {"IOS": "ic_route_manager_start"}
    ROUTE_FINISH = {"IOS": "ic_route_manager_finish"}
    ROUTE_METRO = {"IOS": "ic_20px_route_planning_metro", "Android": "transit_panel"}

    DRIVING_OPTIONS = {"IOS": LocalizedButtons.DEFINE_ROADS, "Android": "driving_options_btn_title"}

    # Booking.com ones
    MORE_ON_BOOKING = {"Android": "tv__place_hotel_more_on_web", "IOS": BookingButtons.MORE_ON_BOOKING_BUTTON}
    MORE_REVIEWS_ON_BOOKING = {"Android": "tv__place_hotel_reviews_more",
                               "IOS": BookingButtons.MORE_REVIEWS_ON_BOOKING_BUTTON}
    DETAILS_ON_BOOKING = {"Android": "ll__more", "IOS": BookingButtons.DETAILS_ON_BOOKING_BUTTON}

    HOTEL_FILTER = {"IOS": LocalizedButtons.HOTEL_FILTER, "Android": "filter_button"}
    HOTEL_FILTER_CLEAR = {"IOS": "ic clear filters", "Android": "filter_icon"}
    HOTEL_DESCRIPTION = {"IOS": None, "Android": "ll__place_hotel_description"}
    HOTEL_GOOD_REVIEW = {"IOS": "ic_good", "Android": "tv__positive_review"}
    HOTEL_BAD_REVIEW = {"IOS": "ic_bad", "Android": "tv__negative_review"}
    HOTEL_PP_TAXI_VEZET = {"IOS": "ic_taxi_logo_vezet", "Android": "ll__place_page_taxi"}

    NOT_NOW = {"IOS": LocalizedButtons.NOT_NOW, "Android": "show_on_map_decline_btn"}

    CUISINE = {"Android": "cuisine", "IOS": None}
    LOGIN_OSM = {"Android": "login_osm", "IOS": LocalizedButtons.OSM}
    OSM_USERNAME_FIELD = {"Android": "osm_username", "IOS": None}
    OSM_PASSWORD_FIELD = {"Android": "osm_password", "IOS": None}
    ENTER_OSM_BUTTON = {"Android": "login", "IOS": None}

    DOWNLOAD_GUIDES = {"Android": "download_routers_btn", "IOS": LocalizedButtons.DOWNLOAD_GUIDES}
    GET_DIRECT_LINK = {"Android": "get_direct_link_text", "IOS": LocalizedButtons.GET_DIRECT_LINK}
    UPLOAD_AND_PUBLISH = {"Android": "upload_and_publish_text", "IOS": LocalizedButtons.UPLOAD_AND_PUBLISH}
    EDIT_ON_WEB = {'Android': "edit_on_web_btn", "IOS": LocalizedButtons.EDIT_ONLINE}
    BOOKMARKS_MORE = {"Android": "bookmarks_more", "IOS": LocalizedButtons.MORE}
    BOOKMARKS_SEARCH = {'Android': "bookmarks_search", "IOS": LocalizedButtons.SEARCH_IN_THE_LIST}

    PLUS_DOWNLOADER_BUTTON = {"Android": "fab", "IOS": "ic nav bar add"}
    DOWNLOAD_ALL = {"Android": "action", "IOS": LocalizedButtons.DOWNLOAD_ALL_BUTTON}
    SUMMARY = {"Android": "summary"}

    PP_SUBTITLE = {"Android": "tv__subtitle"}
    POI_DESCRIPTION = {"Android": "poi_description"}
    PROMO_POI_DESCRIPTION = {"Android": "promo_poi_description"}
    CATALOG_PROMO_PP = {"Android": "catalog_promo_container"}
    PROMO_POI_CARD = {"Android": "promo_poi_card"}
    PROMO_POI_CTA_BUTTON = {"Android": "place_single_bookmark_cta", "IOS": LocalizedButtons.VIEW}
    AD_BANNER = {"Android": "banner_container", "IOS": "ic_ads_fb"}
    RESET_BTN = {"Android": "reset", "IOS": LocalizedButtons.RESET}
    AD_CLOSE = {"Android": "remove_btn", "IOS": "ic_ad_close"}
    AD_REMOVE = {"Android": "tv__action_remove", "IOS": LocalizedButtons.REMOVE_ADS}


    def get(self):
        if get_settings("System", "platform") == "Android":
            return "{}:id/{}".format(get_settings("Android", "package"), self.value["Android"])
        else:
            ios_locator = self.value["IOS"]
            if type(ios_locator) != str and ios_locator is not None:
                return ios_locator.get()
            else:
                return ios_locator


class LocalizedMapsNames(Localized):
    UNKNOWN_PLACE = {"ru": "Неизвестное место", "en": "Unknown Place"}

    RUSSIA = {"ru": "Россия", "en": "Russia"}
    CHINA = {"ru": "Китай", "en": "China"}
    ARGENTINA = {"ru": "Аргентина", "en": "Argentina"}
    GERMANY = {"ru": "Германия", "en": "Germany"}
    USA = {"ru": "Соединённые Штаты Америки", "en": "United States of America"}
    SPAIN = {"ru": "Испания", "en": "Spain"}
    FRANCE = {"ru": "Франция", "en": "France"}
    CZECH = {"ru": "Чехия", "en": "Czech Republic"}
    PORTUGAL = {"ru": "Португалия", "en": "Portugal"}
    NORTH_KOREA = {"ru": "Корейская Народно-Демократическая Республика", "en": "North Korea"}
    GREAT_BRITAIN = {"ru": "Великобритания", "en": "United Kingdom"}
    ITALY = {"ru": "Италия", "en": "Italy"}
    DOMODEDOVO = {"ru": "Домодедово", "en": "Domodedovo"}
    IRELAND = {"ru": "Ирландия", "en": "Ireland"}

    CONNACHT = {"ru": "Коннахт", "en": "Connacht"}
    LEINSTER = {"ru": "Ленстер", "en": "Leinster"}
    MUNSTER = {"ru": "Манстер", "en": "Munster"}
    ULSTER = {"ru": "Ольстер", "en": "Ulster"}

    DUBLIN = {"ru": "Дублин", "en": "Dublin"}

    ANDORRA = {"ru": "Андорра", "en": "Andorra"}
    EGYPT = {"ru": "Египет", "en": "Egypt"}
    MOSCOW = {"ru": "Москва", "en": "Moscow"}
    MOSCOW_OBLAST = {"ru": "Московская область", "en": "Moscow Oblast"}
    VORONEZH = {"ru": "Воронежская область", "en": "Voronezh Oblast"}
    LIPETSK = {"ru": "Липецкая область", "en": "Lipetsk Oblast"}
    TULA = {"ru": "Тульская область", "en": "Tula Oblast"}
    NOVGOROD = {"ru": "Новгородская область", "en": "Novgorod Oblast"}
    TVER = {"ru": "Тверская область", "en": "Tver Oblast"}
    YAROSLAVL = {"ru": "Ярославская область", "en": "Yaroslavl Oblast"}
    ALTAI_KRAI = {"ru": "Алтайский край", "en": "Altai Krai"}
    VLADIVOSTOK = {"ru": "Владивосток", "en": "Vladivostok"}
    PRIMORSKY_KRAI = {"ru": "Приморский край", "en": "Primorsky Krai"}
    NIZHNIY_NOVGOROD = {"ru": "Нижний Новгород", "en": "Nizhny Novgorod"}
    CHELYABINSK = {"ru": "Челябинск", "en": "Chelyabinsk"}

    HEBEI = {"ru": "Хэбэй", "en": "Hebei"}
    BUENOS_AIRES = {"ru": "Буэнос-Айрес", "en": "Buenos Aires"}
    HAMBURG = {"ru": "Гамбург", "en": "Hamburg"}
    SAN_FRANCISCO = {"ru": "Сан-Франциско", "en": "San Francisco"}
    MADRID = {"ru": "Мадрид", "en": "Madrid"}
    SEVILLE = {"ru": "Севилья", "en": "Seville"}
    SICILY = {"ru": "Сицилия", "en": "Sicily"}
    PARIS = {"ru": "Париж", "en": "Paris"}
    PRAGUE = {"ru": "Прага", "en": "Prague"}
    LONDON = {"ru": "Лондон", "en": "London"}
    AMSTERDAM = {"ru": "Амстердам", "en": "Amsterdam"}
    NEWYORK = {"ru": "Нью-Йорк", "en": "New York"}
    BERLIN = {"ru": "Берлин", "en": "Berlin"}
    PORTO = {"ru": "Порту", "en": "Porto"}

    # states
    CALIFORNIA = {"ru": "Калифорния", "en": "California"}


class LocalizedCategories(Localized):
    CAPITAL = {"ru": "Столица", "en": "Capital"}
    COUNTRY = {"ru": "Страна", "en": "Country"}
    CITY = {"ru": "Город", "en": "City"}
    HOTEL = {"ru": "Гостиница", "en": "Hotel"}
    HOTELS = {"ru": "Отели", "en": "Hotels"}
    SIGHTS = {"ru": "Достопримечательность", "en": "Sights"}
    WHERE_TO_EAT = {"ru": "Где поесть", "en": "Where to eat"}
    THEATRE = {"ru": "Театр", "en": "Theatre"}
    CHURCH = {"ru": "Храм", "en": "Church"}
    MOUNTAIN = {'ru': "Гора", "en": "Mountain"}

    ATTRACTION = {"ru": "Достопримечательность", "en": "Attraction"}
    MUSEUM = {"ru": "Музей", "en": "Museum"}
    PARK = {"ru": "Парк", "en": "Park"}
    ZOO = {"ru": "Зоопарк", "en": "Zoo"}
    MONUMENT = {"ru": "Монумент", "en": "Monument"}
    MEMORIAL = {"ru": "Памятник", "en": "Memorial"}
    FOOD = {"ru": "Гастрономия", "en": "Food"}
    FOODS = {"ru": "Еда", "en": "Food"}

    BUILDING = {"ru": "Здание", "en": "Building"}
    SHOPPING = {"ru": "Шоппинг", "en": "Shopping"}
    BUS_STOP = {"ru": "Остановка ", "en": "Bus stop "}

    RESTAURANT = {"ru": "Ресторан", "en": "Restaurant"}
    CAFE = {"ru": "Кафе", "en": "Cafe"}
    MARKETPLACE = {"ru": "Рынок", "en": "Marketplace"}
    BAR = {"ru": "Бар", "en": "Bar"}
    PUB = {"ru": "Паб", "en": "Pub"}
    FASTFOOD = {"ru": "Фастфуд", "en": "Fast Food"}
    GROCERY = {"ru": "Продуктовый магазин", "en": "Convenience Store"}
    SHOP = {"en": "Shop", "ru": "Магазин"}
    CLOTHES_SHOP = {"en": "Clothes Shop", "ru": "Магазин одежды"}
    BEAUTY_SHOP = {"en": "Beauty Shop", "ru": "Салон красоты"}
    JEWELRY = {"en": "Jewelry", "ru": "Ювелирный магазин"}
    FLORISTS = {"en": "Florist’s", "ru": "Цветочный магазин"}
    CAR_SHOP = {"en": "Car Shop", "ru": "Автосалон"}
    TICKET_SHOP = {"en": "Ticket Shop", "ru": "Билетная касса"}
    OPTICIAN = {"en": "Optician’s", "ru": "Оптика"}
    LIQUOR_STORE = {"en": "Liquor Store", "ru": "Магазин алкоголя"}
    BOOKSTORE = {'en': "Bookstore", "ru": "Книжный магазин"}
    GIFT_SHOP = {"en": "Gift Shop", "ru": "Магазин сувениров"}
    VEG_AND_FRUITS = {"ru": "Овощи и фрукты", "en": "Greengrocer's"}
    ELECTRONICS = {"ru": "Электротехника", "en": "Electronics"}
    BAKERY = {"ru": "Булочная", "en": "Bakery"}
    WINE_SHOP = {"ru": "Винный магазин", "en": "Wine Shop"}
    BUTCHERS = {'ru': "Мясная лавка", "en": "Butcher's"}
    HAIRDRESSER = {"ru": "Парикмахерская", "en": "Hairdresser"}
    HARDWARE_STORE = {"ru": "Хозяйственный", "en": "Hardware Store"}

    MALL = {"ru": "Торговый центр", "en": "Mall"}

    BURGER = {"en": "Burger", "ru": "Бургеры"}
    ARAB_CUISINE = {"en": "Arab", "ru": "Арабская кухня"}


class LocalizedSettings(Localized):
    ON_3D = {"ru": "3D здания", "en": "3D buildings"}
    AUTO_DOWNLOAD = {"ru": "Автоматическая загрузка", "en": "Auto-download"}
    DISABLE_AUTODOWNLOAD = {"ru": "Запретить автозагрузку", "en": "Disable autodownload"}
    LATIN = {"ru": "Латинская транслитерация", "en": "Transliteration into Latin"}
    STATISTIC = {"ru": "Сбор статистики", "en": "Send Statistics"}
    GOOGLE_PLAY_SERVICES = {"ru": "Google Play Services", "en": "Google Play Services"}
    LOG_RECORDS = {"ru": "Включить запись логов", "en": "Enable logging"}
    PERSPECTIVE = {"ru": "Перспективный вид", "en": "Perspective view"}
    AUTO_ZOOM = {"ru": "Автозум", "en": "Auto zoom"}
    NIGHT_MODE = {"ru": "Ночной режим", "en": "Night Mode"}
    SPEED_CAMERAS = {"ru": "Камеры скорости", "en": "Speed cameras"}
    POWER_SAVING_MODE = {"ru": "Режим энергосбережения", "en": "Power saving mode"}
    RECENT_TRACK = {"ru": "Недавний путь", "en": "Recent track"}
    ABOUT = {"ru": "О программе", "en": "About MAPS.ME"}
    BOOKMARK_BACKUP = {"ru": "Резервное копирование меток", "en": "Backup Bookmarks"}
    MEASUREMENT_UNITS = {"ru": "Единицы измерения", "en": "Measurement units"}
    MOBILE_INTERNET = {"ru": "Мобильный интернет", "en": "Mobile Internet"}
    INSREASE_FONT = {"ru": "Увеличить шрифт на карте", "en": "Increase font size on the map"}
    ZOOM_BUTTONS = {"ru": "Кнопки масштаба", "en": "Zoom buttons"}
    VOICE_INSTRUCTIONS = {"ru": "Голосовые инструкции", "en": "Voice Instructions"}
    VOICE_LANGUAGE = {"ru": "Язык подсказок", "en": "Voice Language"}
    REMOVE_ADS = {"ru": "Отключить рекламу", "en": "Remove ads"}

    AUTOMATIC = {"ru": "Авто", "en": "Automatic"}
    AUTOMATICALLY = {"ru": "Автоматически", "en": "Auto"}
    ON = {"ru": "Включен", "en": "On"}
    ON_WITH_DOT = {"ru": "Вкл.", "en": "On"}
    OFF = {"ru": "Выключен", "en": "Off"}
    RU_OFF = {"ru": "Выключено", "en": "Off"}
    OFF_WITH_DOT = {"ru": "Выкл.", "en": "Off"}
    AUTO = {"ru": "Авто", "en": "Auto"}
    ALWAYS = {"ru": "Всегда", "en": "Always"}
    NEVER = {"ru": "Никогда", "en": "Never"}
    MAXIMUM = {"ru": "Максимальное энергосбережение", "en": "Maximum power saving"}
    ONE_HOUR = {"ru": "1 час", "en": "1 hour"}
    BY_DEFAULT = {"ru": "По умолчанию", "en": "By default"}
    BY_DATE = {"ru": "По дате", "en": "By date"}
    BY_DISTANCE = {"ru": "По расстоянию", "en": "By distance"}
    BY_TYPE = {"ru": "По типу", "en": "By type"}
    MILES = {"ru": "Мили", "en": "Miles"}
    KILOMETERS = {"ru": "Километры", "en": "Kilometers"}
    ALWAYS_ASK = {"ru": "Всегда спрашивать", "en": "Always Ask"}
    USE_ALWAYS = {"ru": "Всегда", "en": "Use Always"}
    NEVER_USE = {"ru": "Никогда не использовать", "en": "Never Use"}
