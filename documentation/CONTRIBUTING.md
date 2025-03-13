# Contributing to the Project

Welcome to this project! This guide outlines the conventions to follow to maintain code consistency and ensure seamless integration of contributions.

## ✅ Writing Code

### 1. Functions and Typing

- Always declare types explicitly:

```python
def compute_average(values: ArrayFloat) -> Float32:
    return np.mean(values, dtype=Float32)
```

- Use the predefined type aliases from `custom_types.py`:

```python
def process_data(data: ArrayFloat) -> ArrayFloat:
    return data * 1.5
```

### 2. Data Structures 🏗️

-**Dataclasses**: Use dataclasses (without methods) when you need a simple data structure to hold related variables. 🧱

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Measurement:
    timestamp: str
    value: Float32
```

- **Regular Classes**: Use a class with both attributes and methods only when maintaining an internal state is necessary. A convenient public API can also justify the use of a class. 👨‍💻

    -If a method is private, consider placing it outside the class, especially if it doesn't rely heavily on the class's internal state, unless there's a significant number of arguments to pass, who are directly related to the class attributes. 📤

- **NamedTuples**: If your dataclass contains constants that are computed during execution and there are no methods, use a `NamedTuple`. 🧮

    ```python
    from typing import NamedTuple

    class Config(NamedTuple):
        RATE: float = compute_rate()  # Assuming compute_rate() is defined elsewhere
        SCALE: int = 10
    ```

- **Frozen Dataclasses**: If your dataclass contains constants that are computed during execution AND requires methods, use a frozen dataclass. ❄️

    ```python
    from dataclasses import dataclass, field

    @dataclass(frozen=True, slots=True)
    class ImmutableConfig:
        RATE: float = field(default_factory=compute_rate)
        SCALE: int = 10

        def description(self) -> str:
            return f"Rate: {self.RATE}, Scale: {self.SCALE}"
    ```

    -`frozen=True` makes the dataclass immutable after creation. 🧊
    -Use `field(default_factory=...)` for default values that are computed.

- **Enums**: If your data structure represents a set of named constants with hardcoded values AND no methods, use an `Enum`. 🚦

    ```python
    from enum import Enum

    class Status(Enum):
        ACTIVE = "active"
        INACTIVE = "inactive"
        PENDING = "pending"
    ```

    -Enums are great for representing a fixed set of options. 📊

### 3. Handling DataFrames and Series

The project provides `DataFrameFloat` and `SeriesFloat` for strict typing. Use them instead of `pandas.DataFrame` or `pandas.Series` directly, when you know that you values will only contain floats.

```python
from custom_classes import DataFrameFloat, SeriesFloat

df: DataFrameFloat = DataFrameFloat(data=my_array, index=my_dates, columns=my_labels)
```

### 4. Scope

If a function is used only into it's own module, precise it with an underscore:

```python
def _private_function_() -> None:
    pass
```

This allow  IDE to warn you if a function is not used, and facilitate the init.py files when setting up a package, since you will only import the public funcs into it.
Same logic applies with private methods, altough as already said into point 2, it shouldn't happen often.
By definition, there's no private class or const, it will be public for the package.
The public scope of a package will be handled with the init file, like this:

```python
from module import public_func
 __all__: list[str] = [
    'public_func'
]
```

### 5. if / else statements

Conditionnal statements must be used sparsely. Dictionary are preferred when handling different behavioral possiblities:
```python
_HANDLER_REGISTRY = {
    Extension.JSON.value: JSONHandler,
    Extension.PARQUET.value: ParquetHandler,
}


def _create_handler(ext: str) -> FileHandler:
    handler_class = _HANDLER_REGISTRY.get(ext)
    if handler_class is None:
        raise ValueError(f"Unsupported extension: {ext}")
    return handler_class()


@dataclass(frozen=True, slots=True)
class DataFile:
    ext: str
    path: str
    handler: FileHandler = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "handler", _create_handler(self.ext))

```

---

## 📝 Documentation

Use Markdown (`.md`) for general documentation.

Do not write '#' comments.
Also, no docstrings, unless it's in the typing_conventions.

For those, write them in Google-style format:

```python
class SeriesFloat(Series):
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

```

---
