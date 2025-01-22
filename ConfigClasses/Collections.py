from Indicators import BaseIndicator, IndicatorsNormalized
from ConfigClasses.GenericClasses import BaseCollection
from dataclasses import dataclass


class IndicatorsCollection(BaseCollection[BaseIndicator]):
    def __init__(
        self,
        indicators_to_test: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        self.entities: dict[str, BaseIndicator] = {}
        self._load_entities(
            indicators_to_test=indicators_to_test, params_config=params_config
        )

    def _load_entities(
        self,
        indicators_to_test: dict[str, bool],
        params_config: dict[str, dict[str, list[int]]],
    ) -> None:
        for name, cls in IndicatorsNormalized.__dict__.items():
            print(f'cls: {cls}')
            if (
                isinstance(cls, type)
                and issubclass(cls, BaseIndicator)
            ):
                active: bool = indicators_to_test.get(name, False)
                params_values: dict[str, list[int]] = cls.determine_params(
                    name=name, params_config=params_config
                )
                self.entities[name] = cls(
                    name=name,
                    active=active,
                    params_values=params_values,
                )
                print(f'indic: {name}')
                print(f'params: {params_values}')

    @property
    def indicators_params(self) -> list[BaseIndicator]:
        for indicator in self.all_active_entities:
            indicator.get_param_combos()
        return self.all_active_entities

    def get_params(self, name: str) -> dict[str, list[int]]:
        return self.entities[name].params_values

    def set_params(self, name: str, new_params: dict[str, list[int]]) -> None:
        self.entities[name].params_values = new_params

    def update_param_values(self, name: str, param_key: str, values: list[int]) -> None:
        self.entities[name].params_values[param_key] = values


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
            is_active: bool = assets_to_test.get(name, False)
            self.entities[name] = Asset(name=name, active=is_active)
