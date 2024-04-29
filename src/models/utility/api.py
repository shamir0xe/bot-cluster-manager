from pydantic import AnyUrl, BaseModel

from src.models.utility.credentials import Credentials


class API(BaseModel):
    url: AnyUrl
    credentials: Credentials

