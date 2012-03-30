from django.db import models
import math
import datetime


class FtpServer(models.Model):
    address = models.CharField("server's DNS name or IP address", primary_key=True, max_length=200)
    name = models.CharField("optionnal readable name", max_length=30, blank=True)
    online = models.BooleanField()
    size = models.IntegerField()
    last_online = models.DateTimeField()

    # TODO : Move somewhere else
    _suffixes = (
        'o',
        'Kio',
        'Mio',
        'Gio',
        'Tio',
        'Pio',
        'Eio',
        'Zio',
        'Yio',
    )

    # TODO : Locale-dependent
    _times = (
        (1, 'secondes'),
        (60, 'minutes'),
        (60, 'hours'),
        (24, 'days'),
        (7, 'weeks'),
    )

    def display_name(self):
        if self.name != "":
            return self.name
        else:
            return self.address

    def __unicode__(self):
        return self.address

    def display_size(self):
        if self.size == 0:
            return '0'
        exponent = int(math.log(self.size)/math.log(1024))
        ssize = self.size/math.pow(1024, exponent)
        suffix = FtpServer._suffixes[int(exponent)]
        return "%.2f %s" % (ssize, suffix)

    def display_lastonline(self):
        t = (datetime.datetime.now() - self.last_online).total_seconds()
        last_label = ''
        for length, label in FtpServer._times:
            if t > length:
                t /= length
                last_label = label
            else:
                break
        return "%d %s" % (int(t), last_label)


class File(models.Model):
    server = models.ForeignKey(FtpServer, related_name='files')
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=300)
    is_directory = models.BooleanField()

    def __unicode__(self):
        return self.server.__unicode__() + u":" + self.path + u"/" + self.name

    def fullpath(self):
        return self.path + u"/" + self.name
