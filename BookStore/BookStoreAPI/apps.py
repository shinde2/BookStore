from django.apps import AppConfig
from django.db.models.signals import post_migrate


perms = {
    "Carrier": [
        "change_order",
    ],
}


def set_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    manager, __ = Group.objects.get_or_create(name="Manager")
    all_perms = Permission.objects.all()
    manager.permissions.set(all_perms)

    for group_name in perms:
        group, __ = Group.objects.get_or_create(name=group_name)
        for perm in perms[group_name]:
            group.permissions.add(Permission.objects.get(codename=perm))
        group.save()


class BookstoreapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BookStoreAPI'

    def ready(self):
        post_migrate.connect(set_groups, sender=self)
