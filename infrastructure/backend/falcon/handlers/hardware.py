import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from falcon.models import PowerMetricsRaw, Devices, TestItems, TestResults, CompareResults, MetricsStandart, \
    MajorReleases
from falcon.tools.serializers import DatetimeJSONEncoder


@require_GET
def standart_devices(request):
    test_type = request.GET["type"] if "type" in request.GET else None
    test_item = request.GET["test_item_id"] if "test_item_id" in request.GET else None
    lookups = {"metricsstandart__test_item_id": test_item}
    if test_type:
        lookups["metricsstandart__test_result_id__is_{}_test".format(test_type.lower())] = True
    result = Devices.objects.filter(**lookups).distinct()
    data = [item.wrap() for item in result]
    return JsonResponse(data, safe=False)


@require_GET
def standart_tesitems(request):
    test_type = request.GET["type"] if "type" in request.GET else None
    lookups = {"testresults__is_standart": True,
               "testresults__status": "Passed"}
    if test_type:
        lookups["testresults__is_{}_test".format(test_type.lower())] = True
    result = TestItems.objects.filter(**lookups).distinct()
    data = [item.wrap() for item in result]
    return JsonResponse(data, safe=False)


@require_GET
def standart_releases(request):
    test_type = request.GET["type"] if "type" in request.GET else None
    test_item = request.GET["test_item_id"] if "test_item_id" in request.GET else None
    device = request.GET["device_id"] if "device_id" in request.GET else None
    lookups = {"metricsstandart__test_item_id": test_item}
    if test_type:
        lookups["metricsstandart__test_result_id__is_{}_test".format(test_type.lower())] = True
    if device:
        lookups["metricsstandart__device_id"] = device
    result = MajorReleases.objects.filter(**lookups).distinct()
    data = [item.wrap() for item in result]
    return JsonResponse(data, safe=False)


@require_GET
def hardwaredevices(request):
    test_item_id = request.GET["test_item_id"] if "test_item_id" in request.GET else None
    exclude = request.GET["exclude"] if "exclude" in request.GET else None
    lookups = {"buildsessions__type": "hardware",
               "buildsessions__testresults__status": "Passed"}
    if test_item_id:
        lookups["buildsessions__testresults__test_item_id"] = test_item_id
    if exclude:
        result = Devices.objects.filter(**lookups).exclude(pk=exclude).distinct()
    else:
        result = Devices.objects.filter(**lookups).distinct()
    data = [item.wrap() for item in result]
    return JsonResponse(data, safe=False)


@require_GET
def hardwaretesitems(request):
    device_id = request.GET["device_id"] if "device_id" in request.GET else None
    exclude = request.GET["exclude"] if "exclude" in request.GET else None
    lookups = {"type": "hardware",
               "testresults__status": "Passed",
                }
    if device_id:
        lookups["testresults__session__device__id"] = device_id
    if exclude:
        result = TestItems.objects.filter(**lookups).exclude(pk=exclude).distinct()
    else:
        result = TestItems.objects.filter(**lookups).distinct()
    data = [item.wrap() for item in result]
    return JsonResponse(data, safe=False)


@require_GET
def hardwaretestresults(request):
    device_id = request.GET["device_id"] if "device_id" in request.GET else None
    test_item_id = request.GET["test_item_id"] if "test_item_id" in request.GET else None
    if not (device_id and test_item_id):
        return JsonResponse({"status": "error", "error": "You must specify both device_id and test_result_id"},
                            status=400)
    date_from = request.GET["date_from"] if "date_from" in request.GET else None
    date_to = request.GET["date_to"] if "date_to" in request.GET else None
    is_memory = request.GET["is_memory"] if "is_memory" in request.GET else None

    lookups = {"status": "Passed",
               "test_item_id": test_item_id,
               "session__device__id": device_id,
               "session__status": "Passed",
               "is_standart": False
               }
    if date_from:
        lookups["time_start__gt"] = date_from
    if date_to:
        lookups["time_start__lt"] = date_to
    if is_memory == "true":
        lookups["is_memory_test"] = True
    else:
        lookups["is_power_test"] = True

    result = TestResults.objects.filter(**lookups)
    data = [item.wrap() for item in result]
    return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)


