import datetime

from django.core.serializers.json import DjangoJSONEncoder


class DatetimeJSONEncoder(DjangoJSONEncoder):
    """ DjangoJSONEncoder subclass that knows how to encode datetime right. """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return super().default(o)
