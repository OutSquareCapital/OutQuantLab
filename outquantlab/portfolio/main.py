
from outquantlab.portfolio.structures import CLUSTERS_LEVELS
from outquantlab.frames import DatedFloat
import numquant as nq

class BacktestResults:
    assets: DatedFloat
    indics: DatedFloat
    params: DatedFloat

    def __getitem__(self, key: str) -> DatedFloat:
        value: DatedFloat = self.__dict__[key]
        return value

    def __setitem__(self, key: str, value: DatedFloat) -> None:
        self.__dict__[key] = value

    @property
    def portfolio(self) -> DatedFloat:
        return get_portfolio(data=self.assets)

def aggregate_raw_returns(returns_df: DatedFloat) -> BacktestResults:
    results = BacktestResults()
    for lvl in range(len(CLUSTERS_LEVELS), 0, -1):
        returns_df = get_portfolio_returns(
            returns_df=returns_df, grouping_levels=returns_df.columns.names[:lvl]
        )
        returns_df.clean_nans()
        key_name: str = returns_df.columns.names[lvl - 1]
        results[key_name] = returns_df
    return results


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