from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.base import StorageDriver, Container
from .base import Settings
from libcloud.storage.providers import Provider
from .utils import SSLMode, Environment
from functools import cached_property

class DevelopmentSettings(Settings):
    DB__QUERY__SSLMODE = SSLMode.ALLOW
    STORAGE_PROVIDER = Provider.LOCAL