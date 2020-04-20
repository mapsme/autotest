from enum import Enum

from mapsmefr.utils.tools import get_settings


class BookingIosAppLocalizedButtons(Enum):
    CHECK_IN = {"ru": "Регистрация заезда", "en": "Check-in"}
    SELECT = {"ru": "Выбрать", "en": "Select"}
    RESERVE = {"ru": "Забронировать", "en": "Reserve"}
    BOOK_NOW = {"ru": "Забронировать", "en": "Book now"}
    NEXT_STEP = {"ru": "Следующий шаг", "en": "Next step"}
    BOOK_CONFIRMED = {"ru": "Ваше бронирование подтверждено", "en": "Your booking is confirmed"}
    FINAL_STEP = {"ru": "Последний шаг", "en": "Final step"}
    CONTINUE = {"ru": "Продолжить", "en": "Continue"}
    DONE = {"ru": "Готово", "en": "Done"}
    FREE_CANCELLATION = {"ru": "Бесплатная отмена"}
    RESERVATION_NUMBER = {"ru": "Номер подтверждения", "en": "Confirmation Number"}

    def get(self):
        return self.value[get_settings("Android", "locale")]


class BookingAndroidAppLocators(Enum):
    REWIEW_TAB = "//*[contains(@class,'ActionBar$Tab') and ./*[@text='Reviews']]"
    NAVIGATE_UP = "//*[@content-desc='Navigate up']"
    CHECK_IN = "com.booking:id/check_in_date"
    SELECT_DATE = "com.booking:id/date_selection_box"
    CALENDAR_CONFIRM = "com.booking:id/calendar_confirm"
    SEARCH = "com.booking:id/search_search"

    SELECT_ROOMS = "com.booking:id/hotel_action_select"
    CHANGE_DATES = "com.booking:id/hotel_action_change_dates"
    FREE_CANCELLATION = "com.booking:id/quick_filters_free_cancellation"
    SELECT_ROOM = "com.booking:id/rooms_item_select_text_view"

    RESERVE = "com.booking:id/action_button"
    CVC_EDIT = "com.booking:id/credit_card_cvc_edit_text"
    OK_BUTTON = "com.booking:id/button_positive"

    BOOKING_CONFIRMED = "com.booking:id/bp_processing_screen_title"
    VIEW_CONFIRMATION = "com.booking:id/bp_processing_screen_proceed_confirmation_button"
    RESERVATION_NUMBER = "com.booking:id/booking_number"

    def get(self):
        return self.value
