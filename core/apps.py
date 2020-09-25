from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class CoreConfig(AppConfig):
    name = 'core'


# class DefaultAdminConfig(AdminConfig):
#     default_site = 'core.admin.AdminSite'
