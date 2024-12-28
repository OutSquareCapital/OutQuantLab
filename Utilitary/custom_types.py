from numpy.typing import DTypeLike, NDArray
import numpy as np
from collections.abc import Callable
from typing import Any, TypeAlias, Final
from pandas import DataFrame, DatetimeIndex, MultiIndex, Index, Series

Float32: TypeAlias = np.float32
Int32: TypeAlias = np.int32
ArrayFloat: TypeAlias = NDArray[Float32]
ArrayInt: TypeAlias = NDArray[Int32]
ProgressFunc: TypeAlias = Callable[[int, str], None]
IndicatorFunc : TypeAlias = Callable[..., ArrayFloat]
DictVariableDepth: TypeAlias = dict[str, Any]

JsonData: TypeAlias = str
ParquetData: TypeAlias = str
WebpMedia: TypeAlias = str
PngMedia: TypeAlias = str
JSON_EXT: Final = ".json"
PARQUET_EXT: Final = ".parquet"
WEBP_EXT: Final = ".webp"
PNG_EXT: Final = ".png"

class SeriesFloat(Series): # type: ignore
    '''
    Strictly typed Series with:
    - Data of type Float32
    - Index of type list[str] or Index[str]
    '''
    def __init__(
        self, 
        data: ArrayFloat|Series, # type: ignore
        index: Index[str]|list[str]|None = None,
        dtype: type = Float32
        ) -> None:
        if isinstance(data, Series):
            data = data.astype(Float32) # type: ignore
        else:
            if not isinstance(index, (Index, list)):
                raise TypeError("index must be a {list} of strings or a pandas {Index}")
        super().__init__(data=data, index=index, dtype=dtype) # type: ignore

    @property
    def names(self) -> Index[str]:
        return super().index # type: ignore
    @property
    def data(self) -> ArrayFloat:
        return super().values # type: ignore

    @property
    def nparray(
        self, 
        dtype: DTypeLike = Float32, 
        copy: bool = False, 
        na_value: float = np.nan
        ) -> ArrayFloat:
        """override to_numpy method to strictly return Float32 array"""
        array: ArrayFloat = super().to_numpy(dtype=dtype, copy=copy, na_value=na_value) # type: ignore
        return array

class DataFrameFloat(DataFrame):
    '''
    Strictly typed Dataframe with:
    - Data of type Float32
    - Index of type DatetimeIndex
    - Columns of type list[str] or MultiIndex
    '''
    def __init__(
        self, 
        data: ArrayFloat|DataFrame,
        index: DatetimeIndex|None = None,
        columns: list[str]|MultiIndex|Index[str]|None = None,
        dtype: type=Float32,
        ) -> None:
        if isinstance(data, DataFrame):
            data = data.astype(Float32) # type: ignore
        else:
            if not isinstance(index, (DatetimeIndex)):
                raise TypeError("index must be a pandas {DatetimeIndex}")
            if not isinstance(columns, (list, MultiIndex, Index)):
                raise TypeError("columns must be a {list} of strings or a pandas {MultiIndex} or {Index}")
        
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
        """override to_numpy method to strictly return Float32 array"""
        array: ArrayFloat = super().to_numpy(dtype=dtype, copy=copy, na_value=na_value) # type: ignore
        return array