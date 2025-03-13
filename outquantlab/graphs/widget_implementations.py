from outquantlab.graphs.widget_class import WidgetDataFrame
from outquantlab.typing_conventions import DataFrameFloat, ArrayFloat
from outquantlab.graphs.ui_constants import CustomHovers, Colors
from outquantlab.metrics import get_overall_max, get_overall_min
import plotly.graph_objects as go  # type: ignore


class Curves(WidgetDataFrame):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def setup_figure_type(self, data: DataFrameFloat, color_map: dict[str, str]) -> None:
        for column in data.get_names():
            self.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    x=data.dates,
                    y=data[column],
                    mode="lines",
                    name=column,
                    line=dict(width=2, color=color_map[column]),
                )
            )

class Violins(WidgetDataFrame):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def setup_figure_type(self, data: DataFrameFloat, color_map: dict[str, str]) -> None:
        for column in data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Violin(
                    y=data[column],
                    name=column,
                    box_visible=True,
                    points=False,
                    marker=_get_marker_config(color=color_map[column]),
                    box_line_color=Colors.WHITE,
                    hoveron="violins",
                    hoverinfo="y",
                )
            )

        min_by_column: ArrayFloat = get_overall_min(array=data.get_array())
        y_min: ArrayFloat = get_overall_min(array=min_by_column)

        max_by_column: ArrayFloat = get_overall_max(array=data.get_array())
        y_max: ArrayFloat = get_overall_max(array=max_by_column)

        self.figure.update_layout(  # type: ignore
            yaxis=dict(range=[y_min, y_max], showgrid=False),
            xaxis=dict(
                showticklabels=False,
            ),
        )

def _get_marker_config(color: str) -> dict[str, str | dict[str, Colors | int]]:
    return dict(color=color, line=dict(color=Colors.WHITE, width=1))
