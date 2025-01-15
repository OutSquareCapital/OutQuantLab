import os

from DataBase.Data_File import DataFile

BASE_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")


class DataQueries:
    def __init__(self, base_dir: str = BASE_DIR) -> None:
        self.files: dict[str, DataFile] = {}
        self.__generate_datafiles(base_dir)

    def __generate_datafiles(self, base_dir: str = BASE_DIR) -> None:
        for root, _, files in os.walk(base_dir):
            for file_name in files:
                file_path: str = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    file_base, file_ext = os.path.splitext(file_name)
                    datafile = DataFile(ext=file_ext, path=file_path)

                    self.files[file_base] = datafile

    def select(self, file: str) -> DataFile:
        if file not in self.files:
            raise KeyError(f"No file mapped for key: {file}")
        return self.files[file]
