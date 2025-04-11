from pathlib import Path
from dataclasses import dataclass, field
from outquantlab.database.implementations import (
    AssetFiles,
    IndicFiles,
    TickersData,
)

@dataclass(slots=True)
class DBStructure:
    name: str
    path: Path = field(init=False)
    assets: AssetFiles = field(init=False)
    indics: IndicFiles = field(init=False)
    tickers: TickersData = field(init=False)

    def __post_init__(self) -> None:
        self.path: Path = self._get_db_path(db_name=self.name)
        self.assets = AssetFiles(db_path=self.path)
        self.indics = IndicFiles(db_path=self.path)
        self.tickers = TickersData(db_path=self.path)

    def _get_db_path(self, db_name: str) -> Path:
        current_file_path: Path = Path(__file__).resolve()
        current_dir: Path = current_file_path.parent
        return current_dir / db_name