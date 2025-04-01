from dataclasses import dataclass
from inspect import signature

from outquantlab.core.interfaces import BaseConfig
from outquantlab.indicators import BaseIndic, INDICATOR_REGISTRY


@dataclass(slots=True)
class Asset:
    name: str
    active: bool


class IndicsConfig(BaseConfig[BaseIndic]):
    def __init__(
        self,
        indics_active: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        self.entities: dict[str, BaseIndic] = {}
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
            param_names: list[str] = self._get_params_names(cls=cls)
            params_values: dict[str, list[int]] = self._get_params_values(
                param_names=param_names, name=name, params_config=params_config
            )

            self.entities[name] = cls(
                name=name,
                active=_get_active_statut(entity=indics_active, name=name),
                param_values=params_values,
            )

    def _get_params_names(self, cls: type[BaseIndic]) -> list[str]:
        return list(signature(cls.execute).parameters.keys())[2:]


    def _get_params_values(
        self, param_names: list[str], name: str, params_config: dict[str, dict[str, list[int]]]
    ) -> dict[str, list[int]]:
        params_values: dict[str, list[int]] = {
            param: params_config.get(name, {}).get(param, []) for param in param_names
        }
        return params_values

    def get_indics_params(self) -> list[BaseIndic]:
        active_indics: list[BaseIndic] = self.get_all_active_entities()

        for indic in active_indics:
            indic.params.get_valid_pairs()
        return active_indics

    def prepare_indic_params(self) -> dict[str, dict[str, list[int]]]:
        data: dict[str, dict[str, list[int]]] = {}
        for name, indic in self.entities.items():
            data[name] = indic.params.values
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


def _get_active_statut(entity: dict[str, bool], name: str) -> bool:
    return entity.get(name, False)