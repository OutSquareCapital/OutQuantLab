from dataclasses import dataclass

@dataclass(slots=True)
class Asset:
    name: str
    active: bool

def load_entities(assets_to_test: dict[str, bool], asset_names: list[str]) -> dict[str, Asset]:
    assets_objects: dict[str, Asset] = {}
    for name in asset_names:
        is_active: bool = assets_to_test.get(name, False)
        assets_objects[name] = Asset(
            name=name, 
            active=is_active
            )
    return assets_objects

class AssetsCollection:
    def __init__(self, assets_to_test: dict[str, bool], asset_names: list[str]) -> None:
        self.assets_objects: dict[str, Asset] = load_entities(assets_to_test=assets_to_test, asset_names=asset_names)

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