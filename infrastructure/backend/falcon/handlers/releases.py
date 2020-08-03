"""from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from falcon.models import Releases, ReleaseFeatures
from falcon.tools.serializers import DatetimeJSONEncoder


@require_http_methods(["GET", "POST", "DELETE"])
def release(request, id=None):
    if request.method == 'GET':
        is_archive = request.GET["is_archive"] if "is_archive" in request.GET else None
        if id:
            release = Releases.objects.get(pk=id)
            return JsonResponse(release.wrap(), encoder=DatetimeJSONEncoder)
        if is_archive == 'true':
            releases = Releases.objects.filter(is_archive=True)
        elif is_archive == 'false':
            releases = Releases.objects.filter(is_archive=False)
        else:
            releases = Releases.objects.all()
        data = [item.wrap() for item in releases]
        return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

    if request.method == 'POST':
        if id:
            values = request.POST.dict()
            values["is_archive"] = values["is_archive"] == 'true'
            release = Releases(pk=id, **values)
            release.save(update_fields=[key for key in request.POST if key != 'id'])
        else:
            release = Releases(create_time=datetime.now(), is_archive=False, **request.POST.dict())
            release.save()
        return JsonResponse({})

    if request.method == 'DELETE':
        release = Releases.objects.get(pk=id)
        release.delete()
        return JsonResponse({})


@require_http_methods(["GET", "POST"])
def feature(request, id=None):
    if request.method == 'GET':
        if id:
            release = ReleaseFeatures.objects.get(pk=id)
            return JsonResponse(release.wrap(), encoder=DatetimeJSONEncoder)
        if "release_id" in request.GET:
            features = ReleaseFeatures.objects.filter(release_id=int(request.GET["release_id"]))
            data = [item.wrap() for item in features]
            return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)
        releases = ReleaseFeatures.objects.all()
        data = [item.wrap() for item in releases]
        return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

    if request.method == 'POST':
        if id:
            release = ReleaseFeatures(pk=id, **request.POST.dict())
            release.save(update_fields=[key for key in request.POST if key != 'id'])
        else:
            release = ReleaseFeatures(**request.POST.dict())
            release.save()
        return JsonResponse({})"""
