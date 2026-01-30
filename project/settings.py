import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Setup .env file
load_dotenv()
ENV = os.getenv("ENV")
env_path = os.path.join(BASE_DIR, f".env.{ENV}")
load_dotenv(env_path)
print(f"\nEnvironment: {ENV}")

# Env variables
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
STORAGE_AWS = os.environ.get("STORAGE_AWS") == "True"
HOST = os.getenv("HOST")
TEST_HEADLESS = os.getenv("TEST_HEADLESS", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
EMAILS_LEADS_NOTIFICATIONS = os.getenv("EMAILS_LEADS_NOTIFICATIONS").split(",")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")

print(f"DEBUG: {DEBUG}")
print(f"STORAGE_AWS: {STORAGE_AWS}")
print(f"HOST: {HOST}")

# Application definition

INSTALLED_APPS = [
    # Local apps
    "blog",
    "core",
    # Installed apps
    "unfold",  # before django.contrib.admin
    # "unfold.contrib.filters",  # optional, if special filters are needed
    # "unfold.contrib.forms",  # optional, if special form elements are needed
    # "unfold.contrib.inlines",  # optional, if special inlines are needed
    # "unfold.contrib.import_export",  # optional, if django-import-export package is used
    # "unfold.contrib.guardian",  # optional, if django-guardian package is used
    # "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    # "unfold.contrib.location_field",  # optional, if django-location-field package is used
    # "unfold.contrib.constance",  # optional, if django-constance package is used
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Manage static files
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Cors
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# Database
# Setup database for testing and production
IS_TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

if IS_TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "testing.sqlite3"),
        }
    }
else:

    options = {}
    if os.environ.get("DB_ENGINE") == "django.db.backends.mysql":
        options = {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        }

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE"),
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
            "OPTIONS": options,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "es-mx"

TIME_ZONE = "America/Mexico_City"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Cors
if os.getenv("CORS_ALLOWED_ORIGINS") != "None":
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(",")

if os.getenv("CSRF_TRUSTED_ORIGINS") != "None":
    CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")


# Storage settings
if STORAGE_AWS:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # NEW: Django 5 STORAGES configuration
    STORAGES = {
        "default": {
            "BACKEND": "project.storage_backends.PublicMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "project.storage_backends.StaticStorage",
        },
        # Optional: Keep your private storage accessible via a custom key if needed
        "private": {
            "BACKEND": "project.storage_backends.PrivateMediaStorage",
        },
    }

    # These URLs are still needed for reference, but not for the backend config
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"

    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    PRIVATE_MEDIA_LOCATION = "private"

    STATIC_ROOT = None
    MEDIA_ROOT = None

else:
    # Local development
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"

    # NEW: Default local storages
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }


# Setup drf
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "project.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "EXCEPTION_HANDLER": "utils.handlers.custom_exception_handler",
}

# Global datetime format
DATE_FORMAT = "d/b/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

# Setup emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
EMAIL_FROM = EMAIL_HOST_USER
EMAILS_LEADS_NOTIFICATIONS = os.getenv("EMAILS_LEADS_NOTIFICATIONS").split(",")


# Unfold setup
UNFOLD = {
    "SITE_TITLE": "Cancun Airport Transportation",
    "SITE_HEADER": "Cancun Airport Transportation",
    "SITE_SUBHEADER": "Dashboard",
    "SITE_DROPDOWN": [
        {
            "icon": "web",
            "title": "Landing Page",
            "link": "https://cancunsairporttransportation.com/",
        },
    ],
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static(
        "favicon.png"
    ),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    "SITE_LOGO": lambda request: static(
        "logo.svg"
    ),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    "SITE_SYMBOL": "blog",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.png"),
            "attrs": {
                "target": "_blank",
            },
        },
    ],
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": False,  # show/hide "Back" button on changeform in header, default: False
    "ENVIRONMENT": "utils.callbacks.environment_callback",  # environment name in header
    "ENVIRONMENT_TITLE_PREFIX": "utils.callbacks.environment_title_prefix_callback",  # environment name prefix in title tag
    "DASHBOARD_CALLBACK": "utils.callbacks.dashboard_callback",
    "THEME": "light",  # Force theme: "dark" or "light". Will disable theme switcher
    "LOGIN": {
        # "image": lambda request: static("logo.svg"),
        "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
        # Inherits from `unfold.forms.AuthenticationForm`
        # "form": "app.forms.CustomLoginForm",
    },
    "STYLES": [
        lambda request: static("core/css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("core/js/script.js"),
    ],
    # "BORDER_RADIUS": "6px",
    "COLORS": {
        # Base colors: Neutral gray scale from #757575 (gray) to #16161d (near black)
        "base": {
            "50": "oklch(98% .003 247)",
            "100": "oklch(96% .003 247)",
            "200": "oklch(91% .005 247)",
            "300": "oklch(84% .008 247)",
            "400": "oklch(68% .012 247)",
            "500": "oklch(54% .014 247)",  # ~#757575 (Medium Gray)
            "600": "oklch(44% .014 247)",
            "700": "oklch(36% .015 247)",
            "800": "oklch(28% .016 264)",
            "900": "oklch(22% .018 264)",
            "950": "oklch(16% .02 264)",  # ~#16161d (Near Black)
        },
        # Primary colors: Orange accent scale from #ff8400
        "primary": {
            "50": "oklch(97% .025 70)",
            "100": "oklch(94% .055 70)",
            "200": "oklch(89% .095 65)",
            "300": "oklch(82% .145 60)",
            "400": "oklch(75% .18 55)",
            "500": "oklch(70% .19 50)",  # ~#ff8400 (Orange Accent)
            "600": "oklch(62% .175 48)",
            "700": "oklch(53% .155 46)",
            "800": "oklch(45% .13 45)",
            "900": "oklch(38% .1 44)",
            "950": "oklch(28% .07 42)",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "en": "🇬🇧",
    #             "fr": "🇫🇷",
    #             "nl": "🇧🇪",
    #         },
    #     },
    # },
    # "SIDEBAR": {
    #     "show_search": True,  # Search in applications and models names
    #     "command_search": False,  # Replace the sidebar search with the command search
    #     "show_all_applications": True,  # Dropdown with all applications and models
    #     "navigation": [
    #         {
    #             "title": "Apps",
    #             "separator": True,  # Top border
    #             "collapsible": True,  # Collapsible group of links
    #             "items": [
    #                 {
    #                     "title": _("Dashboard"),
    #                     "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
    #                     "link": reverse_lazy("admin:index"),
    #                     "badge": "sample_app.badge_callback",
    #                     "badge_variant": "info",  # info, success, warning, primary, danger
    #                     "badge_style": "solid",  # background fill style
    #                     "permission": lambda request: request.user.is_superuser,
    #                 },
    #                 {
    #                     "title": _("Users"),
    #                     "icon": "people",
    #                     "link": reverse_lazy("admin:auth_user_changelist"),
    #                 },
    #             ],
    #         },
    #     ],
    # },
    "TABS": [
        {
            # These models will display the tab navigation
            "models": [
                "auth.user",
                "auth.group",
            ],
            # Tab items that appear when viewing any of the above models
            "items": [
                {
                    "title": _("Users"),
                    "link": reverse_lazy("admin:auth_user_changelist"),
                },
                {
                    "title": _("Groups"),
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
            ],
        },
    ],
}
