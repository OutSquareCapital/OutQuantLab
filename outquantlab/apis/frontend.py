from enum import Enum

import uvicorn
from fastapi import APIRouter, FastAPI

from outquantlab.structures import frames


class Server(Enum):
    DATA = "/data"
    PORT = 8000
    IP = "127.0.0.1"
    URL = f"http://{IP}:{PORT}{DATA}"


type BackendData = frames.DatedDict | frames.DistributionDict | frames.SeriesDict


class LabAPI:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.router = APIRouter()
        self._data_store: dict[int, BackendData] = {}
        self._current_id: int = 0
        self._register_routes()

    def _register_routes(self) -> None:
        @self.router.get(path=Server.DATA.value, response_model=None)
        async def get_data() -> dict[int, BackendData]:  # type: ignore
            if not self._data_store:
                raise ValueError("No data available")
            return self._data_store

        self.app.include_router(router=self.router)

    def start_server(self) -> None:
        print(f"Server started at {Server.URL.value}")
        uvicorn.run(app=self.app, host=Server.IP.value, port=Server.PORT.value)

    def send_result(
        self, data: frames.DatedFloat | frames.DefaultFloat | frames.SeriesFloat
    ) -> None:
        result: BackendData = data.convert_to_json()
        self._data_store[self._current_id] = result
        print(
            f"data with id {self._current_id} added to the server at {Server.URL.value}"
        )
        self._current_id += 1
