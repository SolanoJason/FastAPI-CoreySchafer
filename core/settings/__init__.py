from .utils import Environment
from .development import DevelopmentSettings
from .production import ProductionSettings
from .base import Settings

base_settings = Settings() # type: ignore

if base_settings.ENVIRONMENT == Environment.PRODUCTION:
    settings = ProductionSettings() # type: ignore
else:
    settings = DevelopmentSettings() # type: ignore

__all__ = ["settings"]
