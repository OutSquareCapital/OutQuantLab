import outquantlab.metrics as mt
from outquantlab.stats.stats_processors import StatsDF, StatsSeries
from outquantlab.typing_conventions import DataFrameFloat


class StatsProvider:
    @staticmethod
    def get_portfolio_curves(returns_df: DataFrameFloat, length: int) -> StatsDF:
        return StatsDF(
            data=returns_df,
            func=mt.get_equity_curves,
            ascending=True,
            length=length,
        )

    @staticmethod
    def get_assets_sharpes(returns_df: DataFrameFloat) -> StatsSeries:
        return StatsSeries(
            data=returns_df,
            func=mt.get_overall_sharpe_ratio,
            ascending=True,
        )
