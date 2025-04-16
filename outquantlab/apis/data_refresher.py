import yfinance as yf  # type: ignore
from pandas import DataFrame

import numquant as nq
import tradeframe as tf

class YahooData:
    def fetch_data(self, assets: list[str]) -> tf.FrameDated:
        self._test_connection(asset=assets[0])
        return self._get_yf_data(assets=assets)

    def _get_yf_data(self, assets: list[str]) -> tf.FrameDated:
        prices: tf.FrameDated = self._get_prices_data(assets=assets)
        return tf.FrameDated.create_from_np(
            data=nq.arrays.get_pct_returns(prices=prices.get_array()),
            asset_names=prices.get_names(),
            dates=prices.index,
        )


    def _test_connection(self, asset: str) -> None:
        try:
            yf.Ticker(ticker=asset).history(period="1d")  # type: ignore
        except Exception as e:
            raise ConnectionError("Failed to connect to Yahoo Finance") from e

    def _get_prices_data(self, assets: list[str]) -> tf.FrameDated:
        data: DataFrame | None = yf.download(  # type: ignore
            tickers=assets,
            interval="1d",
            auto_adjust=True,
            progress=False,
        )
        if data is None:
            raise ValueError(f"No data returned from Yahoo Finance, from {assets}")
        return tf.FrameDated.create_from_pd(pd_df=data["Close"]) # type: ignore
