import csv
import json
from os.path import join, dirname, abspath

from django.http import JsonResponse, HttpResponse
from django.utils.encoding import smart_str
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from falcon.models import TestItems, BuildSessions, TestResults, TestMarkers, MetricsStandart, MajorReleases, Versions
from falcon.tools.serializers import DatetimeJSONEncoder


@require_http_methods(["GET", "POST", "DELETE"])
def testitem(request, id=None):
    if request.method == 'GET':
        if id:
            test_item = TestItems.objects.get(pk=id)
            return JsonResponse(test_item.wrap())
        if 'type' in request.GET:
            params = {"type": request.GET["type"]}
            if 'marker' in request.GET:
                params["marks__contains"] = [request.GET["marker"]]
            test_items = TestItems.objects.filter(**params)
        else:
            test_items = TestItems.objects.all()
        data = [item.wrap() for item in test_items]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        if id:
            test_item = TestItems(pk=id, **request.POST.dict())
            test_item.save(update_fields=[key for key in request.POST if key != 'id'])
        else:
            test_item = TestItems(**request.POST.dict())
            test_item.save()

    if request.method == 'DELETE':
        test_item = TestItems.objects.get(pk=id)
        test_item.delete()

    return JsonResponse({})


@require_POST
def test_item_refresh(request):
        test_method = request.POST["method_name"] if "method_name" in request.POST else None
        name = request.POST["name"] if "name" in request.POST else None
        markers = json.loads(request.POST["marks"]) if "marks" in request.POST else None
        if not (test_method and name):
            return JsonResponse({"status": "error"}, status=400)

        result = TestItems.objects.filter(method_name=test_method)
        if len(result) == 0:
            result = TestItems.objects.filter(name=name)
        if len(result) == 0:
            values = request.POST.dict()
            if "marks" in values:
                del values["marks"]
            values.update({"marks": markers})
            test_item = TestItems(**values)
            test_item.save()
        else:
            values = request.POST.dict()
            if "marks" in values:
                del values["marks"]
            values.update({"marks": markers})
            test_item = TestItems(pk=result[0].id, **values)
            test_item.save(update_fields=[key for key in values if key != 'id'])

        return JsonResponse({})


@require_http_methods(["GET", "POST"])
def markers(request):
    if request.method == 'GET':
        type = request.GET["type"] if "type" in request.GET else None
        data = [item.marker for item in TestMarkers.objects.all()]
        if type:
            for i, mark in enumerate(data):
                if TestItems.objects.filter(type=type, marks__contains=[mark]).count() == 0:
                    del data[i]
        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        markers = json.loads(request.POST["markers"])
        for mark in markers:
            ms = TestMarkers.objects.filter(marker=mark)
            if len(ms) == 0:
                TestMarkers(marker=mark).save()


@require_http_methods(["GET", "POST", "DELETE"])
def session(request, id=None, type=None):
    if request.method == 'GET':
        limit = int(request.GET["count"]) if "count" in request.GET else 100
        page = int(request.GET["start"]) if "start" in request.GET else 0
        from_s = page * limit
        to_s = page * limit + limit - 1
        if id:
            try:
                session = BuildSessions.objects.get(pk=id)
                return JsonResponse(session.wrap(), encoder=DatetimeJSONEncoder)
            except BuildSessions.DoesNotExist as e:
                return JsonResponse({"status": "error", "error": "Session does not exist"}, status=404)
        if type:
            sessions = BuildSessions.objects.filter(type=type).order_by('-id')[from_s:to_s]
            data = [item.wrap() for item in sessions]
            return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

        if "jenkins_job" in request.GET:
            session = BuildSessions.objects.get(jenkins_job__contains=request.GET["jenkins_job"])
            return JsonResponse(session.pk, safe=False)

        sessions = BuildSessions.objects.all().order_by('-id')[from_s:to_s]
        data = [item.wrap() for item in sessions]
        return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

    if request.method == 'POST':
        if id:
            version = request.POST["version"] if "version" in request.POST else None
            params = request.POST.dict()
            if version:
                ver_id = get_version(version)
                params["version"] = ver_id
            session = BuildSessions(pk=id, **params)
            session.save(update_fields=[key for key in request.POST if key != 'id'])
            data = {}
            if version:
                data["release_id"] = ver_id.major_release.pk
            return JsonResponse(data=data, safe=False)
        else:
            session = BuildSessions(**request.POST.dict())
            session.save()
            return JsonResponse(session.pk, safe=False)

    if request.method == 'DELETE':
        session = BuildSessions.objects.get(pk=id)
        session.delete()
        return JsonResponse(data={})


def get_version(version):
    major_version = version.split("-")[0]
    dots = major_version.split(".")
    if len(dots) > 3:
        major_version = major_version.rsplit(".", 2)[0]
    else:
        major_version = major_version.rsplit(".", 1)[0]
    res = MajorReleases.objects.filter(release=major_version)
    if len(res) == 0:
        release = MajorReleases(release=major_version)
        release.save()
    else:
        release = res[0]
    result = Versions.objects.filter(release_full=version)
    if len(result) == 0:
        version = Versions(release_full=version, major_release=release)
        version.save()
        return version
    return result[0]


@require_http_methods(["GET", "POST", "DELETE"])
def testresult(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                test_result = TestResults.objects.get(pk=id)
                return JsonResponse(test_result.wrap(), encoder=DatetimeJSONEncoder)
            except TestResults.DoesNotExist as e:
                return JsonResponse({"status": "error", "error": "Test result does not exist"}, status=404)
        if "session_id" in request.GET:
            test_results = TestResults.objects.filter(session_id=int(request.GET["session_id"]))
            data = [item.wrap() for item in test_results]
            return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

        test_results = TestResults.objects.all()
        data = [item.wrap() for item in test_results]
        return JsonResponse(data, safe=False, encoder=DatetimeJSONEncoder)

    if request.method == 'POST':
        if id:
            test_result = TestResults(pk=id, **request.POST.dict())
            test_result.save(update_fields=[key for key in request.POST if key != 'id'])
        else:
            values = {key: request.POST[key] for key in request.POST if key != 'test_item_method'}
            if "test_item_method" in request.POST:
                testitem = TestItems.objects.get(method_name=request.POST["test_item_method"])
                values["test_item_id"] = testitem.pk
            test_result = TestResults(**values)
            test_result.save()
            if "is_standart" in request.POST:
                if request.POST["is_standart"] == "True":
                    session = BuildSessions.objects.get(pk=test_result.session.pk)
                    device_id = session.device.pk
                    release = session.version.major_release.pk if session.version else None
                    lookups = {
                        "test_result_id": test_result.pk,
                        "test_item_id": test_result.test_item.id,
                        "device_id": device_id
                    }
                    if release:
                        lookups["release_id"] = release

                    metric = MetricsStandart(**lookups)
                    metric.save()
        return JsonResponse(test_result.pk, safe=False)

    if request.method == 'DELETE':
        test_result = TestResults.objects.get(pk=id)
        test_result.delete()


@require_GET
def csv_download(request, id=None):
    session = BuildSessions.objects.get(pk=id)
    test_results = TestResults.objects.filter(session_id=id)

    path_to_file = dirname(dirname(abspath(__file__)))
    filename = "{}_{}.csv".format(session.build_number, session.device.name.replace(" ", "_"))

    with open(join(path_to_file, filename), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for res in test_results:
            writer.writerow([res.test_item.name, res.status])

    with open(join(path_to_file, filename)) as myfile:
        response = HttpResponse(myfile, content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=%s' % smart_str(filename)
        response['X-Sendfile'] = smart_str(join(path_to_file, filename))
        return response
