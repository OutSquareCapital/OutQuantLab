import os

from outquantlab.database.data_file import DataFile
from outquantlab.database.data_structure import DB_NAME, FileNames


class DataQueries:
    def __init__(self) -> None:
        self.data_files: dict[str, DataFile] = _generate_datafiles()

    def select(self, file: str) -> DataFile:
        try:
            return self.data_files[file]
        except KeyError:
            raise KeyError(f"Data file not found: {file}")

    def print_file_validation(self) -> None:
        validation: dict[str, list[str]] = _validate_file_names(
            actual_files=list(self.data_files.keys())
        )
        print("\nData files structure:")
        _display_data_structure(data_files=self.data_files)
        print("File validation results:")

        if not validation["missing"] and not validation["extra"]:
            print("✓ Perfect match!")

            return

        if validation["missing"]:
            _dispay_missing_files(validation=validation)
        if validation["extra"]:
            _display_extra_files(validation=validation)


def _dispay_missing_files(validation: dict[str, list[str]]) -> None:
    print("\nMissing files (in enum but not found):")
    for file in validation["missing"]:
        print(f"  - {file}")


def _display_extra_files(validation: dict[str, list[str]]) -> None:
    print("\nExtra files (found but not in enum):")
    for file in validation["extra"]:
        print(f"  - {file}")


def _generate_datafiles() -> dict[str, DataFile]:
    data_files: dict[str, DataFile] = {}
    base_dir: str = _get_db_path(db_name=DB_NAME)

    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path: str = os.path.join(root, file)
            file_name, file_ext = os.path.splitext(file)
            datafile = DataFile(ext=file_ext, path=file_path)

            data_files[file_name] = datafile
    return data_files


def _get_db_path(db_name: str) -> str:
    current_file_path: str = os.path.abspath(__file__)
    current_dir: str = os.path.dirname(current_file_path)
    return os.path.join(current_dir, db_name)


def _display_data_structure(data_files: dict[str, DataFile]) -> None:
    for key, value in data_files.items():
        print(
            f"{key}:\n  ext: {value.ext}\n  path: {value.path}\n  handler: {value.handler_name}\n"
        )


def _validate_file_names(actual_files: list[str]) -> dict[str, list[str]]:
    enum_values: list[str] = [name.value for name in FileNames]

    missing_files: list[str] = [
        name for name in enum_values if name not in actual_files
    ]

    extra_files: list[str] = [file for file in actual_files if file not in enum_values]

    return {"missing": missing_files, "extra": extra_files}
