import logging
import sys

from decouple import Csv, config


class Config:
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)
        # Django
        self.django_secret_key = config("django_secret_key", cast=str)
        self.debug = config("debug", bool)
        self.allowed_hosts = config("allowed_hosts", cast=Csv())
        self.cors_origins = config("cors_origins", cast=Csv())
        self.csrf_trusted = config("csrf_trusted", cast=Csv())
        # DB
        self.db_host = config("db_host", cast=str)
        self.db_name = config("db_name", cast=str)
        self.db_user = config("db_user", cast=str)
        self.db_password = config("db_password", cast=str)
        self.db_port = config("db_port", cast=int)
        # SIMPLE_JWT
        self.signing_key = config("signing_key", cast=str)
        # DJOSER EMAIL
        self.email_host = config("email_host", cast=str)
        self.email_host_user = config("email_host_user", cast=str)
        self.email_host_password = config("email_host_password", cast=str)
        self.email_guest = config("email_guest", cast=str)

        self.email_port = config("email_port", cast=str)
        self.domain = config("domain", cast=str)
        self.activation_url = config("activation_url", cast=str)
        self.reset_password_url = config("reset_password_url", cast=str)

logger = logging.getLogger("config")

try:
    CONFIG = Config()
except Exception as error:
    logger.critical(f"config is broken {error}")
    sys.exit(1)
