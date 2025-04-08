
from outquantlab.metrics import get_overall_mean
from outquantlab.portfolio.structures import CLUSTERS_LEVELS
from outquantlab.structures import frames

    
class BacktestResults:
    assets: frames.DatedFloat
    indics: frames.DatedFloat
    params: frames.DatedFloat

    def __getitem__(self, key: str) -> frames.DatedFloat:
        value: frames.DatedFloat = self.__dict__[key]
        return value

    def __setitem__(self, key: str, value: frames.DatedFloat) -> None:
        self.__dict__[key] = value

    @property
    def portfolio(self) -> frames.DatedFloat:
        return get_overall_portfolio(data=self.assets)

def aggregate_raw_returns(returns_df: frames.DatedFloat) -> BacktestResults:
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
    returns_df: frames.DatedFloat, grouping_levels: list[str]
) -> frames.DatedFloat:
    return frames.DatedFloat.from_pandas(
        data=returns_df.T.groupby(level=grouping_levels, observed=True).mean().T  # type: ignore
    )


def get_overall_portfolio(data: frames.DatedFloat) -> frames.DatedFloat:
    return frames.DatedFloat(
        data=get_overall_mean(array=data.get_array(), axis=1),
        index=data.get_index(),
        columns=["portfolio"],
    )