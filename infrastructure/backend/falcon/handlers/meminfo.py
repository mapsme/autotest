import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from falcon.models import MemoryMetricsRaw, CompareResults, TestResults, MetricsStandart


@require_http_methods(["GET", "POST"])
def meminfo(request, test_result_id=None):
    if request.method == "POST":
        if "record_timestamp" in request.POST:
            MemoryMetricsRaw(test_result_id=request.POST["test_result_id"],
                             total_memory_in_bytes=request.POST["total_memory_in_bytes"],
                             record_timestamp=datetime.fromtimestamp(float(request.POST["record_timestamp"]))) \
                .save()
            return JsonResponse({})
        else:
            return JsonResponse({"status": "error", "msg": "no record timestamp in request"}, status=400)

    if request.method == "GET":
        if not test_result_id:
            return JsonResponse({"status": "error", "error": "You must specify test_result_id"}, status=400)
        info = MemoryMetricsRaw.objects.filter(test_result_id=test_result_id).order_by("record_timestamp")
        data = {}
        if len(info) > 0:
            sec_time_data = []
            meminfo_data = []
            first_time = info[0].record_timestamp
            for i, r in enumerate(info):
                delta = (r.record_timestamp - first_time).seconds
                sec_time_data.append(delta)
                meminfo_data.append(round(r.total_memory_in_bytes / 1024))
            data = {"meminfo": list(zip(sec_time_data, meminfo_data))}

            ave = 0
            sum = 0
            if len(info) > 0:
                for r in info:
                    mem = round(r.total_memory_in_bytes / 1024)
                    sum += mem

                ave = round(sum / len(info))
            data["average"] = ave

        return JsonResponse(data, safe=False)


@require_POST
def json_memory_metrics(request):
    first_ids = json.loads(request.POST["first_ids"]) if "first_ids" in request.POST else None
    second_ids = json.loads(request.POST["second_ids"]) if "second_ids" in request.POST else None
    first_name = request.POST["first_name"] if "first_name" in request.POST else None
    second_name = request.POST["second_name"] if "second_name" in request.POST else None

    data = {}
    map_first = []
    for id in first_ids:
        res = MemoryMetricsRaw.objects.filter(test_result_id=id).order_by("record_timestamp")
        map_first.append([item.wrap() for item in res])
    op_first = _get_ave(map_first)
    data_first = _get_data(op_first)

    ave = 0
    sum = 0
    if len(op_first) > 0:
        for r in op_first:
            sum += r["total_memory_in_bytes"]
        ave = round(sum / len(op_first))
    extra = {"average": ave, "name": first_name}

    data_first.update(extra)
    data.update({"first": data_first})

    if second_ids:
        map_second = []
        for id in second_ids:
            res = MemoryMetricsRaw.objects.filter(test_result_id=id).order_by("record_timestamp")
            map_second.append([item.wrap() for item in res])
        op_second = _get_ave(map_second)
        data_second = _get_data(op_second)

        ave = 0
        sum = 0
        if len(op_second) > 0:
            for r in op_second:
                sum += r["total_memory_in_bytes"]
            ave = round(sum / len(op_second))
        extra = {"average": ave, "name": second_name}

        data_second.update(extra)
        data.update({"second": data_second})

    result = CompareResults(data=data, type='memory', first_ids=first_ids, second_ids=second_ids)
    result.save()

    return JsonResponse({"uuid": result.uuid})


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
    res = MemoryMetricsRaw.objects.filter(test_result_id=chosen_id).order_by("record_timestamp")
    map_first.append([item.wrap() for item in res])
    op_first = _get_ave(map_first)
    data_first = _get_data(op_first)

    ave = 0
    sum = 0
    if len(op_first) > 0:
        for r in op_first:
            sum += r["total_memory_in_bytes"]
        ave = round(sum / len(op_first))
    extra = {"average": ave, "name": "Chosen test result"}

    data_first.update(extra)
    data.update({"first": data_first})

    map_second = []
    metrics = MetricsStandart.objects.filter(test_item_id=test_item_id, device_id=device_id, release_id=release_id).order_by("-id")[:1]
    test_res = TestResults.objects.filter(metricsstandart__id=metrics[0].id)
    res = MemoryMetricsRaw.objects.filter(test_result_id=test_res[0].id).order_by("record_timestamp")

    map_second.append([item.wrap() for item in res])
    op_second = _get_ave(map_second)
    data_second = _get_data(op_second)

    ave = 0
    sum = 0
    if len(op_second) > 0:
        for r in op_second:
            sum += r["total_memory_in_bytes"]
        ave = round(sum / len(op_second))
    extra = {"average": ave, "name": "Standart"}

    data_second.update(extra)
    data.update({"second": data_second})
    diff = round((data["first"]["average"] - data["second"]["average"]) / data["second"]["average"] * 100)

    result = CompareResults(data=data, type='memory',  first_ids=[chosen_id], second_ids=[test_res[0].id], diff=diff)
    result.save()

    return JsonResponse({"uuid": result.uuid})


