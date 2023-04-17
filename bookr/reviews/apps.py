from django.apps import AppConfig

# To enable you use a custom admin site:
from django.contrib.admin.apps import AdminConfig


class ReviewsConfig(AppConfig):
    # Default django class.
    name = "reviews"


# Commenting this out to use instead the fully custom admin app.
# class ReviewsAdminConfig(AdminConfig):
#     # Using the BookrAdminSite from the root project's admin.py file.
#     default_site = "admin.BookrAdminSite"
