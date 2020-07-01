# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid as uuid
from datetime import timezone

import pytz
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models


class Bookings(models.Model):
    id = models.AutoField(primary_key=True)
    test_result = models.ForeignKey('TestResults', models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    hotel_id = models.IntegerField(blank=True, null=True)
    aid = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)
    booking_time = models.DateTimeField(blank=True, null=True)
    reservation_id = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(null=True)

    class Meta:
        db_table = 'bookings'

    def wrap(self):
        return {
            "id": self.pk, "name": self.name, "status": self.status, "hotel_id": self.hotel_id,
            "aid": self.aid, "url": self.url, "booking_time": self.booking_time,
            "reservation_id": self.reservation_id, "price": self.price,
        }


class BuildSessions(models.Model):
    id = models.AutoField(primary_key=True)
    build_number = models.IntegerField(blank=True, null=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    device = models.ForeignKey('Devices', models.DO_NOTHING, blank=True, null=True)
    caused_by = models.CharField(max_length=100, blank=True, null=True)
    upstream_job = models.CharField(max_length=100, blank=True, null=True)
    upstream_build_number = models.CharField(max_length=10, blank=True, null=True)
    upstream_url = models.CharField(max_length=250, blank=True, null=True)
    jenkins_job = models.CharField(max_length=250, blank=True, null=True)
    release = models.CharField(max_length=20, blank=True, null=True)
    release_type = models.CharField(max_length=20, blank=True, null=True)
    test_count = models.IntegerField(blank=True, null=True)
    version = models.ForeignKey('Versions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'build_sessions'

    def wrap(self):
        tests = self.test_count
        passed_tests = None
        failed_tests = None
        pie = None
        if tests:
            passed_tests = len(TestResults.objects.filter(session_id=self.id, status="Passed"))
            failed_tests = len(TestResults.objects.filter(session_id=self.id, status="Failed"))

        if tests is not None and passed_tests is not None and failed_tests is not None:
            if self.status:
                pie = "Passed {}/{}".format(passed_tests, tests)
            else:
                pie = "{}%".format(round((passed_tests+failed_tests)/tests*100))

        result = {
            'id': self.pk, 'build_number': self.build_number, 'time_start': self.time_start, 'time_end': self.time_end,
            'type': self.type, 'caused_by': self.caused_by, 'upstream_job': self.upstream_job,
            'upstream_build_number': self.upstream_build_number, 'upstream_url': self.upstream_url,
            'jenkins_job': self.jenkins_job, "status": self.status if self.status else "In progress",
            'release': self.release, 'release_type': self.release_type, "device_name": self.device.name,
            "device_id": self.device.id, "device_status": self.device.status, "test_count": self.test_count, "test_pie": pie,
            "version": self.version.wrap() if self.version else None
        }

        if self.type == "monkey":
            count = MonkeyCrashes.objects.filter(session_id=self).count()
            result["count"] = count

        return result


class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=50)
    udid = models.CharField(max_length=100, blank=True, null=True)
    platform_name = models.CharField(max_length=20, blank=True, null=True)
    platform_version = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    battery_level = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'devices'

    def wrap(self):
        return {
            'id': self.pk, 'name': self.name,
            'status': self.status, 'battery_level': self.battery_level,
            'platform_name': self.platform_name, 'platform_version': self.platform_version,
            'device_id': self.device_id, 'udid': self.udid
        }


class MemoryMetricsRaw(models.Model):
    id = models.AutoField(primary_key=True)
    record_timestamp = models.DateTimeField()
    total_memory_in_bytes = models.IntegerField()
    test_result = models.ForeignKey('TestResults', models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'memory_metrics_raw'

    def wrap(self):
        return {
            "id": self.pk, "record_timestamp": self.record_timestamp,
            "total_memory_in_bytes": self.total_memory_in_bytes
        }


class MetricsStandart(models.Model):
    id = models.AutoField(primary_key=True)
    test_result = models.ForeignKey("TestResults", models.CASCADE, blank=True, null=True)
    device = models.ForeignKey(Devices, models.DO_NOTHING, blank=True, null=True)
    test_item = models.ForeignKey('TestItems', models.DO_NOTHING, blank=True, null=True)
    release = models.ForeignKey("MajorReleases", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'metrics_standart'


class UniqueCrash(models.Model):
    id = models.AutoField(primary_key=True)
    crash_text = models.CharField(max_length=100000, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    device = models.ForeignKey(Devices, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    release = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'unique_monkey_crashes'

    def wrap(self):
        crashes_count = MonkeyCrashes.objects.filter(unique_crash=self).count()
        return {
            "id": self.pk, "device_name": self.device.name, "release": self.release, "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "crash_text": self.crash_text, "count": crashes_count
        }


class MonkeyCrashes(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(BuildSessions, models.CASCADE, blank=True, null=True)
    crash_number = models.IntegerField(blank=True, null=True)
    full_crash_text = models.CharField(max_length=3000, blank=True, null=True)
    unique_crash = models.ForeignKey(UniqueCrash, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'monkey_crashes'

    def wrap(self):
        is_new = self.session.time_start.replace(tzinfo=timezone.utc) == self.unique_crash.date
        return {
            "id": self.pk, "crash_number": self.crash_number, "crash_text": self.full_crash_text, "unique_crash": self.unique_crash.pk,
            "is_new": is_new# session_id?
        }


class PowerMetricsRaw(models.Model):
    id = models.AutoField(primary_key=True)
    current = models.FloatField()
    voltage = models.FloatField()
    power = models.FloatField()
    charge = models.FloatField()
    energy = models.FloatField()
    record_timestamp = models.DateTimeField()
    test_result = models.ForeignKey('TestResults', models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'power_metrics_raw'

    def wrap(self):
        return {
            "id": self.pk, "current": self.current, "voltage": self.voltage, "power": self.power, "charge": self.charge,
            "energy": self.energy, "record_timestamp": self.record_timestamp
        }


class MajorReleases(models.Model):
    id = models.AutoField(primary_key=True)
    release = models.CharField(max_length=20)

    class Meta:
        db_table = 'major_releases'

    def wrap(self):
        return {"id": self.pk, "release": self.release}


class Versions(models.Model):
    id = models.AutoField(primary_key=True)
    release_full = models.CharField(max_length=20)
    major_release = models.ForeignKey('MajorReleases', models.CASCADE, null=True)

    class Meta:
        db_table = 'versions'

    def wrap(self):
        return {"id": self.pk, "version": self.release_full, "release": self.major_release.release}

"""class ReleaseFeatures(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    requirements_status = models.CharField(max_length=50, blank=True, null=True)
    dev_status = models.CharField(max_length=50, blank=True, null=True)
    testing_status = models.CharField(max_length=50, blank=True, null=True)
    release = models.ForeignKey('Releases', models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'release_features'

    def wrap(self):
        return {
            "id": self.pk, "name": self.name, "requirements_status": self.requirements_status,
            "dev_status": self.dev_status, "testing_status": self.testing_status
        }


class Releases(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(null=True)
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    is_archive = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'releases'

    def wrap(self):
        return {
            "id": self.pk, "name": self.name, "status": self.status, "create_time": self.create_time,
            "time_start": self.time_start, "time_end": self.time_end, "is_archive": self.is_archive
        } """


class TestItems(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    method_name = models.CharField(max_length=250, blank=True, null=True)
    comment = models.CharField(max_length=1500, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    marks = ArrayField(models.CharField(max_length=250), blank=True, null=True)

    class Meta:
        db_table = 'test_items'

    def wrap(self):
        return {
            'id': self.pk, 'name': self.name,
            'method_name': self.method_name, 'comment': self.comment,
            'type': self.type
        }


class TestResults(models.Model):
    id = models.AutoField(primary_key=True)
    test_item = models.ForeignKey(TestItems, models.DO_NOTHING, blank=True, null=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField(blank=True, null=True)
    session = models.ForeignKey(BuildSessions, models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    is_memory_test = models.BooleanField(blank=True, null=True)
    is_power_test = models.BooleanField(blank=True, null=True)
    is_standart = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        db_table = 'test_results'

    def wrap(self):
        logs = TestResultLog.objects.filter(test_result__id=self.pk).order_by("timestamp")
        sorted_logs = []
        for i, log in enumerate(logs):
            if len(sorted_logs) == 0:
                sorted_logs.append([log.wrap()])
            else:
                if log.log == logs[i-1].log:
                    sorted_logs[-1].append(log.wrap())
                else:
                    sorted_logs.append([log.wrap()])

        data = {
            'id': self.pk, 'test_name': self.test_item.name,
            'session_id': self.session.pk, 'time_start': self.time_start, 'time_end': self.time_end,
            'type': self.test_item.type, "test_item_id": self.test_item.pk,
            "status": self.status if self.status else "In progress",
            'is_memory_test': self.is_memory_test, 'is_power_test': self.is_power_test,
            "logs": sorted_logs
        }
        if self.time_start and self.time_end:
            data["time"] = round((self.time_end - self.time_start).seconds / 60)
        return data


class TestMarkers(models.Model):
    id = models.AutoField(primary_key=True)
    marker = models.CharField(max_length=250)
    name = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'pytest_markers'


class CompareResults(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    data = JSONField()
    type = models.CharField(max_length=20)
    first_ids = ArrayField(models.IntegerField(), null=True)
    second_ids = ArrayField(models.IntegerField(), null=True)
    diff = models.IntegerField(null=True)

    class Meta:
        db_table = 'compare_results'

    def wrap(self):
        return {
            "id": self.pk, "uuid": self.uuid, "data": self.data, "type": self.type, "diff": self.diff
        }


class TestResultLog(models.Model):
    id = models.AutoField(primary_key=True)
    test_result = models.ForeignKey(TestResults, models.CASCADE, blank=True, null=True)
    log = models.CharField(max_length=5000)
    file = models.ImageField(blank=True, upload_to="screencaps")
    timestamp = models.DateTimeField()
    is_fail = models.BooleanField(default=False)
    before = models.BooleanField(default=True)

    def wrap(self):
        return {
            "id": self.pk, "log": self.log, "timestamp": self.timestamp, "file": self.file.url, "is_fail": self.is_fail, "before": self.before
        }