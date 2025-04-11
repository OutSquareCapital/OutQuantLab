from typing import TypedDict

from pandas import Series

import numquant as nq


class SeriesDict(TypedDict):
    data: list[float]
    index: list[str]


class SeriesFloat(Series):  # type: ignore
    def __init__(
        self,
        data: nq.Float2D | list[float],
        index: list[str],
    ) -> None:
        super().__init__(data=data, index=index, dtype=nq.Float32)  # type: ignore

    def get_array(self) -> nq.Float2D:
        return self.to_numpy(dtype=nq.Float32, copy=False, na_value=nq.Nan)  # type: ignore

    def get_names(self) -> list[str]:
        return self.index.tolist()  # type: ignore

    def sort_data(self, ascending: bool) -> "SeriesFloat":
        data_array: nq.Float2D = self.get_array()
        sorted_indices: nq.Int2D = nq.arrays.get_sorted_indices(
            array=data_array, ascending=ascending
        )
        sorted_array: nq.Float2D = data_array[sorted_indices]
        sorted_index: list[str] = [self.get_names()[i] for i in sorted_indices]
        return SeriesFloat(data=sorted_array, index=sorted_index)

    def convert_to_json(self) -> SeriesDict:
        data: list[float] = self.get_array().tolist()
        index: list[str] = self.get_names()
        return SeriesDict(data=data, index=index)
