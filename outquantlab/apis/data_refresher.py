import yfinance as yf  # type: ignore
from pandas import DataFrame
import numquant as nq
from enum import StrEnum
import polars as pl

class YFConstants(StrEnum):
    CLOSE = "Close"
    TEST = "AAPL"
    PERIOD = "1d"
    DATE = "Date"

class YahooData:
    def __init__(self, connect:bool = False) -> None:
        if connect:
            try:
                yf.Ticker(ticker=YFConstants.TEST).history(period=YFConstants.PERIOD)  # type: ignore
            except Exception as e:
                raise ConnectionError("Failed to connect to Yahoo Finance") from e
        
    def refresh_data(self, assets: list[str]) -> None:
        prices: pl.DataFrame = self._get_prices_data(assets=assets)
        dates: pl.DataFrame = prices.select(YFConstants.DATE)
        prices_data: pl.DataFrame = prices.drop([YFConstants.DATE])
        prices_values: nq.Float2D = prices_data.to_numpy()
        asset_names: list[str] = prices_data.columns
        self.prices: pl.DataFrame = pl.DataFrame(
            data=prices_values,
            schema=asset_names
        )
        self.returns: pl.DataFrame = pl.DataFrame(
            data=nq.arrays.get_pct_returns(prices=prices_values),
            schema=asset_names
        )

        self.dates = pl.DataFrame(data=dates)


    def _get_prices_data(self, assets: list[str]) -> pl.DataFrame:
        data: DataFrame | None = yf.download(  # type: ignore
            tickers=assets,
            interval=YFConstants.PERIOD,
            auto_adjust=True,
            progress=False,
        )
        if data is None:
            raise ValueError(f"No data returned from Yahoo Finance, from {assets}")
        return pl.from_pandas(data=data[YFConstants.CLOSE], include_index=True) # type: ignore
