from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
import debug_toolbar

# Using a custom admin site without overriding "admin.site":
# from bookr_admin.admin import admin_site
from .views import profile, download_read_history

# You can use the "include" function in one of three ways:
# include(module, namespace=None) or
# include(pattern_list) or
# include((pattern_list, app_namespace), namespace=None), where
# "pattern_list" can point to a module as shown below.
#
# "namespace" is the instance namespace and it can be different from
# the application namespace. (It can be set to non None values.)
urlpatterns = [
    # "namespace=accounts" => you can use a set-up url for the
    # included auth.urls in a template as such: {% url "accounts:
    # login" %}. login is a url path's name in the contrib.urls file.
    path(
        "accounts/", include(("django.contrib.auth.urls", "auth"), namespace="accounts")
    ),
    # A successful login redirects to the accounts/profile page.
    path("accounts/profile/", profile, name="profile"),
    path("accounts/profile/read_books", download_read_history, name="read_books"),
    path("allauth/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    # "admin.site" not overridden => path("admin/", admin_site.urls),
    path("", include("reviews.urls")),
    path("filters/", include("filter_demo.urls"), name="filter_demo"),
    path("bookmgt/", include("book_management.urls"), name="book_management"),
    path("testing/", include("bookr_test.urls")),
]

# NOTE: In settings, you have the "STATIC_URL" option, which can be
# used to serve static files as follows: localhost:8000/static/<filename>,
# or with namespacing: localhost:8000/static/reviews/<filename>.

# You can only use the static view if debug=True.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
