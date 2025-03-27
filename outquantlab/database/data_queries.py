from pathlib import Path
from outquantlab.database.data_file import JSONFile, ParquetFile
from typing import NamedTuple


class AssetFiles(NamedTuple):
    active: JSONFile[str, bool]
    clusters: JSONFile[str, dict[str, list[str]]]


class IndicFiles(NamedTuple):
    active: JSONFile[str, bool]
    params: JSONFile[str, dict[str, list[int]]]
    clusters: JSONFile[str, dict[str, list[str]]]


class BacktestFiles(NamedTuple):
    results: JSONFile[str, dict[str, list[str]]]
    returns: ParquetFile
    prices: ParquetFile
    
class DataBase(NamedTuple):
    assets: AssetFiles
    indics: IndicFiles
    backtest: BacktestFiles

DB = "data"


def get_db() -> DataBase:
    db_path: Path = _get_db_path(db_name=DB)
    return DataBase(
        assets=_get_asset_files(db_path=db_path),
        indics=_get_indic_files(db_path=db_path),
        backtest=_get_backtest_files(db_path=db_path),
    )

def _get_db_path(db_name: str) -> Path:
    current_file_path: Path = Path(__file__).resolve()
    current_dir: Path = current_file_path.parent
    return current_dir / db_name


def _get_asset_files(db_path: Path) -> AssetFiles:
    return AssetFiles(
        active=JSONFile(db_path=db_path, file_name="assets_active"),
        clusters=JSONFile(db_path=db_path, file_name="assets_clusters"),
    )


def _get_indic_files(db_path: Path) -> IndicFiles:
    return IndicFiles(
        active=JSONFile(db_path=db_path, file_name="indics_active"),
        params=JSONFile(db_path=db_path, file_name="indics_params"),
        clusters=JSONFile(db_path=db_path, file_name="indics_clusters"),
    )


def _get_backtest_files(db_path: Path) -> BacktestFiles:
    return BacktestFiles(
        results=JSONFile(db_path=db_path, file_name="backtest_results"),
        returns=ParquetFile(db_path=db_path, file_name="returns_data"),
        prices=ParquetFile(db_path=db_path, file_name="prices_data"),
    )
