from enum import Enum
import uvicorn
from fastapi import APIRouter, FastAPI

import tradeframe as tf


class Server(Enum):
    DATA = "/data"
    PORT = 8000
    IP = "127.0.0.1"
    URL = f"http://{IP}:{PORT}{DATA}"

type Frames = tf.FrameDated | tf.FrameDefault | tf.SeriesDated | tf.SeriesNamed | tf.SeriesDefault

class LabServer:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.router = APIRouter()
        self._data_store: dict[int, dict[str, float]] = {}
        self._current_id: int = 0
        self._register_routes()

    def _register_routes(self) -> None:
        @self.router.get(path=Server.DATA.value, response_model=None)
        async def get_data() -> dict[int, dict[str, float]]:  # type: ignore
            if not self._data_store:
                raise ValueError("No data available")
            return self._data_store

        self.app.include_router(router=self.router)

    def start_server(self) -> None:
        print(f"Server started at {Server.URL.value}")
        uvicorn.run(app=self.app, host=Server.IP.value, port=Server.PORT.value)

    def store_result(
        self, data: Frames
    ) -> None:
        result: dict[str, float] = data.get_last_row_dict()
        self._data_store[self._current_id] = result
        print(
            f"data with id {self._current_id} added to the server at {Server.URL.value}"
        )
        self._current_id += 1