@require_GET
def average_power(request, test_result_id=None):
    if not test_result_id:
        test_result_id = request.GET["test_result_id"] if "test_result_id" in request.GET else None
    if not test_result_id:
        return JsonResponse({"status": "error", "msg": "You should specify test_result_id"}, status=400)
    first = PowerMetricsRaw.objects.filter(test_result_id=test_result_id).order_by("record_timestamp").first()
    last = PowerMetricsRaw.objects.filter(test_result_id=test_result_id).order_by("record_timestamp").last()
    res = 0
    if first and last:
        delta = (last.record_timestamp - first.record_timestamp).seconds
        period = 60 * 60
        res = round(last.charge / delta * period)

    return JsonResponse({"average_charge": res})


@require_http_methods(["GET", "POST"])
def metricsraw(request, test_result_id=None):
    if request.method == "POST":
        cl = request.headers['Content-Length']
        data = request.body.decode()
        data_json = json.loads(json.loads(data))
        pmr = PowerMetricsRaw(current=data_json["current"], voltage=data_json["voltage"], power=data_json["power"],
                              charge=data_json["record"]["current"], energy=data_json["record"]["power"],
                              record_timestamp=datetime.fromtimestamp(int(data_json["timestamp"]) / 1e3),
                              test_result_id=data_json["testid"])
        pmr.save()
        return JsonResponse({})

    if request.method == "GET":
        if not test_result_id:
            return JsonResponse({"status": "error", "error": "You must specify test_result_id"}, status=400)
        info = PowerMetricsRaw.objects.filter(test_result_id=test_result_id).order_by("record_timestamp")
        data = {}
        ave = 0
        if len(info) > 0:
            delta = (info.last().record_timestamp - info[0].record_timestamp).seconds
            period = 60 * 60
            ave = round(info.last().charge / delta * period)

            data = _get_data([item.wrap() for item in info])
            data["average"] = ave

            if "key" in request.GET:
                return JsonResponse(data[request.GET["key"]])
        return JsonResponse(data)


@require_GET
def check_standart(request):
    device_id = request.GET["device_id"] if "device_id" in request.GET else None
    test_item_method = request.GET["test_item_method"] if "test_item_method" in request.GET else None
    metric_type = request.GET["metric_type"] if "metric_type" in request.GET else None # power/memory
    release = request.GET["release_id"] if "release_id" in request.GET else None

    lookups = {
        "test_item__method_name": test_item_method,
        "device_id": device_id,
        "release_id": release,
        "test_result__is_{}_test".format(metric_type): True
    }

    res = MetricsStandart.objects.filter(**lookups).order_by("-id")[:1]
    if len(res) == 0:
        del lookups["release_id"]
        res = MetricsStandart.objects.filter(**lookups).order_by("-id")[:1]
        if len(res) == 0:
            return JsonResponse(False, safe=False)
    return JsonResponse(True, safe=False)


@require_POST
def metrics_standart(request):
    chosen_id = request.POST["chosen"] if "chosen" in request.POST else None
    device_id = request.POST["device_id"] if "device_id" in request.POST else None
    test_item_id = request.POST["test_item_id"] if "test_item_id" in request.POST else None
    release_id = request.POST["release_id"] if "release_id" in request.POST else None
    if not chosen_id:
        return JsonResponse({"status": "error", "error": "You must specify chosen test result id"}, status=400)
    data = {}
    map_first = []
    res = PowerMetricsRaw.objects.filter(test_result_id=chosen_id).order_by("record_timestamp")
    map_first.append([item.wrap() for item in res])
    op_first = _get_ave_full(map_first)
    data_first = _get_data(op_first)

    ave = 0
    if len(op_first) > 0:
        delta = (op_first[-1]["record_timestamp"] - op_first[0]["record_timestamp"]).seconds
        period = 60 * 60
        ave = round(op_first[-1]["charge"] / delta * period)
    extra = {"average": ave, "name": "Chosen test result"}

    data_first.update(extra)
    data.update({"first": data_first})

    map_second = []
    metrics = MetricsStandart.objects.filter(test_item_id=test_item_id, device_id=device_id, release_id=release_id).order_by("-id")[:1]
    test_res = TestResults.objects.filter(metricsstandart__id=metrics[0].id)
    res = PowerMetricsRaw.objects.filter(test_result_id=test_res[0].id).order_by("record_timestamp")
    map_second.append([item.wrap() for item in res])
    op_second = _get_ave_full(map_second)
    data_second = _get_data(op_second)

    ave = 0
    if len(op_second) > 0:
        delta = (op_second[-1]["record_timestamp"] - op_second[0]["record_timestamp"]).seconds
        period = 60 * 60
        ave = round(op_second[-1]["charge"] / delta * period)
    extra = {"average": ave, "name": "Standart"}

    data_second.update(extra)
    data.update({"second": data_second})

    diff = round((data["first"]["average"] - data["second"]["average"]) / data["second"]["average"] * 100)

    result = CompareResults(data=data, type='hardware', first_ids=[chosen_id], second_ids=[test_res[0].id], diff=diff)
    result.save()

    return JsonResponse({"uuid": result.uuid})


