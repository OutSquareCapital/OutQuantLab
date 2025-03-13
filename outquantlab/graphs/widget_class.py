from abc import ABC, abstractmethod
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from collections.abc import Callable
from typing import TypeAlias
import plotly.graph_objects as go  # type: ignore

StatSerieInterface: TypeAlias = Callable[[DataFrameFloat], SeriesFloat]
StatDataFrameInterface: TypeAlias = Callable[[DataFrameFloat, int], DataFrameFloat]

SetupDF: TypeAlias = Callable[[DataFrameFloat, dict[str, str]], go.Figure]
SetupSeries: TypeAlias = Callable[[SeriesFloat, dict[str, str]], go.Figure]

SeriesWidget: TypeAlias = Callable[[SeriesFloat, str], go.Figure]
DataframeWidget: TypeAlias = Callable[[DataFrameFloat, str], go.Figure]


class GraphDF(ABC):
    
    @abstractmethod
    def compute_stats(self, data: DataFrameFloat, length: int) -> DataFrameFloat:
        pass

    @abstractmethod
    def setup_graph(self, data: DataFrameFloat, colors: dict[str, str]) -> go.Figure:
        pass

    
    @abstractmethod
    def format_plot(self, data: DataFrameFloat, title: str) -> go.Figure:
        pass
    
    @abstractmethod
    def plot(self, data: DataFrameFloat, length:int) -> go.Figure:
        self.compute_stats(data, length)

    @property
    def name(self) -> str:
        return self.__name__