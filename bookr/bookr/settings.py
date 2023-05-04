"""Settings using the 'django-configurations' app.

The manage.py file will also have to be updated to accomodate these
changes.
"""

from pathlib import Path

from configurations import Configuration, values


class Dev(Configuration):
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    SECRET_KEY = "+&upt2f0jpm*63=7jpj0qd+dbg8&9dv1bf86*3gl42c5u^#c_x"
    # To ensure "DEBUG" is read from an environment variable if set,
    # else the default here, "True," is used. (You can use os.environ
    # to set environment variables, or set them from the command line.)
    DEBUG = values.BooleanValue(True)
    # "ListValue" converts comma-separated string values into a list:
    # "a,b,c" -> ["a", "b", "c"].
    ALLOWED_HOSTS = values.ListValue([])
    INSTALLED_APPS = [
        # --------ADMIN CONCERNS------
        # Since this app ("bookr_admin") has been stripped off
        # AppConfig(in its apps.py file), we only need it to point to
        # the admin configuration.
        # "admin.site" thus generally points to this app's admin site.
        "bookr_admin.apps.BookrAdminConfig",
        # "reviews.apps.ReviewsAdminConfig",  # Custom admin site.
        # Due to the above, you can't use the default admin app, i.e. "
        # django.contrib.admin" should be commented out.
        # By default, this admin app tries to find the admin module in
        # every app of our project, and if found, it loads its
        # contents.
        # ------DEFAULTS---------
        # "django.contrib.admin",
        # This approach has been altered to use a fully custom admin
        # site as an app with its own templates, etc. (See under the
        # "user-created apps section.")
        "django.contrib.sites",  # Added for "django-allauth."
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # ------USER-CREATED-------
        "reviews",
        "bookr_admin",
        "filter_demo",
        "book_management",
        # ------THIRD-PARTY------
        "rest_framework",
        # There are other auth schemes. This one updates the database,
        # so you should run migrations when you add to this list.
        "rest_framework.authtoken",
        "bookr_test",
        "debug_toolbar",
        # NOTE: First add => run the "migrate" command to create
        # "allauth's" (and "contrib.site") models. This => you can add
        # new social apps (from providers listed down here) with the
        # admin interface.
        "allauth",
        "allauth.socialaccount",
        # Supported providers for authentication are as follows.
        # You can create a social app for Google using your Google
        # Developers console, and a Github social app with your Github
        # profile. Both provide a client ID and secret key that can be
        # used to create a social app in the admin interface (or
        # through the shell.)
        "allauth.socialaccount.providers.google",
        "allauth.socialaccount.providers.github",
    ]

    # Needed for "allauth." It is possible to have the same django app
    # on different sites with different behaviors for each site, but
    # with data being shared across.
    SITE_ID = 1  # Random num.

    # Redirect on login to the book list page.
    LOGIN_REDIRECT_URL = "/"

    # IPs to display the django debug toolbar.
    INTERNAL_IPS = ["127.0.0.1"]

    # Middleware objects wrap the whole request-response cycle,
    # injecting useful attributes into both request and response
    # objects.
    MIDDLEWARE = [
        # "DebugToolbarMiddleware" should be the first.
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # The url path searched for the url mappings.
    ROOT_URLCONF = "bookr.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],  # Base 'templates' dir.
            "APP_DIRS": True,  # Namespacing enabled or not.
            "OPTIONS": {
                "context_processors": [
                    # These return dicts merged with the passed-in
                    # context variables to the 'render' call
                    # automatically for all views. Hence, 'request' is
                    # automatically available
                    # in all app templates (passed through the render
                    # call).
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "bookr.wsgi.application"

    # Configure this based on the database you're using.
    #
    # Here, we use a url to connect to the database we're using, local
    # or remote. The format for the url is
    # <protocol>://<username>:<password>@<host>:<port>/<db_name>.
    # Since sqlite doesn't have "username" and "password" attrs, we
    # have <protocol>://<host>/<path> or, locally
    # <protocol>:///<path>.
    #
    # Using DatabaseURLValue returns a dict of required db attrs.
    # Also, this approach enables you to set the db url with an env
    # var. Hence, you can override with a production db url.
    # Note that "DatabaseURLValue" works with the dj-database-url app,
    # hence, it must be installed. (Check "dj_database_url.config" as
    # an alternative [also "dj_database_url.urlpase" method].)
    DATABASES = values.DatabaseURLValue(
        f"sqlite:///{BASE_DIR}/db.sqlite3",
        # To be consistent with other django env vars:
        environ_prefix="DJANGO",  # => env var = "DJANGO_DATABASE_URL."
    )

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # This identifies urls that need to retrieve static files.
    # All urls that have "STATIC_URL" as part of them are mapped to the
    # 'static' view, which handles the logic for translating from the
    # url to the static file's on-disk location, and serving.
    # It can be interpolated using the "static" template tag and
    # concatenated to the given string arg when a template is rendered.
    STATIC_URL = "/static/"
    # For use by "FileSystemFinder" (which can serve static files from
    # arbitrary directories).
    # You can add more searchable directories to the list.
    # First file found is what gets served. (Search is carried out
    # based on list's order.)
    STATICFILES_DIRS = [BASE_DIR / "static"]
    # Though not shown, you can use "STATICFILES_STORAGE" to customize
    # storage concerns, e.g. caching. It contains a dotted path to the
    # storage engine (as a str).
    #
    # You can define "STATICFILES_FINDERS," a list of finders, but you
    # have to ensure that the defaults, "AppDirectoriesFinder" and
    # FileSystemFinder, are in the list.
    #
    # You can define "STATIC_ROOT," which is the folder that all static
    # files get copied to when running the "collectstatic" management
    # command. (Checkout the "findstatic" management command.)

    # Media
    # Project dir where media files are stored:
    MEDIA_ROOT = BASE_DIR / "media"
    # For use in templates and for serving media files through a url:
    MEDIA_URL = "/media/"


class Production(Dev):
    DEBUG = False
    # "SecretValue" => can't set environ defaults, else exception.
    SECRET_KEY = values.SecretValue()
