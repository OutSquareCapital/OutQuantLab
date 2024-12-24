import os
from typing import Final

N_THREADS: Final = os.cpu_count()

SAVED_DATA_FOLDER: Final = os.path.join(os.path.dirname(__file__), "Saved_Data")

ASSETS_TO_TEST_CONFIG_FILE: Final = os.path.join(SAVED_DATA_FOLDER, "assets_to_backtest.json")
INDICATORS_PARAMS_FILE: Final = os.path.join(SAVED_DATA_FOLDER, "param_values.json")
INDICATORS_TO_TEST_FILE: Final = os.path.join(SAVED_DATA_FOLDER, "methods_to_backtest.json")
INDICATORS_CLUSTERS_FILE: Final = os.path.join(SAVED_DATA_FOLDER, "methods_clusters.json")
ASSETS_CLUSTERS_FILE: Final = os.path.join(SAVED_DATA_FOLDER, "assets_clusters.json")
INDICATORS_MODULE: Final = 'Signals'

FILE_PATH_YF: Final = os.path.join(SAVED_DATA_FOLDER, "price_data.parquet")

MEDIAS_FOLDER: Final = os.path.join(os.path.dirname(__file__), "Medias")
HOME_PAGE_PHOTO: Final = os.path.join(MEDIAS_FOLDER, "home_page.webp")
BACKTEST_PAGE_PHOTO: Final = os.path.join(MEDIAS_FOLDER, "loading_page.png")
DASHBOARD_PAGE_PHOTO: Final = os.path.join(MEDIAS_FOLDER, "dashboard_page.png")
APP_ICON_PHOTO: Final = os.path.join(MEDIAS_FOLDER, "app_logo.png")