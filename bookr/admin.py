from django.contrib import admin

# This approach is now replaced by the use of a custom admin app.
class BookrAdminSite(admin.AdminSite):
    # Using a custom admin object.
    site_title = "Bookr Admin"
    site_header = "Bookr administration"
    index_title = "Bookr site admin"
    # The template is in the root templates folder.
    logout_template = "admin_logged_out.html"
