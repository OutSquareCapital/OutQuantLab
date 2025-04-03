from fastapi import FastAPI
import uvicorn
from outquantlab.structures import frames
from enum import Enum

class Server(Enum):
    DATA = "/data"
    PORT = 8000
    IP = "127.0.0.1"
    URL = f"http://{IP}:{PORT}{DATA}"

type BackendData = frames.DatedDict | frames.DistributionDict | frames.SeriesDict

_app = FastAPI()
_data_store: dict[str, BackendData] = {}

def start_server() -> None:
    print(f"Server started at {Server.URL.value}")
    uvicorn.run(app=_app, host=Server.IP.value, port=Server.PORT.value)

def send_data_to_server(id: str, results: BackendData) -> None:
    _data_store[id] = results

@_app.get(path=Server.DATA.value, response_model=None)
def get_all_data() -> dict[str, BackendData]:
    if not _data_store:
        raise ValueError("No data available")
    return _data_store