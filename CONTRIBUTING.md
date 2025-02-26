# Contributing to the Project

Welcome to this project! This guide outlines the conventions to follow to maintain code consistency and ensure seamless integration of contributions.

---

## 📌 General Principles

1. **Preferred Paradigm**: Functional programming (FP) is the default. Functions should be pure whenever possible.
2. **Data Structures**:  
   - If a data structure repeats, use a dataclass with `slots=True` but **without methods** (it serves as a struct).
   - A class **with both attributes and methods** should only be used if maintaining an internal state is necessary.
3. **Strict Type Annotations**:  
   - **All** variables, function arguments, and return types must be explicitly typed.
   - Type aliases (`TypeAlias`) must be used where appropriate.
   - Type hints must align with the project's `custom_types.py` and `custom_classes.py` standards.
   - Deprecated typing module (List instead of list for example) must NOT be used
4. **Linting and Formatting**:  
   - **Ruff** is used for linting and import formatting.
   - **Pylance** must run in strict mode.
   - All inlay hints must be enabled.
5. **Code Style**:  
   - Use `pyproject.toml` for formatting rules.
   - Follow `black`'s default line length (88 characters).
   - Avoid unnecessary one-liners for better readability.
6. **Imports**:  
   - Group imports: standard library first, third-party libraries next, then project-specific modules.
   - Use explicit imports whenever possible.

---

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

### 2. Using Dataclasses and Enums as Structs

If a data structure with variables is required (to better handle related variables when passing them as arguments for example), use a dataclass with no methods:

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Measurement:
    timestamp: str
    value: Float32
```

If methods and state management are necessary, justify the use of a "regular" class.
A convenient API is a justification. But by default, if a method is private, it should be outside of the class, unless there's a whole lot of arguments to pass.
If the dataclass contain constants that are computed during execution AND there's no method, use a NamedTuple.
If there's a method, use a frozen dataclass.
If there's no method and the constants values are hardcoded, use an Enum.

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
This allow  IDE to warn you if a function is not used, and facilitate the __init__.py files when setting up a package, since you will only import the public funcs into it. 
Same logic applies with private methods, altough as already said into point 2, it shouldn't happen often.
By definition, there's no private class or const, it will be public for the package.
The public scope of a package will be handled with the init file, like this:
```python
from module import public_func
 __all__: list[str] = [
    'public_func'
]
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