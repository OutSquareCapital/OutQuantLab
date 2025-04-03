# Contributing to the Project

Welcome to this project! This guide outlines the conventions to follow to maintain code consistency and ensure seamless integration of contributions.

## ✅ Writing Code

### Python Native libraries

Always use Python 3.10+ native type syntax:

````python

def process(items: list[str]) -> dict[str, int]:
````

Not:

````python

from typing import List, Dict
def process(items: List[str]) -> Dict[str, int]:
````

#### Type Aliases

Use simple assignment syntax:

````python

type Matrix = list[list[float]]
````

Not:

````python

from typing import TypeAlias
Matrix: TypeAlias = list[list[float]]
````

#### Modern generics

Use modern class generics:

````python

class Container[T]:
def __init__(self, value: T):
    self.value = T
````

Not:

````python

from typing import TypeVar, Generic
T = TypeVar('T')
class Container(Generic[T]):
...
````

#### Callables

Import from collections.abc:

````python

from collections.abc import Callable

Processor = Callable[[str, int], float]
````

Not:

````python

from typing import Callable
````

#### File Paths

Use pathlib exclusively:

````python

from pathlib import Path

config_path = Path('config') / 'settings.yaml'
````

Not:

````python

import os

config_path = os.path.join('config', 'settings.yaml')
````

### 1. Strict Typing for Robust Code

#### Core Philosophy

Python's type system exists to eliminate entire categories of bugs before runtime. Treat types as executable documentation - every annotation should make the code's intent clearer while enabling IDE autocompletion and static analysis.
Absolute Requirements

Total Coverage: Every variable, argument, and return value must have a type annotation.

No Any Escapes: The Any type is banned except in one narrowly defined case (see Abstract Methods section).

#### Type Annotation Deep Dive

##### Primitive Types

Always use the most specific type possible:

```python

def calculate_tax(income: float, years: int) -> float:
...

```

##### Collections

Precise collection types prevent mixed-type errors:

```python

def process_employees(employees: list[Employee], departments: set[str]) -> dict[str, Employee]:
...

Callbacks
Fully specify callback signatures:
```

```python

from collections.abc import Callable

PriceAdjuster = Callable[[float, int], float]

def apply_discount(price: float, adjuster: PriceAdjuster) -> float:
return adjuster(price, 10)
```

##### Generics

Modern generic classes with bounds:

```python

class Animal(ABC): ...

class Dog(Animal): ...
class Cat(Animal): ...

class Kennel[T: (Dog, Cat)]:  # Only accepts Dog or Cat types
def __init__(self, pet: T):
self.pet = pet
```

##### Abstract Base Classes

When using ABCs with potentially variable arguments:

```python

class DataParser(ABC):
@abstractmethod
def parse(self, *args: Any) -> DataFrame:  # Any permitted ONLY here
pass

class CSVParser(DataParser):
def parse(self, filepath: str, delimiter: str = ",") -> DataFrame:
...
```

Key points about ABCs:

Method returns must ALWAYS be concrete, even if arguments use Any

Prefer type bounds when possible:

```python

class Storage[T: (str, bytes)](ABC):
@abstractmethod
def save(self, data: T) -> bool:
...
```

#### Why We Ban Most Flexibility

The Any Problem

```python

def process(data: Any) -> Any:  # BANNED - provides zero type safety
...

String Type Pitfalls
```

```python

def create() -> "Employee":  # BANNED - breaks static analysis
...
```

Legacy Typing Issues

```python

from typing import List, Dict  # BANNED - deprecated syntax
```

#### Real-World Examples

Good Practice

```python

class Vehicle[T]:
def __init__(self, model: T):
self.model = T

def get_specs(self) -> dict[str, T]:
...

class ElectricVehicle(Vehicle[str]):
...
```

Anti-Patterns

```python

class OldStyle:  # Missing generics
def store(self, item):  # Missing type
...

def old_callback(func):  # No Callable typing
...
```

#### Performance Considerations

Modern type hints:

Have zero runtime overhead

Actually improve performance in IDEs (faster autocomplete)

Reduce debugging time by catching errors during development

Debugging Aid

Proper typing turns this runtime error:

```python

TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Into this development-time error:

```python

