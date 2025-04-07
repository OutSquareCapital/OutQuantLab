from dataclasses import dataclass, field
from typing import NamedTuple

import outquantlab.metrics as mt
from outquantlab.apis import start_server
from outquantlab.stats.processors import (
    AggregateProcessor,
    EquityProcessor,
    RollingProcessor,
    SamplingProcessor,
    TableProcessor,
)
from outquantlab.structures import arrays, frames


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
        self.equity = EquityProcessor(_func=arrays.get_prices, _ascending=True)

    def send_results(self, results: frames.DatedFloat) -> None:
        self.rolling.sharpe_ratio.send_to_api(data=results, length=1250)
        self.overall.sharpe_ratio.send_to_api(data=results)
        self.distribution.send_to_api(data=results, frequency=20)
        start_server()
