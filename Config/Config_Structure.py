from dataclasses import dataclass
from Database import load_config_file, save_config_file, load_asset_names
from Utilitary import JsonData, ParquetData

@dataclass(slots=True)
class Asset:
    name: str
    active: bool
    category: str

class AssetsCollection:
    def __init__(self, assets_to_test: JsonData, assets_data: ParquetData) -> None:
        self.assets_to_test: JsonData = assets_to_test
        self.assets_data: ParquetData = assets_data
        self.assets_objects: dict[str, Asset] = {}
        self.load_entities()

    def load_entities(self) -> None:
        assets_to_test = load_config_file(self.assets_to_test)
        asset_names = load_asset_names(self.assets_data)
        for name in asset_names:
            is_active = assets_to_test.get(name, False)
            self.assets_objects[name] = Asset(
                name=name, 
                active=is_active,
                category=''
                )

    @property
    def all_entities_names(self) -> list[str]:
        return list(self.assets_objects.keys())

    @property
    def all_entities(self) -> list[Asset]:
        return list(self.assets_objects.values())

    @property
    def all_active_entities_names(self) -> list[str]:
        return [entity.name for entity in self.assets_objects.values() if entity.active]

    @property
    def all_active_entities(self) -> list[Asset]:
        return [entity for entity in self.assets_objects.values() if entity.active]

    def get_entity(self, name: str) -> Asset:
        return self.assets_objects[name]

    def is_active(self, name: str) -> bool:
        return self.assets_objects[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.assets_objects[name].active = active

    def save(self) -> None:
        active_entities = {name: entity.active for name, entity in self.assets_objects.items()}
        save_config_file(self.assets_to_test, active_entities, indent=3)