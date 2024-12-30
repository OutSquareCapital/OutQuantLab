from dataclasses import dataclass

@dataclass(slots=True)
class Asset:
    name: str
    active: bool
    category: str

class AssetsCollection:
    def __init__(self, assets_to_test: dict[str, bool], assets_data: list[str]) -> None:
        self.assets_to_test: dict[str, bool] = assets_to_test
        self.asset_names: list[str] = assets_data
        self.assets_objects: dict[str, Asset] = {}
        self.load_entities()

    def load_entities(self) -> None:
        for name in self.asset_names:
            is_active: bool = self.assets_to_test.get(name, False)
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

    @property
    def all_active_entities_dict(self) -> dict[str, bool]:
        return {name: entity.active for name, entity in self.assets_objects.items()}

    def get_entity(self, name: str) -> Asset:
        return self.assets_objects[name]

    def is_active(self, name: str) -> bool:
        return self.assets_objects[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.assets_objects[name].active = active