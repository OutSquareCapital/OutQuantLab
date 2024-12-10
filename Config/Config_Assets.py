from dataclasses import dataclass
from typing import Dict, List, Any
from .Config_Common import load_config_file, save_config_file, load_asset_names
from Files import ASSETS_TO_TEST_CONFIG_FILE, ASSETS_CLASSES_FILE, FILE_PATH_YF

@dataclass
class Asset:
    name: str
    active: bool

class AssetsCollection:
    def __init__(self):
        self._assets: Dict[str, Asset] = {}
        self.clusters: Dict[str, Any] = {}
        self._load()

    def _load(self):

        assets_names = load_asset_names(FILE_PATH_YF)
        assets_to_test = load_config_file(ASSETS_TO_TEST_CONFIG_FILE)
        self.clusters = load_config_file(ASSETS_CLASSES_FILE)

        for asset_name in assets_names:
            is_active = assets_to_test.get(asset_name, False)
            self._assets[asset_name] = Asset(name=asset_name, active=is_active)

    def get_all_objects_names(self) -> List[str]:
        return list(self._assets.keys())

    def get_all_objects(self) -> List[Asset]:
        return list(self._assets.values())

    def get_object(self, name: str) -> Asset:
        return self._assets[name]

    def is_active(self, name: str) -> bool:
        return self._assets[name].active

    def set_active(self, name: str, active: bool):
        self._assets[name].active = active

    def get_active_assets(self) -> List[Asset]:
        return [asset for asset in self._assets.values() if asset.active]

    def get_active_asset_names(self) -> List[str]:
        return [asset.name for asset in self._assets.values() if asset.active]

    def update_clusters_structure(self, new_structure: Dict[str, Any]):
        self.clusters = new_structure

    def save(self):
        assets_active_config = {asset.name: asset.active for asset in self._assets.values()}
        save_config_file(ASSETS_TO_TEST_CONFIG_FILE, assets_active_config, indent=3)
        save_config_file(ASSETS_CLASSES_FILE, self.clusters, indent=3)