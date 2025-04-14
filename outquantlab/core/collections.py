from outquantlab.core.interfaces import BaseConfig
from outquantlab.indicators import INDICATOR_REGISTRY, GenericIndic
from outquantlab.portfolio import Asset

class IndicsConfig(BaseConfig[GenericIndic]):
    def __init__(
        self,
        indics_active: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        self.entities: dict[str, GenericIndic] = {}
        self._load_entities(
            indics_active=indics_active,
            params_config=params_config,
        )

    def _load_entities(
        self,
        indics_active: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        for name, cls in INDICATOR_REGISTRY.items():
            params_values: dict[str, list[int]] = params_config[name]

            self.entities[name] = cls(
                name=name,
                active=_get_active_statut(entity=indics_active, name=name),
                param_values=params_values,
            )

    def get_indics_params(self) -> list[GenericIndic]:
        active_indics: list[GenericIndic] = self.get_all_active_entities()
        for indic in active_indics:
            try:
                indic.get_valid_pairs()
            except Exception as e:
                raise ValueError(
                    f"Error in {indic.name}: {e}"
                ) from e
        return active_indics

    def prepare_indic_params(self) -> dict[str, dict[str, list[int]]]:
        data: dict[str, dict[str, list[int]]] = {}
        for name, indic in self.entities.items():
            data[name] = indic.params_values
        return data


class AssetsConfig(BaseConfig[Asset]):
    def __init__(self, assets_active: dict[str, bool]) -> None:
        self.entities: dict[str, Asset] = {}
        self._load_entities(assets_active=assets_active)

    def _load_entities(
        self, assets_active: dict[str, bool]
    ) -> None:
        for name in assets_active.keys():
            self.entities[name] = Asset(
                name=name, active=_get_active_statut(entity=assets_active, name=name)
            )

    def update_assets(self, names: list[str]) -> None:
        new_assets: dict[str, Asset] = {}
        for name in names:
            new_assets[name] = Asset(name=name, active=False)
        self.entities = new_assets

def _get_active_statut(entity: dict[str, bool], name: str) -> bool:
    return entity.get(name, False)