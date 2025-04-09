from dataclasses import dataclass, field
from typing import NamedTuple

import outquantlab.metrics as mt
from outquantlab.stats.processors import (
    AggregateProcessor,
    EquityProcessor,
    RollingProcessor,
    SamplingProcessor,
    TableProcessor,
)


class AggregateProcessorsRegistery(NamedTuple):
    returns = AggregateProcessor(_func=mt.get_total_returns)
    sharpe_ratio = AggregateProcessor(_func=mt.get_overall_sharpe_ratio)
    volatility = AggregateProcessor(
        _func=mt.get_overall_volatility_annualized,
        _ascending=False,
    )
    drawdown = AggregateProcessor(_func=mt.get_overall_average_drawdown)
    skewness = AggregateProcessor(
        _func=mt.get_overall_monthly_skewness, _ascending=False
    )


class RollingProcessorsRegistery(NamedTuple):
    sharpe_ratio = RollingProcessor(_func=mt.get_rolling_sharpe_ratio, _ascending=False)
    volatility = RollingProcessor(_func=mt.get_rolling_volatility_annualized)
    drawdown = RollingProcessor(_func=mt.get_rolling_drawdown)
    skewness = RollingProcessor(_func=mt.get_rolling_skewness, _ascending=False)


@dataclass(slots=True)
class Stats:
    overall: AggregateProcessorsRegistery = field(init=False)
    rolling: RollingProcessorsRegistery = field(init=False)
    distribution: SamplingProcessor = field(init=False)
    correlation: TableProcessor = field(init=False)
    equity: EquityProcessor = field(init=False)

    def __post_init__(self) -> None:
        self.overall = AggregateProcessorsRegistery()
        self.rolling = RollingProcessorsRegistery()
        self.distribution = SamplingProcessor(
            _func=mt.get_returns_distribution, _ascending=True
        )
        self.correlation = TableProcessor(
            _func=mt.get_filled_correlation_matrix, _ascending=False
        )
        self.equity = EquityProcessor(_func=mt.get_equity, _ascending=True)
