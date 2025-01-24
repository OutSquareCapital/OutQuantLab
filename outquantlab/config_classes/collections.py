from outquantlab.indicators import BaseIndic, IndicatorsNormalized, DataArrays
from outquantlab.config_classes.generic_classes import BaseCollection
from dataclasses import dataclass
from inspect import signature


class IndicsCollection(BaseCollection[BaseIndic]):
    def __init__(
        self,
        indics_to_test: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
        data_arrays: DataArrays,
    ) -> None:
        self.entities: dict[str, BaseIndic] = {}
        self._load_entities(
            indics_to_test=indics_to_test,
            params_config=params_config,
            data_arrays=data_arrays,
        )

    def _load_entities(
        self,
        indics_to_test: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
        data_arrays: DataArrays,
    ) -> None:
        for name, cls in IndicatorsNormalized.__dict__.items():
            if isinstance(cls, type) and issubclass(cls, BaseIndic):
                active: bool = indics_to_test.get(name, False)
                param_names: list[str] = list(signature(cls.execute).parameters.keys())[
                    1:
                ]
                params_values: dict[str, list[int]] = {
                    param: params_config.get(name, {}).get(param, [])
                    for param in param_names
                }

                self.entities[name] = cls(
                    name=name,
                    active=active,
                    param_values=params_values,
                    data_arrays=data_arrays,
                )

    def get_indics_params(self) -> list[BaseIndic]:
        active_indics: list[BaseIndic] = self.get_all_active_entities()
        for indicator in active_indics:
            indicator.param_combos = indicator.filter_valid_pairs()
        return active_indics


@dataclass(slots=True)
class Asset:
    name: str
    active: bool


class AssetsCollection(BaseCollection[Asset]):
    def __init__(self, assets_to_test: dict[str, bool], asset_names: list[str]) -> None:
        self.entities: dict[str, Asset] = {}
        self._load_entities(assets_to_test=assets_to_test, asset_names=asset_names)

    def _load_entities(
        self, assets_to_test: dict[str, bool], asset_names: list[str]
    ) -> None:
        for name in asset_names:
            active: bool = assets_to_test.get(name, False)
            self.entities[name] = Asset(name=name, active=active)
