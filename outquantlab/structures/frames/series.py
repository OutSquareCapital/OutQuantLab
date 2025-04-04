from typing import TypedDict

from pandas import Series

import outquantlab.structures.arrays as arrays


class SeriesDict(TypedDict):
    data: list[float]
    index: list[str]


class SeriesFloat(Series):  # type: ignore
    def __init__(
        self,
        data: arrays.Float2D | list[float],
        index: list[str],
    ) -> None:
        super().__init__(data=data, index=index, dtype=arrays.Float32)  # type: ignore

    def get_array(self) -> arrays.Float2D:
        return self.to_numpy(dtype=arrays.Float32, copy=False, na_value=arrays.Nan)  # type: ignore

    def get_names(self) -> list[str]:
        return self.index.tolist()  # type: ignore

    def sort_data(self, ascending: bool) -> "SeriesFloat":
        data_array: arrays.Float2D = self.get_array()
        sorted_indices: arrays.Int2D = arrays.get_sorted_indices(
            array=data_array, ascending=ascending
        )
        sorted_array: arrays.Float2D = data_array[sorted_indices]
        sorted_index: list[str] = [self.get_names()[i] for i in sorted_indices]
        return SeriesFloat(data=sorted_array, index=sorted_index)

    @classmethod
    def from_pandas(cls, data: Series) -> "SeriesFloat":  # type: ignore
        return cls(
            data=data.to_numpy(dtype=arrays.Float32, copy=False, na_value=arrays.Nan),  # type: ignore
            index=data.index,  # type: ignore
        )

    @classmethod
    def from_array_list(
        cls, data: list[arrays.Float2D], index: list[str]
    ) -> "SeriesFloat":
        return cls(data=arrays.combine(arrays_list=data), index=index)

    def convert_to_json(self) -> SeriesDict:
        data: list[float] = self.get_array().tolist()
        index: list[str] = self.get_names()
        return SeriesDict(data=data, index=index)