@require_POST
def json_power_metrics(request):
    first_ids = json.loads(request.POST["first_ids"]) if "first_ids" in request.POST else None
    second_ids = json.loads(request.POST["second_ids"]) if "second_ids" in request.POST else None
    first_name = request.POST["first_name"] if "first_name" in request.POST else None
    second_name = request.POST["second_name"] if "second_name" in request.POST else None

    data = {}
    map_first = []
    for id in first_ids:
        res = PowerMetricsRaw.objects.filter(test_result_id=id).order_by("record_timestamp")
        map_first.append([item.wrap() for item in res])
    op_first = _get_ave_full(map_first)
    data_first = _get_data(op_first)

    ave = 0
    if len(op_first) > 0:
        delta = (op_first[-1]["record_timestamp"] - op_first[0]["record_timestamp"]).seconds
        period = 60 * 60
        ave = round(op_first[-1]["charge"] / delta * period)
    extra = {"average": ave, "name": first_name}

    data_first.update(extra)
    data.update({"first": data_first})

    if second_ids:
        map_second = []
        for id in second_ids:
            res = PowerMetricsRaw.objects.filter(test_result_id=id).order_by("record_timestamp")
            map_second.append([item.wrap() for item in res])
        op_second = _get_ave_full(map_second)
        data_second = _get_data(op_second)

        ave = 0
        if len(op_second) > 0:
            delta = (op_second[-1]["record_timestamp"] - op_second[0]["record_timestamp"]).seconds
            period = 60 * 60
            ave = round(op_second[-1]["charge"] / delta * period)
        extra = {"average": ave, "name": second_name}

        data_second.update(extra)
        data.update({"second": data_second})

    result = CompareResults(data=data, type='hardware', first_ids=first_ids, second_ids=second_ids)
    result.save()

    return JsonResponse({"uuid": result.uuid})


@require_GET
def get_diff_standart(request):
    chosen_id = request.GET["chosen"] if "chosen" in request.GET else None
    device_id = request.GET["device_id"] if "device_id" in request.GET else None
    test_item_method = request.GET["test_item_method"] if "test_item_method" in request.GET else None
    release_id = request.GET["release_id"] if "release_id" in request.GET else None

    first = PowerMetricsRaw.objects.filter(test_result_id=chosen_id).order_by("record_timestamp").first()
    last = PowerMetricsRaw.objects.filter(test_result_id=chosen_id).order_by("record_timestamp").last()
    res1 = 0
    if first and last:
        delta = (last.record_timestamp - first.record_timestamp).seconds
        period = 60 * 60
        res1 = round(last.charge / delta * period)

    metrics = MetricsStandart.objects.filter(test_item__method_name=test_item_method, device_id=device_id,
                                             release_id=release_id).order_by("-id")[:1]
    if len(metrics) == 0:
        metrics = MetricsStandart.objects.filter(test_item__method_name=test_item_method, device_id=device_id).order_by("-id")[:1]
    test_res = TestResults.objects.filter(metricsstandart__id=metrics[0].id)

    first = PowerMetricsRaw.objects.filter(test_result_id=test_res[0].id).order_by("record_timestamp").first()
    last = PowerMetricsRaw.objects.filter(test_result_id=test_res[0].id).order_by("record_timestamp").last()
    res2 = 0
    if first and last:
        delta = (last.record_timestamp - first.record_timestamp).seconds
        period = 60 * 60
        res2 = round(last.charge / delta * period)

    diff = 100
    if res2 != 0:
        diff = round((res1 - res2) / res2 * 100)

    return JsonResponse(diff, safe=False)

