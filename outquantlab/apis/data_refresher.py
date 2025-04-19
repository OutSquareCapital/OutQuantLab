import yfinance as yf  # type: ignore
from pandas import DataFrame
import numquant as nq
import polars as pl
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class YFData:
    prices: pl.DataFrame
    returns: pl.DataFrame
    dates: pl.DataFrame


class YahooData:
    _CLOSE = "Close"
    _TEST = "AAPL"
    _PERIOD = "1d"
    _DATE = "Date"

    def check_connection(self) -> None:
        try:
            yf.Ticker(ticker=self._TEST).history(period=self._PERIOD)  # type: ignore
        except Exception as e:
            raise ConnectionError("Failed to connect to Yahoo Finance") from e

    def fetch_data(self, assets: list[str]) -> YFData:
        prices: pl.DataFrame = self._get_prices_data(assets=assets)
        dates: pl.DataFrame = prices.select(self._DATE)
        prices_data: pl.DataFrame = prices.drop([self._DATE])
        prices_values: nq.Float2D = prices_data.to_numpy()
        asset_names: list[str] = prices_data.columns
        return YFData(
            prices=prices_data,
            returns=pl.DataFrame(
                data=nq.arrays.get_pct_returns(prices=prices_values), schema=asset_names
            ),
            dates=dates,
        )

    def _get_prices_data(self, assets: list[str]) -> pl.DataFrame:
        data: DataFrame | None = yf.download(  # type: ignore
            tickers=assets,
            interval=self._PERIOD,
            auto_adjust=True,
            progress=False,
        )
        if data is None:
            raise ValueError(f"No data returned from Yahoo Finance, from {assets}")
        return pl.from_pandas(data=data[self._CLOSE], include_index=True)  # type: ignore
