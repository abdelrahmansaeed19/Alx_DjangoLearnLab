from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Sets up user groups and assigns permissions'

    def handle(self, *args, **options):
        Book = apps.get_model('bookshelf', 'Book')
        permissions = Permission.objects.filter(content_type__app_label='bookshelf', content_type__model='book')

        group_permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, perm_codenames in group_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()
            for codename in perm_codenames:
                perm = permissions.get(codename=codename)
                group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully.'))
