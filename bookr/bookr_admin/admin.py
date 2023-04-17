"""A foray into creating a custom admin site."""

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.http import HttpRequest

# Note that we haven't registered any models wiith this custom admin
# object. This is because installed apps still reference the default
# "admin.site" property. We can override this. (Check bookr_admin.
# apps.) If this is done, you don't have to update each app to use
# this admin site (i.e. manually) as the "admin.site" reference now
# points to our custom admin site.
#
# Manual way, starting with User: (=> django.contrib.auth.models.User.)
# from django.contrib.auth.admin import User


class BookrAdmin(admin.AdminSite):
    site_title = "Bookr Admin"
    site_header = "Bookr Administration"
    index_title = "Bookr site admin"
    # Checkout what overriding "site_url" does.
    logout_template = "admin/logout.html"

    # Views are created as methods.
    def profile_view(self, request: HttpRequest) -> TemplateResponse:
        # For proper url resolution. ("self.name" is populated by
        # default by AdminSite.):
        request.current_app = self.name
        # To get the template variables, e.g. site_title, passed to
        # all templates of the admin site:
        context = self.each_context(request)
        return TemplateResponse(request, "admin/admin_profile.html", context)

    # Generate the urlpatterns for your view(s):
    def get_urls(self):
        urls = super().get_urls()  # Default admin urls.
        # Add your custom views here.
        # Restrict views to only logged-in admins by wrapping view
        # references with "self.admin_view."
        url_patterns = [path("admin_profile/", self.admin_view(self.profile_view))]
        return urls + url_patterns

    def each_context(self, request: HttpRequest) -> dict:
        context = super().each_context(request)
        # The objects in this context get passed to every template of
        # the admin site.
        context["username"] = request.user.username
        return context


# Better to override "admin.site" so the following steps aren't needed.
#
# You need an instance of this class. The goal is to use this instead
# of the default admin.site property. (This is for the manual approach)
# admin_site = BookrAdmin(name="bookr_admin")
# admin_site.register(User)
