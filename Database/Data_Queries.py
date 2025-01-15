import os

from DataBase.Data_File import DataFile

DATA_DIR: str = "Data"


def get_base_dir(data_dir: str = DATA_DIR) -> str:
    current_file_path: str = os.path.abspath(__file__)
    current_dir: str = os.path.dirname(current_file_path)
    return os.path.join(current_dir, data_dir)


def generate_datafiles() -> dict[str, DataFile]:
    data_files: dict[str, DataFile] = {}
    base_dir: str = get_base_dir()

    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path: str = os.path.join(root, file)
            file_name, file_ext = os.path.splitext(file)
            datafile = DataFile(ext=file_ext, path=file_path)

            data_files[file_name] = datafile
    return data_files

class DataQueries:
    def __init__(self) -> None:
        self.data_files: dict[str, DataFile] = generate_datafiles()

    def select(self, file: str) -> DataFile:
        if file not in self.data_files:
            raise KeyError(f"No file mapped for key: {file}")
        return self.data_files[file]
