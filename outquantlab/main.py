from outquantlab.backtest import Backtestor
from outquantlab.indicators import GenericIndic
from outquantlab.structures import frames
from outquantlab.portfolio import BacktestResults, get_multi_index, aggregate_raw_returns, get_clusters

class OutQuantLab:
    def __init__(self, indics: list[GenericIndic], returns_df: frames.DatedFloat) -> None:
        self.indics: list[GenericIndic] = indics
        self.returns_df: frames.DatedFloat = returns_df

    def backtest(self) -> frames.DatedFloat:
        process = Backtestor(
            pct_returns=self.returns_df.get_array(),
            indics=self.indics,
        )
        multi_index = get_multi_index(
            asset_names=self.returns_df.get_names(),
            indics=self.indics
        )
        return frames.DatedFloat(
            data=process.process_backtest(),
            index=self.returns_df.get_index(),
            columns=multi_index
            )
    
    def get_portfolio(self, data: frames.DatedFloat) -> BacktestResults:
        return aggregate_raw_returns(returns_df=data)
    
    def get_clusters(self, data: frames.DatedFloat) -> dict[str, list[str]]:
        data.clean_nans(total=True)
        return get_clusters(
            returns_array=data.get_array(),
            asset_names=data.get_names(),
            max_clusters=5
        )