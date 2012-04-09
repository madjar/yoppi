from django.core.management.base import LabelCommand, CommandError
from yoppi.indexer.app import Indexer
from yoppi.ftp.models import FtpServer

from django.conf import settings as django_settings


try:
    settings = django_settings.INDEXER_SETTINGS
except KeyError:
    settings = {}


class Command(LabelCommand):
    args = '<server_address> [server_address [...]]'
    help = '(re-)index the specified FTP server'
    label = 'address'

    def __init__(self):
        super(LabelCommand, self).__init__()
        self.indexer = Indexer(**settings)

    def handle_label(self, label, **options):
        self.stdout.write('Indexing "%s"...\n' % label)
        try:
            self.indexer.index(label)
        except ValueError as e:
            raise CommandError("%s: %s" % (e.__class__.__name__, e))
