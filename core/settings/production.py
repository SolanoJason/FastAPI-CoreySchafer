from libcloud.storage.drivers.google_storage import GoogleStorageDriver
from libcloud.storage.base import Container, StorageDriver
from libcloud.common.google import GoogleAuthType
from pydantic import Field, SecretStr, field_validator
from functools import cached_property
from .base import Settings
from .utils import SSLMode, Environment

class ProductionSettings(Settings):
    DB__QUERY__SSLMODE = SSLMode.REQUIRE
    STORAGE_DRIVER_CLASS = GoogleStorageDriver

    # Google Cloud Storage service-account credentials. Keep these in the
    # deployment secret manager rather than in source control.
    GCS_PROJECT: str = Field(..., min_length=1)
    GCS_BUCKET: str = Field(..., min_length=1)
    GCS_SERVICE_ACCOUNT_EMAIL: str = Field(..., min_length=1)
    GCS_PRIVATE_KEY: SecretStr = Field(..., min_length=1)

    @field_validator("GCS_PRIVATE_KEY", mode="before")
    @classmethod
    def normalize_private_key(cls, value: str) -> str:
        return value.replace("\\n", "\n")

    @cached_property
    def driver(self) -> StorageDriver:
        return self.STORAGE_DRIVER_CLASS(
            self.GCS_SERVICE_ACCOUNT_EMAIL,
            self.GCS_PRIVATE_KEY.get_secret_value(),
            project=self.GCS_PROJECT,
            auth_type=GoogleAuthType.SA,
        )

    @cached_property
    def container(self) -> Container:
        return self.driver.get_container(self.GCS_BUCKET)
