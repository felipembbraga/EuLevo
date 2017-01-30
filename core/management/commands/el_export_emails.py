from sys import stdout
import six

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django_extensions.management.commands.export_emails import Command as DECommand
from django_extensions.management.utils import signalcommand


class Command(DECommand):

    @signalcommand
    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("extra arguments supplied")
        group = options['group']
        if group and not Group.objects.filter(name=group).count() == 1:
            names = six.u("', '").join(g['name'] for g in Group.objects.values('name')).encode('utf-8')
            if names:
                names = "'" + names + "'."
            raise CommandError("Unknown group '" + group + "'. Valid group names are: " + names)
        if len(args) and args[0] != '-':
            outfile = open(args[0], 'w')
        else:
            outfile = stdout

        User = get_user_model()
        qs = User.objects.all().order_by('email')
        if group:
            qs = qs.filter(groups__name=group).distinct()
        qs = qs.values('email')
        self.emails(qs, outfile)