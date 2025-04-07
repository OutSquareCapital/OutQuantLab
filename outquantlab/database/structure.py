from pathlib import Path
from typing import NamedTuple

from outquantlab.database.implementations import (
    AssetFiles,
    IndicFiles,
    TickersData,
)


class DBStructure(NamedTuple):
    assets: AssetFiles
    indics: IndicFiles
    tickers: TickersData


def get_db_structure(db_name: str) -> DBStructure:
    db_path: Path = _get_db_path(db_name=db_name)
    return DBStructure(
        assets=AssetFiles(db_path=db_path),
        indics=IndicFiles(db_path=db_path),
        tickers=TickersData(db_path=db_path),
    )


def _get_db_path(db_name: str) -> Path:
    current_file_path: Path = Path(__file__).resolve()
    current_dir: Path = current_file_path.parent
    return current_dir / db_name
