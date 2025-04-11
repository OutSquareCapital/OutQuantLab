from dataclasses import dataclass, field
import numquant as nq
from outquantlab.stats.processors import (
    AggregateProcessor,
    EquityProcessor,
    RollingProcessor,
    SamplingProcessor,
    TableProcessor,
)

@dataclass(slots=True, frozen=True)
class AggregateProcessorsRegistery:
    returns = AggregateProcessor(_func=nq.metrics.agg.get_total_returns)
    sharpe_ratio = AggregateProcessor(_func=nq.metrics.agg.get_sharpe_ratio)
    volatility = AggregateProcessor(
        _func=nq.metrics.agg.get_volatility_annualized,
        _ascending=False,
    )
    drawdown = AggregateProcessor(_func=nq.metrics.agg.get_average_drawdown)
    skewness = AggregateProcessor(
        _func=nq.metrics.agg.get_monthly_skewness, _ascending=False
    )

@dataclass(slots=True, frozen=True)
class RollingProcessorsRegistery:
    sharpe_ratio = RollingProcessor(
        _func=nq.metrics.roll.get_sharpe_ratio, _ascending=False
    )
    volatility = RollingProcessor(_func=nq.metrics.roll.get_volatility_annualized)
    drawdown = RollingProcessor(_func=nq.metrics.roll.get_rolling_drawdown)
    skewness = RollingProcessor(_func=nq.metrics.roll.get_skewness, _ascending=False)


@dataclass(slots=True)
class Stats:
    overall: AggregateProcessorsRegistery = AggregateProcessorsRegistery()
    rolling: RollingProcessorsRegistery = RollingProcessorsRegistery()
    distribution: SamplingProcessor = field(init=False)
    correlation: TableProcessor = field(init=False)
    equity: EquityProcessor = field(init=False)

    def __post_init__(self) -> None:
        self.distribution = SamplingProcessor(
            _func=nq.metrics.roll.get_returns_distribution, _ascending=True
        )
        self.correlation = TableProcessor(
            _func=nq.metrics.agg.get_filled_correlation_matrix, _ascending=False
        )
        self.equity = EquityProcessor(_func=nq.metrics.roll.get_equity, _ascending=True)