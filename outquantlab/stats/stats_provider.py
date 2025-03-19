import outquantlab.metrics as mt
from outquantlab.stats.stats_processors import (
    StatsCurves,
    StatsBars,
    StatsOverall,
    StatsDistribution,
    StatsHeatMap,
)
from outquantlab.typing_conventions import DataFrameFloat


class StatsProvider:
    @staticmethod
    def process_correlation_matrix(returns_df: DataFrameFloat) -> StatsHeatMap:
        return StatsHeatMap(
            data=returns_df,
            func=mt.get_filled_correlation_matrix,
        )

    @staticmethod
    def process_stats_equity(returns_df: DataFrameFloat, length: int) -> StatsCurves:
        return StatsCurves(
            data=returns_df,
            func=mt.get_equity_curves,
            ascending=True,
            length=length,
        )

    @staticmethod
    def process_rolling_volatility(
        returns_df: DataFrameFloat, length: int
    ) -> StatsCurves:
        return StatsCurves(
            data=returns_df,
            func=mt.get_rolling_volatility,
            ascending=False,
            length=length,
        )

    @staticmethod
    def process_rolling_drawdown(
        returns_df: DataFrameFloat, length: int
    ) -> StatsCurves:
        return StatsCurves(
            data=returns_df,
            func=mt.get_rolling_drawdown,
            ascending=False,
            length=length,
        )

    @staticmethod
    def process_rolling_sharpe_ratio(
        returns_df: DataFrameFloat, length: int
    ) -> StatsCurves:
        return StatsCurves(
            data=returns_df,
            func=mt.rolling_sharpe_ratio,
            ascending=True,
            length=length,
        )

    @staticmethod
    def process_rolling_smoothed_skewness(
        returns_df: DataFrameFloat, length: int
    ) -> StatsCurves:
        return StatsCurves(
            data=returns_df,
            func=mt.rolling_skewness,
            ascending=True,
            length=length,
        )

    @staticmethod
    def process_stats_distribution(
        returns_df: DataFrameFloat, frequency: int
    ) -> StatsDistribution:
        return StatsDistribution(
            data=returns_df,
            func=mt.get_returns_distribution,
            ascending=True,
            frequency=frequency,
        )

    @staticmethod
    def process_overall_returns(returns_df: DataFrameFloat) -> StatsBars:
        return StatsBars(
            data=returns_df,
            func=mt.get_total_returns,
            ascending=True,
        )

    @staticmethod
    def process_overall_sharpe_ratio(returns_df: DataFrameFloat) -> StatsBars:
        return StatsBars(
            data=returns_df,
            func=mt.get_overall_sharpe_ratio,
            ascending=True,
        )

    @staticmethod
    def process_overall_volatility(returns_df: DataFrameFloat) -> StatsBars:
        return StatsBars(
            data=returns_df,
            func=mt.get_overall_volatility_annualized,
            ascending=False,
        )

    @staticmethod
    def process_overall_average_drawdown(returns_df: DataFrameFloat) -> StatsBars:
        return StatsBars(
            data=returns_df,
            func=mt.get_overall_average_drawdown,
            ascending=False,
        )

    @staticmethod
    def process_overall_average_correlation(returns_df: DataFrameFloat) -> StatsBars:
        return StatsBars(
            data=returns_df,
            func=mt.get_overall_average_correlation,
            ascending=False,
        )

    @staticmethod
    def process_overall_monthly_skew(returns_df: DataFrameFloat) -> StatsBars:
        return StatsBars(
            data=returns_df,
            func=mt.get_overall_monthly_skewness,
            ascending=True,
        )

    @staticmethod
    def process_overall_stats(returns_df: DataFrameFloat) -> StatsOverall:
        return StatsOverall(
            data=returns_df,
            overall_metrics=[
                mt.get_total_returns,
                mt.get_overall_sharpe_ratio,
                mt.get_max_drawdown,
                mt.get_overall_volatility_annualized,
            ],
        )
