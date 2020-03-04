import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from falcon.models import Devices


def device(request, id=None, device_id=None):
    if request.method == 'GET':
        if id:
            devices = Devices.objects.get(pk=id)
            return JsonResponse(devices.wrap())
        if device_id:
            try:
                devices = Devices.objects.get(device_id=device_id)
                return JsonResponse(devices.wrap())
            except Devices.DoesNotExist as e:
                return JsonResponse({"status": "error", "error": "Device does not exist"}, status=404)

        if "status" in request.GET:
            devices = Devices.objects.filter(status=request.GET["status"])
        else:
            devices = Devices.objects.all().order_by("status")
        data = [item.wrap() for item in devices]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        if id:
            device = Devices(pk=id, **request.POST.dict())
            device.save(update_fields=[key for key in request.POST if key != 'id'])
        else:
            device = Devices(**request.POST.dict())
            device.save()

    if request.method == 'DELETE':
        device = Devices.objects.get(pk=id)
        device.delete()

    return JsonResponse({})


@require_POST
def refresh(request):
    active_devices = json.loads(request.POST["active_devices"])
    platform = request.POST["platform_name"] if "platform_name" in request.POST else "Android"
    devices = Devices.objects.filter(platform_name=platform)
    for dev in devices:
        dev_info = dev.wrap()
        for ad in active_devices:
            if type(ad) == str:
                condition = dev_info["device_id"] == ad or dev_info["udid"] == ad
            else:
                condition = dev_info["device_id"] == ad["name"] or dev_info["udid"] == ad["name"]

            if condition:
                dev.status = "Active"
                if type(ad) != str:
                    dev.battery_level = int(ad["battery"])
                break
        else:
            dev.status = "Disabled"
            dev.battery_level = -1
        dev.save()

    return JsonResponse({})
