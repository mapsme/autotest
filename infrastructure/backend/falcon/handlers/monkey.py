from datetime import datetime, timedelta, timezone

from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET

from falcon.models import MonkeyCrashes, UniqueCrash, BuildSessions


@require_http_methods(["GET", "POST"])
def monkey_crash(request, id=None):
    if request.method == "GET":
        session_id = request.GET["session_id"] if "session_id" in request.GET else None
        count = bool(request.GET["count"]) if "count" in request.GET else None
        if id:
            result = MonkeyCrashes.objects.get(pk=id)
            return JsonResponse(result.wrap())
        if session_id:
            if count:
                result = MonkeyCrashes.objects.filter(session_id=session_id).count()
                return JsonResponse({"count": result})
            else:
                result = MonkeyCrashes.objects.filter(session_id=session_id).order_by("id")
                data = [item.wrap() for item in result]
                return JsonResponse(data, safe=False)

    if request.method == "POST":
        pars = request.POST.dict()
        err_text = request.POST["error_text"] if "error_text" in request.POST else None
        if err_text:
            del pars["error_text"]
        else:
            pass
        unique_crashes = UniqueCrash.objects.filter(crash_text=err_text)
        if len(unique_crashes) == 0:
            session = BuildSessions.objects.get(pk=pars["session_id"])
            uc = UniqueCrash(crash_text=err_text, date=session.time_start,
                             device=session.device, release=session.version.release_full)
            uc.save()
        else:
            uc = unique_crashes[0]
        pars["unique_crash"] = uc
        MonkeyCrashes(**pars).save()

    return JsonResponse({})

@require_GET
def unique_crash(request, id=None):
    if not id:
        limit = int(request.GET["count"])
        page = int(request.GET["start"])

        from_s = page*limit
        to_s =  page*limit + limit - 1
        res = UniqueCrash.objects.all().order_by("-date")[from_s:to_s]
        data = [item.wrap() for item in res]
        return JsonResponse(data, safe=False)
    res = UniqueCrash.objects.get(pk=id)
    return JsonResponse(res.wrap(), safe=False)


@require_GET
def top_unique(request):
    period = request.GET["period"] if "period" in request.GET else None
    count = int(request.GET["count"]) if "count" in request.GET else None
    if period == "month":
        crashes = MonkeyCrashes.objects.filter(session__time_start__gte=datetime.now() - timedelta(days=31))\
            .values('unique_crash').annotate(total=Count('unique_crash')).order_by('-total')[:count]
        data = {"crashes": [x["unique_crash"] for x in crashes]}
        return JsonResponse(data, safe=False)

@require_GET
def search_unique(request):
    text = request.GET["text"] if "text" in request.GET else None
    crashes = UniqueCrash.objects.all()
    res = []
    for cr in crashes:
        searched = text.replace("//", "").replace("\n","").replace(" ","").replace("\t","")
        searching = cr.crash_text.replace("//", "").replace("\n","").replace(" ","").replace("\t","")
        if searched in searching:
            res.append(cr)
    return JsonResponse([x.wrap() for x in res], safe=False)


@require_GET
def unique_crash_stats(request, id):
    if id:
        period = request.GET["period"] if "period" in request.GET else None
        crash = UniqueCrash.objects.get(pk=id)
        if period != "release":
            if period == "all":
                crashes = [x for x in MonkeyCrashes.objects.filter(unique_crash=crash).order_by("id")]
            if period == "month":
                crashes = [x for x in MonkeyCrashes.objects.filter(unique_crash=crash,
                                                                   session__time_start__gte=datetime.now() - timedelta(
                                                                       days=31)).order_by("id")]
        else:
            release = request.GET["release"] if "release" in request.GET else None
            crashes1 = [x for x in MonkeyCrashes.objects.filter(unique_crash=crash, session__version__release_full__startswith=release).order_by("id")]
            crashes2 = [x for x in MonkeyCrashes.objects.filter(unique_crash=crash, session__release__startswith=release,
                                                                session__version__isnull=True).order_by("id")]
            crashes = crashes1 + crashes2

        data = {"len": len(crashes)}
        timeline = {}
        releases = set()
        devices = set()
        day_len = 0
        if len(crashes) > 0:
            cur_day = crashes[0].session.time_start.date()
            data["start"] = crashes[0].session.time_start.date()
            for cr in crashes:
                rel = cr.session.version.release_full if cr.session.version else cr.session.release
                rel = rel.split("-")[0]
                dots = rel.split(".")
                if len(dots) > 3:
                    major_version = rel.rsplit(".", 1)[0]
                else:
                    major_version = rel
                releases.add(major_version)
                devices.add(cr.session.device.name)
                if cr.session.time_start.date() == cur_day:
                    day_len = day_len + 1
                else:
                    timeline[cur_day.strftime("%d.%m.%Y")] = day_len
                    for i in range((cr.session.time_start.date() - cur_day).days):
                        timeline[(cur_day + timedelta(days=i+1)).strftime("%d.%m.%Y")] = 0
                    day_len = 1
                    cur_day = cr.session.time_start.date()
            timeline[cur_day.strftime("%d.%m.%Y")] = day_len
        #for i in range((datetime.now().date() - cur_day).days):
        #    timeline[(cur_day + timedelta(days=i + 1)).strftime("%d.%m.%Y")] = 0
        data["timeline"] = [timeline[x] for x in timeline]
        data["releases"] = ", ".join(releases)
        data["devices"] = ", ".join(devices)
        return JsonResponse(data, safe=False)


@require_GET
def unique_releases(request, id):
    if id:
        crash = UniqueCrash.objects.get(pk=id)
        crashes = [x for x in MonkeyCrashes.objects.filter(unique_crash=crash)]
        releases = set()
        for cr in crashes:
            rel = cr.session.version.release_full if cr.session.version else cr.session.release
            rel = rel.split("-")[0]
            dots = rel.split(".")
            if len(dots) > 3:
                major_version = rel.rsplit(".", 1)[0]
            else:
                major_version = rel
            releases.add(major_version)
        return JsonResponse(list(releases), safe=False)

@require_GET
def session_stats(request):
    session_id = request.GET["session_id"] if "session_id" in request.GET else None
    session = BuildSessions.objects.get(pk=session_id)
    all_crashes = MonkeyCrashes.objects.filter(session_id=session_id)
    all_unique = set([x.unique_crash for x in all_crashes])
    new_unique = [x for x in all_unique if x.date==session.time_start.replace(tzinfo=timezone.utc)]
    return JsonResponse({"all": len(all_crashes), "unique": len(all_unique), "new": len(new_unique)})
