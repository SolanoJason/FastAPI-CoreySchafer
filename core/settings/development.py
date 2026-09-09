from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.base import StorageDriver, Container
from .base import Settings
from .utils import SSLMode, Environment
from functools import cached_property

class DevelopmentSettings(Settings):
    DB__QUERY__SSLMODE = SSLMode.ALLOW
    STORAGE_DRIVER_CLASS = LocalStorageDriver

    @cached_property
    def driver(self) -> StorageDriver:
        return self.STORAGE_DRIVER_CLASS(self.MEDIA_ROOT)

    @cached_property
    def container(self) -> Container:
        return self.driver.get_container("")