from django.apps import AppConfig


def create_manager_group(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from blog.models import BlogPost
    from products.models import GuineaPig

    manager_group, created = Group.objects.get_or_create(name="Manager")

    if created:
        blog_post_ct = ContentType.objects.get_for_model(BlogPost)
        guinea_pig_ct = ContentType.objects.get_for_model(GuineaPig)

        permissions = Permission.objects.filter(
            content_type__in=[blog_post_ct, guinea_pig_ct]
        )
        manager_group.permissions.set(permissions)


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(create_manager_group, sender=self)
