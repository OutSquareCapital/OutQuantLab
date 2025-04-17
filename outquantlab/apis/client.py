import requests
from typing import TypedDict
import tradeframe as tf

EXTERNAL = "https://jsonplaceholder.typicode.com/posts/1"


class Quote(TypedDict):
    bid_price: float
    ask_price: float


class FoortData(TypedDict):
    date: str
    nid: str
    quote: Quote


class LabClient:
    def __init__(self) -> None:
        self.url = EXTERNAL

    def request_data(self) -> FoortData:
        try:
            response: requests.Response = requests.get(self.url)
            data: FoortData = response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error fetching data from {self.url}: {e}")
        return data

    def return_data(self, data: tf.FrameDefault) -> None:
        try:
            signal: dict[str, float] = data.get_last_row_dict()
            requests.post(url=self.url, json=signal)
        except Exception as e:
            raise ValueError(f"Error sending data to {self.url}: {e}")
