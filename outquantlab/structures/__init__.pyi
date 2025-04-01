"""**OutQuantLab Structures Package**

This package provides type definitions and specialized classes for performing numerical computations with strict type safety, specifically designed for quantitative financial applications.

---

**Package Organization**

**1. Type Aliases**
- `Float32` : Represents the NumPy `float32` type for single-precision floating-point numbers.
- `Int32`   : Represents the NumPy `int32` type for 32-bit integers.
- `ArrayFloat` : NumPy array specialized in storing `Float32` values.
- `ArrayInt`   : NumPy array specialized in storing `Int32` values.

**2. Custom Classes**
- `SeriesDict` : General purpose type for representing a financial series in JSON format.
- `DataFrameDict` : General purpose type for representing a financial DataFrame in JSON format.
- `SeriesFloat` : General purpose subclass of pandas Series for storing `float32` data. Attributes include the numeric data and index. The initializer sets up the series with type safety.
- `DataFrameFloat` : General purpose subclass of pandas DataFrame for handling time-series financial data in `float32`. Attributes include data, index, and columns. The initializer ensures data is stored with strict float type.

---

"""

from typing import TypeAlias, TypedDict

from numpy import float32, int32
from numpy.typing import NDArray
from pandas import DataFrame, DatetimeIndex, Index, MultiIndex, Series

Float32: TypeAlias = float32
"""**Description**: Represents the NumPy `float32` type for single-precision floating-point numbers.

**Example**:
```python
val: Float32 = 3.14
```"""

Int32: TypeAlias = int32
"""**Description**: Represents the NumPy `int32` type for 32-bit integers.

**Example**:
```python
number: Int32 = 42
```"""

ArrayFloat: TypeAlias = NDArray[Float32]
"""**Description**: NumPy array specialized in storing `Float32` values.

**Example**:
```python
import numpy as np
arr: ArrayFloat = np.array([1.0, 2.0, 3.0], dtype=float32)
```"""

ArrayInt: TypeAlias = NDArray[Int32]
"""**Description**: NumPy array specialized in storing `Int32` values.

**Example**:
```python
import numpy as np
arr_int: ArrayInt = np.array([1, 2, 3], dtype=int32)
```"""

class SeriesDict(TypedDict):
    """**SeriesDict**

    General purpose type for representing a financial series in JSON format.

    Attributes:
        `data` (`list[float]`): List of numeric values.
        `index` (`list[str]`): Labels corresponding to each data point.

    Initialization follows standard TypedDict usage.

    **Example**:
    ```python
    series: SeriesDict = {"data": [1.0, 2.5, 3.7], "index": ["A", "B", "C"]}
    ```"""

    data: list[float]
    index: list[str]

class DataFrameDict(TypedDict):
    """**DataFrameDict**

    General purpose type for representing a financial DataFrame in JSON format.

    Attributes:
        `data` (`list[list[float]]`): 2D list of numeric values.
        `index` (`list[str]`): Row labels.
        `columns` (`list[str]`): Column names.

    Initialization follows standard TypedDict usage.

    **Example**:
    ```python
    df: DataFrameDict = {"data": [[1.0, 2.0], [3.0, 4.0]], "index": ["Row1", "Row2"], "columns": ["A", "B"]}
    ```"""

    data: list[list[float]]
    index: list[str]
    columns: list[str]

class SeriesFloat(Series):  # type: ignore
    """**SeriesFloat**

    General purpose subclass of pandas Series for storing `float32` data with extended functionalities.

    **Attributes**:
    - ``data`` (`ArrayFloat | Series | list[float]`): The numeric data stored in `float32` format.
    - ``index`` (`MultiIndex | Index | list[str] | None`): Labels associated with the data.

    **Initialization**:
    The constructor ensures that the input data is stored as `float32`, enforcing strict type safety.
    Use the provided class methods ``from_float_list`` or ``from_array_list`` for creating instances when not using an existing Series, DataFrame, or Array.

    **Methods**:
    - ``get_array``: Returns the underlying NumPy array.
    - ``get_names``: Retrieves the index labels.
    - ``sort_data``: Returns a new ``SeriesFloat`` sorted in ascending or descending order.
    - ``from_float_list``: Creates an instance from a list of floats.
    - ``from_array_list``: Creates an instance from a list of NumPy arrays.
    - ``convert_to_json``: Exports the series as a JSON-compatible dictionary.
    """
    def __init__(
        self,
        data: ArrayFloat | Series | list[float],  # type: ignore
        index: list[str] | None = None,
    ) -> None: ...
    def get_array(self) -> ArrayFloat:
        """Return the underlying NumPy array of the series."""
        ...
    def get_names(self) -> list[str]:
        """Return the list of index labels."""
        ...
    def sort_data(self, ascending: bool) -> "SeriesFloat":
        """Return a new SeriesFloat sorted in ascending or descending order."""
        ...
    @classmethod
    def from_float_list(cls, data: list[float], index: list[str]) -> "SeriesFloat":
        """Create an instance from a list of floats and corresponding index."""
        ...
    @classmethod
    def from_array_list(cls, data: list[ArrayFloat], index: list[str]) -> "SeriesFloat":
        """Create an instance by combining a list of NumPy arrays with an index."""
        ...
    def convert_to_json(self) -> SeriesDict:
        """Export the series as a JSON-compatible dictionary."""
        ...

class DataFrameFloat(DataFrame):
    """**DataFrameFloat**

    General purpose subclass of pandas DataFrame optimized for handling time-series financial data in `float32`.

    **Attributes**:
    - ``data`` (`ArrayFloat | DataFrame | None`): The primary container of numeric data in `float32`.
    - ``index`` (`DatetimeIndex | None`): Temporal index used for time-series representation.
    - ``columns`` (`list[str] | MultiIndex | Index | None`): Column labels of the DataFrame.

    **Initialization**:
    The constructor initializes the DataFrame ensuring that all numeric data is stored as `float32`
    for consistency and performance in quantitative financial analysis.

    **Methods**:
    - ``dates``: Property to access the temporal index.
    - ``get_array``: Returns the underlying NumPy array representation.
    - ``get_names``: Retrieves the column names, correctly handling single and multi-index formats.
    - ``sort_data``: Returns a new DataFrameFloat with columns sorted based on the mean of their values.
    - ``convert_to_json``: Exports the DataFrame as a JSON-compatible dictionary.
    """
    def __init__(
        self,
        data: ArrayFloat | DataFrame | None = None,
        index: DatetimeIndex | None = None,
        columns: list[str] | MultiIndex | Index | None = None,  # type: ignore
    ) -> None: ...
    @property
    def dates(self) -> DatetimeIndex:
        """Access and return the temporal index of the DataFrame."""
        ...
    def get_array(self) -> ArrayFloat:
        """Return the underlying NumPy array of the DataFrame."""
        ...
    def get_names(self) -> list[str]:
        """Retrieve the column names."""
        ...
    def sort_data(self, ascending: bool) -> "DataFrameFloat":
        """Return a new DataFrameFloat with columns sorted by their mean values."""
        ...
    def clean_nans(self) -> None:
        """Remove NaN values from the DataFrame. This method modifies the DataFrame in place."""
        ...
    def convert_to_json(self) -> DataFrameDict:
        """Export the DataFrame as a JSON-compatible dictionary."""
        ...

__all__: list[str] = [
    "Float32",
    "Int32",
    "ArrayFloat",
    "ArrayInt",
    "SeriesFloat",
    "DataFrameFloat",
    "DataFrameDict",
    "SeriesDict",
]
