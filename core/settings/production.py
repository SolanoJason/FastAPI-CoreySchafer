from libcloud.storage.drivers.google_storage import GoogleStorageDriver
from libcloud.storage.base import Container, StorageDriver
from libcloud.common.google import GoogleAuthType
from libcloud.storage.providers import Provider
from pydantic import Field, SecretStr, field_validator
from functools import cached_property
from .base import Settings
from .utils import SSLMode, Environment

class ProductionSettings(Settings):
    DB__QUERY__SSLMODE = SSLMode.REQUIRE
    STORAGE_PROVIDER = Provider.GOOGLE_STORAGE

    STORAGE_KEY: SecretStr
    STORAGE_SECRET: SecretStr
    STORAGE_BUCKET: str