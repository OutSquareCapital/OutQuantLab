from pathlib import Path
from outquantlab.database.implementations import (
    AssetFiles,
    IndicFiles,
    TickersDataFiles
)


class DBStructure:
    def __init__(self, db_name: str) -> None:
        self.path: Path = self._get_db_path(db_name=db_name)
        self.assets = AssetFiles(db_path=self.path)
        self.indics = IndicFiles(db_path=self.path)
        self.tickers = TickersDataFiles(db_path=self.path)

    def _get_db_path(self, db_name: str) -> Path:
        current_file_path: Path = Path(__file__).resolve()
        current_dir: Path = current_file_path.parent
        return current_dir / db_name