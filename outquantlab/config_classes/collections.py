from inspect import signature

from outquantlab.config_classes.generic_classes import BaseConfig
from outquantlab.indicators import IndicsNormalized, BaseIndic
from dataclasses import dataclass


@dataclass(slots=True)
class Asset:
    name: str
    active: bool


class IndicsConfig(BaseConfig[BaseIndic]):
    def __init__(
        self,
        indics_to_test: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        self.entities: dict[str, BaseIndic] = {}
        self._load_entities(
            indics_to_test=indics_to_test,
            params_config=params_config,
        )

    def _load_entities(
        self,
        indics_to_test: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        for name, cls in IndicsNormalized.__dict__.items():
            if isinstance(cls, type) and issubclass(cls, BaseIndic):
                active: bool = indics_to_test.get(name, False)
                param_names: list[str] = list(signature(cls.execute).parameters.keys())[
                    2:
                ]
                params_values: dict[str, list[int]] = {
                    param: params_config.get(name, {}).get(param, [])
                    for param in param_names
                }

                self.entities[name] = cls(
                    name=name,
                    active=active,
                    param_values=params_values,
                )

    def get_indics_params(self) -> list[BaseIndic]:
        active_indics: list[BaseIndic] = self.get_all_active_entities()

        for indic in active_indics:
            indic.filter_valid_pairs()

            if not indic.param_combos:
                raise ValueError(
                    f"Aucune combinaison valide trouvée pour l'indicateur {indic.name}"
                )

            indic.strategies_nb = len(indic.param_combos)

        return active_indics

    def prepare_indic_params(self) -> dict[str, dict[str, list[int]]]:
        data: dict[str, dict[str, list[int]]] = {}
        for name, indicator in self.entities.items():
            data[name] = indicator.params_values
        return data


class AssetsConfig(BaseConfig[Asset]):
    def __init__(self, assets_to_test: dict[str, bool], asset_names: list[str]) -> None:
        self.entities: dict[str, Asset] = {}
        self._load_entities(assets_to_test=assets_to_test, asset_names=asset_names)

    def _load_entities(
        self, assets_to_test: dict[str, bool], asset_names: list[str]
    ) -> None:
        for name in asset_names:
            active: bool = assets_to_test.get(name, False)
            self.entities[name] = Asset(name=name, active=active)