error: Argument 1 to "calculate" has incompatible type "str"; expected "int"
```

#### Maintenance Benefits

A fully typed codebase:

Documents itself through types

Enables reliable refactoring

Makes onboarding faster (types show intent)

Catches mistakes during code review

### 2. Data Structures: Typed and Structured Data Handling 🏗️

Use typed data structures to enforce strict typing, improve IDE autocompletion, and ensure clean code organization. Always prefer these over raw dictionaries, tuples, or lists when the structure’s members (keys/fields) are known in advance.

#### Enums and StrEnums (Immutable, Predefined, Pure Data)

Use these for fixed sets of named constants where both keys and values are known at development time. Ideal for categories, states, or configurations.

Example:

```python

from enum import Enum  

class Status(Enum):  
ACTIVE = "active"  
INACTIVE = "inactive"  
```

Why: Self-documenting, type-safe, and memory-efficient.

When: Hardcoded values with no behavior.

#### NamedTuples (Immutable, Computed, Pure Data)

Use for lightweight, immutable groupings of related variables when methods aren’t needed. Faster attribute access than dictionaries but slower than dataclasses.

Example:

```python

from typing import NamedTuple  

class Coordinates(NamedTuple):  
x: float  
y: float  
```

Why: Immutable, memory-efficient, and clear intent.

When: Variables are logically related (e.g., function returns or configuration bundles).

#### Frozen Dataclasses (Immutable, Computed, Mostly Data)

Use when you need immutability with minor behavior (e.g., a method or __post_init__). Combines data integrity with minimal logic.

Example:

```python

from dataclasses import dataclass  

@dataclass(frozen=True, slots=True)  
class ImmutableConfig:  
rate: float  
scale: int = 10  

def describe(self) -> str:  
return f"Rate: {self.rate}, Scale: {self.scale}"  
```

Why: Immutability + methods without state changes.

When: Data groups needing validation or simple derived properties.

#### Dataclasses (Mutable, Computed, Mostly Data)

Use for mutable data structures with optional methods. Always enable slots=True for faster attribute access.

Example:

```python

from dataclasses import dataclass  

@dataclass(slots=True)  
class Measurement:  
timestamp: str  
value: float  
```

Why: Clean separation of data and behavior; optimizes attribute access.

When: Mutable data with auxiliary methods (e.g., __post_init__).

#### Regular Classes (Mutable, Computed, Mostly Behavioral)

Use only when maintaining internal state or providing a complex API. Avoid "God objects"; split data and logic where possible.

Example:

```python

class Vehicle:  
def __init__(self, specs: CarSpecs, pilot: Pilot):  
self.specs = specs  # NamedTuple  
self.pilot = pilot  # NamedTuple  

def accelerate(self) -> None:  
...  
```

Why: Encapsulates closely related data and behavior.

When: Core logic depends on mutable state.

Key Principles

Group related data: Split large classes into smaller structures (e.g., Pilot + CarSpecs instead of a monolithic Car).

Immutability first: Default to frozen dataclasses or NamedTuples unless mutability is required.

Slots: Always use slots=True in dataclasses for performance.

Constants over variables: Prefer NamedTuple or Enum for invariants.

### 3. Handling DataFrames and Series

The project provides `DataFrameFloat` and `SeriesFloat` for strict typing. Use them instead of `pandas.DataFrame` or `pandas.Series` directly, when you know that you values will only contain floats.

```python
from custom_classes import DataFrameFloat, SeriesFloat

df: DataFrameFloat = DataFrameFloat(data=my_array, index=my_dates, columns=my_labels)
```

### 4. Scope

. Scope Control & Visibility Management
Private vs Public Convention

Functions/Methods:

Prefix with _ when only used within their module/class

Enables IDE unused code warnings

Clearly communicates intended scope

```python

def _internal_helper() -> None:  # Module-private
pass

class Processor:
def _cleanup(self) -> None:  # Class-private
pass

Constants/Classes:

Always public at module level

Control visibility via __all__ in __init__.py
```

Package Interface Control

Explicitly define public API in __init__.py:

```python

from .submodule import public_func, PublicClass
from .utils import config_loader

__all__: list[str] = [
'public_func',
'PublicClass',
'config_loader'
]
```

Import Conventions

Internal Project Packages:

Use consistent abbreviations for frequently used modules

Abbreviate based on clear, obvious patterns

```python


import outquantlab.metrics as mt
import outquantlab.data_processing as dp
```

External Packages:

Current standard (to be evaluated):

```python

from pandas import DataFrame
from numpy import ndarray, isnan

Potential future standard (requires team decision):

```

```python

import pandas as pd
import numpy as np
```

Special Cases:

Follow established community conventions:

```python

