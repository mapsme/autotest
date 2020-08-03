from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from falcon.models import Bookings
from falcon.tools.serializers import DatetimeJSONEncoder


@require_http_methods(["GET", "POST"])
def booking(request, id=None):
    if request.method == 'GET':
        if id:
            res = Bookings.objects.get(pk=id)
            return JsonResponse(res.wrap())
        if "test_result_id" in request.GET:
            results = Bookings.objects.filter(test_result_id=request.GET["test_result_id"])
        else:
            results = Bookings.objects.all()
        data = [item.wrap() for item in results]
        return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

    if request.method == 'POST':
        if id:
            res = Bookings(pk=id, **request.POST.dict())
            res.save(update_fields=[key for key in request.POST if key != 'id'])
            return JsonResponse("")
        else:
            res = Bookings(**request.POST.dict())
            res.save()
            return JsonResponse(res.pk, safe=False)
