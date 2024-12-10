import os

SAVED_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Saved_Data")

ASSETS_TO_TEST_CONFIG_FILE = os.path.join(SAVED_DATA_FOLDER, "assets_to_backtest.json")
INDICATORS_PARAMS_FILE = os.path.join(SAVED_DATA_FOLDER, "param_values.json")
INDICATORS_TO_TEST_FILE = os.path.join(SAVED_DATA_FOLDER, "methods_to_backtest.json")
INDICATORS_CLUSTERS_FILE = os.path.join(SAVED_DATA_FOLDER, "methods_classes.json")
ASSETS_CLUSTERS_FILE = os.path.join(SAVED_DATA_FOLDER, "assets_classes.json")
INDICATORS_MODULE = 'Signals'

FILE_PATH_YF = os.path.join(SAVED_DATA_FOLDER, "price_data.parquet")

MEDIAS_FOLDER = os.path.join(os.path.dirname(__file__), "Medias")
HOME_PAGE_PHOTO = os.path.join(MEDIAS_FOLDER, "home_page.webp")
BACKTEST_PAGE_PHOTO = os.path.join(MEDIAS_FOLDER, "loading_page.png")
DASHBOARD_PAGE_PHOTO = os.path.join(MEDIAS_FOLDER, "dashboard_page.png")
APP_ICON_PHOTO = os.path.join(MEDIAS_FOLDER, "app_logo.png")