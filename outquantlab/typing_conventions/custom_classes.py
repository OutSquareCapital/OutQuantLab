from numpy import nan, argsort, nanmean
from numpy.typing import DTypeLike
from pandas import DataFrame, DatetimeIndex, Index, MultiIndex, Series

from outquantlab.typing_conventions.custom_types import ArrayFloat, Float32, ArrayInt


class SeriesFloat(Series):  # type: ignore
    """
    Strictly typed Series for managing floating-point data.

    This class enforces:
    - Data of type Float32.
    - Index of type list[str], Index, or MultiIndex.
    """

    def __init__(
        self,
        data: ArrayFloat | Series,  # type: ignore
        index: MultiIndex | Index | list[str] | None = None,  # type: ignore
        dtype: type = Float32,
    ) -> None:
        if isinstance(data, Series):
            data = data.astype(dtype=Float32)  # type: ignore

        super().__init__(data=data, index=index, dtype=dtype)  # type: ignore

    def get_array(
        self, dtype: DTypeLike = Float32, copy: bool = False, na_value: float = nan
    ) -> ArrayFloat:
        return super().to_numpy(dtype=dtype, copy=copy, na_value=na_value)  # type: ignore

    def get_names(self) -> list[str]:
        return self.index.tolist() # type: ignore

    def sort_data(self, ascending: bool) -> "SeriesFloat":
        array: ArrayFloat = self.get_array()
        sorted_indices: ArrayInt = argsort(array)
        if not ascending:
            sorted_indices = sorted_indices[::-1]
        sorted_array: ArrayFloat = array[sorted_indices]
        sorted_index: list[str] = [self.get_names()[i] for i in sorted_indices]
        return SeriesFloat(data=sorted_array, index=sorted_index)


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
        dtype: type = Float32,
    ) -> None:
        if data is None:
            data = DataFrame(dtype=Float32)
        if isinstance(data, DataFrame):
            data = data.astype(dtype=Float32)  # type: ignore
        super().__init__(data=data, index=index, columns=columns, dtype=dtype)  # type: ignore

    @property
    def dates(self) -> DatetimeIndex:
        return super().index  # type: ignore

    def get_array(
        self, dtype: DTypeLike = Float32, copy: bool = False, na_value: float = nan
    ) -> ArrayFloat:
        return super().to_numpy(dtype=dtype, copy=copy, na_value=na_value)  # type: ignore

    def get_names(self) -> list[str]:
        if isinstance(self.columns, MultiIndex):
            labels: list[str] = [
                "_".join(col).replace(" ", "_") for col in self.columns.to_list() # type: ignore
            ]
        else:
            labels: list[str] = self.columns.to_list()  # type: ignore
        return labels

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
