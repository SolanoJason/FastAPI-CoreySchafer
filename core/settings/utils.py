import enum
from typing import Annotated
from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(enum.StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class SSLMode(enum.StrEnum):
    DISABLE = "disable"
    ALLOW = "allow"
    PREFER = "prefer"
    REQUIRE = "require"
    VERIFY_CA = "verify-ca"
    VERIFY_FULL = "verify-full"
