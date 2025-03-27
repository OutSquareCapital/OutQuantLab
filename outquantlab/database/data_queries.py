from pathlib import Path

from outquantlab.database.data_file import JSONFile, ParquetFile

DB = "data"

class DataQueries:
    def __init__(self) -> None:
        db_path: Path = self._get_db_path(db_name=DB)
        self.assets_active: JSONFile = JSONFile(db_path=db_path, file_name="assets_active")
        self.assets_clusters: JSONFile = JSONFile(db_path=db_path, file_name="assets_clusters")
        self.indics_active: JSONFile = JSONFile(db_path=db_path, file_name="indics_active")
        self.indics_params: JSONFile = JSONFile(db_path=db_path, file_name="indics_params")
        self.indics_clusters: JSONFile = JSONFile(db_path=db_path, file_name="indics_clusters")
        self.backtest_results: JSONFile = JSONFile(db_path=db_path, file_name="backtest_results")
        self.returns_data: ParquetFile = ParquetFile(db_path=db_path, file_name="returns_data")
        self.prices_data: ParquetFile = ParquetFile(db_path=db_path, file_name="prices_data")

    def _get_db_path(self, db_name: str) -> Path:
        current_file_path: Path = Path(__file__).resolve()
        current_dir: Path = current_file_path.parent
        return current_dir / db_name

    def check_data(self) -> None:
        for name, value in self.__dict__.items():
            print(f"{name}:\n {value}")