from numpy import nan
from numpy.typing import DTypeLike
from pandas import DataFrame, DatetimeIndex, Index, MultiIndex, Series

from outquantlab.typing_conventions.custom_types import ArrayFloat, Float32


class SeriesFloat(Series):  # type: ignore
    """
    Strictly typed Series for managing floating-point data.

    This class enforces:
    - Data of type Float32.
    - Index of type list[str], Index, or MultiIndex.

    **Methods**:
        >>> @property
        >>> def names(self) -> list[str]:

        *Returns the index of the Series as a list of strings.*

        >>> def get_array()(
        ...     self,
        ...     dtype: DTypeLike = Float32,
        ...     copy: bool = False,
        ...     na_value: float = np.nan
        ... ) -> ArrayFloat:

        *Converts the Series to a NumPy array with specified dtype, copy, and NA value.*
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

    @property
    def names(self) -> list[str]:  # type: ignore
        return super().index  # type: ignore

    def get_array(
        self, dtype: DTypeLike = Float32, copy: bool = False, na_value: float = nan
    ) -> ArrayFloat:
        return super().to_numpy(dtype=dtype, copy=copy, na_value=na_value)  # type: ignore

    def sort_data(self, ascending: bool = True) -> None:
        return SeriesFloat(super().sort_values(ascending=ascending, inplace=True))  # type: ignore


class DataFrameFloat(DataFrame):
    """
    Strictly typed DataFrame for managing floating-point data.

    This class enforces:
    - Data of type Float32.
    - Index of type DatetimeIndex.
    - Columns of type list[str], Index, or MultiIndex.

    **Methods**:
        >>> @property
        >>> def dates(self) -> DatetimeIndex:

        *Returns the index of the DataFrame as a DatetimeIndex.*

        >>> def get_array()(
        ...     self,
        ...     dtype: DTypeLike = Float32,
        ...     copy: bool = False,
        ...     na_value: float = np.nan,
        ... ) -> ArrayFloat:

        *Converts the DataFrame to a NumPy array with specified dtype, copy, and NA value.*
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

    def convert_multiindex_to_labels(self) -> list[str]:
        if isinstance(self.columns, MultiIndex):
            labels: list[str] = [
                "_".join(col).replace(" ", "_") for col in self.columns.to_list()
            ]
        else:
            labels: list[str] = self.columns.to_list()
        return labels