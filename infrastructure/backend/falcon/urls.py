from django.conf.urls import url

from falcon.handlers import *
from falcon.handlers import jenkins
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    url(r'^device(/|)((?P<id>[0-9]{1,4})|)$', devices.device),
    url(r'^device(/|)((?P<device_id>[a-zA-Z0-9]+)|)$', devices.device),
    url(r'^device/kill(/|)((?P<id>[0-9]{1,4})|)$', jenkins.kill_appium_session),
    url(r'^refresh$', devices.refresh),
    url(r'^markers$', sessions.markers),

    url(r'^testitem(/|)((?P<id>[0-9]+)|)$', sessions.testitem),
    url(r'^testitem/refresh$', sessions.test_item_refresh),
    url(r'^session(/|)((?P<id>[0-9]+)|)$', sessions.session),
    url(r'^session(/|)((?P<type>[a-zA-Z]+)|)$', sessions.session),
    url(r'^testresult(/|)((?P<id>[0-9]+)|)$', sessions.testresult),
    url(r'^download/csv(/|)((?P<id>[0-9]+)|)$', sessions.csv_download),
    url(r'^crashes/unique(/|)((?P<id>[0-9]+)|)$', monkey.unique_crash),
    url(r'^crashes/top$', monkey.top_unique),
    url(r'^crashes/search$', monkey.search_unique),
    url(r'^crashes/stats(/|)((?P<id>[0-9]+)|)$', monkey.unique_crash_stats),
    url(r'^crashes/releases(/|)((?P<id>[0-9]+)|)$', monkey.unique_releases),
    url(r'^monkey/sessionstats$', monkey.session_stats),

    #url(r'^release(/|)((?P<id>[0-9]+)|)$', releases.release),
    #url(r'^feature(/|)((?P<id>[0-9]+)|)$', releases.feature),

    url(r'^meminfo(/|)((?P<test_result_id>[0-9]+)|)$', meminfo.meminfo),
    url(r'^metricsraw(/|)((?P<test_result_id>[0-9]+)|)$', hardware.metricsraw),

    url(r'^hardwaredevices$', hardware.hardwaredevices),
    url(r'^hardwaretesitems$', hardware.hardwaretesitems),
    url(r'^hardwaretestresults$', hardware.hardwaretestresults),
    url(r'^standart/devices$', hardware.standart_devices),
    url(r'^standart/testitems$', hardware.standart_tesitems),
    url(r'^standart/releases$', hardware.standart_releases),
    url(r'^standart/check$', hardware.check_standart),
    url(r'^diff/power$', hardware.get_diff_standart),
    url(r'^diff/memory$', meminfo.get_diff_standart),
    url(r'^average/power(/|)((?P<test_result_id>[0-9]+)|)$', hardware.average_power),
    url(r'^average/memory(/|)((?P<test_result_id>[0-9]+)|)$', meminfo.average_memory),

    url(r'^monkeycrash(/|)((?P<id>[0-9]+)|)$', monkey.monkey_crash),
    url(r'^booking(/|)((?P<id>[0-9]+)|)$', booking.booking),

    url(r'^jsonmetrics/power$', hardware.json_power_metrics),
    url(r'^jsonmetrics/memory$', meminfo.json_memory_metrics),
    url(r'^standartmetrics/power$', hardware.metrics_standart),
    url(r'^standartmetrics/memory$', meminfo.metrics_standart),
    url(r'^comparing/result$', hardware.compare_results),

    url(r'^start/buildcheck$', jenkins.start_build_check),
    url(r'^start/refresh$', jenkins.device_refresh),
    url(r'^testlog$', sessions.test_log),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
