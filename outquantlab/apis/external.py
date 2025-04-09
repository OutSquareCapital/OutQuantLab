import requests
from outquantlab.structures import frames

EXTERNAL = "https://jsonplaceholder.typicode.com/posts/1"

class ExternalAPI:
    def __init__(self) -> None:
        self.url = EXTERNAL

    def get_data(self) -> frames.SeriesFloat:
        response: requests.Response = requests.get(self.url)
        
        if response.status_code == 200:
            data: dict[str, float] = response.json()
            return frames.SeriesFloat.from_dict(data=data)  
        else:
            raise ValueError(f"Failed to fetch data from {self.url}, status code: {response.status_code}")
    
    def send_data(self, data: frames.DatedFloat) -> None:
        data_dict: frames.DatedDict = data.convert_to_json()
        response: requests.Response = requests.post(self.url, json=data_dict)
        if response.status_code == 201:
            print("Data sent successfully")
        else:
            raise ValueError(f"Failed to send data to {self.url}, status code: {response.status_code}")