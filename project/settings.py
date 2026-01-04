import logging
import os
from socket import gethostbyname
from uuid import uuid4

import dj_database_url
import environ
import validators
from split_settings.tools import include, optional

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django.request")

include(optional("settings_local.py"))

root = environ.Path(__file__, "../..")

os.sys.path.insert(0, root())
os.sys.path.insert(0, os.path.join(root(), "apps"))

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    ROLE=(str, "prod"),
    SECRET_KEY=(str, None),
    BASE_URL=(str, None),
    CORS_ALLOWED_ORIGINS=(list, None),
    CSRF_TRUSTED_ORIGINS=(list, None),
    DB_DSN=(str, None),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROLE = env("ROLE")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

BASE_URL = env("BASE_URL")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
allowed_hosts = set()
for host in ALLOWED_HOSTS:
    if not validators.domain(host):
        continue

    try:
        ip: str = gethostbyname(host)
        allowed_hosts.add(ip)
    except Exception as e:
        ...

ALLOWED_HOSTS += list(allowed_hosts)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    "admin_auto_filters",
    "rangefilter",
    "apps.core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "solo",
    "django_essentials_kit",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [root("project/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"

DB_DSN = env("DB_DSN")
DATABASES = {"default": dj_database_url.config(default=env("DB_DSN"))}
DATABASES["default"].update({"TEST": {"NAME": f"test_{uuid4().hex[:6]}"}})
DATABASES["default"]["CONN_MAX_AGE"] = 300
FIXTURE_DIRS = [root("project/fixtures")]
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

USE_TZ = True
TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"
LANGUAGES = [
    ("en", _("English")),
]
USE_I18N = True
USE_L10N = True

MEDIA_URL = "/media/"
MEDIA_ROOT = root("media")

STATIC_URL = "/static/"
STATIC_ROOT = root("static")
STATICFILES_DIRS = [root("project/static")]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "INFO", "handlers": ["console"]},
    "formatters": {
        "verbose": {
            "format": "[%(levelname)s][%(asctime)s] %(module)s.%(funcName)s:%(lineno)d: %(message)s",
        },
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "django": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "django.server": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "django.request": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django.commands": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "django.db.backends": {"level": "WARNING", "handlers": ["console"], "propagate": False},
    },
}

APPEND_SLASH = True

LOGIN_URL = "/admin/login/"

if ROLE == "test":
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()

    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

elif ROLE == "debug":
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

import django
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy

django.utils.translation.ugettext = gettext_lazy
django.utils.encoding.force_text = force_str

from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "Y-m-d H:i:s"
en_formats.DATE_FORMAT = "Y-m-d"

include(optional("settings_local.py"))
