from dataclasses import dataclass
from outquantlab.core.collections import AssetsConfig, IndicsConfig

@dataclass(slots=True)
class AppConfig:
    indics_config: IndicsConfig
    assets_config: AssetsConfig