@require_GET
def get_diff_standart(request):
    chosen_id = request.GET["chosen"] if "chosen" in request.GET else None
    device_id = request.GET["device_id"] if "device_id" in request.GET else None
    test_item_method = request.GET["test_item_method"] if "test_item_method" in request.GET else None
    result = MemoryMetricsRaw.objects.filter(test_result_id=chosen_id).order_by("record_timestamp")
    ave1 = 0
    sum = 0
    if len(result) > 0:
        for r in result:
            mem = round(r.total_memory_in_bytes / 1024)
            sum += mem

        ave1 = round(sum / len(result))

    metrics = MetricsStandart.objects.filter(test_item__method_name=test_item_method, device_id=device_id).order_by("-id")[:1]
    test_res = TestResults.objects.filter(metricsstandart__id=metrics[0].id)

    result = MemoryMetricsRaw.objects.filter(test_result_id=test_res[0].id).order_by("record_timestamp")

    ave2 = 0
    sum = 0
    if len(result) > 0:
        for r in result:
            mem = round(r.total_memory_in_bytes / 1024)
            sum += mem

        ave2 = round(sum / len(result))

    diff = round((ave1 - ave2) / ave2 * 100)

    return JsonResponse(diff, safe=False)


def _get_ave(res):
    minimal = min([len(x) for x in res if len(x) > 0])
    ave_full = []
    ave1 = res[0][:minimal]
    for i, r in enumerate(ave1):
        ave1[i]["total_memory_in_bytes"] = sum([x[i]["total_memory_in_bytes"] for x in res])
    l = len(res)
    for i, r in enumerate(ave1):
        ave_full.append(r)
        ave_full[i]["total_memory_in_bytes"] = round(r["total_memory_in_bytes"] / l / 1024)
    return ave_full


def _get_data(result):
    sec_time_data = []
    memory_data = []
    first_time = result[0]["record_timestamp"]

    min_time_data = []
    min_memory_data = []

    minute = 1
    sum = 0
    counter = 0
    min_time_data.append(0)
    min_memory_data.append(result[0]["total_memory_in_bytes"])

    for i, r in enumerate(result):
        delta = (r["record_timestamp"] - first_time).seconds
        sec_time_data.append(delta)
        memory_data.append(r["total_memory_in_bytes"])

        if delta < minute * 60:
            sum = sum + r["total_memory_in_bytes"]
            counter = counter + 1
        else:
            if counter > 0:
                min_time_data.append(minute)
                min_memory_data.append(sum / counter)
            minute = minute + 1
            counter = 0
            sum = 0

    data = {"memory": {"sec": list(zip(sec_time_data, memory_data)),
                       "min": list(zip(min_time_data, min_memory_data))}
            }

    return data


@require_GET
def average_memory(request, test_result_id):
    result = MemoryMetricsRaw.objects.filter(test_result_id=test_result_id).order_by("record_timestamp")
    ave = 0
    sum = 0
    if len(result) > 0:
        for r in result:
            mem = round(r.total_memory_in_bytes / 1024)
            sum += mem

        ave = round(sum / len(result))
    return JsonResponse({"average_memory": ave})
