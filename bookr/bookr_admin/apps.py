from django.apps import AppConfig

# Overriding the default "admin.site" property to avoid manually
# registering models here.
from django.contrib.admin.apps import AdminConfig


# AdminConfig defines the app that should be used as the default admin
# site, and overrides django's admin site's default behaviour.
class BookrAdminConfig(AdminConfig):
    default_site = "bookr_admin.admin.BookrAdmin"
