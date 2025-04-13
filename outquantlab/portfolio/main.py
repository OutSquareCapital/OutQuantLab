
from outquantlab.frames import DatedFloat
import numquant as nq
from dataclasses import dataclass, field

@dataclass(slots=True)
class BacktestResults:
    params: DatedFloat
    portfolio: DatedFloat = field(init=False)
    assets: DatedFloat = field(init=False)
    indics: DatedFloat = field(init=False)
    
    def __post_init__(self):
        self.indics = get_portfolio_returns(
            returns_df=self.params, grouping_levels=["assets", "indics"]
        )
        self.assets = get_portfolio_returns(
            returns_df=self.indics, grouping_levels=["assets"]
        )
        self.portfolio = get_portfolio(data=self.assets)

def get_portfolio_returns(
    returns_df: DatedFloat, grouping_levels: list[str]
) -> DatedFloat:
    return DatedFloat.from_pandas(
        data=returns_df.T.groupby(level=grouping_levels, observed=True).mean().T  # type: ignore
    )


def get_portfolio(data: DatedFloat) -> DatedFloat:
    return DatedFloat(
        data=nq.metrics.agg.get_mean(array=data.get_array(), axis=1),
        index=data.get_index(),
        columns=["portfolio"],
    )
