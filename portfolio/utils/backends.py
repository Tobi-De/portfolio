from django.core.cache import cache
from maintenance_mode.backends import AbstractStateBackend

from core.models import Maintenance


class CacheBackend(AbstractStateBackend):
    def get_value(self):
        value = cache.get("MAINTENANCE_MODE", default="0")
        if value not in ["0", "1"]:
            raise ValueError("cache content value is not 0|1")
        value = bool(int(value))
        return value

    def set_value(self, value):
        value = str(int(value))
        if value not in ["0", "1"]:
            raise ValueError("state file content value is not 0|1")
        cache.set("MAINTENANCE_MODE", value)


class DatabaseBackend(AbstractStateBackend):
    def get_value(self):
        return Maintenance.get_value()

    def set_value(self, value):
        Maintenance.set_value(value=value)
