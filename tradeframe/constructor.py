from abc import ABC
from typing import Self, Any
import polars as pl


class _Token:
    __slots__: tuple[()] = ()
    pass

class TradeFrameConstructor(ABC):
    _internal_token = _Token()

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        _token: Any | None = kwargs.get('_token', None)
        if _token is not cls._internal_token:
            raise RuntimeError("Use a class method to instantiate")

        return super().__new__(cls)

    
    def __init__(self, data: pl.DataFrame, _token: _Token | None= None) -> None:
        self._data: pl.DataFrame = data

    def __repr__(self) -> str:
        return f"{self._data}"

    @classmethod
    def _construct(cls, data: pl.DataFrame) -> Self:
        return cls(data, _token=cls._internal_token)