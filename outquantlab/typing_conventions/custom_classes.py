from numpy import argsort, array, concatenate, nan, nanmean
from pandas import DataFrame, DatetimeIndex, Index, MultiIndex, Series

from outquantlab.typing_conventions.custom_types import ArrayFloat, ArrayInt, Float32


class SeriesFloat(Series):  # type: ignore
    """
    Strictly typed Series for managing floating-point data.

    This class enforces:
    - Data of type Float32.
    - Index of type list[str], Index, or MultiIndex.
    """

    def __init__(
        self,
        data: ArrayFloat | Series | list[float],  # type: ignore
        index: MultiIndex | Index | list[str] | None = None,  # type: ignore
    ) -> None:
        super().__init__(data=data, index=index, dtype=Float32)  # type: ignore

    def get_array(self) -> ArrayFloat:
        return self.to_numpy(dtype=Float32, copy=False, na_value=nan)  # type: ignore

    def get_names(self) -> list[str]:
        return self.index.tolist()  # type: ignore

    def sort_data(self, ascending: bool) -> "SeriesFloat":
        data_array: ArrayFloat = self.get_array()
        sorted_indices: ArrayInt = argsort(data_array)
        if not ascending:
            sorted_indices = sorted_indices[::-1]
        sorted_array: ArrayFloat = data_array[sorted_indices]
        sorted_index: list[str] = [self.get_names()[i] for i in sorted_indices]
        return SeriesFloat(data=sorted_array, index=sorted_index)

    @classmethod
    def from_float_list(cls, data: list[float], index: list[str]) -> "SeriesFloat":
        array_data: ArrayFloat = array(data, dtype=Float32)
        return cls(data=array_data, index=index)

    @classmethod
    def from_array_list(cls, data: list[ArrayFloat], index: list[str]) -> "SeriesFloat":
        combined_array: ArrayFloat = concatenate([r.reshape(1) for r in data])
        return cls(data=combined_array, index=index)

    def convert_to_json(self) -> dict[str, list[str]]:
        data: list[str] = self.values.tolist()  # type: ignore
        index: list[str] = [str(idx) for idx in self.index]  # type: ignore
        return {"data": data, "index": index}


class DataFrameFloat(DataFrame):
    """
    Strictly typed DataFrame for managing floating-point data.

    This class enforces:
    - Data of type Float32.
    - Index of type DatetimeIndex.
    - Columns of type list[str], Index, or MultiIndex.
    """

    def __init__(
        self,
        data: ArrayFloat | DataFrame | None = None,
        index: DatetimeIndex | None = None,
        columns: list[str] | MultiIndex | Index | None = None,  # type: ignore
    ) -> None:
        if data is None:
            data = DataFrame(dtype=Float32)
        super().__init__(data=data, index=index, columns=columns, dtype=Float32)  # type: ignore

    @property
    def dates(self) -> DatetimeIndex:
        return self.index  # type: ignore

    def get_array(self) -> ArrayFloat:
        return self.to_numpy(dtype=Float32, copy=False, na_value=nan)  # type: ignore

    def get_names(self) -> list[str]:
        if isinstance(self.columns, MultiIndex):
            return ["_".join(col).replace(" ", "_") for col in self.columns.to_list()]
        return self.columns.to_list()

    def sort_data(self, ascending: bool) -> "DataFrameFloat":
        mean_values: ArrayFloat = nanmean(self.get_array(), axis=0)
        sorted_indices: ArrayInt = argsort(a=mean_values)
        if not ascending:
            sorted_indices = sorted_indices[::-1]

        sorted_data: ArrayFloat = self.get_array()[:, sorted_indices]
        sorted_columns: list[str] = [self.columns[i] for i in sorted_indices]

        return DataFrameFloat(
            data=sorted_data, columns=sorted_columns, index=self.dates
        )

    def convert_to_json(self) -> dict[str, list[str]]:
        column_data: list[str] = []
        for col_name in self.columns:
            values: list[str] = self[col_name].values.tolist()  # type: ignore
            column_data.append(values)  # type: ignore

        return {
            "data": column_data,
            "index": [str(idx) for idx in self.dates],
            "columns": self.columns.tolist(),
        }
