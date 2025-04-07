from outquantlab.backtest import Backtestor
from outquantlab.indicators import BaseIndic
from outquantlab.structures import arrays, frames
from outquantlab.portfolio import BacktestResults, get_multi_index, aggregate_raw_returns, get_clusters

class OutQuantLab:
    def __init__(self, indics: list[BaseIndic], returns_df: frames.DatedFloat) -> None:
        self.indics: list[BaseIndic] = indics
        self.returns_df: frames.DatedFloat = returns_df

    def backtest(self) -> arrays.Float2D:
        process = Backtestor(
            pct_returns=self.returns_df.get_array(),
            indics=self.indics,
        )
        return process.process_backtest()
    
    def get_portfolio(self, data: arrays.Float2D) -> BacktestResults:
        multi_index = get_multi_index(
            asset_names=self.returns_df.get_names(),
            indics=self.indics
        )
    
        overall_frame = frames.DatedFloat(
            data=data,
            index=self.returns_df.get_index(),
            columns=multi_index
            )
        return aggregate_raw_returns(returns_df=overall_frame)
    
    def get_clusters(self, data: frames.DatedFloat) -> dict[str, list[str]]:
        data.clean_nans(total=True)
        return get_clusters(
            returns_array=data.get_array(),
            asset_names=data.get_names(),
            max_clusters=5
        )