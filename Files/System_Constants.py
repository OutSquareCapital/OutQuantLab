import os
from typing import Final
from dataclasses import dataclass
from .custom_types import JSON_EXT, PARQUET_EXT, JsonData, ParquetData, PngMedia,  WebpMedia, PNG_EXT, WEBP_EXT

N_THREADS: Final = os.cpu_count() or 8

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
class ConfigFiles:
    paths: SystemPaths

    def _make_path(self, name: str, ext_type: str) -> str:
        return os.path.join(self.paths.saved_data, f"{name}{ext_type}")
    
    @property
    def assets_to_test(self) -> JsonData:
        return self._make_path('assets_to_test', JSON_EXT)

    @property
    def indics_params(self) -> JsonData:
        return self._make_path('indics_params', JSON_EXT)
    
    @property
    def indics_to_test(self) -> JsonData:
        return self._make_path('indics_to_test', JSON_EXT)
    
    @property
    def indics_clusters(self) -> JsonData:
        return self._make_path('indics_clusters', JSON_EXT)
    
    @property
    def assets_clusters(self) -> JsonData:
        return self._make_path('assets_clusters', JSON_EXT)

    @property
    def price_data(self) -> ParquetData:
        return self._make_path('price_data', PARQUET_EXT)

@dataclass(frozen=True)
class MediaFiles:
    paths: SystemPaths

    def _make_path(self, name: str, ext_type: str) -> str:
        return os.path.join(self.paths.saved_data, f"{name}{ext_type}")

    @property
    def home_page(self) -> WebpMedia:
        return self._make_path('home_page', WEBP_EXT)
    
    @property
    def loading_page(self) -> PngMedia:
        return self._make_path('loading_page', PNG_EXT)

    @property
    def dashboard_page(self) -> PngMedia:
        return self._make_path('dashboard_page', PNG_EXT)
    
    @property
    def app_logo(self) -> PngMedia:
        return self._make_path('app_logo', PNG_EXT)

system_paths = SystemPaths()
CONFIG = ConfigFiles(system_paths)
MEDIA = MediaFiles(system_paths)