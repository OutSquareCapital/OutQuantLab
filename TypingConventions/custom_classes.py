from typing import Any, Protocol

import numpy as np
from numpy.typing import DTypeLike
from pandas import DataFrame, DatetimeIndex, Index, MultiIndex, Series

from TypingConventions.custom_types import ArrayFloat, Float32


class FileHandler(Protocol):
    """
    Protocol who defines the standard interface for file operations,
    ensuring consistency across all handler implementations.

    **Methods**:
        >>> def load(self, path: str) -> Any:

        *Reads data from the file at the given path.*

        >>> def save(self, path: str, data: Any) -> None:

        *Writes data to the file at the given path.*
    """

    def load(self, path: str) -> Any:
        raise NotImplementedError

    def save(self, path: str, data: Any) -> None:
        raise NotImplementedError


class SeriesFloat(Series): # type: ignore
    """
    Strictly typed Series for managing floating-point data.

    This class enforces:
    - Data of type Float32.
    - Index of type list[str], Index, or MultiIndex.

    **Methods**:
        >>> @property
        >>> def names(self) -> list[str]:

        *Returns the index of the Series as a list of strings.*

        >>> @property
        >>> def nparray(
        ...     self, 
        ...     dtype: DTypeLike = Float32, 
        ...     copy: bool = False, 
        ...     na_value: float = np.nan
        ... ) -> ArrayFloat:

        *Converts the Series to a NumPy array with specified dtype, copy, and NA value.*
    """
    def __init__(
        self, 
        data: ArrayFloat|Series, # type: ignore
        index: MultiIndex|Index|list[str]|None = None, # type: ignore
        dtype: type = Float32
        ) -> None:
        if isinstance(data, Series):
            data = data.astype(dtype=Float32) # type: ignore
        else:
            if not isinstance(index, (Index, MultiIndex, list)):
                raise TypeError("index must be a a pandas {Index}, {MultiIndex}, or a {list} of strings")

        super().__init__(data=data, index=index, dtype=dtype) # type: ignore

    @property
    def names(self) -> list[str]: # type: ignore
        return super().index # type: ignore

    @property
    def nparray(
        self, 
        dtype: DTypeLike = Float32, 
        copy: bool = False, 
        na_value: float = np.nan
        ) -> ArrayFloat:
        array: ArrayFloat = super().to_numpy(dtype=dtype, copy=copy, na_value=na_value) # type: ignore
        return array

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

        >>> @property
        >>> def nparray(
        ...     self,
        ...     dtype: DTypeLike = Float32,
        ...     copy: bool = False,
        ...     na_value: float = np.nan,
        ... ) -> ArrayFloat:

        *Converts the DataFrame to a NumPy array with specified dtype, copy, and NA value.*
    """
    def __init__(
        self, 
        data: ArrayFloat|DataFrame,
        index: DatetimeIndex|None = None,
        columns: list[str]|MultiIndex|Index|None = None, # type: ignore
        dtype: type=Float32,
        ) -> None:
        if isinstance(data, DataFrame):
            data = data.astype(dtype=Float32) # type: ignore
        else:
            if not isinstance(index, (DatetimeIndex)):
                raise TypeError("index must be a pandas {DatetimeIndex}")

        super().__init__(data=data, index=index, columns=columns, dtype=dtype) # type: ignore

    @property
    def dates(self) -> DatetimeIndex:
        return super().index # type: ignore

    @property
    def nparray(
        self, 
        dtype: DTypeLike = Float32, 
        copy: bool = False, 
        na_value: float = np.nan
        ) -> ArrayFloat:
        array: ArrayFloat = super().to_numpy(dtype=dtype, copy=copy, na_value=na_value) # type: ignore
        return array