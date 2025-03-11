import outquantlab.metrics as mt
from outquantlab.stats.stats_interfaces import OverallMetricFunc
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat

metrics_func: list[OverallMetricFunc] = [
    mt.calculate_total_returns,
    mt.overall_sharpe_ratio,
    mt.calculate_max_drawdown,
    mt.overall_volatility_annualized,
]


def _format_metric_name(name: str) -> str:
    return name.replace("_", " ").title()


def get_metrics(returns_df: DataFrameFloat) -> SeriesFloat:
    array: ArrayFloat = returns_df.get_array()
    results: list[ArrayFloat] = [func(array) for func in metrics_func]
    names: list[str] = [
        _format_metric_name(name=func.__name__) for func in metrics_func
    ]
    results_list: list[float] = [result.item() for result in results]
    return SeriesFloat.from_float_list(data=results_list, index=names)