from numba import njit  # Community standard
import plotly.express as px  # Official recommendation
```

#### Rules of thumb

Consistency First:

Within a module, never mix import as and from import styles for the same package

Across project, maintain one style per external package

Readability Matters:

Prefer explicit imports (from pandas import DataFrame) when:

Only 1-2 items are needed

The type name is self-documenting

Use namespace imports (import pandas as pd) when:

Many items are used

The package has well-known abbreviations

Document Exceptions:

```python


# Special case: Following numba's official convention
from numba import njit, prange
```

Justification

Project Consistency: Internal abbreviations create predictable patterns

Maintainability: Explicit imports show dependencies clearly

Community Alignment: Reduces cognitive load when:

Onboarding new team members

Reading community code examples

Examples

Preferred:

```python

import outquantlab.visualization as viz  # Internal consistency
from pandas import DataFrame  # Current project standard
from plotly.graph_objects import Figure  # Explicit import
```

Requires Discussion!

Forbidden:

```python

from pandas import *  # Never acceptable
import DataFrame     # Undefined origin
```

Control Flow & String Handling
Conditional Statements: The Last Resort

Core Principle:

Treat if/else blocks as code smells in business logic

They violate the Open/Closed principle

Make testing more difficult (exponential branch combinations)

Preferred Alternatives:

1: Dictionary Dispatch (For behavioral variations):

```python

_PAYMENT_PROCESSORS = {
PaymentType.CREDIT: process_credit_payment,
PaymentType.CRYPTO: process_crypto_payment,
PaymentType.BANK: process_bank_transfer,
}

def process_payment(payment_type: PaymentType, amount: float) -> Receipt:
processor = _PAYMENT_PROCESSORS.get(payment_type)
if not processor:
raise UnsupportedPaymentError(payment_type)
return processor(amount)
```

2: Polymorphism (For complex behaviors):

```python

class Animal(ABC):
@abstractmethod
def speak(self) -> str: ...

class Dog(Animal):
def speak(self) -> str:
return "Woof!"

class Cat(Animal):
def speak(self) -> str:
return "Meow!"

def animal_farm(animals: list[Animal]) -> None:
for animal in animals:
print(animal.speak())  # No conditionals needed
```

3: State Pattern:

```python

class OrderState(ABC):
@abstractmethod
def next_state(self) -> OrderState: ...

class Pending(OrderState):
def next_state(self) -> OrderState:
return Processing()

class Processing(OrderState):
def next_state(self) -> OrderState:
return Shipped()
```

When to Use If/Else:

Only for trivial, non-business logic (e.g., input sanitation)

Never exceed 2-3 branches

Always include else clauses for exhaustiveness

The String Problem

Why Strings Are Dangerous:

No IDE autocompletion

No type safety

Enable hidden coupling

Make refactoring hazardous

String-Free Alternatives:

1: Enums (For fixed sets of values):

```python

class Color(Enum):
RED = auto()
BLUE = auto()
GREEN = auto()

def set_theme(color: Color) -> None:  # Not str!
...
```

2: Typed Constants (For magic values):

```python

MAX_RETRIES: Final[int] = 3
TIMEOUT: Final[float] = 30.0
```

3: Data Classes (For structured data):

```python

@dataclass
class Address:
street: str
city: str
zip_code: str  # Still a string, but typed and bound to context

# Not: {"street": "...", "city": "..."}

```

Allowed String Uses:

Literal user-facing text

Serialization boundaries (JSON/YAML)

External system communication

With strict validation:

```python

def validate_zip_code(code: str) -> ZipCode:
if not re.match(r"\d{5}", code):
raise InvalidZipCodeError
return ZipCode(code)
```

Real-World Impact

Before (Dangerous):

```python

def handle_response(response_type: str):  # What strings are valid?
if response_type == "ok":
...
elif response_type == "error":
...
# Forgotten case: "partial_success"
```

After (Robust):

```python

class ResponseType(Enum):
OK = auto()
ERROR = auto()
PARTIAL_SUCCESS = auto()

def handle_response(response: ResponseType):  # All cases visible in IDE
...
```

Performance Notes

Enum checks are faster than string comparisons

Dictionary lookups outperform long if/else chains

Polymorphic calls are optimized by Python's method cache

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
```...    : bool = False,
...     na_value: float = np.nan
... ) -> arrays.Float2D:

*Converts the Series to a NumPy array with specified dtype```,, and NA value.*
"""
```

---
