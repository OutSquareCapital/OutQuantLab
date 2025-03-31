from typing import NamedTuple
import outquantlab.metrics as mt
from dataclasses import dataclass, field
from outquantlab.stats.processors import (
    AggregateProcessor,
    RollingProcessor,
    SamplingProcessor,
    TableProcessor,
    EquityProcessor
)


class AggregateProcessorsRegistery(NamedTuple):
    returns: AggregateProcessor
    sharpe_ratio: AggregateProcessor
    volatility: AggregateProcessor
    drawdown: AggregateProcessor
    skewness: AggregateProcessor


class RollingProcessorsRegistery(NamedTuple):
    sharpe_ratio: RollingProcessor
    volatility: RollingProcessor
    drawdown: RollingProcessor
    skewness: RollingProcessor


@dataclass(slots=True)
class Stats:
    overall: AggregateProcessorsRegistery = field(init=False)
    rolling: RollingProcessorsRegistery = field(init=False)
    distribution: SamplingProcessor = field(init=False)
    correlation: TableProcessor = field(init=False)
    equity: EquityProcessor = field(init=False)

    def __post_init__(self) -> None:
        self.overall = AggregateProcessorsRegistery(
            returns=AggregateProcessor(_func=mt.get_total_returns),
            sharpe_ratio=AggregateProcessor(_func=mt.get_overall_sharpe_ratio),
            volatility=AggregateProcessor(
                _func=mt.get_overall_volatility_annualized,
                _ascending=False,
            ),
            drawdown=AggregateProcessor(_func=mt.get_overall_average_drawdown),
            skewness=AggregateProcessor(
                _func=mt.get_overall_monthly_skewness, _ascending=False
            ),
        )
        self.rolling = RollingProcessorsRegistery(
            sharpe_ratio=RollingProcessor(
                _func=mt.get_rolling_sharpe_ratio, _ascending=False
            ),
            volatility=RollingProcessor(_func=mt.get_rolling_volatility_annualized),
            drawdown=RollingProcessor(_func=mt.get_rolling_drawdown),
            skewness=RollingProcessor(_func=mt.get_rolling_skewness, _ascending=False),
        )
        self.distribution = SamplingProcessor(
            _func=mt.get_returns_distribution, _ascending=False
        )
        self.correlation = TableProcessor(
            _func=mt.get_filled_correlation_matrix, _ascending=False
        )
        self.equity = EquityProcessor(
            _func=mt.get_equity_curves, _ascending=True
        )
