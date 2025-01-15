import os

from DataBase.Data_File import DataFile

DATA_DIR: str = "Data"


def get_base_dir(data_dir: str = DATA_DIR) -> str:
    current_file_path: str = os.path.abspath(__file__)
    current_dir: str = os.path.dirname(current_file_path)
    return os.path.join(current_dir, data_dir)


class DataQueries:
    def __init__(self) -> None:
        self.base_dir: str = get_base_dir()
        self.files: dict[str, DataFile] = {}
        self.__generate_datafiles()

    def __generate_datafiles(self) -> None:
        for root, _, files in os.walk(self.base_dir):
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
