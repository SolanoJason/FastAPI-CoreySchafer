from libcloud.storage.drivers.google_storage import GoogleStorageDriver
from .base import Settings
from .utils import SSLMode, Environment

class ProductionSettings(Settings):
    DB__QUERY__SSLMODE = SSLMode.REQUIRE
    STORAGE_DRIVER_CLASS = GoogleStorageDriver