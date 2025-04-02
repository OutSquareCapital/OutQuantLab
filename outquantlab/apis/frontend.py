from fastapi import FastAPI
import uvicorn
from outquantlab.structures import DataFrameDict, SeriesDict
from enum import Enum

class Server(Enum):
    DATA = "/data"
    PORT = 8000
    IP = "127.0.0.1"
    URL = f"http://{IP}:{PORT}{DATA}"


_app = FastAPI()
_data_store: dict[str, DataFrameDict | SeriesDict] = {}

def start_server() -> None:
    print(f"Server started at {Server.URL.value}")
    uvicorn.run(app=_app, host=Server.IP.value, port=Server.PORT.value)

def send_data_to_server(id: str, results: DataFrameDict | SeriesDict) -> None:
    _data_store[id] = results

@_app.get(path=Server.DATA.value)
def get_all_data() -> dict[str, DataFrameDict | SeriesDict]:
    if not _data_store:
        raise ValueError("No data available")
    return _data_store