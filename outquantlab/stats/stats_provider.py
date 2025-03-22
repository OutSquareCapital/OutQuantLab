from outquantlab.stats.metric_class import (
    CurvesMetric,
    BarsMetric,
    HistogramMetric,
    HeatMapMetric,
    OverallMetrics,
)
import outquantlab.metrics as mt

class StatsProvider:
    def __init__(self) -> None:
        self.overall_stats = OverallMetrics(
            overall_metrics=[
                mt.get_overall_sharpe_ratio,
                mt.get_overall_volatility_annualized,
                mt.get_overall_average_drawdown,
            ]
        )
        self.equity_curves = CurvesMetric(func=mt.get_equity_curves, ascending=True)
        self.rolling_sharpe_ratio = CurvesMetric(
            func=mt.get_rolling_sharpe_ratio, ascending=True
        )
        self.rolling_volatility = CurvesMetric(
            func=mt.get_rolling_volatility, ascending=False
        )
        self.rolling_drawdown = CurvesMetric(
            func=mt.get_rolling_drawdown, ascending=False
        )
        self.rolling_skewness = CurvesMetric(
            func=mt.get_rolling_skewness, ascending=True
        )
        self.returns_distribution = HistogramMetric(
            func=mt.get_returns_distribution, ascending=True
        )
        self.total_returns = BarsMetric(func=mt.get_total_returns, ascending=True)
        self.overall_sharpe = BarsMetric(
            func=mt.get_overall_sharpe_ratio, ascending=True
        )
        self.overall_volatility = BarsMetric(
            func=mt.get_overall_volatility_annualized, ascending=False
        )
        self.overall_skewness = BarsMetric(
            func=mt.get_overall_monthly_skewness, ascending=True
        )
        self.overall_drawdown = BarsMetric(
            func=mt.get_overall_average_drawdown, ascending=False
        )
        self.overall_correlation = BarsMetric(
            func=mt.get_overall_average_correlation, ascending=False
        )
        self.correlation_matrix = HeatMapMetric(
            func=mt.get_filled_correlation_matrix, ascending=False
        )