from outquantlab.stats.stats_processors import StatsSeries, StatsDF
from outquantlab.typing_conventions import DataFrameFloat
import outquantlab.metrics as mt

def get_portfolio_curves(returns_df: DataFrameFloat, length: int) -> StatsDF:
    return StatsDF(
        data=returns_df,
        func=mt.get_equity_curves,
        ascending=True,
        length=length,
    )

def get_total_returns(returns_df: DataFrameFloat) -> StatsSeries:
    return StatsSeries(
        data=returns_df,
        func=mt.get_overall_sharpe_ratio,
        ascending=True,
    )