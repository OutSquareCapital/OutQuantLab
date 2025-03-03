from enum import StrEnum

DB_NAME = "data"

class Extension(StrEnum):
    JSON = ".json"
    PARQUET = ".parquet"

class FileNames(StrEnum):
    ASSETS_ACTIVE = "assets_active"
    ASSETS_NAMES = "assets_names"
    ASSETS_CLUSTERS = "assets_clusters"
    INDICS_ACTIVE = "indics_active"
    INDICS_PARAMS = "indics_params"
    INDICS_CLUSTERS = "indics_clusters"
    RETURNS_DATA = "returns_data"
    PRICES_DATA = "prices_data"