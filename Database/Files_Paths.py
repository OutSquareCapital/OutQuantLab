from typing import Any, Final
from dataclasses import dataclass
import os
from Utilitary import JSON_EXT, PARQUET_EXT, WEBP_EXT, PNG_EXT

@dataclass(frozen=True)
class SystemPaths:
    base_dir: Final[str] = os.path.dirname(__file__)

    @property
    def saved_data(self) -> str:
        return os.path.join(self.base_dir, "Saved_Data")

    @property
    def medias(self) -> str:
        return os.path.join(self.base_dir, "Medias")

@dataclass(frozen=True)
class ConfigFilesPaths:
    paths: SystemPaths

    def _make_path(self, name: str, ext_type: str) -> str:
        return os.path.join(self.paths.saved_data, f"{name}{ext_type}")

    @property
    def assets_to_test(self) -> Any:
        return self._make_path(name='assets_to_test', ext_type=JSON_EXT)

    @property
    def indics_params(self) -> Any:
        return self._make_path(name='indics_params', ext_type=JSON_EXT)

    @property
    def indics_to_test(self) -> Any:
        return self._make_path(name='indics_to_test', ext_type=JSON_EXT)

    @property
    def indics_clusters(self) -> Any:
        return self._make_path(name='indics_clusters', ext_type=JSON_EXT)

    @property
    def assets_clusters(self) -> Any:
        return self._make_path(name='assets_clusters', ext_type=JSON_EXT)

    @property
    def price_data(self) -> Any:
        return self._make_path(name='price_data', ext_type=PARQUET_EXT)

@dataclass(frozen=True)
class MediaFilesPaths:
    paths: SystemPaths

    def _make_path(self, name: str, ext_type: str) -> str:
        return os.path.join(self.paths.medias, f"{name}{ext_type}")

    @property
    def home_page(self) -> Any:
        return self._make_path(name='home_page', ext_type=WEBP_EXT)

    @property
    def loading_page(self) -> Any:
        return self._make_path(name='loading_page', ext_type=PNG_EXT)

    @property
    def dashboard_page(self) -> Any:
        return self._make_path(name='dashboard_page', ext_type=PNG_EXT)

    @property
    def app_logo(self) -> Any:
        return self._make_path(name='app_logo', ext_type=PNG_EXT)

system_paths = SystemPaths()
CONFIG = ConfigFilesPaths(paths=system_paths)
MEDIA = MediaFilesPaths(paths=system_paths)
