from pydantic import BaseModel


class NetworkConfigData(BaseModel):
    max_retries: int
    max_errors: int
    sleep_interval: float
