from numpy.typing import NDArray
import numpy as np
from collections.abc import Callable
from typing import Any, TypeAlias, Final
from pandas import DataFrame, DatetimeIndex, MultiIndex, Index, Series

ArrayFloat: TypeAlias = NDArray[np.float32]
ArrayInt: TypeAlias = NDArray[np.int32]
ProgressFunc: TypeAlias = Callable[[int, str], Any]
IndicatorFunc : TypeAlias = Callable[..., ArrayFloat]

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
    - Data of type np.float32
    - Index of type list[str] or Index[str]
    '''
    def __init__(
        self, 
        data: ArrayFloat|Series, # type: ignore
        index: Index|list[str]|None = None, # type: ignore
        dtype: type = np.float32
        ) -> None:
        if isinstance(data, Series):
            data = data.astype(np.float32) # type: ignore
        else:
            if not isinstance(index, (Index, list)):
                raise TypeError("index must be a {list} of strings or a pandas {Index}")
        super().__init__(data=data, index=index, dtype=dtype) # type: ignore

    @property
    def values(self) -> ArrayFloat: # type: ignore
        return super().values # type: ignore

    @classmethod
    def from_series(cls, series: Series) -> 'SeriesFloat': # type: ignore
        return cls(series.astype(np.float32), index=series.index) # type: ignore
    
    def round(self, decimals: int = 0, *args, **kwargs) -> 'SeriesFloat': # type: ignore
        rounded_series: Series = super().round(decimals, *args, **kwargs) # type: ignore
        return SeriesFloat.from_series(rounded_series) # type: ignore

class DataFrameFloat(DataFrame):
    '''
    Strictly typed Dataframe with:
    - Data of type np.float32
    - Index of type DatetimeIndex
    - Columns of type list[str] or MultiIndex
    '''
    def __init__(
        self, 
        data: ArrayFloat|DataFrame,
        index: DatetimeIndex|None = None,
        columns: list[str]|MultiIndex|Index|None = None, # type: ignore
        dtype: type=np.float32,
        ) -> None:
        if isinstance(data, DataFrame):
            data = data.astype(np.float32) # type: ignore
        else:
            if not isinstance(index, (DatetimeIndex)):
                raise TypeError("index must be a pandas {DatetimeIndex}")
            if not isinstance(columns, (list, MultiIndex, Index)):
                raise TypeError("columns must be a {list} of strings or a pandas {MultiIndex} or {Index}")
        
        super().__init__(data=data, index=index, columns=columns, dtype=dtype) # type: ignore

    @property
    def values(self) -> ArrayFloat: # type: ignore
        return super().values # type: ignore

    @property
    def index(self) -> DatetimeIndex: # type: ignore
        return super().index # type: ignore

    @classmethod
    def from_dataframe(cls, df: DataFrame) -> 'DataFrameFloat':
        return cls(df.astype(np.float32), index=df.index, columns=df.columns) # type: ignore

    def round(self, decimals: int = 0, *args, **kwargs) -> 'DataFrameFloat': # type: ignore
        rounded_df = super().round(decimals, *args, **kwargs) # type: ignore
        return DataFrameFloat.from_dataframe(rounded_df)
