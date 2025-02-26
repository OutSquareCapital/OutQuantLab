from enum import Enum

DB_NAME = "data"

class Extension(Enum):
    JSON = ".json"
    PARQUET = ".parquet"

class FileNames(Enum):
    ASSETS_TO_TEST = "assets_to_test"
    ASSETS_NAMES = "assets_names"
    ASSETS_CLUSTERS = "assets_clusters"
    INDICS_TO_TEST = "indics_to_test"
    INDICS_PARAMS = "indics_params"
    INDICS_CLUSTERS = "indics_clusters"
    RETURNS_DATA = "returns_data"
    PRICES_DATA = "prices_data"