@require_GET
def compare_results(request):
    if not "uuid" in request.GET:
        return JsonResponse({"status": "error", "reason": "you must specify uuid"}, status=400)
    result = CompareResults.objects.get(uuid=request.GET["uuid"])
    return JsonResponse(result.wrap(), encoder=DatetimeJSONEncoder)


def _get_ave_full(res):
    minimal = min([len(x) for x in res if len(x) > 0])
    ave_full = []
    ave1 = res[0][:minimal]
    for i, r in enumerate(ave1):
        ave1[i]["current"] = sum([x[i]["current"] for x in res])
        ave1[i]["voltage"] = sum([x[i]["voltage"] for x in res])
        ave1[i]["power"] = sum([x[i]["power"] for x in res])
        ave1[i]["charge"] = sum([x[i]["charge"] for x in res])
        ave1[i]["energy"] = sum([x[i]["energy"] for x in res])

    l = len(res)
    for i, r in enumerate(ave1):
        ave_full.append(r)
        ave_full[i]["charge"] = r["charge"] / l
        ave_full[i]["current"] = r["current"] / l
        ave_full[i]["voltage"] = r["voltage"] / l
        ave_full[i]["power"] = r["power"] / l
        ave_full[i]["energy"] = r["energy"] / l
    return ave_full


def _get_data(result):
    sec_time_data = []
    current_data = []
    voltage_data = []
    power_data = []
    charge_data = []
    energy_data = []
    first_time = result[0]["record_timestamp"]

    min_time_data = []
    min_current_data = []
    min_voltage_data = []
    min_power_data = []
    min_charge_data = []
    min_energy_data = []

    minute = 1
    cur_sum = 0
    volt_sum = 0
    power_sum = 0
    counter = 0
    min_time_data.append(0)
    min_current_data.append(result[0]["current"])
    min_voltage_data.append(result[0]["voltage"])
    min_power_data.append(result[0]["power"])
    min_energy_data.append(result[0]["energy"])
    min_charge_data.append(result[0]["charge"])

    for i, r in enumerate(result):
        delta = (r["record_timestamp"] - first_time).seconds
        sec_time_data.append(delta)
        current_data.append(r["current"])
        voltage_data.append(r["voltage"])
        power_data.append(r["power"])
        charge_data.append(r["charge"])
        energy_data.append(r["energy"])

        if delta < minute * 60:
            cur_sum = cur_sum + r["current"]
            volt_sum = volt_sum + r["voltage"]
            power_sum = power_sum + r["power"]
            counter = counter + 1
        else:
            if counter > 0:
                min_energy_data.append(r["energy"])
                min_charge_data.append(r["charge"])
                min_time_data.append(minute)
                min_current_data.append(cur_sum / counter)
                min_voltage_data.append(volt_sum / counter)
                min_power_data.append(power_sum / counter)
            minute = minute + 1
            counter = 0
            cur_sum = 0
            volt_sum = 0
            power_sum = 0

    data = {"current": {"sec": list(zip(sec_time_data, current_data)),
                        "min": list(zip(min_time_data, min_current_data))},
            "voltage": {"sec": list(zip(sec_time_data, voltage_data)),
                        "min": list(zip(min_time_data, min_voltage_data))},
            "power": {"sec": list(zip(sec_time_data, power_data)),
                      "min": list(zip(min_time_data, min_power_data))},
            "charge": {"sec": list(zip(sec_time_data, charge_data)),
                       "min": list(zip(min_time_data, min_charge_data))},
            "energy": {"sec": list(zip(sec_time_data, energy_data)),
                       "min": list(zip(min_time_data, min_energy_data))}
            }

    return data
