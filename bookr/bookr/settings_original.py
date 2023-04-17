"""Settings in the original structure (though with project configurations)."""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "+&upt2f0jpm*63=7jpj0qd+dbg8&9dv1bf86*3gl42c5u^#c_x"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # --------Admin concerns------
    # Since this app ("bookr_admin") has been stripped off "AppConfig"
    # (in its apps.py file), we only need it to point to the admin
    # configuration.
    # "admin.site" thus generally points to this app's admin site.
    "bookr_admin.apps.BookrAdminConfig",
    # "reviews.apps.ReviewsAdminConfig",  # Using a custom admin site.
    # Due to the above, you can't use the default admin app, i.e. "
    # django.contrib.admin" should be commented out.
    # By default, this admin app tries to find the admin module in
    # every app of our project, and if found, it loads its contents.
    # ------Defaults---------
    # "django.contrib.admin",
    # This approach has been altered to use a fully custom admin site
    # as an app with its own templates, etc. (See under the "user-
    # created apps section.")
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # ------User-created-------
    "reviews",
    "bookr_admin",
    "filter_demo",
    "book_management",
    # ------Third-party------
    "rest_framework",
    # There are other auth schemes. This one updates the database, so
    # you should run migrations when you add to this list.
    "rest_framework.authtoken",
    "bookr_test",
]

# Middleware objects wrap the whole request-response cycle, injecting
# useful attributes into both request and response objects.
MIDDLEWARE = [
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
        "DIRS": [BASE_DIR / "templates"],  # Use base 'templates' dir.
        "APP_DIRS": True,  # Namespacing enabled or not.
        "OPTIONS": {
            "context_processors": [
                # These return dicts merged with the passed-in context
                # variables to the 'render' call automatically for all
                # views. Hence, 'request' is automatically available
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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Configure this based on the database you're using.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# This identifies urls that need to retrieve static files.
# All urls that have "STATIC_URL" as part of them are mapped to the
# 'static' view, which handles the logic for translating from the url
# to the static file's on-disk location, and serving.
# It can be interpolated using the "static" template tag and
# concatenated to the string arg when a template is rendered.
STATIC_URL = "/static/"

# For use by "FileSystemFinder" (which can serve static files from
# arbitrary directories).
# You can add more searchable directories to the list.
# First file found is what gets served. (Search is carried out based
# on list's order.)
STATICFILES_DIRS = [BASE_DIR / "static"]

# Though not shown, you can use "STATICFILES_STORAGE" to customize
# storage concerns, e.g. caching. It contains a dotted path to the
# storage engine (as a str).
#
# You can define "STATICFILES_FINDERS," a list of finders, but you have
# to ensure that the defaults, "AppDirectoriesFinder" and
# "FileSystemFinder," are in the list.
#
# You can define "STATIC_ROOT," which is the folder that all static
# files get copied to when running the "collectstatic" management
# command. (Checkout the "findstatic" management command.)


# Media
# Project dir where media files are stored:
MEDIA_ROOT = BASE_DIR / "media"

# For use in templates and for serving media files through a url:
MEDIA_URL = "/media/"
