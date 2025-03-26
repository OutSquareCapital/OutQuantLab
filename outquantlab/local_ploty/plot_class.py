from typing import NamedTuple
import outquantlab.metrics as mt
from dataclasses import dataclass, field
from outquantlab.local_ploty.stats import (
    AggregateStat,
    RollingStat,
    SamplingStat,
    TableStat,
)


class OverallStatsRegistery(NamedTuple):
    returns: AggregateStat
    sharpe_ratio: AggregateStat
    volatility: AggregateStat
    drawdown: AggregateStat
    skewness: AggregateStat


class RollingStatsRegistery(NamedTuple):
    sharpe_ratio: RollingStat
    volatility: RollingStat
    drawdown: RollingStat
    skewness: RollingStat


@dataclass(slots=True)
class Stats:
    overall: OverallStatsRegistery = field(init=False)
    rolling: RollingStatsRegistery = field(init=False)
    distribution: SamplingStat = field(init=False)
    correlation: TableStat = field(init=False)

    def __post_init__(self) -> None:
        self.overall = OverallStatsRegistery(
            returns=AggregateStat(_func=mt.get_total_returns),
            sharpe_ratio=AggregateStat(_func=mt.get_overall_sharpe_ratio),
            volatility=AggregateStat(
                _func=mt.get_overall_volatility_annualized,
                _ascending=False,
            ),
            drawdown=AggregateStat(_func=mt.get_overall_average_drawdown),
            skewness=AggregateStat(
                _func=mt.get_overall_monthly_skewness, _ascending=False
            ),
        )
        self.rolling = RollingStatsRegistery(
            sharpe_ratio=RollingStat(
                _func=mt.get_rolling_sharpe_ratio, _ascending=False
            ),
            volatility=RollingStat(_func=mt.get_rolling_volatility),
            drawdown=RollingStat(_func=mt.get_rolling_drawdown),
            skewness=RollingStat(_func=mt.get_rolling_skewness, _ascending=False),
        )
        self.distribution = SamplingStat(
            _func=mt.get_returns_distribution, _ascending=False
        )
        self.correlation = TableStat(
            _func=mt.get_filled_correlation_matrix, _ascending=False
        )
